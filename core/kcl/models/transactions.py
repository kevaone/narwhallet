import json
from core.kcl.models.transaction import MTransaction
from core.kcl.db_utils import SQLInterface
from core.kcl.db_utils import Scripts


class MTransactions():
    @staticmethod
    def sort(item):
        return item[0]

    @staticmethod
    def sort_dict(item):
        return item['time']

    def get_tx_by_txid(self, txid: str,
                       cache_interface: SQLInterface) -> MTransaction:
        _tx = cache_interface.execute_sql(Scripts.SELECT_TX_FULL,
                                          (txid, ), 3)
        _vin = cache_interface.execute_sql(Scripts.SELECT_TX_VIN,
                                           (txid, ), 3)
        _vout = cache_interface.execute_sql(Scripts.SELECT_TX_VOUT,
                                            (txid, ), 3)

        if len(_tx) == 1:
            _txx = MTransaction()
            _txx.fromSQL(_tx, _vin, _vout)
            _return = _txx
        else:
            _return = None
        return _return

    def add_fromJson(self, _json: dict,
                     cache_interface: SQLInterface) -> MTransaction:
        _tx = MTransaction()
        _tx.fromJson(_json)
        cache_interface.execute_sql(Scripts.INSERT_TX,
                                    (_tx.txid, _tx.hash, _tx.version,
                                     _tx.size, _tx.vsize, _tx.locktime,
                                     len(_tx.vin), len(_tx.vout),
                                     _tx.blockhash, _tx.confirmations,
                                     _tx.time, _tx.blocktime, _tx.hex), 2)
        for i in range(0, len(_tx.vin)):
            _vin = _tx.vin[i]
            if _vin.coinbase is None:
                cache_interface.execute_sql(Scripts.INSERT_TX_VIN,
                                            (_tx.txid, i, _vin.txid,
                                             _vin.vout, _vin.scriptSig.asm,
                                             _vin.scriptSig.hex,
                                             'witness_v0_keyhash', '',
                                             json.dumps(_vin.txinwitness),
                                             _vin.sequence), 2)
            else:
                cache_interface.execute_sql(Scripts.INSERT_TX_VIN,
                                            (_tx.txid, i, _vin.txid, '', '',
                                             '', 'coinbase', _vin.coinbase,
                                             '', _vin.sequence), 2)

        for i in range(0, len(_tx.vout)):
            _vout = _tx.vout[i]
            if len(_vout.scriptPubKey.addresses) > 0:
                _addresses = json.dumps(_vout.scriptPubKey.addresses)
                cache_interface.execute_sql(Scripts.INSERT_TX_VOUT,
                                            (_tx.txid, _vout.value, _vout.n,
                                             _vout.scriptPubKey.asm,
                                             _vout.scriptPubKey.hex,
                                             _vout.scriptPubKey.reqSigs,
                                             _vout.scriptPubKey.type,
                                             _addresses), 2)
            else:
                cache_interface.execute_sql(Scripts.INSERT_TX_VOUT,
                                            (_tx.txid, _vout.value, _vout.n,
                                             _vout.scriptPubKey.asm,
                                             _vout.scriptPubKey.hex,
                                             '', '', ''), 2)

        return _tx

    def update(self, tx: dict, cache_interface: SQLInterface):
        _tx = MTransaction()
        _tx.fromJson(tx)
        _result = cache_interface.execute_sql(Scripts.UPDATE_TX,
                                              (_tx.txid, _tx.hash,
                                               _tx.version, _tx.size,
                                               _tx.vsize, _tx.locktime,
                                               len(_tx.vin), len(_tx.vout),
                                               _tx.blockhash,
                                               _tx.confirmations, _tx.time,
                                               _tx.blocktime, _tx.hex,
                                               _tx.txid), 1)
        return _result
