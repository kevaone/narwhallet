import os
import json
import bleach
import re

from narwhallet.control.shared import MShared
from narwhallet.core.kcl.cache import MCache


class Feed():
    def __init__(self, theme, ipfs_gateway):
        self.feed = []
        self.page_theme = theme
        self.ipfs_gateway = ipfs_gateway
        self.allowed_tags = ['img', 'a', 'abbr', 'acronym', 'b',
                             'blockquote', 'code', 'em', 'i', 'li',
                             'ol', 'strong', 'ul', 'tt', 'pre', 'br',
                             'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
        self.allowed_attributes = {'img': ['src'], 'a': ['href', 'title'],
                                   'abbr': ['title'], 'acronym': ['title']}
        self.allowed_styles = []
        self.allowed_protocols = ['http', 'https', 'mailto']

    def strap_content(self, file):
        _path = os.path.join(self.page_theme, file)
        _data = ''
        with open(_path) as f:
            _data = f.read()

        return _data

    def get_feed_meta(self, section):
        return self.strap_content(section+'_feed_meta.html')

    def get_feed_item(self, kind=None):
        if kind == 'reply':
            _content = self.strap_content('profile_feed_reply.html')
        elif kind == 'reward':
            _content = self.strap_content('profile_feed_reward.html')
        elif kind == 'bid_script':
            _content = self.strap_content('profile_feed_bid.html')
        elif kind == 'post':
            _content = self.strap_content('profile_feed_repost.html')
        elif kind == 'html':
            _content = self.strap_content('profile_feed_html.html')
        elif kind == 'nft_listing':
            _content = self.strap_content('nft_feed.html')
        elif kind == 'nft_listing_image':
            _content = self.strap_content('nft_feed_image_auction.html')
        elif kind == 'nft_listing_numbers':
            _content = self.strap_content('nft_feed_number_auction.html')
        else:
            _content = self.strap_content('profile_feed.html')
        return _content

    def extract_html_title(self, _item):
        _titles = re.findall(r'<title>[^</title>].*</title>', _item)

        for _title in _titles:
            return _title

    def link_IPFS(self, _item):
        _ipfs_images = re.findall(r'\{\{[^|image(|/png|/jpeg|/jpg|/gif)\}\}].*|image|image/png|image/jpeg|image/jpg|image/gif\}\}', _item)

        for _image in _ipfs_images:
            _gw = self.ipfs_gateway
            _image_link = (_image
                           .replace('{{', '<br /><img src="' + _gw)
                           .replace('|image/png}}', '">')
                           .replace('|image/jpeg}}', '">')
                           .replace('|image/jpg}}', '">')
                           .replace('|image/gif}}', '">')
                           .replace('|image}}', '">'))
            _item = _item.replace(_image, _image_link)

        if _item.startswith(' <br />'):
            _item = _item[7:len(_item)]
        elif _item.startswith('<br />'):
            _item = _item[6:len(_item)]

        return _item

    def replace_content(self, key, value, kind=None):
        if kind == 'reply':
            _feeditem = self.get_feed_item('reply')
        elif kind == 'reward':
            _feeditem = self.get_feed_item('reward')
        elif kind == 'bid_script':
            _feeditem = self.get_feed_item('bid_script')
        elif kind == 'post':
            _feeditem = self.get_feed_item('post')
        elif kind == 'html':
            _feeditem = self.get_feed_item('html')
        elif kind == 'nft_listing':
            _feeditem = self.get_feed_item('nft_listing')
        elif kind == 'nft_listing_image':
            _feeditem = self.get_feed_item('nft_listing_image')
        elif kind == 'nft_listing_numbers':
            _feeditem = self.get_feed_item('nft_listing_numbers')
        else:
            _feeditem = self.get_feed_item()

        _i = _feeditem.replace('$key', bleach.clean(key, strip=True))

        if kind == 'html':
            _i = _i.replace('$value', value.replace('"', '&quot;'))
        else:
            _i = _i.replace('$value', bleach.clean(value,
                            tags=self.allowed_tags,
                            attributes=self.allowed_attributes,
                            styles=self.allowed_styles,
                            protocols=self.allowed_protocols,
                            strip=False, strip_comments=True))

        return _i

    def get_feed(self, _namespace, _ns_replies, cache: MCache):
        _feed = self.get_feed_meta('profile')
        _items = ''
        _shortcode = 0
        _ns_name = ''
        for key in _namespace:
            _nft_flag = False
            _key = key[6]

            if not isinstance(_key, str):
                _key = str(_key)

            if _ns_name == '' and '_KEVA_NS_' in key[5]:
                try:
                    _k = json.loads(_key)['displayName']
                except Exception:
                    _k = _key
                _ns_name = _k

            _shortcode = str(len(str(key[0])))+str(key[0])+str(key[1])
            # TODO add special flag to keys

            if ('displayName' in _key
                    and 'price' in _key
                    and 'desc' in _key
                    and 'addr' in _key):
                _nft_flag = True
                _nft = json.loads(_key)
                _res = 'Name: ' + _nft['displayName']
                _res = _res + '<br />Asking Price: ' + _nft['price']
                _res = _res + '<br />Description: ' + _nft['desc']
                _res = self.replace_content('NFT Auction', _res)
            # elif key.isSpecial('post'):
            else:
                _value = self.link_IPFS(_key)
                _res = self.replace_content(str(key[5]), _value)

            _tx = cache.tx.get_tx_by_txid(key[2])
            _res = _res.replace('$tx', _tx.txid)
            _res = _res.replace('$time', MShared.get_timestamp(_tx.time)[1])

            # TODO Add reply tracking to core namespace classes
            _replies = ''
            if key[2] in _ns_replies:
                for _r in _ns_replies[key[2]]:
                    if _r[6] == 'reward':
                        _ri = str(_r[5])
                    else:
                        _ri = self.link_IPFS(str(_r[5]))
                    _ri = self.replace_content(_r[4], _ri, _r[6])
                    _ri = _ri.replace('$rewards', '').replace('$replies', '')
                    _rbk = '<a href="$who/' + _r[0] + '">@'
                    if _r[1] != '':
                        _r[1] = ' - ' + _r[1]
                    _rbk = _rbk + _r[0] + _r[1] + '</a>'
                    _ri = _ri.replace('$keva_one_id', _rbk)
                    _ri = _ri.replace('$txid', _r[2])
                    _replies = _replies + _ri
            _rewards = ''
            _res = _res.replace('$rewards', _rewards)
            _res = _res.replace('$replies', _replies)

            if '_KEVA_NS_' in str(key[5]):
                if _nft_flag is True:
                    _items = _items + _res
            else:
                _items = _items + _res

        _bk = '<a href="$who/' + _shortcode + '">@'
        _bk = _bk + _shortcode + ' - ' + _ns_name + '</a>'
        _items = _items.replace('$keva_one_id', _bk)
        _feed = _feed.replace('$feed', _items)

        return _feed

    def get_auction_feed(self, data, auction_type):
        _feed = self.get_feed_meta('nft')
        _feed_rows = ''
        _items = ''
        _item_counter = 0
        _row_counter = 0

        data['auctions'].sort(reverse=True, key=MShared.sort_dict)

        for auction in data['auctions']:
            _i = ''
            if auction['image'] is not None and auction_type == 1:
                auction['image'] = self.link_IPFS(auction['image'])
                _i = self.replace_content('', auction['desc'],
                                          'nft_listing_image')
                _i = _i.replace('$total-keys', '<i class="fas fa-image"></i>')
                _i = (_i.replace(
                      '$images',
                      '<div><div>' + auction['image'] + '</div></div>'))
            elif auction['image'] is None and auction_type == 2:
                _i = self.replace_content('', auction['desc'],
                                          'nft_listing_numbers')
                _i = _i.replace('$images', '')
                _i = _i.replace('$total-keys', '')

            if _i != '':
                _i = _i.replace('$nft_name', auction['displayName'])
                _i = _i.replace('$asking', str(auction['price']))
                _i = _i.replace('$value', auction['desc'])
                _i = _i.replace('$total-bids', str(auction['bids']))
                _i = _i.replace('$high-bid', str(auction['highBid']))
                _i = _i.replace('$keva_one_id',
                                '@' + str(auction['shortcode']))
                _i = _i.replace('$rewards', '')
                _i = _i.replace('$replies', '')
                _i = ('<a href="$who/' + str(auction['shortcode']) +
                      '">' + _i + '</a>')
                _items = _items + _i

                if _row_counter == 3:
                    _feed_rows = _feed_rows + _feed.replace('$feed', _items)
                    _row_counter = 0
                    _items = ''
                else:
                    _row_counter += 1

            _item_counter += 1
            if _item_counter == data['count']:
                _feed_rows = _feed_rows + _feed.replace('$feed', _items)

        _feed = _feed_rows

        return _feed
