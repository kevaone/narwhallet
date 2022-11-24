import json
from typing import List
from PyQt5 import QtCore
from PyQt5.QtGui import QColor, QPixmap
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QLabel
from narwhallet.control.shared import MShared
from narwhallet.core.ksc.utils import Ut
from narwhallet.core.kcl.transaction import MTransactionBuilder


class DShared():
    @staticmethod
    def _test_tx(tx: MTransactionBuilder) -> bool:
        _return = True
        if tx is None:
            _return = False
        elif tx.confirmations == -1:
            _return = False
        elif tx.confirmations < 6:
            _return = False

        return _return

    @staticmethod
    def tx_to_ns(tx, vout):
        _tx = Ut.reverse_bytes(Ut.hex_to_bytes(tx))
        _tx_hash = Ut.hash160(_tx + str(vout).encode())
        return Ut.bytes_to_hex(bytes([53]) + _tx_hash)

    @staticmethod
    def txb_w_changed(dialog, data):
        if data != '-':
            DShared.set_namespace_combo(dialog)

        dialog.check_next()

    @staticmethod
    def set_namespace_combo(dialog):
        dialog.combo_ns.clear()
        dialog.combo_ns.addItem('-', '-')
        dialog.nft_name.setText('')
        _n = dialog.combo_wallet.currentData()
        wallet = dialog.wallets.get_wallet_by_name(_n)
        MShared.list_unspents(wallet, dialog.kex)
        _tmp_usxo = wallet.get_usxos()
        for tx in _tmp_usxo:
            # TODO Check for usxo's used by bids
            _tx = dialog.cache.tx.get_tx_by_txid(tx['tx_hash'])

            if _tx is None:
                _tx = MShared.get_tx(tx['tx_hash'], dialog.kex, True)
                if _tx is not None:
                    _tx = dialog.cache.tx.add_from_json(_tx)

            if _tx is not None:
                if ('OP_KEVA'
                        in _tx.vout[tx['tx_pos']].scriptPubKey.asm):

                    _ns = _tx.vout[tx['tx_pos']].scriptPubKey.asm.split(' ')[1]
                    _ns = dialog.cache.ns.convert_to_namespaceid(_ns)
                    _block = dialog.cache.ns.ns_block(_ns)[0]
                    _b_s = str(_block[0])
                    _block = str(str(len(_b_s)) + _b_s + str(_block[1]))
                    _name = (dialog.cache.ns.get_namespace_by_key_value(
                        _ns, '\x01_KEVA_NS_'))
                    if len(_name) == 0:
                        _name = (dialog.cache.ns
                                 .get_namespace_by_key_value(_ns, '_KEVA_NS_'))
                        if len(_name) > 0:
                            _name = _name[0][1]
                    else:
                        _name = _name[0][1]

                    if 'displayName' in _name:
                        _name = json.loads(_name)['displayName']

                    dialog.combo_ns.addItem(_block+' - '+_name, _ns+':'+tx['a'])
