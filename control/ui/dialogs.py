import json
import math
import os
import time
from typing import Callable

from PyQt5.QtWidgets import QDialog, QDialogButtonBox

from control.narwhallet_settings import MNarwhalletSettings
from control.shared import MShared

from core.kcl.file_utils import ConfigLoader
from core.kcl.db_utils import SQLInterface
from core.kcl.models.wallets import MWallets
from core.kcl.models.book_addresses import MBookAddresses
from core.kcl.models.transactions import MTransactions

from core.kex import KEXclient

from core.kui.main import NarwhalletUI
from core.kui.ux.dialogs.tx_builder_simple_send import Ui_simple_send_dlg
from core.kui.ux.dialogs.tx_builder_keva_op import Ui_keva_op_send_dlg
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
# While sending dialogs open encrypted wallets will remain unlocked...
class MDialogs():
    def __init__(self, user_path: str,
                 narwhallet_settings: MNarwhalletSettings,
                 _view: NarwhalletUI, KEX: KEXclient,
                 wallets: MWallets, tx_cache: MTransactions,
                 address_book: MBookAddresses, add_wallet_watch,
                 create_watch_wallet, get_K: Callable,
                 refresh_namespace_tab_data, ns_cache):
        self.user_path = user_path
        self._v = _view
        self.ui = self._v.ui
        self.KEX = KEX
        self.wallets = wallets
        self.tx_cache = tx_cache
        self.settings = narwhallet_settings
        self.address_book = address_book
        self.add_wallet_watch = add_wallet_watch
        self.create_watch_wallet = create_watch_wallet
        self.get_K = get_K
        self.refresh_namespace_tab_data = refresh_namespace_tab_data
        # TODO Refine this
        self.cache_path = os.path.join(self.user_path, 'narwhallet_cache.db')
        self._db_cache = SQLInterface(self.cache_path)
        self.ns_cache = ns_cache
        # self.address_book = MBookAddresses()

    def simple_send_dialog(self):
        _di = QDialog()
        _di.ui = Ui_simple_send_dlg()
        _di.ui.setupUi(_di)
        _di.ui.wallets = self.wallets
        _di.ui.tx_cache = self.tx_cache
        _di.ui.KEX = self.KEX
        _fee = MShared.get_fee_rate(self.KEX)
        if _fee == -1:
            _ = self.warning_dialog('Could not get fee rate!',
                                    False, 1)
            return
        
        _di.ui.user_path = self.user_path
        _di.ui._new_tx.set_fee(_fee)
        _di.ui.feerate.setText(str(_fee))
        for _w in self.wallets.wallets:
            if _w.kind != 1 and _w.kind != 3 and _w.locked is False:
                # NOTE We don't want wallets to relock while interacting
                _w.set_updating(True)
                _di.ui.w.addItem(_w.name+' - '+str(round(_w.balance, 8)),
                                 _w.name)
        for _addr in self.address_book.addresses:
            _aa = self.address_book.addresses[_addr].address
            _abi = self.address_book.addresses[_addr].name + ' - ' + _aa
            _di.ui.address_book.addItem(_abi, _aa)
        # _di.show()
        _result = _di.exec_()

        for _w in self.wallets.wallets:
            if _w.kind != 1 and _w.kind != 3 and _w.locked is False:
                _w.set_updating(False)

        if _result != 0:
            _bc_result = self.KEX.call(self.KEX.api.bc_tx.broadcast,
                                       [_di.ui.raw_tx])
            if _bc_result != '':
                _bc_result = json.loads(_bc_result)

                if 'error' in _bc_result.keys():
                    _msg = _bc_result['error']
                    _msg_t = 1
                else:
                    _msg = 'TX Sent!'
                    _msg_t = 2
                _ = self.warning_dialog(_msg, False, _msg_t)
            else:
                _ = self.warning_dialog('Call Error', False, 1)

    def create_namespace_send_dialog(self):
        _di = QDialog()
        _di.ui = Ui_keva_op_send_dlg()
        _di.ui.setupUi(_di)
        _di.ui.wallets = self.wallets
        _di.ui.tx_cache = self.tx_cache
        _di.ui.KEX = self.KEX
        _fee = MShared.get_fee_rate(self.KEX)
        if _fee == -1:
            _ = self.warning_dialog('Could not get fee rate!',
                                    False, 1)
            return

        _di.ui.user_path = self.user_path
        _di.ui._new_tx.set_fee(_fee)
        _di.ui.feerate.setText(str(_fee))
        _di.ui.value.setMinimumHeight(28)
        _di.ui.value.setMaximumHeight(28)
        _di.ui.key_v.setVisible(False)
        _di.ui.key_v_l.setVisible(False)
        for _w in self.wallets.wallets:
            if _w.kind != 1 and _w.kind != 3 and _w.locked is False:
                _w.set_updating(True)
                _di.ui.w.addItem(_w.name + ' - ' + str(round(_w.balance, 8)),
                                 _w.name)

        # _di.show()
        _result = _di.exec_()

        for _w in self.wallets.wallets:
            if _w.kind != 1 and _w.kind != 3 and _w.locked is False:
                _w.set_updating(False)

        if _result != 0:
            _bc_result = self.KEX.call(self.KEX.api.bc_tx.broadcast,
                                       [_di.ui.raw_tx])
            if _bc_result != '':
                _bc_result = json.loads(_bc_result)

                if 'error' in _bc_result.keys():
                    _msg = _bc_result['error']
                    _msg_t = 1
                else:
                    _msg = 'TX Sent!'
                    _msg_t = 2
                _ = self.warning_dialog(_msg, False, _msg_t)
            else:
                _ = self.warning_dialog('Call Error', False, 1)

    def create_namespace_key_send_dialog(self):
        _di = QDialog()
        _di.ui = Ui_keva_op_send_dlg()
        _di.ui.setupUi(_di)
        _di.ui.wallets = self.wallets
        _di.ui.tx_cache = self.tx_cache
        _di.ui.KEX = self.KEX
        _fee = MShared.get_fee_rate(self.KEX)
        if _fee == -1:
            _ = self.warning_dialog('Could not get fee rate!',
                                    False, 1)
            return

        _di.ui.user_path = self.user_path
        _di.ui._new_tx.set_fee(_fee)
        _di.ui.feerate.setText(str(_fee))
        _di.setWindowTitle('Narwhallet - Create Key')
        _di.ui.value_l.setText('Value: ')

        _selection = self.ui.ns_tab.tbl_ns.selectedRanges()
        if len(_selection) == 0:
            return

        if _selection[0].topRow() != _selection[0].bottomRow():
            return
        else:
            _row = _selection[0].topRow()
        _w = self.ui.ns_tab.tbl_ns.item(_row, 2).text()
        _wallet = self.wallets.get_wallet_by_name(_w)
        _wallet.set_updating(True)
        _di.ui.w.addItem(_w, _w)
        _di.ui.w.setCurrentIndex(1)
        _di.ui.w.setEnabled(False)

        _di.ui._ns = self.ui.ns_tab.tbl_ns.item(_row, 5).text()
        _di.ui._ns_address = self.ui.ns_tab.tbl_ns.item(_row, 6).text()

        _di.ui.set_availible_usxo(True)

        # _di.show()
        _result = _di.exec_()

        _wallet.set_updating(False)

        if _result != 0:
            _bc_result = self.KEX.call(self.KEX.api.bc_tx.broadcast,
                                       [_di.ui.raw_tx])
            if _bc_result != '':
                _bc_result = json.loads(_bc_result)

                if 'error' in _bc_result.keys():
                    _msg = _bc_result['error']
                    _msg_t = 1
                else:
                    _msg = 'TX Sent!'
                    _msg_t = 2
                    # TODO Check if new key was bid and track used usxo's if so

                _ = self.warning_dialog(_msg, False, _msg_t)
            else:
                _ = self.warning_dialog('Call Error', False, 1)

    def edit_namespace_key_send_dialog(self):
        _di = QDialog()
        _di.ui = Ui_keva_op_send_dlg()
        _di.ui.setupUi(_di)
        _di.ui.wallets = self.wallets
        _di.ui.tx_cache = self.tx_cache
        _di.ui.KEX = self.KEX
        _fee = MShared.get_fee_rate(self.KEX)
        if _fee == -1:
            _ = self.warning_dialog('Could not get fee rate!',
                                    False, 1)
            return

        _di.ui.user_path = self.user_path
        _di.ui._new_tx.set_fee(_fee)
        _di.ui.feerate.setText(str(_fee))
        _di.setWindowTitle('Narwhallet - Create Key')
        _di.ui.value_l.setText('Value: ')

        _selection = self.ui.ns_tab.tbl_ns.selectedRanges()
        if len(_selection) == 0:
            return

        if _selection[0].topRow() != _selection[0].bottomRow():
            return
        else:
            _row = _selection[0].topRow()
        _w = self.ui.ns_tab.tbl_ns.item(_row, 2).text()
        _wallet = self.wallets.get_wallet_by_name(_w)
        _wallet.set_updating(True)
        _di.ui.w.addItem(_w, _w)
        _di.ui.w.setCurrentIndex(1)
        _di.ui.w.setEnabled(False)

        _di.ui._ns = self.ui.ns_tab.tbl_ns.item(_row, 5).text()
        _di.ui._ns_address = self.ui.ns_tab.tbl_ns.item(_row, 6).text()
        _di.ui._ns_key = self.ui.ns_tab.list_ns_keys.currentItem().text()
        _di.ui._ns_value = self.ui.ns_tab.ns_tab_text_key_value.toPlainText()

        _di.ui.set_availible_usxo(True)
        _di.ui.txb_build_simple_send()
        _di.ui.next_btn.setVisible(False)
        _di.ui.back_btn.setVisible(False)

        # _di.show()
        _result = _di.exec_()

        _wallet.set_updating(False)

        if _result != 0:
            _bc_result = self.KEX.call(self.KEX.api.bc_tx.broadcast,
                                       [_di.ui.raw_tx])
            if _bc_result != '':
                _bc_result = json.loads(_bc_result)

                if 'error' in _bc_result.keys():
                    _msg = _bc_result['error']
                    _msg_t = 1
                else:
                    _msg = 'TX Sent!'
                    _msg_t = 2
                _ = self.warning_dialog(_msg, False, _msg_t)
            else:
                _ = self.warning_dialog('Call Error', False, 1)

    def delete_namespace_key_send_dialog(self):
        _di = QDialog()
        _di.ui = Ui_keva_op_send_dlg()
        _di.ui.setupUi(_di)
        _di.ui.wallets = self.wallets
        _di.ui.tx_cache = self.tx_cache
        _di.ui.KEX = self.KEX
        _fee = MShared.get_fee_rate(self.KEX)
        if _fee == -1:
            _ = self.warning_dialog('Could not get fee rate!',
                                    False, 1)
            return

        _di.ui.user_path = self.user_path
        _di.ui._new_tx.set_fee(_fee)
        _di.ui.feerate.setText(str(_fee))
        _di.setWindowTitle('Narwhallet - Delete Key')
        _di.ui.value_l.setText('Value: ')

        _selection = self.ui.ns_tab.tbl_ns.selectedRanges()
        if len(_selection) == 0:
            return

        if _selection[0].topRow() != _selection[0].bottomRow():
            return
        else:
            _row = _selection[0].topRow()
        _w = self.ui.ns_tab.tbl_ns.item(_row, 2).text()
        _wallet = self.wallets.get_wallet_by_name(_w)
        _wallet.set_updating(True)
        _di.ui.w.addItem(_w, _w)
        _di.ui.w.setCurrentIndex(1)
        _di.ui.w.setEnabled(False)

        _di.ui._ns = self.ui.ns_tab.tbl_ns.item(_row, 5).text()
        _di.ui._ns_address = self.ui.ns_tab.tbl_ns.item(_row, 6).text()
        _di.ui._ns_key = self.ui.ns_tab.list_ns_keys.currentItem().text()
        _di.ui._ns_value = ''

        _di.ui.set_availible_usxo(True)
        _di.ui.txb_build_simple_send()
        _di.ui.next_btn.setVisible(False)
        _di.ui.back_btn.setVisible(False)

        # _di.show()
        _result = _di.exec_()
        _wallet.set_updating(False)

        if _result != 0:
            _bc_result = self.KEX.call(self.KEX.api.bc_tx.broadcast,
                                       [_di.ui.raw_tx])
            if _bc_result != '':
                _bc_result = json.loads(_bc_result)

                if 'error' in _bc_result.keys():
                    _msg = _bc_result['error']
                    _msg_t = 1
                else:
                    _msg = 'TX Sent!'
                    _msg_t = 2
                _ = self.warning_dialog(_msg, False, _msg_t)
            else:
                _ = self.warning_dialog('Call Error', False, 1)

    def transfer_namespace_send_dialog(self):
        _di = QDialog()
        _di.ui = Ui_keva_op_send_dlg()
        _di.ui.setupUi(_di)
        _di.ui.wallets = self.wallets
        _di.ui.tx_cache = self.tx_cache
        _di.ui.KEX = self.KEX
        _fee = MShared.get_fee_rate(self.KEX)
        if _fee == -1:
            _ = self.warning_dialog('Could not get fee rate!',
                                    False, 1)
            return

        _di.ui.user_path = self.user_path
        _di.ui._new_tx.set_fee(_fee)
        _di.ui.feerate.setText(str(_fee))
        _di.setWindowTitle('Narwhallet - Transfer Namespace')
        _di.ui.value_l.setText('Value: ')

        _selection = self.ui.ns_tab.tbl_ns.selectedRanges()
        if len(_selection) == 0:
            return

        if _selection[0].topRow() != _selection[0].bottomRow():
            return
        else:
            _row = _selection[0].topRow()
        _w = self.ui.ns_tab.tbl_ns.item(_row, 2).text()
        _wallet = self.wallets.get_wallet_by_name(_w)
        _wallet.set_updating(True)
        _di.ui.w.addItem(_w, _w)
        _di.ui.w.setCurrentIndex(1)
        _di.ui.w.setEnabled(False)

        _di.ui._ns = self.ui.ns_tab.tbl_ns.item(_row, 5).text()
        _di.ui._ns_address = self.ui.ns_tab.tbl_ns.item(_row, 6).text()
        _di.ui.set_availible_usxo(True)

        for _addr in self.address_book.addresses:
            _aa = self.address_book.addresses[_addr].address
            _abi = self.address_book.addresses[_addr].name + ' - '
            _abi = _abi + _aa
            _di.ui.address_book.addItem(_abi, _aa)
        _di.ui.address_book.setVisible(True)

        _di.ui.value.setPlainText(str(time.time()))
        _di.ui.key_v.setText('wxfr')
        _di.ui.next_btn.setEnabled(False)
        _di.ui._isTransfer = True

        # _di.show()
        _result = _di.exec_()

        _wallet.set_updating(False)

        if _result != 0:
            _bc_result = self.KEX.call(self.KEX.api.bc_tx.broadcast,
                                       [_di.ui.raw_tx])
            if _bc_result != '':
                _bc_result = json.loads(_bc_result)

                if 'error' in _bc_result.keys():
                    _msg = _bc_result['error']
                    _msg_t = 1
                else:
                    _msg = 'TX Sent!'
                    _msg_t = 2
                _ = self.warning_dialog(_msg, False, _msg_t)
            else:
                _ = self.warning_dialog('Call Error', False, 1)

    def add_wallet_watch_address_dialog(self):
        _di = QDialog()
        _di.ui = Ui_add_watch_addr_dlg()
        _di.ui.setupUi(_di)
        # _di.show()
        _result = _di.exec_()

        if _result != 0:
            _l = _di.ui.label_d.text()
            if _l == '':
                _l = None
            self.add_wallet_watch(_di.ui.address_d.text(), _l)

    def add_wallet_watch_dialog(self):
        _di = QDialog()
        _di.ui = Ui_add_wallet_watch_dlg()
        _di.ui.setupUi(_di)
        # _di.show()
        _result = _di.exec_()

        if _result != 0:
            self.create_watch_wallet(_di.ui.name_d.text())

    def add_namespace_favorite_dialog(self):
        _di = QDialog()
        _di.ui = Ui_add_ns_fav_dlg()
        _di.ui.setupUi(_di)
        # _di.show()
        _result = _di.exec_()

        if _result != 0:
            self.get_K(int(_di.ui.name_d.text()), 'favorites',
                       self._db_cache, self.KEX, self.tx_cache, self.ns_cache)
            self.refresh_namespace_tab_data()

    def create_wallet_dialog(self):
        _di = QDialog()
        _di.ui = Ui_create_wallet_dlg()
        _di.ui.setupUi(_di)
        # _di.show()
        _result = _di.exec_()
        # _xp = int(_di.ui.lineEdit_1.text())

        if _result != 0:
            _func_call = _di.ui.ret_wallet()
            self.wallets._fromMWallet(_func_call)
            self.wallets.save_wallet(_func_call.name)
            (self.ui.w_tab.tbl_w
             .add_wallet(self.wallets
                         .get_wallet_by_name(_func_call.name).toDict()))
            if _func_call.kind != 1:
                self.ui.u_tab.wallet_select.addItem(_func_call.name)

    def restore_wallet_dialog(self):
        _di = QDialog()
        _di.ui = Ui_restore_wallet_dlg()
        _di.ui.setupUi(_di)
        # _di.show()
        _result = _di.exec_()

        if _result != 0:
            _func_call = _di.ui.ret_wallet()
            self.wallets._fromMWallet(_func_call)
            self.wallets.save_wallet(_func_call.name)
            (self.ui.w_tab.tbl_w
             .add_wallet(self.wallets
                         .get_wallet_by_name(_func_call.name).toDict()))

    @staticmethod
    def warning_dialog(message, isYesNo, msgType):
        _b_ok = QDialogButtonBox.Ok
        _b_cancel = QDialogButtonBox.Cancel
        _di = QDialog()
        _di.ui = Ui_warning_dlg()
        _di.ui.setupUi(_di)
        _di.ui.set_message(message)
        if isYesNo is True:
            _di.ui.buttonBox.button(_b_ok).setText('Yes')
            _di.ui.buttonBox.button(_b_cancel).setText('No')

        if msgType == 1:
            _di.ui.label_1.setPixmap(_di.ui._error_pic)
            _di.ui.buttonBox.button(_b_cancel).setVisible(False)
        elif msgType == 2:
            _di.ui.label_1.setPixmap(_di.ui._success_pic)
            _di.ui.buttonBox.button(_b_cancel).setVisible(False)

        _result = _di.exec()

        return _result

    @staticmethod
    def lockbox_dialog(mode):
        _di = QDialog()
        _di.ui = Ui_lockbox_dlg()
        _di.ui.setupUi(_di, mode)

        _result = _di.exec_()
        _func_call = ''
        if _result != 0:
            _func_call = _di.ui.ret()

        return _func_call

    def view_wallet_address_dialog(self, row, column):
        _di = QDialog()
        _di.ui = Ui_v_addr_dlg()

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
        _di.ui.setupUi(_di)

        _di.ui.label_d.setText(self.ui.w_tab.tbl_addr.item(row, 5).text())
        (_di.ui.address_d
         .setPlainText(self.ui.w_tab.tbl_addr.item(row, 1).text()))
        (_di.ui.details_received_d
         .setText(self.ui.w_tab.tbl_addr.item(row, 2).text()))
        (_di.ui.details_sent_d
         .setText(self.ui.w_tab.tbl_addr.item(row, 3).text()))
        (_di.ui.details_balance_d
         .setText(self.ui.w_tab.tbl_addr.item(row, 4).text()))
        _di.ui.details_locked_d.setText('<todo>')

        _di.ui.set_qr(self.ui.w_tab.tbl_addr.item(row, 1).text())
        _di.ui.set_qr_uri(self.ui.w_tab.tbl_addr.item(row, 1).text())
        # _di.show()
        _result = _di.exec_()

        if _result != 0:
            if _di.ui.label_d.text() != _tmp_label:
                _addr.set_label(_di.ui.label_d.text())
                self.wallets.save_wallet(_w.name)

    def view_wallet_change_address_dialog(self, row, column):
        _di = QDialog()
        _di.ui = Ui_v_change_addr_dlg()

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
        _di.ui.setupUi(_di)

        _di.ui.label_d.setText(self.ui.w_tab.tbl_addr2.item(row, 5).text())
        (_di.ui.address_d
         .setPlainText(self.ui.w_tab.tbl_addr2.item(row, 1).text()))
        (_di.ui.details_received_d
         .setText(self.ui.w_tab.tbl_addr2.item(row, 2).text()))
        (_di.ui.details_sent_d
         .setText(self.ui.w_tab.tbl_addr2.item(row, 3).text()))
        (_di.ui.details_balance_d
         .setText(self.ui.w_tab.tbl_addr2.item(row, 4).text()))
        _di.ui.details_locked_d.setText('<todo>')

        # _di.show()
        _result = _di.exec_()

        if _result != 0:
            if _di.ui.label_d.text() != _tmp_label:
                _addr.set_label(_di.ui.label_d.text())
                self.wallets.save_wallet(_w.name)

    def view_wallet_transaction_dialog(self, row, column):
        _di = QDialog()
        _di.ui = Ui_v_tx_dlg()
        _di.ui.setupUi(_di)

        _ws = self.ui.w_tab.tbl_w.selectedRanges()
        # HACK FIX for no wallet selected:
        if len(_ws) == 0:
            return

        # if _ws[0].topRow() == _ws[0].bottomRow():
        #    _n = self.ui.w_tab.tbl_w.item(_ws[0].topRow(), 3).text()
            # _w = self.wallets.get_wallet_by_name(_n)

        _tr = self.ui.w_tab.tbl_tx.item(row, 5).text()
        _db_cache = SQLInterface(self.cache_path)
        _t = self.tx_cache.get_tx_by_txid(_tr, _db_cache)

        _di.ui.txid_d.setPlainText(_t.txid)
        _di.ui.hash_d.setPlainText(_t.hash)
        _di.ui.blockhash_d.setPlainText(_t.blockhash)
        _di.ui.hex_d.setPlainText(_t.hex)
        _t_dict = _t.toDict()
        _di.ui.json_d.setPlainText(json.dumps(_t_dict, indent=4))

        for vin in range(0, len(_t.vin)):
            _di.ui.add_vin(vin, _t.vin[vin])

        for vout in range(0, len(_t.vout)):
            _di.ui.add_vout(vout, _t.vout[vout])

        _result = _di.exec_()

        if _result != 0:
            pass

    def add_electrumx_peer_dialog(self):
        _di = QDialog(self._v)
        _di.ui = Ui_add_electrumx_peer_dlg()
        _di.ui.setupUi(_di)
        # _di.show()
        _result = _di.exec_()

        # TODO: type validate before dialog accept
        # TODO: check for exsistance before addition
        if _result != 0:
            peer = ['', '', 0, False, False]
            peer[0] = _di.ui.comboBox.currentText()
            peer[1] = _di.ui.lineEdit.text()
            peer[2] = _di.ui.lineEdit_2.text()
            peer[3] = False if _di.ui.checkBox.checkState() == 0 else True

            _p = {'coin': peer[0],
                  'host': peer[1],
                  'port': peer[2], 'type': 'HTTP',
                  'tls': peer[3],
                  'ping': '0ms', 'status': 'disconnected'}

            self.settings.add_electrumx_peer(peer)
            _ = self.KEX.add_peer(peer[1], int(peer[2]),
                                  bool(peer[3]), peer[4])
            self.ui.settings_tab.elxp_tbl.add_peer(_p)

            _dat = ConfigLoader(os.path.join(self.user_path, 'settings.json'))
            _dat.save(json.dumps(self.settings.toDict(), indent=4).encode())

    def add_addressbook_item_dialog(self):
        _di = QDialog()
        _di.ui = Ui_add_ab_item_dlg()
        _di.ui.setupUi(_di)
        # _di.show()
        _result = _di.exec_()

        if _result != 0:
            _func_call = _di.ui.ret_address()
            if _func_call.address not in self.address_book.addresses:
                self.address_book._addresses[_func_call.address] = _func_call
                self.address_book.save_address_book()
                self.ui.ab_tab.tbl_addr._add_bookaddress(_func_call.toDict())
                self.ui.ab_tab.tbl_addr.resizeColumnsToContents()

    def view_addressbook_item_dialog(self, row):
        _di = QDialog(self._v)
        _di.ui = Ui_v_ab_item_dlg()
        _di.ui.setupUi(_di)
        # _di.show()
        _addr = self.ui.ab_tab.tbl_addr.item(row, 3).text()
        _addr_name = self.ui.ab_tab.tbl_addr.item(row, 2).text()
        _addr_label = self.ui.ab_tab.tbl_addr.item(row, 6).text()
        _di.ui.lineEdit.setText(_addr_name)
        _di.ui.lineEdit_3.setPlainText(_addr)
        _di.ui.lineEdit_2.setText(_addr_label)

        _di.ui.set_qr(_addr)
        _di.ui.set_qr_uri(_addr)
        _result = _di.exec_()

        if _result != 0:
            _update_table = False
            if _addr_label != _di.ui.lineEdit_2.text():
                (self.address_book.addresses[_addr]
                 .set_label(_di.ui.lineEdit_2.text()))
                _update_table = True

            if _addr_name != _di.ui.lineEdit.text():
                (self.address_book.addresses[_addr]
                 .set_name(_di.ui.lineEdit.text()))
                _update_table = True

            if _update_table is True:
                self.address_book.save_address_book()
                (self.ui.ab_tab.tbl_addr
                 .add_bookaddresses(self.address_book.toDictList()))
