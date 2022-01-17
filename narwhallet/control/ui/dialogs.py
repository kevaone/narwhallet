import json
import os
import time

from PyQt5.QtWidgets import QDialogButtonBox

from narwhallet.control.narwhallet_settings import MNarwhalletSettings
from narwhallet.control.shared import MShared
# from narwhallet.core.ksc.utils import Ut
from narwhallet.core.kcl.file_utils import ConfigLoader
from narwhallet.core.kcl.cache import MCache
from narwhallet.core.kcl.wallet import MWallet, MWallets
from narwhallet.core.kcl.addr_book import MBookAddress, MBookAddresses
from narwhallet.core.kex import KEXclient
from narwhallet.core.kui.main import NarwhalletUI
from narwhallet.core.kui.ux.dialogs import (Ui_add_ab_item_dlg,
                                            Ui_add_electrumx_peer_dlg,
                                            Ui_add_ns_fav_dlg,
                                            Ui_add_wallet_watch_dlg,
                                            Ui_add_watch_addr_dlg,
                                            Ui_create_wallet_dlg,
                                            Ui_lockbox_dlg,
                                            Ui_restore_wallet_dlg,
                                            Ui_send_dlg,
                                            Ui_v_ab_item_dlg,
                                            Ui_v_addr_dlg,
                                            Ui_v_tx_dlg,
                                            Ui_warning_dlg)


# TODO Add time check to abort send dialogs if left open to long
# NOTE While sending dialogs open encrypted wallets will remain unlocked...
class MDialogs():
    def __init__(self, user_path: str,
                 narwhallet_settings: MNarwhalletSettings,
                 _view: NarwhalletUI, kex: KEXclient,
                 wallets: MWallets, cache: MCache,
                 address_book: MBookAddresses):
        self.user_path = user_path
        self.ui = _view.ui
        self.kex = kex
        self.wallets = wallets
        self.cache = cache
        self.settings = narwhallet_settings
        self.address_book = address_book

    def populate_wallet_combo(self, combo):
        for _w in self.wallets.wallets:
            if _w.kind != 1 and _w.kind != 3 and _w.locked is False:
                # NOTE We don't want wallets to relock while interacting
                _w.set_updating(True)
                combo.addItem(_w.name+' - '+str(round(_w.balance, 8)),
                              _w.name)

    def populate_addressbook_combo(self, combo):
        for _addr in self.address_book.addresses:
            _aa = self.address_book.addresses[_addr].address
            _abi = self.address_book.addresses[_addr].name + ' - ' + _aa
            combo.addItem(_abi, _aa)

    def populate_namespace_special_keys_combo(self, combo):
        for _key in self.cache.ns.special_keys:
            _abi = _key + ' - ' + self.cache.ns.special_keys[_key]['tooltip']
            combo.addItem(_abi, _key)

    def send_dialog(self, _di: Ui_send_dlg):
        _fee = MShared.get_fee_rate(self.kex)
        if _fee == -1:
            _ = self.warning_dialog('Could not get fee rate!',
                                    False, 1)
            return

        _di.send_info.feerate.setText(str(_fee))
        _di.new_tx.set_fee(_fee)
        _di.bid_tx.set_fee(_fee)

        _result = _di.exec_()

        for _w in self.wallets.wallets:
            if _w.kind != 1 and _w.kind != 3 and _w.locked is False:
                _w.set_updating(False)

        if _result != 0:
            _bc_result = MShared.broadcast(_di.raw_tx, self.kex)
            if isinstance(_bc_result[1], dict):
                _result = json.dumps(_bc_result[1])
            else:
                _result = _bc_result[1]
            _ = self.warning_dialog(_result, False, int(_bc_result[0]))

    def simple_send_dialog(self):
        _di = Ui_send_dlg()
        _di.setupUi(0)
        _di.wallets = self.wallets
        _di.cache = self.cache
        _di.kex = self.kex
        self.populate_wallet_combo(_di.wallet_combo.combo)
        self.populate_addressbook_combo(_di.address_combo.combo)
        self.send_dialog(_di)

    def create_namespace_send_dialog(self):
        _di = Ui_send_dlg()
        _di.setupUi(2)
        self.populate_wallet_combo(_di.wallet_combo.combo)
        _di.wallets = self.wallets
        _di.cache = self.cache
        _di.kex = self.kex
        self.send_dialog(_di)

    def create_namespace_key_send_dialog(self):
        _di = Ui_send_dlg()
        _di.setupUi(3)
        (self
         .populate_namespace_special_keys_combo(_di.special_keys_combo.combo))
        _di.wallets = self.wallets
        _di.cache = self.cache
        _di.kex = self.kex

        _selection = self.ui.ns_tab.tbl_ns.selectedRanges()
        if len(_selection) == 0:
            return

        if _selection[0].topRow() != _selection[0].bottomRow():
            return

        _row = _selection[0].topRow()
        _w = self.ui.ns_tab.tbl_ns.item(_row, 2).text()
        _wallet = self.wallets.get_wallet_by_name(_w)
        _wallet.set_updating(True)
        _di.wallet = _wallet
        _di.wallet_combo.combo.addItem(_wallet.name, _wallet.name)
        _di.wallet_combo.combo.setCurrentIndex(1)
        _ns = self.ui.ns_tab.tbl_ns.item(_row, 5).text()
        _di.ns_combo.combo.setCurrentIndex(_di.ns_combo.combo.findText(_ns))

        # _di.set_availible_usxo(True, False, '')

        self.send_dialog(_di)
        _wallet.set_updating(False)

    def edit_namespace_key_send_dialog(self):
        _di = Ui_send_dlg()
        _di.setupUi(4)
        _di.wallets = self.wallets
        _di.cache = self.cache
        _di.kex = self.kex

        _selection = self.ui.ns_tab.tbl_ns.selectedRanges()
        if len(_selection) == 0:
            return

        if _selection[0].topRow() != _selection[0].bottomRow():
            return

        _row = _selection[0].topRow()
        _w = self.ui.ns_tab.tbl_ns.item(_row, 2).text()
        _wallet = self.wallets.get_wallet_by_name(_w)
        _wallet.set_updating(True)
        _di.wallet = _wallet
        _di.wallet_combo.combo.addItem(_wallet.name, _wallet.name)
        _di.wallet_combo.combo.setCurrentIndex(1)

        _ns = self.ui.ns_tab.tbl_ns.item(_row, 5).text()
        _di.ns_combo.combo.setCurrentIndex(_di.ns_combo.combo.findText(_ns))
        _key = self.ui.ns_tab.list_ns_keys.currentItem().text()
        _value = self.ui.ns_tab.ns_tab_text_key_value.toPlainText()
        if _key == '_KEVA_NS_':
            _key = '\x01_KEVA_NS_'
            _value = {'displayName': _value}
            _value = json.dumps(_value, separators=(',', ':'))

        _di.namespace_key_input.key.setText(_key)
        _di.namespace_value_input.value.setPlainText(_value)

        # _di.set_availible_usxo(True)
        # _di.txb_build_simple_send()

        self.send_dialog(_di)
        _wallet.set_updating(False)

    def delete_namespace_key_send_dialog(self):
        _di = Ui_send_dlg()
        _di.setupUi(5)
        _di.wallets = self.wallets
        _di.cache = self.cache
        _di.kex = self.kex

        _selection = self.ui.ns_tab.tbl_ns.selectedRanges()
        if len(_selection) == 0:
            return

        if _selection[0].topRow() != _selection[0].bottomRow():
            return

        _row = _selection[0].topRow()
        _w = self.ui.ns_tab.tbl_ns.item(_row, 2).text()
        _wallet = self.wallets.get_wallet_by_name(_w)
        _wallet.set_updating(True)
        _di.wallet = _wallet
        _di.wallet_combo.combo.addItem(_wallet.name, _wallet.name)
        _di.wallet_combo.combo.setCurrentIndex(1)

        _ns = self.ui.ns_tab.tbl_ns.item(_row, 5).text()
        _di.ns_combo.combo.setCurrentIndex(_di.ns_combo.combo.findText(_ns))
        _key = self.ui.ns_tab.list_ns_keys.currentItem().text()
        _di.namespace_key_input.key.setText(_key)
        _di.namespace_value_input.value.setPlainText('')

        # _di.set_availible_usxo(True)
        # _di.txb_build_simple_send()

        self.send_dialog(_di)
        _wallet.set_updating(False)

    def transfer_namespace_send_dialog(self):
        _di = Ui_send_dlg()
        _di.setupUi(9)
        _di.wallets = self.wallets
        self.populate_addressbook_combo(_di.address_combo.combo)
        _di.cache = self.cache
        _di.kex = self.kex

        _selection = self.ui.ns_tab.tbl_ns.selectedRanges()
        if len(_selection) == 0:
            return

        if _selection[0].topRow() != _selection[0].bottomRow():
            return

        _row = _selection[0].topRow()
        _w = self.ui.ns_tab.tbl_ns.item(_row, 2).text()
        _wallet = self.wallets.get_wallet_by_name(_w)
        _wallet.set_updating(True)
        _di.wallet = _wallet
        _di.wallet_combo.combo.addItem(_wallet.name, _wallet.name)
        _di.wallet_combo.combo.setCurrentIndex(1)
        _ns = self.ui.ns_tab.tbl_ns.item(_row, 5).text()
        _di.ns_combo.combo.setCurrentIndex(_di.ns_combo.combo.findText(_ns))

        _di.namespace_value_input.value.setPlainText(str(time.time()))
        _di.namespace_key_input.key.setText('wxfr')

        # _di.set_availible_usxo(True)
        self.send_dialog(_di)

        _wallet.set_updating(False)

    def auction_namespace_dialog(self):
        _di = Ui_send_dlg()
        _di.setupUi(6)
        self.populate_wallet_combo(_di.wallet_combo.combo)
        _di.wallets = self.wallets
        _di.cache = self.cache
        _di.kex = self.kex
        self.send_dialog(_di)

    def bid_namespace_dialog(self, tx=False, action=None):
        _di = Ui_send_dlg()
        _di.setupUi(7)
        self.populate_wallet_combo(_di.wallet_combo.combo)
        _di.wallets = self.wallets
        _di.cache = self.cache
        _di.kex = self.kex

        if tx is not False:
            _di.namespace_key_input.key.setText(tx)
            _data = json.loads(action[3])['data']
            _di.amount_input.amount.setText(_data['data'])

        self.send_dialog(_di)

        if tx is not False:
            self.cache.actions.update(action[0], action[1], action[2], 1)

    def action_dialog(self, action):
        _di = Ui_send_dlg()

        _ns_key = action[1]
        _data = json.loads(action[3])['data']

        if action[2] == 'comment':
            _di.setupUi(3)
            _di.action = 'comment'
            _ns_key = '0001' + _ns_key
            _di.setWindowTitle('Narwhallet - Key Comment')
            _di.namespace_key_input.key.setReadOnly(True)
            _di.wallet_combo.combo.setEnabled(True)
            _di.ns_combo.combo.setEnabled(True)
        elif action[2] == 'reward':
            _di.setupUi(10)
            _di.action = 'reward'
            _ns_key = '0003' + _ns_key
            _di.amount_input.amount.setText(_data['data'])
        elif action[2] == 'repost':
            _di.setupUi(3)
            _di.action = 'repost'
            _ns_key = '0002' + _ns_key
            _di.setWindowTitle('Narwhallet - Key Repost')
            _di.namespace_key_input.key.setReadOnly(True)
            _di.wallet_combo.combo.setEnabled(True)
            _di.ns_combo.combo.setEnabled(True)
        elif action[2] == 'bid':
            _di.setupUi(7)
            _di.action = 'bid'
            # NOTE Key prefix '0001' for bids added in later step
            # _ns_key = _ns_key
            _di.setWindowTitle('Narwhallet - Auction Bid')
            _di.namespace_key_input.key.setReadOnly(True)

        _di.wallets = self.wallets
        _di.cache = self.cache
        _di.kex = self.kex
        self.populate_wallet_combo(_di.wallet_combo.combo)
        _di.namespace_key_input.key.setText(_ns_key)
        _di.namespace_value_input.value.setPlainText(_data['data'])

        if action[2] == 'reward':
            _di.check_tx_is_ns_key()
            _di.namespace_value_input.value.setPlainText('')
        elif action[2] == 'bid':
            _di.namespace_value_input.value.setPlainText('')

        self.send_dialog(_di)

        self.cache.actions.update(action[0], action[1], action[2], 1)

    def accept_bid_namespace_dialog(self, wallet: MWallet):
        _di = Ui_send_dlg()
        _di.setupUi(8)
        _di.wallets = self.wallets
        _di.wallet = wallet
        _di.cache = self.cache
        _di.kex = self.kex
        _di.wallet_combo.combo.addItem(wallet.name, wallet.name)
        _di.wallet_combo.combo.setCurrentIndex(1)

        _bid_selection = self.ui.nft_tab.tbl_bids_2.selectedRanges()
        if len(_bid_selection) == 0:
            return

        if _bid_selection[0].topRow() != _bid_selection[0].bottomRow():
            return

        _row = _bid_selection[0].topRow()

        _ns = self.ui.nft_tab.ns.text()
        _di.auction_info.nft_name.setText(self.ui.nft_tab.display_name.text())
        _di.auction_info.nft_desc.setText(self.ui.nft_tab.desc.text())
        _di.auction_info.nft_hashtags.setText(self.ui.nft_tab.hashtags.text())
        _di.auction_info.nft_ns.setText(_ns)
        _di.auction_info.nft_address.setText(self.ui.nft_tab.address.text())
        _di.auction_info.nft_price.setText(self.ui.nft_tab.asking.text())
        (_di.auction_info.nft_shortcode
         .setText(self.ui.nft_tab.shortcode.text()))
        (_di.namespace_key_input.key
         .setText(self.ui.nft_tab.tbl_bids_2.item(_row, 6).text()))

        _di.ns_combo.combo.setCurrentIndex(_di.ns_combo.combo.findText(_ns))

        _di.check_tx_is_bid()
        self.send_dialog(_di)

    @staticmethod
    def add_wallet_watch_address_dialog():
        _di = Ui_add_watch_addr_dlg()
        _di.setupUi()
        _result = _di.exec_()

        if _result != 0:
            _a = _di.address.widgets[0].text()
            _l = _di.label.widgets[0].text()
            if _a == '':
                _a = None

            if _l == '':
                _l = None
        else:
            _a = None
            _l = None

        return _a, _l

    @staticmethod
    def add_wallet_watch_dialog() -> str:
        _di = Ui_add_wallet_watch_dlg()
        _di.setupUi()
        _result = _di.exec_()

        if _result != 0:
            _name = _di.name.widgets[0].text()
            if _name == '':
                _name = None
        else:
            _name = None

        return _name

    @staticmethod
    def add_namespace_favorite_dialog():
        _di = Ui_add_ns_fav_dlg()
        _di.setupUi()
        _result = _di.exec_()

        if _result != 0:
            _shortcode = _di.shortcode.widgets[0].text()
            if _shortcode == '':
                _shortcode = None
        else:
            _shortcode = None

        return _shortcode

    @staticmethod
    def create_wallet_dialog() -> MWallet:
        _di = Ui_create_wallet_dlg()
        _di.setupUi()
        _result = _di.exec_()

        if _result != 0:
            _wallet = _di.ret_wallet()
        else:
            _wallet = None

        return _wallet

    @staticmethod
    def restore_wallet_dialog() -> MWallet:
        _di = Ui_restore_wallet_dlg()
        _di.setupUi()
        _result = _di.exec_()

        if _result != 0:
            try:
                _wallet = _di.ret_wallet()
            except Exception as Ex:
                _ = MDialogs.warning_dialog(str(Ex), False, 1)
                _wallet = None
        else:
            _wallet = None

        return _wallet

    @staticmethod
    def warning_dialog(message, isYesNo, msgType):
        _b_ok = QDialogButtonBox.Ok
        _b_cancel = QDialogButtonBox.Cancel
        _di = Ui_warning_dlg()
        _di.setupUi()
        _di.set_message(message)
        if isYesNo is True:
            _di.buttonBox.button(_b_ok).setText('Yes')
            _di.buttonBox.button(_b_cancel).setText('No')

        if msgType == 1:
            _di.message_pic.label.setPixmap(_di.error_pic)
            _di.buttonBox.button(_b_cancel).setVisible(False)
        elif msgType == 2:
            _di.message_pic.label.setPixmap(_di.success_pic)
            _di.buttonBox.button(_b_cancel).setVisible(False)

        _result = _di.exec()

        return _result

    @staticmethod
    def lockbox_dialog(mode):
        _di = Ui_lockbox_dlg()
        _di.setupUi(mode)

        _result = _di.exec_()
        _func_call = ''
        if _result != 0:
            _func_call = _di.ret()

        return _func_call

    def view_wallet_address_dialog(self, row, _column):
        _di = Ui_v_addr_dlg()

        _ws = self.ui.w_tab.tbl_w.selectedRanges()
        # HACK FIX for no wallet selected:
        if len(_ws) == 0:
            return

        if _ws[0].topRow() == _ws[0].bottomRow():
            _n = self.ui.w_tab.tbl_w.item(_ws[0].topRow(), 3).text()
            _w = self.wallets.get_wallet_by_name(_n)

        _addr = (_w.addresses
                 .get_address_by_name(self.ui.w_tab.tbl_addr.item(row, 1)
                                      .text()))
        _tmp_label = self.ui.w_tab.tbl_addr.item(row, 5).text()
        _di.setupUi()

        (_di.label.widgets[0]
         .setText(self.ui.w_tab.tbl_addr.item(row, 5).text()))
        (_di.address.widgets[0]
         .setPlainText(self.ui.w_tab.tbl_addr.item(row, 1).text()))
        (_di.recevied.widgets[0]
         .setText(self.ui.w_tab.tbl_addr.item(row, 2).text()))
        (_di.sent.widgets[0]
         .setText(self.ui.w_tab.tbl_addr.item(row, 3).text()))
        (_di.balance.widgets[0]
         .setText(self.ui.w_tab.tbl_addr.item(row, 4).text()))
        _di.locked.widgets[0].setText('<todo>')

        _di.set_qr(self.ui.w_tab.tbl_addr.item(row, 1).text())

        _result = _di.exec_()

        if _result != 0:
            if _di.label.widgets[0].text() != _tmp_label:
                _addr.set_label(_di.label.widgets[0].text())
                self.wallets.save_wallet(_w.name)

    def view_wallet_change_address_dialog(self, row, _column):
        _di = Ui_v_addr_dlg()

        _ws = self.ui.w_tab.tbl_w.selectedRanges()
        # HACK FIX for no wallet selected:
        if len(_ws) == 0:
            return

        if _ws[0].topRow() == _ws[0].bottomRow():
            _n = self.ui.w_tab.tbl_w.item(_ws[0].topRow(), 3).text()
            _w = self.wallets.get_wallet_by_name(_n)

        _addr = (_w.change_addresses
                 .get_address_by_name(self.ui.w_tab.tbl_addr2.item(row, 1)
                                      .text()))
        _tmp_label = self.ui.w_tab.tbl_addr2.item(row, 5).text()
        _di.setupUi()

        (_di.label.widgets[0]
         .setText(self.ui.w_tab.tbl_addr2.item(row, 5).text()))
        (_di.address.widgets[0]
         .setPlainText(self.ui.w_tab.tbl_addr2.item(row, 1).text()))
        (_di.recevied.widgets[0]
         .setText(self.ui.w_tab.tbl_addr2.item(row, 2).text()))
        (_di.sent.widgets[0]
         .setText(self.ui.w_tab.tbl_addr2.item(row, 3).text()))
        (_di.balance.widgets[0]
         .setText(self.ui.w_tab.tbl_addr2.item(row, 4).text()))
        _di.locked.widgets[0].setText('<todo>')

        _di.set_qr(self.ui.w_tab.tbl_addr2.item(row, 1).text())

        _result = _di.exec_()

        if _result != 0:
            if _di.label.widgets[0].text() != _tmp_label:
                _addr.set_label(_di.label.widgets[0].text())
                self.wallets.save_wallet(_w.name)

    def view_wallet_transaction_dialog(self, row, _column):
        _di = Ui_v_tx_dlg()
        _di.setupUi()

        _ws = self.ui.w_tab.tbl_w.selectedRanges()
        # HACK FIX for no wallet selected:
        if len(_ws) == 0:
            return

        _tr = self.ui.w_tab.tbl_tx.item(row, 5).text()

        _t = self.cache.tx.get_tx_by_txid(_tr)

        _di.txid.widgets[0].setPlainText(_t.txid)
        _di.hash.widgets[0].setPlainText(_t.hash)
        _di.block_hash.widgets[0].setPlainText(_t.blockhash)
        _di.hex_d.setPlainText(_t.hex)
        _t_dict = _t.to_dict()
        _di.json_d.setPlainText(json.dumps(_t_dict, indent=4))

        for c, vin in enumerate(_t.vin):
            _di.add_vin(c, vin)

        for c, vout in enumerate(_t.vout):
            _di.add_vout(c, vout)

        _result = _di.exec_()

        if _result != 0:
            pass

    def add_electrumx_peer_dialog(self):
        _di = Ui_add_electrumx_peer_dlg()
        _di.setupUi()
        _result = _di.exec_()

        # TODO: type validate before dialog accept
        # TODO: check for exsistance before addition
        if _result != 0:
            peer = ['', '', 0, False, False]
            peer[0] = _di.coin.widgets[0].currentData()
            peer[1] = _di.host.widgets[0].text()
            peer[2] = _di.host.widgets[2].text()
            peer[3] = _di.host.widgets[3].isChecked()

            self.settings.add_electrumx_peer(peer)
            _ = self.kex.add_peer(peer[1], int(peer[2]),
                                  bool(peer[3]), peer[4])
            self.ui.settings_tab.elxp_tbl.add_peer(peer[0], peer[1],
                                                   peer[2], peer[3])

            _dat = ConfigLoader(os.path.join(self.user_path, 'settings.json'))
            _dat.save(json.dumps(self.settings.to_dict(), indent=4).encode())

    @staticmethod
    def add_addressbook_item_dialog() -> MBookAddress:
        _di = Ui_add_ab_item_dlg()
        _di.setupUi()
        _result = _di.exec_()

        if _result != 0:
            _address = _di.ret_address()
        else:
            _address = None

        return _address

    def view_addressbook_item_dialog(self, row):
        _di = Ui_v_ab_item_dlg()
        _di.setupUi()

        _addr = self.ui.ab_tab.tbl_addr.item(row, 3).text()
        _addr_name = self.ui.ab_tab.tbl_addr.item(row, 2).text()
        _addr_label = self.ui.ab_tab.tbl_addr.item(row, 6).text()
        _di.name.widgets[0].setText(_addr_name)
        _di.address.widgets[0].setPlainText(_addr)
        _di.label.widgets[0].setText(_addr_label)

        _di.set_qr(_addr)
        _result = _di.exec_()

        if _result != 0:
            _update_table = False
            if _addr_label != _di.label.widgets[0].text():
                (self.address_book.addresses[_addr]
                 .set_label(_di.label.widgets[0].text()))
                _update_table = True

            if _addr_name != _di.name.widgets[0].text():
                (self.address_book.addresses[_addr]
                 .set_name(_di.name.widgets[0].text()))
                _update_table = True

            if _update_table is True:
                self.address_book.save_address_book()
                (self.ui.ab_tab.tbl_addr
                 .add_bookaddresses(self.address_book.to_dict_list()))
