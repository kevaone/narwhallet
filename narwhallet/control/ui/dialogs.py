import json
import os
import time

from PyQt5.QtWidgets import QDialogButtonBox

from narwhallet.control.narwhallet_settings import MNarwhalletSettings
from narwhallet.control.shared import MShared
# from narwhallet.core.ksc.utils import Ut
from narwhallet.core.kcl.file_utils import ConfigLoader
from narwhallet.core.kcl.models.cache import MCache
from narwhallet.core.kcl.models.wallets import MWallets
from narwhallet.core.kcl.models.wallet import MWallet
from narwhallet.core.kcl.models.book_addresses import MBookAddresses
from narwhallet.core.kcl.models.book_address import MBookAddress

from narwhallet.core.kex import KEXclient

from narwhallet.core.kui.main import NarwhalletUI
from narwhallet.core.kui.ux.dialogs.tx_builder_send import Ui_send_dlg
from narwhallet.core.kui.ux.dialogs.create_wallet import Ui_create_wallet_dlg
from narwhallet.core.kui.ux.dialogs.add_wallet_watch_address import Ui_add_watch_addr_dlg
from narwhallet.core.kui.ux.dialogs.add_wallet_watch import Ui_add_wallet_watch_dlg
from narwhallet.core.kui.ux.dialogs.restore_wallet import Ui_restore_wallet_dlg
from narwhallet.core.kui.ux.dialogs.view_wallet_address import Ui_v_addr_dlg
from narwhallet.core.kui.ux.dialogs.view_wallet_change_address import Ui_v_change_addr_dlg
from narwhallet.core.kui.ux.dialogs.view_wallet_transaction import Ui_v_tx_dlg
from narwhallet.core.kui.ux.dialogs.add_addressbook_item import Ui_add_ab_item_dlg
from narwhallet.core.kui.ux.dialogs.view_addressbook_item import Ui_v_ab_item_dlg
from narwhallet.core.kui.ux.dialogs.add_electrumx_peer import Ui_add_electrumx_peer_dlg
from narwhallet.core.kui.ux.dialogs.lockbox import Ui_lockbox_dlg
from narwhallet.core.kui.ux.dialogs.warning_dialog import Ui_warning_dlg
from narwhallet.core.kui.ux.dialogs.add_namespace_favorite import Ui_add_ns_fav_dlg


# TODO Add time check to abort send dialogs if left open to long
# NOTE While sending dialogs open encrypted wallets will remain unlocked...
class MDialogs():
    def __init__(self, user_path: str,
                 narwhallet_settings: MNarwhalletSettings,
                 _view: NarwhalletUI, kex: KEXclient,
                 wallets: MWallets, cache: MCache,
                 address_book: MBookAddresses):
        self.user_path = user_path
        self._v = _view
        self.ui = self._v.ui
        self.kex = kex
        self.wallets = wallets
        self.cache = cache
        self.settings = narwhallet_settings
        self.address_book = address_book
        # TODO Refine this
        self.cache_path = os.path.join(self.user_path, 'narwhallet_cache.db')

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

    def send_dialog(self, _di: Ui_send_dlg):
        _fee = MShared.get_fee_rate(self.kex)
        if _fee == -1:
            _ = self.warning_dialog('Could not get fee rate!',
                                    False, 1)
            return

        _di.send_info.feerate.setText(str(_fee))
        _di.new_tx.set_fee(_fee)
        _di.bid_tx.set_fee(_fee)

        # _result = _di.exec_()

        for _w in self.wallets.wallets:
            if _w.kind != 1 and _w.kind != 3 and _w.locked is False:
                _w.set_updating(False)

        # if _result != 0:
        #     _bc_result = MShared.broadcast(_di.raw_tx, self.kex)
        #     if isinstance(_bc_result[1], dict):
        #         _result = json.dumps(_bc_result[1])
        #     else:
        #         _result = _bc_result[1]
        #     _ = self.warning_dialog(_result, False, int(_bc_result[0]))

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
        # _di.wallet_combo.setEnabled(False)
        _ns = self.ui.ns_tab.tbl_ns.item(_row, 5).text()
        # _ns_address = self.ui.ns_tab.tbl_ns.item(_row, 6).text()
        # _di.ns_combo.combo.addItem(_ns, _ns_address)
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
        # _di.wallet_combo.setEnabled(False)

        _ns = self.ui.ns_tab.tbl_ns.item(_row, 5).text()
        # _ns_address = self.ui.ns_tab.tbl_ns.item(_row, 6).text()
        # _di.ns_combo.combo.addItem(_ns, _ns_address)
        # _di.ns_combo.combo.setCurrentIndex(1)
        _di.ns_combo.combo.setCurrentIndex(_di.ns_combo.combo.findText(_ns))
        _key = self.ui.ns_tab.list_ns_keys.currentItem().text()
        _value = self.ui.ns_tab.ns_tab_text_key_value.toPlainText()
        if _key == '_KEVA_NS_':
            _key = '\x01_KEVA_NS_'
            _value = {'displayName': _value}
            _value = json.dumps(_value, separators=(',', ':'))

        _di.namespace_key_input.key.setText(_key)
        _di.namespace_value_input.value.setPlainText(_value)
        # _di.namespace_key_input.key.setReadOnly(True)
        # _di.namespace_value_input.value.setReadOnly(True)

        # _di.set_availible_usxo(True)
        # _di.txb_build_simple_send()
        # _di.buttonBox.next.setVisible(False)
        # _di.buttonBox.back.setVisible(False)

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
        # _di.wallet_combo.setEnabled(False)

        _ns = self.ui.ns_tab.tbl_ns.item(_row, 5).text()
        # _ns_address = self.ui.ns_tab.tbl_ns.item(_row, 6).text()
        # _di.ns_combo.combo.addItem(_ns, _ns_address)
        # _di.ns_combo.combo.setCurrentIndex(1)
        _di.ns_combo.combo.setCurrentIndex(_di.ns_combo.combo.findText(_ns))
        _key = self.ui.ns_tab.list_ns_keys.currentItem().text()
        _di.namespace_key_input.key.setText(_key)
        _di.namespace_value_input.value.setPlainText('')

        # _di.set_availible_usxo(True)
        # _di.txb_build_simple_send()
        # _di.buttonBox.next.setVisible(False)
        # _di.buttonBox.back.setVisible(False)

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
        # _di.wallet_combo.setEnabled(False)

        _ns = self.ui.ns_tab.tbl_ns.item(_row, 5).text()
        # _ns_address = self.ui.ns_tab.tbl_ns.item(_row, 6).text()
        # _di.ns_combo.combo.addItem(_ns, _ns_address)
        # _di.ns_combo.combo.setCurrentIndex(1)
        _di.ns_combo.combo.setCurrentIndex(_di.ns_combo.combo.findText(_ns))

        _di.namespace_value_input.value.setPlainText(str(time.time()))
        _di.namespace_key_input.key.setText('wxfr')
        # _di.buttonBox.next.setEnabled(False)

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
        _di.setupUi(10)
        self.populate_wallet_combo(_di.wallet_combo.combo)
        _di.wallets = self.wallets
        _di.cache = self.cache
        _di.kex = self.kex

        _data = json.loads(action[3])['data']

        if action[2] == 'comment':
            _di.action = 'comment'
        elif action[2] == 'reward':
            _di.action = 'reward'
            _di.amount_input.amount.setText(_data['data'])
        elif action[2] == 'repost':
            _di.action = 'repost'

        _di.namespace_key_input.key.setText(action[1])
        _di.namespace_value_input.value.setPlainText(_data['data'])

        # _di.setWindowTitle('Narwhallet - Complete Action')

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
        # _di.wallet_combo.combo.setEnabled(False)

        _bid_selection = self.ui.nft_tab.tbl_bids_2.selectedRanges()
        if len(_bid_selection) == 0:
            return

        if _bid_selection[0].topRow() != _bid_selection[0].bottomRow():
            return

        _row = _bid_selection[0].topRow()

        _di.auction_info.nft_name.setText(self.ui.nft_tab.display_name.text())
        _di.auction_info.nft_desc.setText(self.ui.nft_tab.desc.text())
        _di.auction_info.nft_hashtags.setText(self.ui.nft_tab.hashtags.text())
        _di.auction_info.nft_ns.setText(self.ui.nft_tab.ns.text())
        _di.auction_info.nft_address.setText(self.ui.nft_tab.address.text())
        _di.auction_info.nft_price.setText(self.ui.nft_tab.asking.text())
        (_di.auction_info.nft_shortcode
         .setText(self.ui.nft_tab.shortcode.text()))
        (_di.namespace_key_input.key
         .setText(self.ui.nft_tab.tbl_bids_2.item(_row, 6).text()))

        self.send_dialog(_di)

    @staticmethod
    def add_wallet_watch_address_dialog():
        _di = Ui_add_watch_addr_dlg()
        _di.setupUi()
        _result = _di.exec_()

        if _result != 0:
            _a = _di.address_d.text()
            _l = _di.label_d.text()
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
            _name = _di.name_d.text()
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
            _shortcode = _di.name_d.text()
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
            _di.label_1.setPixmap(_di.error_pic)
            _di.buttonBox.button(_b_cancel).setVisible(False)
        elif msgType == 2:
            _di.label_1.setPixmap(_di.success_pic)
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

        _di.label_d.setText(self.ui.w_tab.tbl_addr.item(row, 5).text())
        (_di.address_d
         .setPlainText(self.ui.w_tab.tbl_addr.item(row, 1).text()))
        (_di.details_received_d
         .setText(self.ui.w_tab.tbl_addr.item(row, 2).text()))
        (_di.details_sent_d
         .setText(self.ui.w_tab.tbl_addr.item(row, 3).text()))
        (_di.details_balance_d
         .setText(self.ui.w_tab.tbl_addr.item(row, 4).text()))
        _di.details_locked_d.setText('<todo>')

        _di.set_qr(self.ui.w_tab.tbl_addr.item(row, 1).text())

        _result = _di.exec_()

        if _result != 0:
            if _di.label_d.text() != _tmp_label:
                _addr.set_label(_di.label_d.text())
                self.wallets.save_wallet(_w.name)

    def view_wallet_change_address_dialog(self, row, _column):
        _di = Ui_v_change_addr_dlg()

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

        _di.label_d.setText(self.ui.w_tab.tbl_addr2.item(row, 5).text())
        (_di.address_d
         .setPlainText(self.ui.w_tab.tbl_addr2.item(row, 1).text()))
        (_di.details_received_d
         .setText(self.ui.w_tab.tbl_addr2.item(row, 2).text()))
        (_di.details_sent_d
         .setText(self.ui.w_tab.tbl_addr2.item(row, 3).text()))
        (_di.details_balance_d
         .setText(self.ui.w_tab.tbl_addr2.item(row, 4).text()))
        _di.details_locked_d.setText('<todo>')

        _result = _di.exec_()

        if _result != 0:
            if _di.label_d.text() != _tmp_label:
                _addr.set_label(_di.label_d.text())
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

        _di.txid_d.setPlainText(_t.txid)
        _di.hash_d.setPlainText(_t.hash)
        _di.blockhash_d.setPlainText(_t.blockhash)
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
            peer[0] = _di.comboBox.currentText()
            peer[1] = _di.lineEdit.text()
            peer[2] = _di.lineEdit_2.text()
            peer[3] = False if _di.checkBox.checkState() == 0 else True

            _p = {'coin': peer[0],
                  'host': peer[1],
                  'port': peer[2], 'type': 'HTTP',
                  'tls': peer[3],
                  'ping': '0ms', 'status': 'disconnected'}

            self.settings.add_electrumx_peer(peer)
            _ = self.kex.add_peer(peer[1], int(peer[2]),
                                  bool(peer[3]), peer[4])
            self.ui.settings_tab.elxp_tbl.add_peer(_p)

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
        _di.lineEdit.setText(_addr_name)
        _di.lineEdit_3.setPlainText(_addr)
        _di.lineEdit_2.setText(_addr_label)

        _di.set_qr(_addr)
        _result = _di.exec_()

        if _result != 0:
            _update_table = False
            if _addr_label != _di.lineEdit_2.text():
                (self.address_book.addresses[_addr]
                 .set_label(_di.lineEdit_2.text()))
                _update_table = True

            if _addr_name != _di.lineEdit.text():
                (self.address_book.addresses[_addr]
                 .set_name(_di.lineEdit.text()))
                _update_table = True

            if _update_table is True:
                self.address_book.save_address_book()
                (self.ui.ab_tab.tbl_addr
                 .add_bookaddresses(self.address_book.to_dict_list()))
