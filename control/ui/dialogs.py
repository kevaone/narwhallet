import json
import os
import time

from PyQt5.QtWidgets import QDialogButtonBox

from control.narwhallet_settings import MNarwhalletSettings
from control.shared import MShared

from core.kcl.file_utils import ConfigLoader
from core.kcl.models.cache import MCache
from core.kcl.models.wallets import MWallets
from core.kcl.models.wallet import MWallet
from core.kcl.models.book_addresses import MBookAddresses
from core.kcl.models.book_address import MBookAddress

from core.kex import KEXclient

from core.kui.main import NarwhalletUI
from core.kui.ux.dialogs.tx_builder_simple_send import Ui_simple_send_dlg
from core.kui.ux.dialogs.tx_builder_keva_op import Ui_keva_op_send_dlg
from core.kui.ux.dialogs.tx_builder_keva_nft import Ui_keva_op_nft_dlg
from core.kui.ux.dialogs.tx_builder_keva_nft_bid import Ui_keva_op_nft_bid_dlg
from core.kui.ux.dialogs.tx_builder_keva_nft_accept_bid import Ui_keva_op_nft_accept_bid_dlg
from core.kui.ux.dialogs.create_wallet import Ui_create_wallet_dlg
from core.kui.ux.dialogs.add_wallet_watch_address import Ui_add_watch_addr_dlg
from core.kui.ux.dialogs.add_wallet_watch import Ui_add_wallet_watch_dlg
from core.kui.ux.dialogs.restore_wallet import Ui_restore_wallet_dlg
from core.kui.ux.dialogs.view_wallet_address import Ui_v_addr_dlg
from core.kui.ux.dialogs.view_wallet_change_address import Ui_v_change_addr_dlg
from core.kui.ux.dialogs.view_wallet_transaction import Ui_v_tx_dlg
from core.kui.ux.dialogs.add_addressbook_item import Ui_add_ab_item_dlg
from core.kui.ux.dialogs.view_addressbook_item import Ui_v_ab_item_dlg
from core.kui.ux.dialogs.add_electrumx_peer import Ui_add_electrumx_peer_dlg
from core.kui.ux.dialogs.lockbox import Ui_lockbox_dlg
from core.kui.ux.dialogs.warning_dialog import Ui_warning_dlg
from core.kui.ux.dialogs.add_namespace_favorite import Ui_add_ns_fav_dlg


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

    def simple_send_dialog(self):
        _di = Ui_simple_send_dlg()
        _di.setupUi()
        _di.wallets = self.wallets
        _di.cache = self.cache
        _di.kex = self.kex
        _fee = MShared.get_fee_rate(self.kex)
        if _fee == -1:
            _ = self.warning_dialog('Could not get fee rate!',
                                    False, 1)
            return

        _di.user_path = self.user_path
        _di.new_tx.set_fee(_fee)
        _di.feerate.setText(str(_fee))
        for _w in self.wallets.wallets:
            if _w.kind != 1 and _w.kind != 3 and _w.locked is False:
                # NOTE We don't want wallets to relock while interacting
                _w.set_updating(True)
                _di.w.addItem(_w.name+' - '+str(round(_w.balance, 8)),
                              _w.name)
        for _addr in self.address_book.addresses:
            _aa = self.address_book.addresses[_addr].address
            _abi = self.address_book.addresses[_addr].name + ' - ' + _aa
            _di.address_book.addItem(_abi, _aa)
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

    def create_namespace_send_dialog(self):
        _di = Ui_keva_op_send_dlg()
        _di.setupUi()
        _di.wallets = self.wallets
        _di.cache = self.cache
        _di.kex = self.kex
        _fee = MShared.get_fee_rate(self.kex)
        if _fee == -1:
            _ = self.warning_dialog('Could not get fee rate!',
                                    False, 1)
            return

        _di.user_path = self.user_path
        _di.new_tx.set_fee(_fee)
        _di.feerate.setText(str(_fee))
        _di.value.setMinimumHeight(28)
        _di.value.setMaximumHeight(28)
        _di.key_v.setVisible(False)
        _di.key_v_l.setVisible(False)
        for _w in self.wallets.wallets:
            if _w.kind != 1 and _w.kind != 3 and _w.locked is False:
                _w.set_updating(True)
                _di.w.addItem(_w.name + ' - ' + str(round(_w.balance, 8)),
                              _w.name)

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

    def create_namespace_key_send_dialog(self):
        _di = Ui_keva_op_send_dlg()
        _di.setupUi()
        _di.wallets = self.wallets
        _di.cache = self.cache
        _di.kex = self.kex
        _fee = MShared.get_fee_rate(self.kex)
        if _fee == -1:
            _ = self.warning_dialog('Could not get fee rate!',
                                    False, 1)
            return

        _di.user_path = self.user_path
        _di.new_tx.set_fee(_fee)
        _di.feerate.setText(str(_fee))
        _di.setWindowTitle('Narwhallet - Create Key')
        _di.value_l.setText('Value: ')

        _selection = self.ui.ns_tab.tbl_ns.selectedRanges()
        if len(_selection) == 0:
            return

        if _selection[0].topRow() != _selection[0].bottomRow():
            return

        _row = _selection[0].topRow()
        _w = self.ui.ns_tab.tbl_ns.item(_row, 2).text()
        _wallet = self.wallets.get_wallet_by_name(_w)
        _wallet.set_updating(True)
        _di.w.addItem(_w, _w)
        _di.w.setCurrentIndex(1)
        _di.w.setEnabled(False)
        _di.ns = self.ui.ns_tab.tbl_ns.item(_row, 5).text()
        _di.ns_address = self.ui.ns_tab.tbl_ns.item(_row, 6).text()

        _di.set_availible_usxo(True)
        _result = _di.exec_()

        _wallet.set_updating(False)

        if _result != 0:
            _bc_result = MShared.broadcast(_di.raw_tx, self.kex)
            if isinstance(_bc_result[1], dict):
                _result = json.dumps(_bc_result[1])
            else:
                _result = _bc_result[1]
            _ = self.warning_dialog(_result, False, int(_bc_result[0]))

    def edit_namespace_key_send_dialog(self):
        _di = Ui_keva_op_send_dlg()
        _di.setupUi()
        _di.wallets = self.wallets
        _di.cache = self.cache
        _di.kex = self.kex
        _fee = MShared.get_fee_rate(self.kex)
        if _fee == -1:
            _ = self.warning_dialog('Could not get fee rate!',
                                    False, 1)
            return

        _di.user_path = self.user_path
        _di.new_tx.set_fee(_fee)
        _di.feerate.setText(str(_fee))
        _di.setWindowTitle('Narwhallet - Edit Key')
        _di.value_l.setText('Value: ')

        _selection = self.ui.ns_tab.tbl_ns.selectedRanges()
        if len(_selection) == 0:
            return

        if _selection[0].topRow() != _selection[0].bottomRow():
            return

        _row = _selection[0].topRow()
        _w = self.ui.ns_tab.tbl_ns.item(_row, 2).text()
        _wallet = self.wallets.get_wallet_by_name(_w)
        _wallet.set_updating(True)
        _di.w.addItem(_w, _w)
        _di.w.setCurrentIndex(1)
        _di.w.setEnabled(False)

        _di.ns = self.ui.ns_tab.tbl_ns.item(_row, 5).text()
        _di.ns_address = self.ui.ns_tab.tbl_ns.item(_row, 6).text()
        _key = self.ui.ns_tab.list_ns_keys.currentItem().text()
        _value = self.ui.ns_tab.ns_tab_text_key_value.toPlainText()
        if _key == '_KEVA_NS_':
            _key = '\x01_KEVA_NS_'
            _value = {'displayName': _value}
            _value = json.dumps(_value, separators=(',', ':'))

        _di.ns_key = _key
        _di.ns_value = _value
        _di.key_v.setReadOnly(True)
        _di.value.setReadOnly(True)

        _di.set_availible_usxo(True)
        _di.txb_build_simple_send()
        _di.next_btn.setVisible(False)
        _di.back_btn.setVisible(False)
        _result = _di.exec_()

        _wallet.set_updating(False)

        if _result != 0:
            _bc_result = MShared.broadcast(_di.raw_tx, self.kex)
            if isinstance(_bc_result[1], dict):
                _result = json.dumps(_bc_result[1])
            else:
                _result = _bc_result[1]
            _ = self.warning_dialog(_result, False, int(_bc_result[0]))

    def delete_namespace_key_send_dialog(self):
        _di = Ui_keva_op_send_dlg()
        _di.setupUi()
        _di.wallets = self.wallets
        _di.cache = self.cache
        _di.kex = self.kex
        _fee = MShared.get_fee_rate(self.kex)
        if _fee == -1:
            _ = self.warning_dialog('Could not get fee rate!',
                                    False, 1)
            return

        _di.user_path = self.user_path
        _di.new_tx.set_fee(_fee)
        _di.feerate.setText(str(_fee))
        _di.setWindowTitle('Narwhallet - Delete Key')
        _di.value_l.setText('Value: ')

        _selection = self.ui.ns_tab.tbl_ns.selectedRanges()
        if len(_selection) == 0:
            return

        if _selection[0].topRow() != _selection[0].bottomRow():
            return

        _row = _selection[0].topRow()
        _w = self.ui.ns_tab.tbl_ns.item(_row, 2).text()
        _wallet = self.wallets.get_wallet_by_name(_w)
        _wallet.set_updating(True)
        _di.w.addItem(_w, _w)
        _di.w.setCurrentIndex(1)
        _di.w.setEnabled(False)

        _di.ns = self.ui.ns_tab.tbl_ns.item(_row, 5).text()
        _di.ns_address = self.ui.ns_tab.tbl_ns.item(_row, 6).text()
        _di.ns_key = self.ui.ns_tab.list_ns_keys.currentItem().text()
        _di.ns_value = ''

        _di.set_availible_usxo(True)
        _di.txb_build_simple_send()
        _di.next_btn.setVisible(False)
        _di.back_btn.setVisible(False)
        _result = _di.exec_()
        _wallet.set_updating(False)

        if _result != 0:
            _bc_result = MShared.broadcast(_di.raw_tx, self.kex)
            if isinstance(_bc_result[1], dict):
                _result = json.dumps(_bc_result[1])
            else:
                _result = _bc_result[1]
            _ = self.warning_dialog(_result, False, int(_bc_result[0]))

    def transfer_namespace_send_dialog(self):
        _di = Ui_keva_op_send_dlg()
        _di.setupUi()
        _di.wallets = self.wallets
        _di.cache = self.cache
        _di.kex = self.kex
        _fee = MShared.get_fee_rate(self.kex)
        if _fee == -1:
            _ = self.warning_dialog('Could not get fee rate!',
                                    False, 1)
            return

        _di.user_path = self.user_path
        _di.new_tx.set_fee(_fee)
        _di.feerate.setText(str(_fee))
        _di.setWindowTitle('Narwhallet - Transfer Namespace')
        _di.value_l.setText('Value: ')

        _selection = self.ui.ns_tab.tbl_ns.selectedRanges()
        if len(_selection) == 0:
            return

        if _selection[0].topRow() != _selection[0].bottomRow():
            return

        _row = _selection[0].topRow()
        _w = self.ui.ns_tab.tbl_ns.item(_row, 2).text()
        _wallet = self.wallets.get_wallet_by_name(_w)
        _wallet.set_updating(True)
        _di.w.addItem(_w, _w)
        _di.w.setCurrentIndex(1)
        _di.w.setEnabled(False)

        _di.ns = self.ui.ns_tab.tbl_ns.item(_row, 5).text()
        _di.ns_address = self.ui.ns_tab.tbl_ns.item(_row, 6).text()
        _di.set_availible_usxo(True)

        for _addr in self.address_book.addresses:
            _aa = self.address_book.addresses[_addr].address
            _abi = self.address_book.addresses[_addr].name + ' - '
            _abi = _abi + _aa
            _di.address_book.addItem(_abi, _aa)
        _di.address_book.setVisible(True)

        _di.value.setPlainText(str(time.time()))
        _di.key_v.setText('wxfr')
        _di.next_btn.setEnabled(False)
        _di.is_transfer = True
        _result = _di.exec_()

        _wallet.set_updating(False)

        if _result != 0:
            _bc_result = MShared.broadcast(_di.raw_tx, self.kex)
            if isinstance(_bc_result[1], dict):
                _result = json.dumps(_bc_result[1])
            else:
                _result = _bc_result[1]
            _ = self.warning_dialog(_result, False, int(_bc_result[0]))

    def auction_namespace_dialog(self):
        _di = Ui_keva_op_nft_dlg()
        _di.setupUi()
        _di.wallets = self.wallets
        _di.cache = self.cache
        _di.kex = self.kex
        _fee = MShared.get_fee_rate(self.kex)
        if _fee == -1:
            _ = self.warning_dialog('Could not get fee rate!',
                                    False, 1)
            return

        _di.new_tx.set_fee(_fee)
        _di.feerate.setText(str(_fee))
        _di.setWindowTitle('Narwhallet - Create Auction')

        for _wallet in self.wallets.wallets:
            if _wallet.kind == 0:
                _di.combo_wallet.addItem(_wallet.name, _wallet.name)

        _result = _di.exec_()

        if _result != 0:
            _bc_result = MShared.broadcast(_di.raw_tx, self.kex)
            # print('_bc_result', type(_bc_result), _bc_result)
            if isinstance(_bc_result[1], dict):
                _result = json.dumps(_bc_result[1])
            else:
                _result = _bc_result[1]
            _ = self.warning_dialog(_result, False, int(_bc_result[0]))

    def bid_namespace_dialog(self):
        _di = Ui_keva_op_nft_bid_dlg()
        _di.setupUi()
        _di.wallets = self.wallets
        _di.cache = self.cache
        _di.kex = self.kex
        _fee = MShared.get_fee_rate(self.kex)
        if _fee == -1:
            _ = self.warning_dialog('Could not get fee rate!',
                                    False, 1)
            return

        _di.new_tx.set_fee(_fee)
        _di.bid_tx.set_fee(_fee)
        _di.feerate.setText(str(_fee))
        _di.setWindowTitle('Narwhallet - Create Bid')

        for _wallet in self.wallets.wallets:
            if _wallet.kind == 0:
                _di.combo_wallet.addItem(_wallet.name, _wallet.name)

        _result = _di.exec_()

        if _result != 0:
            _bc_result = MShared.broadcast(_di.raw_tx, self.kex)
            # print('_bc_result', type(_bc_result), _bc_result)
            if isinstance(_bc_result[1], dict):
                _result = json.dumps(_bc_result[1])
            else:
                _result = _bc_result[1]
            _ = self.warning_dialog(_result, False, int(_bc_result[0]))

    def accept_bid_namespace_dialog(self):
        _di = Ui_keva_op_nft_accept_bid_dlg()
        _di.setupUi()
        _di.wallets = self.wallets
        _di.cache = self.cache
        _di.kex = self.kex
        _fee = MShared.get_fee_rate(self.kex)
        if _fee == -1:
            _ = self.warning_dialog('Could not get fee rate!',
                                    False, 1)
            return

        _di.new_tx.set_fee(_fee)
        _di.bid_tx.set_fee(_fee)
        _di.feerate.setText(str(_fee))
        _di.setWindowTitle('Narwhallet - Create Bid')

        for _wallet in self.wallets.wallets:
            if _wallet.kind == 0:
                _di.combo_wallet.addItem(_wallet.name, _wallet.name)

        _result = _di.exec_()

        if _result != 0:
            _bc_result = MShared.broadcast(_di.raw_tx, self.kex)
            # print('_bc_result', type(_bc_result), _bc_result)
            if isinstance(_bc_result[1], dict):
                _result = json.dumps(_bc_result[1])
            else:
                _result = _bc_result[1]
            _ = self.warning_dialog(_result, False, int(_bc_result[0]))

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
            _wallet = _di.ret_wallet()
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
        _di.set_qr_uri(self.ui.w_tab.tbl_addr.item(row, 1).text())

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
        _di.set_qr_uri(_addr)
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
