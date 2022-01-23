from typing import Optional
from narwhallet.core.ksc.utils import Ut
from narwhallet.core.kcl.bip_utils.base58 import Base58Encoder
from narwhallet.core.kcl.kevacoin.namespace import MNamespace
from narwhallet.core.kcl.cache.db_utils import SQLInterface


class MNamespaces():
    def __init__(self, db_interface: SQLInterface):
        self.dbi = db_interface
        self._special_keys: dict = {}

    @property
    def special_keys(self) -> dict:
        return self._special_keys

    def set_special_keys(self, special_keys: dict) -> None:
        self._special_keys = special_keys

    @staticmethod
    def sort(item):
        return item[0]

    @staticmethod
    def sort_dict(item):
        return item['date']

    @staticmethod
    def convert_to_namespaceid(nsid: str):
        try:
            _id = Base58Encoder.CheckEncode(Ut.hex_to_bytes(nsid))
            return _id
        except Exception:
            return Exception('Invailid Namespaceid')

    @staticmethod
    def _decode(value):
        try:
            _d2 = Ut.int_to_bytes(int(value), None, 'little').decode()
        except Exception:
            try:
                _d2 = Ut.hex_to_bytes(value).decode()
            except Exception:
                _d2 = value
                # print('error', _d2, value)
        return _d2

    # TODO Move types to own class; stubbing as strings here for now
    def get_key_type(self, key, value) -> Optional[str]:
        _type = None
        if key == '_KEVA_NS_':
            _type = 'root_ns'
        elif key == '\x01_KEVA_NS_':
            if 'displayName' in value and 'price' in value and 'addr' in value:
                _type = 'nft_auction'
            else:
                _type = 'root_ns_update'
        elif key[:4] == '0001' and len(key) == 68:
            if value[:10] == '70736274ff':
                _type = 'nft_bid'
            else:
                _type = 'reply'
        elif key[:4] == '0002' and len(key) == 68:
            _type = 'repost'
        elif key[:4] == '0003' and len(key) == 68:
            _type = 'reward'
        elif key[:4] == '0004' and len(key) == 68:
            _type = 'nft_auction'
        elif key[:4] == '0005' and len(key) == 68:
            _type = 'nft_confirm_sell'
        elif key in self.special_keys:
            _type = self.special_keys[key]['tooltip']

        return _type

    def from_raw(self, block: int, n: int, tx: str,
                 nsid: str, op: str, key: str, value: str,
                 address: str):

        _ns = self.convert_to_namespaceid(nsid)
        key = self._decode(key)
        value = self._decode(value)
        _r = self.dbi.execute_sql(self.dbi.scripts.INSERT_NS,
                                  (block, n, tx, _ns, op,
                                   key,
                                   value,
                                   self.get_key_type(key, value),
                                   address), 2)
        return _r

    def get_view(self):
        _r = self.dbi.execute_sql(self.dbi.scripts.SELECT_NS_VIEW_1, (), 3)
        return _r

    def get_namespace_by_txid(self, txid: str, nsid: str) -> MNamespace:
        _ns = self.convert_to_namespaceid(nsid)
        _r = self.dbi.execute_sql(self.dbi.scripts.SELECT_NS_BY_TXID,
                                  (txid, _ns, ), 3)
        return _r

    def get_namespace_by_id(self, nsid: str) -> MNamespace:
        _r = self.dbi.execute_sql(self.dbi.scripts.SELECT_NS,
                                  (nsid, ), 3)
        return _r

    def get_namespace_by_key(self, block, nsid: str, key: str) -> MNamespace:
        _ns = self.convert_to_namespaceid(nsid)
        _r = self.dbi.execute_sql(self.dbi.scripts.SELECT_NS_BY_KEY,
                                  (block, _ns, self._decode(key)), 3)
        return _r

    def get_namespace_by_key_value(self, _ns: str, key: str):
        _r = self.dbi.execute_sql(self.dbi.scripts.SELECT_NS_KEY_VALUE,
                                  (_ns, key), 3)
        return _r

    def get_namespace_key_replies(self, _key_tx: str):
        _r = self.dbi.execute_sql(self.dbi.scripts.SELECT_NS_KEY_REPLIES,
                                  ('____'+_key_tx, ), 3)
        return _r

    def get_namespace_auctions(self, _ns: str):
        _r = self.dbi.execute_sql(self.dbi.scripts.SELECT_NS_AUCTIONS,
                                  (_ns, ), 3)
        # TODO Assemble rest of auction data
        return _r

    def get_namespace_bids(self, _ns: str):
        _r = self.dbi.execute_sql(self.dbi.scripts.SELECT_NS_BIDS,
                                  (_ns, ), 3)
        # TODO Assemble rest of bid data
        return _r

    def get_ns_by_shortcode(self, shortcode: int) -> MNamespace:
        _bs = str(shortcode)
        _block = int(_bs[1:int(_bs[0])+1])

        if int(_bs[0])+1 < len(_bs):
            _n = int(_bs[int(_bs[0])+1:])
            _ns_id = self.dbi.execute_sql(self.dbi.scripts.SELECT_NS_BY_POS,
                                          (_block, _n), 3)
        else:
            _ns_id = []

        if len(_ns_id) == 1:
            _r = self.dbi.execute_sql(self.dbi.scripts.SELECT_NS,
                                      (_ns_id[0][0], ), 3)
        else:
            _r = []

        return _r

    def get_root_namespace_by_id(self, nsid: str,
                                 convert: bool = False) -> MNamespace:
        if convert is True:
            nsid = self.convert_to_namespaceid(nsid)
        _r = self.dbi.execute_sql(self.dbi.scripts.SELECT_NS_ROOT_TEST,
                                  (nsid, ), 3)
        return _r

    def key_count(self, nsid):
        _r = self.dbi.execute_sql(self.dbi.scripts.SELECT_NS_COUNT,
                                  (nsid, ), 3)
        return _r

    def ns_block(self, nsid):
        _r = self.dbi.execute_sql(self.dbi.scripts.SELECT_NS_BLOCK,
                                  (nsid, ), 3)
        return _r

    def ns_root_value(self, nsid):
        _r = self.dbi.execute_sql(self.dbi.scripts.SELECT_NS_ROOT_VALUE,
                                  (nsid, ), 3)
        return _r

    def last_address(self, nsid):
        _r = self.dbi.execute_sql(self.dbi.scripts.SELECT_NS_LAST_ADDRESS,
                                  (nsid, ), 3)
        return _r

    def update_key(self, block: int, n: int, tx: str,
                   nsid: str, key: str, value: str,
                   address: str):

        _ns = self.convert_to_namespaceid(nsid)
        key = self._decode(key)
        value = self._decode(value)
        _r = self.dbi.execute_sql(self.dbi.scripts.UPDATE_NS_KEY,
                                  (block, n, tx, value,
                                   self.get_key_type(key, value),
                                   address, _ns,
                                   key), 1)
        return _r

    def mark_key_deleted(self, block: int, nsid: str, key: str):
        _ns = self.convert_to_namespaceid(nsid)
        key = self._decode(key)

        _r = self.dbi.execute_sql(self.dbi.scripts.UPDATE_NS_KEY_MARK,
                                  ('deleted', _ns,
                                   key, block), 1)
        return _r

    def delete_key(self, nsid, key, block):
        _ns = self.convert_to_namespaceid(nsid)
        _r = self.dbi.execute_sql(self.dbi.scripts.DELETE_NS_KEY,
                                  (_ns, self._decode(key), block, ), 1)
        return _r