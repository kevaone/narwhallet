import os
import json
import shutil
import time
from typing import Dict, List, Optional
from PyQt5.QtCore import QThread, Qt
from PyQt5.QtGui import QClipboard

from narwhallet.control.narwhallet_settings import MNarwhalletSettings
from narwhallet.control.ui.dialogs import MDialogs
from narwhallet.control.shared import MShared

from narwhallet.core.kui.main import NarwhalletUI
from narwhallet.core.kui.kexc_worker import Worker
from narwhallet.core.kui.ux.widgets.generator import UShared

from narwhallet.core.kex import KEXclient
from narwhallet.core.kcl.file_utils import ConfigLoader
from narwhallet.core.kcl.cache import MCache
from narwhallet.core.kcl.wallet import MAddress, MWallet, MWallets
from narwhallet.core.kcl.addr_book import MBookAddresses
from narwhallet.core.kcl.transaction import keva_psbt, MTransaction
from narwhallet.core.kcl.wallet_utils import _wallet_utils as WalletUtils
from narwhallet.core.ksc.utils import Ut


class NarwhalletController():
    def __init__(self, view: NarwhalletUI, program_path: str,
                 clipboard: QClipboard):
        self._v: NarwhalletUI = view
        self.ui = self._v.ui
        self.program_path: str = program_path
        self.user_path: str = self.set_paths()
        self.cache_path = os.path.join(self.user_path, 'narwhallet_cache.db')
        self.settings: MNarwhalletSettings = MNarwhalletSettings()
        self.wallets: MWallets = MWallets()
        self.cache = MCache(self.cache_path)
        self.address_book: MBookAddresses = MBookAddresses()
        self._t: Dict[str, QThread] = {}
        self._o: Dict[str, Worker] = {}
        self.KEX: KEXclient = KEXclient()
        self.ws: int = -1  # NOTE Selected wallet index in table
        self._clipboard: QClipboard = clipboard

        self.dialogs: MDialogs = MDialogs(self.user_path,
                                          self.settings,
                                          self._v, self.KEX, self.wallets,
                                          self.cache, self.address_book)

        self.load_settings()
        self.load_wallets()
        self._connect_signals()

    def copy_to_clipboard(self, data):
        self._clipboard.setText(data)

    def set_paths(self) -> str:
        _user_home = os.path.expanduser('~')
        _narwhallet_path = os.path.join(_user_home, '.narwhallet')

        if os.path.isdir(_narwhallet_path) is False:
            # TODO Add error handling
            os.mkdir(_narwhallet_path)
            os.mkdir(os.path.join(_narwhallet_path, 'wallets'))

        if os.path.isfile(os.path.join(_narwhallet_path,
                                       'settings.json')) is False:
            print('settings.json created.')
            shutil.copy(os.path.join(self.program_path,
                                     'config/settings.json'), _narwhallet_path)

        if os.path.isfile(os.path.join(_narwhallet_path,
                                       'narwhallet.addressbook')) is False:
            print('narwhallet.addressbook created.')
            shutil.copy(os.path.join(self.program_path,
                                     'config/narwhallet.addressbook'),
                        _narwhallet_path)

        if os.path.isfile(os.path.join(_narwhallet_path,
                                       'special_keys.json')) is False:
            print('special_keys.json created.')
            shutil.copy(os.path.join(self.program_path,
                                     'config/special_keys.json'),
                        _narwhallet_path)

        return _narwhallet_path

    def _add_wallet(self, wallet: MWallet):
        self.wallets.from_mwallet(wallet)
        self.wallets.save_wallet(wallet.name)
        self.ui.w_tab.tbl_w.add_wallet(wallet.to_dict())
        if wallet.kind != 1:
            self.ui.u_tab.wallet_combo.combo.addItem(wallet.name)

    def create_wallet(self):
        _wallet = self.dialogs.create_wallet_dialog()
        if _wallet is not None:
            self._add_wallet(_wallet)

    def restore_wallet(self):
        _wallet = self.dialogs.restore_wallet_dialog()
        if _wallet is not None:
            self._add_wallet(_wallet)

    def create_watch_wallet(self):
        _name = self.dialogs.add_wallet_watch_dialog()
        if _name != '':
            _w = MWallet()
            _w.set_kind(3)
            _w.set_coin('KEVACOIN')
            _w.set_bip('bip49')
            _w.set_name(_name)
            self.wallets.from_mwallet(_w)
            self.wallets.save_wallet(_w.name)
            self.ui.w_tab.tbl_w.add_wallet(_w.to_dict())

    def add_wallet_watch(self):
        _a, _l = self.dialogs.add_wallet_watch_address_dialog()
        if _a != '':
            _n = self.ui.w_tab.tbl_w.gtext(self.ws, 3)
            if isinstance(_n, str):
                _w = self.wallets.get_wallet_by_name(_n)
                if _w is not None:
                    _w.addresses.from_pool(_a, _l)
                    self.wallets.save_wallet(_w.name)

    def add_addressbook_item(self):
        _address = self.dialogs.add_addressbook_item_dialog()
        if _address is not None:
            if _address.address not in self.address_book.addresses:
                self.address_book.addresses[_address.address] = _address
                self.address_book.save_address_book()
                self.ui.ab_tab.tbl_addr.add_bookaddress(_address.to_dict())
                self.ui.ab_tab.tbl_addr.resizeColumnsToContents()

    def add_namespace_favorite(self):
        _shortcode = self.dialogs.add_namespace_favorite_dialog()
        if _shortcode != 0:
            MShared.get_K(int(_shortcode), self.cache, self.KEX)

            self.refresh_namespace_tab_data()

    def load_wallets(self):
        self.wallets.set_root_path(os.path.join(self.user_path, 'wallets'))
        for file in os.listdir(self.wallets.root_path):
            _tf = os.path.isdir(os.path.join(self.wallets.root_path, file))
            if _tf is False:
                self.wallets.load_wallet(file)
                _w = self.wallets.get_wallet_by_name(file)
                if _w is not None:
                    self.ui.w_tab.tbl_w.add_wallet(_w.to_dict())
                    if _w.kind != 1 and _w.kind != 3 and _w.locked is False:
                        self.ui.u_tab.wallet_combo.combo.addItem(_w.name)
        self.ui.w_tab.tbl_w.resizeColumnsToContents()
        self.refresh_namespace_tab_data()

    def load_settings(self):
        # TODO Clean up
        self.set_dat = ConfigLoader(os.path.join(self.user_path,
                                                 'settings.json'))
        self.set_dat.load()
        self.settings.from_dict(self.set_dat.data)
        self.cache.interface.setup_tables()

        _special_keys = ConfigLoader(os.path.join(self.user_path,
                                                  'special_keys.json'))
        _special_keys.load()
        self.cache.ns.set_special_keys(_special_keys.data)

        try:
            self.address_book.load_address_book(self.user_path)
            (self.ui.ab_tab.tbl_addr
             .add_bookaddresses(self.address_book.to_dict_list()))
        except Exception:
            print('Error Loading address book')

        self.ui.settings_tab.path_meta_e.setPlainText(self.user_path)

        _sync: Dict[str, List[bool, bool, int]] = self.settings.sync
        self.ui.settings_tab.s_a_wallet.setChecked(_sync['wallets'][0])
        self.ui.settings_tab.s_t_wallet_l.setChecked(_sync['wallets'][1])
        self.ui.settings_tab.s_t_wallet_e.setText(str(_sync['wallets'][2]))

        self.KEX.active_peer = self.settings.primary_peer
        for peer in self.settings.electrumx_peers:
            self.ui.settings_tab.elxp_tbl.add_peer(peer[0], peer[1],
                                                   peer[2], peer[3])

            _ = self.KEX.add_peer(peer[1], int(peer[2]), peer[3], peer[4])

        if self.settings.electrumx_auto_connect:
            (self.ui.settings_tab.elxp_tbl
             .update_peer_status(self.settings.primary_peer, 'connecting...'))
            _tn = self.KEX.peers[self.settings.primary_peer].host
            _tn = _tn + ':'
            _tn = _tn + str(self.KEX.peers[self.settings.primary_peer].port)
            self.threader(_tn,
                          self.KEX.peers[self.settings.primary_peer].connect,
                          None, None, self.ex_c, self.settings.primary_peer)
        self.ui.settings_tab.elxp_tbl.update_active(self.settings.primary_peer)

        self.ui.w_tab.tbl_addr2.hideColumn(6)
        (self.ui.settings_tab.auto_lock_e
         .setText(str(self.settings.auto_lock_timer)))
        self.ui.settings_tab.show_change.setChecked(self.settings.show_change)
        self.ui.w_tab.tabWidget_2.setTabVisible(2, self.settings.show_change)

    def reset_cache(self):
        _msg = 'Are you sure you want to reset transaction/namespace caches?'
        if self.dialogs.warning_dialog(_msg, True, 0) == 1:
            self.cache.interface.reset_tables()
            self.ui.w_tab.tbl_w.clearSelection()
            self.refresh_namespace_tab_data()

    def threader(self, name: str, command, command_params_1,
                 command_params_2, work_done_func, optional: int = -1):
        # 1 - create Worker and Thread inside the Form, no parent!
        self._o[name] = Worker(name, command, command_params_1,
                               command_params_2, optional)
        self._t[name] = QThread()
        # 2 - Connect Worker`s Signals to Form method slots to post data.
        self._o[name].work_done.connect(work_done_func)
        # 3 - Move the Worker object to the Thread object
        self._o[name].moveToThread(self._t[name])
        # 4 - Connect Worker Signals to the Thread slots
        self._o[name].finished.connect(self._t[name].quit)
        # 5 - Connect Thread started signal to Worker operational slot method
        if 'timer' not in name:
            self._t[name].started.connect(self._o[name].do_work)
        else:
            self._t[name].started.connect(self._o[name].do_timer_work)
        # 6 - Start the thread
        self._t[name].start()

    def lock_wallet(self, name):
        _reloaded = self.wallets.relock_wallet(name)
        if _reloaded is True:
            _r = self.ui.w_tab.tbl_w.findItems(name, Qt.MatchFlag.MatchExactly)
            if len(_r) == 1:
                _w = self.wallets.get_wallet_by_name(name)
                if _w is not None:
                    self.ui.w_tab.tbl_w.update_wallet(_w, _r[0].row())
                    if self.ui.w_tab.tbl_w.currentRow() == _r[0].row():
                        self.refresh_wallet_data_tabs('', '', _r[0].row())

    def t_restart(self, i: str):
        # print('timer restarting', i)
        self._t[i].quit()
        self._t[i].wait()

        if i == 'wallet_lock_timer':
            for wallet in self.wallets.wallets:
                self.lock_wallet(wallet.name)

            self.threader(i, time.sleep, 60, None, self.t_restart)
        else:
            if self.settings.sync[i.replace('_timer', '')][1] is True:
                if 'wallets' in i:
                    self._update_wallets()

            if self.settings.sync[i.replace('_timer', '')][2] >= 60:
                self.threader(i, time.sleep,
                              self.settings.sync[i.replace('_timer', '')][2],
                              None, self.t_restart)

    def t_cleanup(self):
        self.cache.interface.close_cursor()
        for k, t in self._o.items():
            t.b = 1

        for k, t in self._t.items():
            if t.isRunning():
                print('Closing thread', k)
                t.quit()
                t.wait()

    def _connect_signals(self):
        self.ui.w_tab.tbl_w.itemSelectionChanged.connect(self.wallet_selected)
        self.ui.w_tab.tbl_w.cellClicked.connect(self.wallet_selected)
        self.ui.w_tab.tbl_addr.cellClicked.connect(self.w_address_selected)
        self.ui.w_tab.tbl_addr2.cellClicked.connect(self.w_c_address_selected)
        self.ui.w_tab.tbl_tx.cellClicked.connect(self.w_tx_selected)
        self.ui.w_tab.btn_addr.clicked.connect(self._get_unused_address)
        self.ui.w_tab.btn_addr2.clicked.connect(self._get_unused_changeaddress)
        self.ui.w_tab.cpmnemonic.clicked.connect(self.w_mnemnomic_copy_click)
        self.ui.w_tab.cpseed.clicked.connect(self.wallet_seed_copy_click)
        self.ui.w_tab.cpxprv.clicked.connect(self.wallet_xprv_copy_click)
        self.ui.w_tab.cpxpub.clicked.connect(self.wallet_xpub_copy_click)
        self.ui.ab_tab.tbl_addr.cellClicked.connect(self.ab_address_selected)
        self.ui.ns_tab.tbl_ns.itemSelectionChanged.connect(self.ns_selected)
        self.ui.ns_tab.tbl_ns.cellClicked.connect(self.ns_cell_clicked)
        (self.ui.ns_tab.list_ns_keys
         .itemSelectionChanged.connect(self.ns_key_selected))
        self.ui.ns_tab.btn_val_edit.clicked.connect(self.ns_key_value_edit)
        # self.ui.ns_tab.btn_val_save.clicked.connect(self.ns_key_value_save)
        self.ui.ns_tab.btn_val_del.clicked.connect(self.ns_key_delete_click)
        self.ui.ns_tab.sel_ns_sc_bvpic.clicked.connect(self.ns_sc_copy_click)
        self.ui.ns_tab.sel_ns_n_bvpic.clicked.connect(self.ns_name_copy_click)
        (self.ui.nft_tab.tbl_auctions
         .itemSelectionChanged.connect(self.nft_auction_selected))
        (self.ui.nft_tab.tbl_auctions
         .cellClicked.connect(self.nft_auction_selected))
        (self.ui.nft_tab.tbl_bids
         .itemSelectionChanged.connect(self.nft_mybid_selected))
        self.ui.nft_tab.tbl_bids.cellClicked.connect(self.nft_mybid_selected)
        (self.ui.nft_tab.tbl_bids_2
         .itemSelectionChanged.connect(self.nft_bid_selected))
        self.ui.nft_tab.tbl_bids_2.cellClicked.connect(self.nft_bid_selected)
        (self.ui.u_tab.wallet_combo.combo
         .currentTextChanged.connect(self.sign_wallet_changed))
        (self.ui.u_tab.address_combo.combo
         .currentTextChanged.connect(self.sign_address_changed))
        self.ui.u_tab.sbutton.clicked.connect(self.sign_message)
        self.ui.u_tab.vbutton.clicked.connect(self.verify_message)
        self.ui.u_tab.mv_submit.clicked.connect(self.util_submit)
        self.ui.settings_tab.reset_cache.clicked.connect(self.reset_cache)
        (self.ui.settings_tab.elxp_tbl
         .cellClicked.connect(self.electrumx_peer_selected))
        # Dialogs
        self.ui.w_tab.btn_send.clicked.connect(self.dialogs.simple_send_dialog)
        (self.ui.ns_tab.btn_create
         .clicked.connect(self.dialogs.create_namespace_send_dialog))
        (self.ui.ns_tab.btn_fav
         .clicked.connect(self.add_namespace_favorite))
        (self.ui.ns_tab.btn_key_add
         .clicked.connect(self.dialogs.create_namespace_key_send_dialog))
        (self.ui.nft_tab.btn_create_auction
         .clicked.connect(self.dialogs.auction_namespace_dialog))
        (self.ui.nft_tab.btn_create_bid
         .clicked.connect(self.dialogs.bid_namespace_dialog))
        (self.ui.nft_tab.btn_create_accept_bid
         .clicked.connect(self.dialogs.accept_bid_namespace_dialog))
        (self.ui.w_tab.btn_watch_addr
         .clicked.connect(self.add_wallet_watch))
        (self.ui.w_tab.btn_create
         .clicked.connect(self.create_wallet))
        (self.ui.w_tab.btn_restore
         .clicked.connect(self.restore_wallet))
        (self.ui.w_tab.btn_watch
         .clicked.connect(self.create_watch_wallet))
        (self.ui.ab_tab.btn_create
         .clicked.connect(self.add_addressbook_item))
        (self.ui.settings_tab.elxp_btn_add
         .clicked.connect(self.dialogs.add_electrumx_peer_dialog))

        (self.ui.settings_tab.auto_lock_e
         .textChanged.connect(self.save_settings))
        self.ui.settings_tab.show_change.clicked.connect(self.show_change)
        self.ui.settings_tab.s_a_wallet.clicked.connect(self.save_settings)
        self.ui.settings_tab.s_t_wallet_l.clicked.connect(self.save_settings)
        (self.ui.settings_tab.s_t_wallet_e
         .textChanged.connect(self.save_settings))

        if self.settings.auto_lock_timer >= 30:
            self.threader('wallet_lock_timer', time.sleep,
                          self.settings.auto_lock_timer, None, self.t_restart)

        if self.settings.sync['wallets'][2] >= 60:
            self.threader('wallets_timer', time.sleep,
                          self.settings.sync['wallets'][2],
                          None, self.t_restart)

    def util_submit(self, _i):
        _selected = self.ui.u_tab.m_select.currentText()
        _input = self.ui.u_tab.msa_e.toPlainText()
        _results = self.ui.u_tab.mvs_result.toPlainText()
        # if self.ui.u_tab.mishex.isChecked() is True:
        #     _input_value = _input.replace('\n', '')
        #     _input_value = Ut.hex_to_bytes(_input_value)

        if _selected == 'Sha256':
            _result = Ut.bytes_to_hex(Ut.sha256(_input))
        elif _selected == 'dSha256':
            _res = Ut.sha256(Ut.sha256(_input))
            _result = Ut.bytes_to_hex(_res)
        elif _selected == 'Hash160':
            _result = Ut.bytes_to_hex(Ut.hash160(_input))
        elif _selected == 'int4byte':
            _in = int(_input)
            _res = Ut.int_to_bytes(_in, 4, 'little')
            _result = Ut.bytes_to_hex(_res)
        elif _selected == 'int8byte':
            _in = int(_input)
            _res = Ut.int_to_bytes(_in, 8, 'little')
            _result = Ut.bytes_to_hex(_res)
        elif _selected == 'Reverse':
            _res = Ut.reverse_bytes(_input.encode())
            _result = Ut.bytes_to_hex(_res)

        self.ui.u_tab.mvs_result.setPlainText(_result + '\n' + _results)

    def wa_ad_click(self, row: int, _column: int):
        self.ui.w_tab.tbl_addr.selectRow(row)

    def ex_c_done(self, flag):
        if flag == 'svr_version' and self.settings.sync['wallets'][0] is True:
            self._update_wallets()

    def _ex_c(self):
        _return = self.KEX.call(self.KEX.api.server.version('Narwhallet',
                                                            1.4, self.KEX.id))
        return _return

    def ex_c(self, _n: str, m: str, i: int):
        self.ui.settings_tab.elxp_tbl.update_peer_status(i, m)

        if m == 'connected':
            self.threader('svr_version', self._ex_c, None, None,
                          self.ex_c_done, -1)
            # self.threader('block_count', self.KEX.call,
            #               self.KEX.api.blockchain_block.count, [],
            #               self.ex_c_done, None)

    def save_settings(self):
        try:
            (self.settings.set_auto_lock_timer(
                int(self.ui.settings_tab.auto_lock_e.text())))
            _s = self.settings.sync
            _s['wallets'][0] = self.ui.settings_tab.s_a_wallet.isChecked()
            _s['wallets'][1] = self.ui.settings_tab.s_t_wallet_l.isChecked()
            _s['wallets'][2] = int(self.ui.settings_tab.s_t_wallet_e.text())
        except Exception:
            return False
        self.set_dat.save(json.dumps(self.settings.to_dict()))
        return True

    def show_change(self):
        (self.settings
         .set_show_change(self.ui.settings_tab.show_change.isChecked()))
        self.ui.w_tab.tabWidget_2.setTabVisible(2, self.settings.show_change)
        self.set_dat.save(json.dumps(self.settings.to_dict()))

    def refresh_wallet_data_tabs(self, _c: str, _m: str, i: int):
        _n = self.ui.w_tab.tbl_w.gtext(i, 3)
        if _n is not None:
            wallet = self.wallets.get_wallet_by_name(_n)
        else:
            wallet = None

        self.refresh_namespace_tab_data()
        if wallet is not None:
            if i == self.ws:
                (self.ui.w_tab.tbl_addr
                 .add_addresses(wallet.addresses.to_dict_list()))
                if self.ui.w_tab.tabWidget_2.isTabVisible(2):
                    (self.ui.w_tab.tbl_addr2
                     .add_addresses(wallet.change_addresses.to_dict_list()))
                (self.ui.w_tab.tbl_tx
                 .add_transactions(self._display_wallet_tx(wallet)))
                self.ui.w_tab.set_info_values(wallet)

            (self.ui.w_tab.tbl_w.stext(i, 6,
             str(round(wallet.balance - wallet.bid_balance, 8))))

            if wallet.bid_balance > 0:
                self.wallets.save_wallet(wallet.name)
            (self.ui.w_tab.tbl_w.stext(i, 7,
             str(round(wallet.bid_balance, 8))))
            (self.ui.w_tab.tbl_w.stext(i, 8,
             MShared.get_timestamp(wallet.last_updated)[1]))

            wallet.set_updating(False)
            self.ui.w_tab.tbl_w.cellWidget(i, 9).ani.stop()

        self.ui.w_tab.tbl_w.resizeColumnsToContents()

    def refresh_nft_tab_data(self, namespaces: List[dict]):
        UShared.remove_table_rows(self.ui.nft_tab.tbl_auctions)
        UShared.remove_table_rows(self.ui.nft_tab.tbl_bids)
        # self.ui.nft_tab.tbl_auctions.clear_rows()
        # self.ui.nft_tab.tbl_bids.clear_rows()
        _wallet_bid_tx = []

        for ns in namespaces:
            _auctions = self.cache.ns.get_namespace_auctions(ns['namespaceid'])
            _bids = self.cache.ns.get_namespace_bids(ns['namespaceid'])

            _auc = []
            for _a in _auctions:
                _tx_time = self.cache.tx.get_tx_time(_a[2])
                _d = [_tx_time, ns['shortcode'],
                      json.loads(_a[4])['price'] + ' KVA', '0',
                      '0.0' + ' KVA', _a[3], _a[2]]
                _auc.append(_d)

            _bi = []
            for _b in _bids:
                _tx_time = self.cache.tx.get_tx_time(_b[2])
                _tx = self.cache.tx.get_tx_vout(_b[4][4:])
                _t = _tx[0][2].split(' ')
                _tx_ns = self.cache.ns.convert_to_namespaceid(_t[1])
                _tx_value = Ut.hex_to_bytes(_t[3]).decode()
                _tx_value = json.loads(_tx_value)['price'] + ' KVA'
                try:
                    _tx_ns_sc = self.cache.ns.ns_block(_tx_ns)[0]
                    _s_b = str(_tx_ns_sc[0])
                    _tx_ns_sc = str(len(_s_b)) + _s_b + str(_tx_ns_sc[1])
                except Exception:
                    _tx_ns_sc = 'Error'
                _bid_psbt = keva_psbt(_b[5])

                for _vi in _bid_psbt.tx.vin:
                    _wallet_bid_tx.append([ns['wallet'], _vi.txid, _vi.vout])

                _d = [_tx_time, ns['shortcode'], _tx_ns_sc, _tx_value,
                      'high_bid' + ' KVA',
                      str(_bid_psbt.tx.vout[1].value / 100000000) + ' KVA',
                      _tx_ns, _b[4][4:]]
                _bi.append(_d)

            if len(_auctions) > 0:
                self.ui.nft_tab.tbl_auctions.add_auctions(ns['wallet'], _auc)

            if len(_bids) > 0:
                self.ui.nft_tab.tbl_bids.add_bids(ns['wallet'], _bi)

        self._scan_wallets_for_bids(_wallet_bid_tx)

    def _scan_wallets_for_bids(self, _wallet_bid):
        for _btx in _wallet_bid:
            _w = self.wallets.get_wallet_by_name(_btx[0])

            # TODO Cleanup better, this not necessarily clear
            if _w is None:
                continue

            for _ad in _w.addresses.addresses:
                for _us in _ad.unspent_tx:
                    _x = _us
                    if _x['tx_hash'] == _btx[1] and _x['tx_pos'] == _btx[2]:
                        (_w.set_bid_balance(
                            _w.bid_balance + (_us['value'] / 100000000)))
                        _w.add_bid_tx([_btx[1], _btx[2],
                                       _us['value'] / 100000000])

            for _ad in _w.change_addresses.addresses:
                for _us in _ad.unspent_tx:
                    _x = _us
                    if _x['tx_hash'] == _btx[1] and _x['tx_pos'] == _btx[2]:
                        (_w.set_bid_balance(
                            _w.bid_balance + (_us['value'] / 100000000)))
                        _w.add_bid_tx([_btx[1], _btx[2],
                                       _us['value'] / 100000000])

    def _set_ns_wallet_name(self, address, wallet: MWallet):
        _name = ''
        for _a in wallet.addresses.addresses:
            if address == _a.address:
                _name = wallet.name
                # TODO Notify user if namespace detected in change address
        for _a in wallet.change_addresses.addresses:
            if address == _a.address:
                _name = wallet.name
        return _name

    def refresh_namespace_tab_data(self):
        # TODO Cleanup
        UShared.remove_table_rows(self.ui.ns_tab.tbl_ns)
        # UShared.remove_table_rows(self.ui.ns_tab.list_ns_keys)
        # self.ui.ns_tab.tbl_ns.clear_rows()
        self.ui.ns_tab.list_ns_keys.clear_rows()
        _asa = self.cache.ns.get_view()

        nd = []
        for p in _asa:
            _key_count = self.cache.ns.key_count(p[0])
            _block = self.cache.ns.ns_block(p[0])
            _oa = self.cache.ns.last_address(p[0])

            pd = {}
            pd['namespaceid'] = p[0]
            pd['address'] = _oa[0][0]
            pd['key_count'] = _key_count[0][0]
            _bl = _block[0][0]
            pd['shortcode'] = str(len(str(_bl)))+str(_bl)+str(_block[0][1])

            pd['date'] = time.time()
            _wallet_name = ''
            for wallet in self.wallets.wallets:
                if wallet.kind != 0:
                    continue

                if _wallet_name != '':
                    break

                _wallet_name = self._set_ns_wallet_name(_oa[0][0], wallet)

            if _wallet_name != '':
                pd['wallet'] = _wallet_name
            else:
                for wallet in self.wallets.wallets:
                    if wallet.kind not in (1, 3):
                        continue

                    for address in wallet.addresses.addresses:
                        if _oa[0][0] == address.address:
                            pd['wallet'] = wallet.name

            if 'wallet' in pd:
                nd.append(pd)

        self.ui.ns_tab.tbl_ns.add_namespaces('_w.name', nd)
        self.refresh_nft_tab_data(nd)

    def wallet_lock(self, wallet: MWallet):
        if wallet.state_lock == 0:
            _msg = 'Wallet is not encrypted.\n\nDo you wish to encrypt?'
            _warn = self.dialogs.warning_dialog(_msg, True, 0)
            if _warn == 1:
                _up = self.dialogs.lockbox_dialog(1)
                if _up != '':
                    wallet.set_k(_up)
                    wallet.set_state_lock(1)
                    wallet.set_locked(False)
                    self.wallets.save_wallet(wallet.name)
                    self.lock_wallet(wallet.name)

    def electrumx_peer_selected(self, row: int, column: int):
        if column == 9:
            self.ui.settings_tab.elxp_tbl.update_active(row)
            self.KEX.peers[self.settings.primary_peer].disconnect()
            (self.ui.settings_tab.elxp_tbl
             .update_peer_status(self.settings.primary_peer, 'disconnected'))
            self.settings.set_primary_peer(row)
            self.set_dat.save(json.dumps(self.settings.to_dict()))
            (self.ui.settings_tab.elxp_tbl
             .update_peer_status(self.settings.primary_peer, 'connecting...'))
            self.KEX.active_peer = self.settings.primary_peer
            _tn = self.KEX.peers[self.settings.primary_peer].host
            _tn = _tn + ':'
            _tn = _tn + str(self.KEX.peers[self.settings.primary_peer].port)
            self.threader(_tn,
                          self.KEX.peers[self.settings.primary_peer].connect,
                          None, None, self.ex_c, self.settings.primary_peer)

    def _update_wallets(self):
        for row in range(self.ui.w_tab.tbl_w.rowCount()):
            _n = self.ui.w_tab.tbl_w.gtext(row, 3)
            _w = None

            if _n is not None:
                _w = self.wallets.get_wallet_by_name(_n)

            if _w is not None:
                # TODO Add these checks to MWallet
                if (_w.last_updated != '' and
                        _w.last_updated is not None and
                        _w.locked is False):
                    _current_time = MShared.get_timestamp()[0]
                    if _current_time - float(_w.last_updated) >= 60:
                        if _w.updating is not True:
                            _w.set_updating(True)
                            self.ui.w_tab.tbl_w.cellWidget(row, 9).ani.start()
                            self.update_wallet(_w, row)

    def _wallet_check_lock(self, row: int, column: int, wallet: MWallet):
        if wallet.locked is False and column == 1:
            self.wallet_lock(wallet)
        elif wallet.locked is True and column in (1, 9):
            _ulk = self.dialogs.lockbox_dialog(0)
            if _ulk != '':
                wallet.set_k(_ulk)
                self.wallets.load_wallet(wallet.name, wallet)

                if wallet.coin is not None:
                    wallet.set_locked(False)
                    self.ui.w_tab.tbl_w.update_wallet(wallet, row)
                    self.refresh_namespace_tab_data()
                    if wallet.kind not in (1, 3):
                        self.ui.u_tab.wallet_combo.combo.addItem(wallet.name)

    def wallet_selected(self, row: int = -1, column: int = -1):
        self.ui.w_tab.tbl_tx.clearSelection()
        self.ui.w_tab.tbl_addr.clearSelection()
        self.ui.w_tab.tbl_addr2.clearSelection()
        if row == -1:
            _row = self.ui.w_tab.tbl_w.selectedRanges()
            if len(_row) > 0:
                row = _row[0].topRow()
            else:
                row = -1
        else:
            self.ui.w_tab.tbl_w.selectRow(row)

        if self.ws != row:
            self.ws = row

        if row == -1:
            UShared.remove_table_rows(self.ui.w_tab.tbl_addr)
            UShared.remove_table_rows(self.ui.w_tab.tbl_addr2)
            UShared.remove_table_rows(self.ui.w_tab.tbl_tx)
            # self.ui.w_tab.tbl_addr.clear_rows()
            # self.ui.w_tab.tbl_addr2.clear_rows()
            # self.ui.w_tab.tbl_tx.clear_rows()
            self.ui.w_tab.reset_info_values()
            return

        _n = self.ui.w_tab.tbl_w.gtext(row, 3)
        if _n is None:
            return

        _w = self.wallets.get_wallet_by_name(_n)
        if _w is None:
            return

        self._wallet_check_lock(row, column, _w)

        self.ui.w_tab.tbl_addr.add_addresses(_w.addresses.to_dict_list())
        if self.ui.w_tab.tabWidget_2.isTabVisible(2):
            (self.ui.w_tab.tbl_addr2
             .add_addresses(_w.change_addresses.to_dict_list()))
        self.ui.w_tab.tbl_tx.add_transactions(self._display_wallet_tx(_w))
        self.ui.w_tab.set_info_values(_w)
        _last_update = _w.last_updated

        if column == 9 and _w.locked is False:
            if _last_update != '' and _last_update is not None:
                _current_time = MShared.get_timestamp()[0]
                if _current_time - float(_last_update) >= 60:
                    if _w.updating is not True:
                        _w.set_updating(True)
                        self.ui.w_tab.tbl_w.cellWidget(row, 9).ani.start()
                        self.update_wallet(_w, row)
            else:
                if _w.updating is not True:
                    _w.set_updating(True)
                    self.ui.w_tab.tbl_w.cellWidget(row, 9).ani.start()
                    self.update_wallet(_w, row)

    def w_tx_selected(self, row: int, column: int):
        self.ui.w_tab.tbl_tx.selectRow(row)
        if column == 0:
            self.dialogs.view_wallet_transaction_dialog(row, column)

    def w_address_selected(self, row: int, column: int):
        self.ui.w_tab.tbl_addr.selectRow(row)
        if column == 0:
            self.dialogs.view_wallet_address_dialog(row, column)
        elif column == 6:
            _data = self.ui.w_tab.tbl_addr.gtext(row, 1)
            if _data is None:
                _data = ''
            self.copy_to_clipboard(_data)

    def w_c_address_selected(self, row: int, column: int):
        self.ui.w_tab.tbl_addr2.selectRow(row)
        if column == 0:
            self.dialogs.view_wallet_change_address_dialog(row, column)

    def w_mnemnomic_copy_click(self, _data):
        self.copy_to_clipboard(self.ui.w_tab.wmnemonic.toPlainText())

    def wallet_seed_copy_click(self, _data):
        self.copy_to_clipboard(self.ui.w_tab.wseed.toPlainText())

    def wallet_xprv_copy_click(self, _data):
        self.copy_to_clipboard(self.ui.w_tab.wxprv.toPlainText())

    def wallet_xpub_copy_click(self, _data):
        self.copy_to_clipboard(self.ui.w_tab.wxpub.toPlainText())

    def ab_address_selected(self, row: int, column: int):
        self.ui.ab_tab.tbl_addr.selectRow(row)
        _a = self.ui.ab_tab.tbl_addr.gtext(row, 3)
        if _a is None:
            return

        if column == 0:
            self.dialogs.view_addressbook_item_dialog(row)
        elif column == 7:
            _msg = 'Are you sure you want to delete this address?'
            _warn = self.dialogs.warning_dialog(_msg, True, 0)
            if _warn == 1:
                _rm = self.address_book.remove_address(_a)
                if _rm is True:
                    self.address_book.save_address_book()
                    (self.ui.ab_tab.tbl_addr
                     .add_bookaddresses(self.address_book.to_dict_list()))
        elif column == 8:
            self.copy_to_clipboard(_a)

    def ns_cell_clicked(self, _row: int, column: int):
        if column == 7:
            _msg = 'Are you sure you want to transfer this Namespace?'
            _warn = self.dialogs.warning_dialog(_msg, True, 0)
            if _warn == 1:
                self.dialogs.transfer_namespace_send_dialog()

    def ns_selected(self):
        self.ui.ns_tab.list_ns_keys.clearSelection()
        _r = self.ui.ns_tab.tbl_ns.selectedRanges()
        if len(_r) > 0:
            row = _r[0].topRow()
        else:
            self.ui.ns_tab.sel_ns_sc.setText('')
            self.ui.ns_tab.sel_ns_name.setText('')
            return

        _n = self.ui.ns_tab.tbl_ns.gtext(row, 2)
        if _n is None:
            return

        _nst = self.ui.ns_tab.tbl_ns.gtext(row, 5)
        if _nst is None:
            return

        if _n in ('live', 'favorites'):
            _w = MWallet()
            _w.set_kind(3)
        else:
            _tw = self.wallets.get_wallet_by_name(_n)
            if _tw is None:
                return
            else:
                _w = _tw

        _key_count = self.cache.ns.key_count(_nst)

        if len(_key_count) > 0:
            _ns = self.cache.ns.get_namespace_by_id(_nst)
            self.ui.ns_tab.list_ns_keys.add_keys(_ns)

        self.ui.ns_tab.sel_ns_key.setText('No key selected')
        self.ui.ns_tab.sel_ns_key_sp.setText('')
        self.ui.ns_tab.sel_ns_key_tx.setText('')
        self.ui.ns_tab.sel_ns_key_tx_sc.setVisible(False)

        if _w.kind not in (1, 3):
            self.ui.ns_tab.btn_key_add.setEnabled(True)
            self.ui.ns_tab.btn_val_edit.setEnabled(False)
            self.ui.ns_tab.btn_val_del.setEnabled(False)
        else:
            self.ui.ns_tab.btn_key_add.setEnabled(False)
            self.ui.ns_tab.btn_val_edit.setEnabled(False)
            self.ui.ns_tab.btn_val_del.setEnabled(False)

        (self.ui.ns_tab.sel_ns_sc
         .setText(self.ui.ns_tab.tbl_ns.item(row, 3).text()))
        (self.ui.ns_tab.sel_ns_name
         .setText(self.ui.ns_tab.tbl_ns.item(row, 5).text()))

        self.ui.ns_tab.ns_tab_text_key_value.setPlainText('')

    def ns_sc_copy_click(self, _data):
        self.copy_to_clipboard(self.ui.ns_tab.sel_ns_sc.text())

    def ns_name_copy_click(self, _data):
        self.copy_to_clipboard(self.ui.ns_tab.sel_ns_name.text())

    def ns_key_delete_click(self, _data):
        _msg = 'Are you sure you want to delete this key?'
        _warn = self.dialogs.warning_dialog(_msg, True, 0)
        if _warn == 1:
            self.dialogs.delete_namespace_key_send_dialog()

    def ns_key_selected(self):
        row = self.ui.ns_tab.tbl_ns.currentRow()
        if row == -1:
            self.ui.ns_tab.ns_tab_text_key_value.setPlainText('')
            self.ui.ns_tab.sel_ns_key.setText('No key selected')
            self.ui.ns_tab.sel_ns_key_sp.setText('')
            self.ui.ns_tab.sel_ns_key_tx.setText('')
            self.ui.ns_tab.sel_ns_key_tx_sc.setVisible(False)
            return
        _n = self.ui.ns_tab.tbl_ns.gtext(row, 2)
        if _n is None:
            return

        _ns = self.ui.ns_tab.tbl_ns.gtext(row, 5)
        if _ns is None:
            return

        if _n in ('live', 'favorites'):
            _w = MWallet()
            _w.set_kind(3)
        else:
            _w = self.wallets.get_wallet_by_name(_n)

        key = self.ui.ns_tab.list_ns_keys.currentItem()
        _value = self.cache.ns.get_namespace_by_key_value(_ns, key.text())
        self.ui.ns_tab.sel_ns_key.setText('Selected key is special:')

        if len(_value) > 0:
            (self.ui.ns_tab.ns_tab_text_key_value
             .setPlainText(str(_value[0][1])))

            _type = self.cache.ns.get_key_type(key.text(), str(_value[0][1]))
            self.ui.ns_tab.sel_ns_key_sp.setText(_type)
        else:
            _type = None

        if _type is None:
            self.ui.ns_tab.sel_ns_key_sp.setText('No')
            self.ui.ns_tab.sel_ns_key_tx.setText('')
        elif _type in ('nft_bid', 'reply', 'repost', 'reward'):
            _ref_tx = self.cache.tx.get_tx_by_txid(key.text()[4:])
            if _ref_tx is not None:
                self.ui.ns_tab.sel_ns_key_tx.setText(_ref_tx.txid)
            # self.ui.ns_tab.sel_ns_key_tx.setVisible(True)

        if _w.kind not in (1, 3):
            self.ui.ns_tab.btn_val_edit.setEnabled(True)
            if key.text() != '_KEVA_NS_':
                self.ui.ns_tab.btn_val_del.setEnabled(True)
        else:
            self.ui.ns_tab.btn_val_edit.setEnabled(False)
            self.ui.ns_tab.btn_val_del.setEnabled(False)

    def nft_auction_selected(self, row: int = -1, _column: int = -1):
        _row = -1
        if row == -1:
            _r = self.ui.nft_tab.tbl_auctions.selectedRanges()
            if len(_r) > 0:
                _row = _r[0].topRow()
            else:
                _row = -1

        if _row != -1:
            self.ui.nft_tab.tbl_bids.clearSelection()
            self.ui.nft_tab.tbl_auctions.selectRow(_row)
            _auction_ns = self.ui.nft_tab.tbl_auctions.gtext(_row, 8)
            _auction_tx = self.ui.nft_tab.tbl_auctions.gtext(_row, 9)
            if _auction_ns is None:
                self.update_selected_auction_data(None, None, True)
                return
            elif _auction_tx is None:
                return

            _auction = self.cache.ns.get_namespace_auctions(_auction_ns)

            if len(_auction) > 0:
                _reactions = (MShared
                              .get_ns_key_reactions(_auction_tx, self.KEX))
                self.update_selected_auction_data(_auction[0], _reactions)

    def nft_mybid_selected(self, row: int = -1, _column: int = -1):
        _row = -1
        if row == -1:
            _r = self.ui.nft_tab.tbl_bids.selectedRanges()
            if len(_r) > 0:
                _row = _r[0].topRow()
            else:
                _row = -1

        if _row != -1:
            self.ui.nft_tab.tbl_auctions.clearSelection()
            self.ui.nft_tab.tbl_bids.selectRow(_row)
            _auction_ns = self.ui.nft_tab.tbl_bids.gtext(_row, 10)
            _auction_tx = self.ui.nft_tab.tbl_bids.gtext(_row, 11)
            if _auction_ns is None:
                self.update_selected_auction_data(None, None, True)
                return
            elif _auction_tx is None:
                return

            _auction = self.cache.ns.get_namespace_auctions(_auction_ns)

            if len(_auction) > 0:
                _reactions = (MShared
                              .get_ns_key_reactions(_auction_tx, self.KEX))
                self.update_selected_auction_data(_auction[0], _reactions)
            else:
                self.update_selected_auction_data(None, None, True)

    def nft_bid_selected(self, row: int = -1, _column: int = -1):
        if row == -1:
            _row = self.ui.nft_tab.tbl_bids_2.selectedRanges()
            if len(_row) > 0:
                row = _row[0].topRow()
            else:
                row = -1
        else:
            self.ui.nft_tab.tbl_bids_2.selectRow(row)

        if _column == 1:
            _owner_addr = self.ui.nft_tab.owner_address.text()
            _w = self.search_wallet_addressses(_owner_addr)

            if _w is not None:
                self.dialogs.accept_bid_namespace_dialog(_w)

    def search_wallet_addressses(self, address: str) -> Optional[MWallet]:
        _return = None
        for _w in self.wallets.wallets:
            for _a in _w.addresses.addresses:
                if _a.address == address:
                    _return = _w
                    break

            if _return is not None:
                break

            for _a in _w.change_addresses.addresses:
                if _a.address == address:
                    _return = _w
                    break

        return _return

    def update_selected_auction_data(self, auction, reactions,
                                     clear: bool = False):
        if clear is True:
            self.ui.nft_tab.display_name.setText('')
            self.ui.nft_tab.ns.setText('')
            self.ui.nft_tab.shortcode.setText('')
            self.ui.nft_tab.desc.setText('')
            self.ui.nft_tab.asking.setText('')
            self.ui.nft_tab.high_bid.setText('')
            self.ui.nft_tab.num_bids.setText('')
            self.ui.nft_tab.owner_address.setText('')
            self.ui.nft_tab.address.setText('')
            self.ui.nft_tab.hashtags.setText('')
            UShared.remove_table_rows(self.ui.nft_tab.tbl_bids_2)
            # self.ui.nft_tab.tbl_bids_2.clear_rows()
        else:
            self.ui.nft_tab.ns.setText(auction[3])
            _nsdat = self.cache.ns.get_namespace_by_id(auction[3])

            if len(_nsdat) > 0:
                if _nsdat[-1][7] == 'root_ns':
                    _sc = (str(len(str(_nsdat[-1][0]))) +
                           str(_nsdat[-1][0]) + str(_nsdat[-1][1]))
                    self.ui.nft_tab.shortcode.setText(_sc)

                if _nsdat[0][7] == 'nft_auction':
                    self.ui.nft_tab.owner_address.setText(_nsdat[0][8])

            _auction = json.loads(auction[4])
            self.ui.nft_tab.display_name.setText(_auction['displayName'])
            self.ui.nft_tab.desc.setText(_auction['desc'])
            self.ui.nft_tab.asking.setText(_auction['price'] + ' KVA')
            self.ui.nft_tab.high_bid.setText('0.0')
            self.ui.nft_tab.num_bids.setText('0')
            self.ui.nft_tab.address.setText(_auction['addr'])
            if 'hashtags' in _auction:
                self.ui.nft_tab.hashtags.setText(_auction['hashtags'])
            self._update_selected_auction_bids(reactions)

    def _update_selected_auction_bids(self, reactions):
        UShared.remove_table_rows(self.ui.nft_tab.tbl_bids_2)
        # self.ui.nft_tab.tbl_bids_2.clear_rows()
        _bids = []
        for _r in reactions['replies']:
            if _r['value'][:10] == '70736274ff':
                _b = keva_psbt(_r['value'])
                _bid_ok = MShared.check_if_bid_valid(_b, self.KEX, self.cache)
                _bids.append([_r['time'], _r['sender']['shortCode'],
                              str(_b.tx.vout[1].value / 100000000) + ' KVA',
                              _bid_ok, _r['tx_hash']])
        self.ui.nft_tab.tbl_bids_2.add_bids(_bids)

    def sign_wallet_changed(self, data: str):
        self.ui.u_tab.address_combo.combo.clear()
        self.ui.u_tab.address_combo.combo.addItem('-', '-')
        if data != '-':
            _w = self.wallets.get_wallet_by_name(data)
            if _w is not None:
                for index in range(0, _w.addresses.count):
                    add = _w.addresses.get_address_by_index(index)
                    (self.ui.u_tab.address_combo.combo
                     .addItem(add.address, str(index)+':1'))
                for index in range(0, _w.change_addresses.count):
                    add = _w.change_addresses.get_address_by_index(index)
                    (self.ui.u_tab.address_combo.combo
                     .addItem(add.address, str(index)+':0'))
        self.ui.u_tab.ss_e.setPlainText('')

    def sign_address_changed(self, _data: str):
        self.ui.u_tab.ss_e.setPlainText('')
        if _data not in ('', '-'):
            _n = self.ui.u_tab.wallet_combo.combo.currentText()
            _w = self.wallets.get_wallet_by_name(_n)
            if _w is None:
                return

            _i_t = self.ui.u_tab.address_combo.combo.currentData().split(':')
            _pub = _w.get_publickey_raw(int(_i_t[0]), int(_i_t[1]))
            self.ui.u_tab.thl_bcp.setText(_pub)
        else:
            self.ui.u_tab.thl_bcp.setText('')

    def sign_message(self, _data: str):
        self.ui.u_tab.ss_e.setPlainText('')
        _n = self.ui.u_tab.wallet_combo.combo.currentText()
        _w = self.wallets.get_wallet_by_name(_n)
        if _w is None:
            return

        _i_t = self.ui.u_tab.address_combo.combo.currentData().split(':')
        _index = int(_i_t[0])
        # if _w.kind == 2:
        #     _ul = self.dialogs.lockbox_dialog(0)
        #     # TODO Test selected address can be derived using pass
        #     return False

        if self.ui.u_tab.thl_ac.isChecked() is True:
            _signature = _w.sign_message(_index,
                                         self.ui.u_tab.sm_e.toPlainText(),
                                         int(_i_t[1]))
        else:
            _data = self.ui.u_tab.thl_bcl.text()
            _dat = Ut.sha256(MShared.load_message_file(_data))
            _signature = _w.sign_message(_index, _dat, int(_i_t[1]))
        self.ui.u_tab.ss_e.setPlainText(_signature)
        return True

    def verify_message(self, _data: str):
        if self.ui.u_tab.vthl_ac.isChecked() is True:
            _v = WalletUtils.verify_message(self.ui.u_tab.vs_e.toPlainText(),
                                            self.ui.u_tab.va_e.text(),
                                            self.ui.u_tab.vm_e.toPlainText())
        else:
            _data = self.ui.u_tab.vthl_bcl.text()
            _dat = Ut.sha256(MShared.load_message_file(_data))
            _v = WalletUtils.verify_message(self.ui.u_tab.vs_e.toPlainText(),
                                            self.ui.u_tab.va_e.text(),
                                            _dat)
        self.ui.u_tab.success_label.setText(_v)

    def ns_key_value_edit(self):
        # self.ui.ns_tab.btn_val_edit.setVisible(False)
        # self.ui.ns_tab.btn_val_save.setVisible(True)
        # self.ui.ns_tab.ns_tab_text_key_value.setReadOnly(False)
        self.dialogs.edit_namespace_key_send_dialog()

    # def ns_key_value_save(self):
    #     self.ui.ns_tab.btn_val_edit.setVisible(True)
    #     self.ui.ns_tab.btn_val_save.setVisible(False)
    #     self.ui.ns_tab.ns_tab_text_key_value.setReadOnly(True)
    #     self.dialogs.edit_namespace_key_send_dialog()

    def update_wallet(self, wallet: MWallet, row: int):
        self.threader(wallet.name + ' -update wallet:', self._update_wallet,
                      wallet, None, self.refresh_wallet_data_tabs, row)

    def _update_wallet(self, wallet: MWallet):
        _cache = MCache(self.cache_path)
        wallet.set_bid_balance(0.0)
        wallet.set_bid_tx([])
        MShared.get_histories(wallet, self.KEX)
        MShared.get_balances(wallet, self.KEX)
        MShared.list_unspents(wallet, self.KEX)
        MShared.get_transactions(wallet, self.KEX, _cache)
        _cache.interface.close_cursor()
        _update_time = MShared.get_timestamp()
        wallet.set_last_updated(_update_time[0])
        self.wallets.save_wallet(wallet.name)

        return 'True'

    def _display_wallet_tx(self, wallet: MWallet) -> list:
        _tx_d: dict = {}
        _tx_d = self.__display_wallet_tx(wallet.addresses.addresses,
                                         _tx_d)
        _tx_d = self.__display_wallet_tx(wallet.change_addresses.addresses,
                                         _tx_d)
        _tx_d_list = list(_tx_d.values())
        _tx_d_list.sort(reverse=True, key=MShared.sort_dict)

        return _tx_d_list

    def __display_wallet_tx(self, addresses: List[MAddress],
                            _tx_d: dict) -> dict:
        for _a in addresses:
            for _t in _a.history:
                _trx = self.cache.tx.get_tx_by_txid(_t['tx_hash'])

                if _trx is None:
                    continue

                if _trx.txid not in _tx_d:
                    _tx_d[_trx.txid] = {}
                    _tx_d[_trx.txid]['txid'] = _trx.txid
                    _tx_d[_trx.txid]['time'] = _trx.time
                    _tx_d[_trx.txid]['blockhash'] = _trx.blockhash
                    _tx_d[_trx.txid]['amount'] = 0.0

                self.__disp_tx_vin(_trx, _tx_d, _a)
                self.__disp_tx_vout(_trx, _tx_d, _a)
                _tx_d[_trx.txid]['confirmations'] = _trx.confirmations

        return _tx_d

    def __disp_tx_vin(self, trx: MTransaction, tx_d: dict,
                      address: MAddress):
        for _in in trx.vin:
            _vo = _in.vout
            _in_tx = self.cache.tx.get_tx_by_txid(_in.txid)

            if _in_tx is None:
                continue

            for _out in _in_tx.vout:
                if (address.address in _out.scriptPubKey.addresses
                        and _out.n == _vo):
                    _am = tx_d[trx.txid]['amount']
                    _am = _am - _out.value
                    tx_d[trx.txid]['amount'] = _am

    def __disp_tx_vout(self, trx: MTransaction, tx_d: dict,
                       address: MAddress):
        for _out in trx.vout:
            if address.address in _out.scriptPubKey.addresses:
                _am = tx_d[trx.txid]['amount']
                tx_d[trx.txid]['amount'] = _am + _out.value

    def _get_unused_address(self):
        _n = self.ui.w_tab.tbl_w.gtext(self.ws, 3)
        if _n is None:
            return
        _w = self.wallets.get_wallet_by_name(_n)
        if _w is None:
            return
        _idx = _w.account_index
        _a = _w.get_unused_address()
        _dat = {'address': _a, 'received': 0.0, 'sent': 0.0, 'balance': 0.0}
        self.ui.w_tab.tbl_addr.add_address(_idx, _dat)
        self.ui.w_tab.tbl_addr.resizeColumnsToContents()
        self.wallets.save_wallet(_w.name)

    def _get_unused_changeaddress(self):
        _n = self.ui.w_tab.tbl_w.gtext(self.ws, 3)
        if _n is None:
            return
        _w = self.wallets.get_wallet_by_name(_n)
        if _w is None:
            return
        _idx = _w.change_index
        _a = _w.get_unused_change_address()
        _dat = {'address': _a, 'received': 0.0, 'sent': 0.0, 'balance': 0.0}
        self.ui.w_tab.tbl_addr2.add_address(_idx, _dat)
        self.ui.w_tab.tbl_addr2.resizeColumnsToContents()
        self.wallets.save_wallet(_w.name)
