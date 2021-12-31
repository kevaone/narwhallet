import json
from typing import List
from narwhallet.core.kcl.models.transaction.script_sig import MScriptSig


class MTransactionInput():
    def __init__(self):
        self._idx: int = None
        self._type: str = None
        self._coinbase: str = None
        self._txid: str = None
        self._vout: int = None
        self._scriptSig: MScriptSig = MScriptSig()
        self._txinwitness: List[str] = []
        self._sequence: int = None

        self.tb_address: int = None
        self.tb_address_chain: int = None
        self.tb_value: int = None

    @property
    def coinbase(self) -> str:
        return self._coinbase

    @property
    def txid(self) -> str:
        return self._txid

    @property
    def vout(self) -> int:
        return self._vout

    @property
    def scriptSig(self) -> MScriptSig:
        return self._scriptSig

    @property
    def txinwitness(self) -> List[str]:
        return self._txinwitness

    @property
    def sequence(self) -> int:
        return self._sequence

    def set_coinbase(self, coinbase: str) -> None:
        self._coinbase = coinbase

    def set_txid(self, txid: str) -> None:
        self._txid = txid

    def set_vout(self, vout: int) -> None:
        self._vout = vout

    def set_scriptSig(self, scriptSig: MScriptSig) -> None:
        self._scriptSig = scriptSig

    def set_txinwitness(self, txinwitness: List[str]) -> None:
        self._txinwitness = txinwitness

    def set_sequence(self, sequence: int) -> None:
        self._sequence = sequence

    def from_sql(self, vin):
        self._idx = vin[0]
        self.set_txid(vin[1])
        self.set_vout(vin[2])
        self.scriptSig.set_asm(vin[3])
        self.scriptSig.set_hex(vin[4])
        self._type = vin[5]
        if vin[6] != '':
            self.set_coinbase(vin[6])
        if vin[7] != '':
            self.set_txinwitness(json.loads(vin[7]))
        self.set_sequence(vin[8])

    def from_json(self, json: dict):
        # TODO Refine this, hack to support cache changing
        if 'coinbase' in json:
            if json['coinbase'] is not None:
                self.set_coinbase(json['coinbase'])
            else:
                self.set_txid(json['txid'])
                self.set_vout(json['vout'])
                self.scriptSig.from_json(json['scriptSig'])
                self.set_txinwitness(json['txinwitness'])
        else:
            self.set_txid(json['txid'])
            self.set_vout(json['vout'])
            self.scriptSig.from_json(json['scriptSig'])
            if 'txinwitness' in json:
                self.set_txinwitness(json['txinwitness'])
        self.set_sequence(json['sequence'])

    def to_list(self) -> list:
        return [self.txid, self.vout, self.scriptSig,
                self.txinwitness, self.sequence]

    def to_dict(self) -> dict:
        if self.coinbase is not None:
            _return = {'coinbase': self.coinbase, 'txid': self.txid,
                       'vout': self.vout,
                       'scriptSig': self.scriptSig.to_dict(),
                       'txinwitness': self.txinwitness,
                       'sequence': self.sequence}
        else:
            _return = {'txid': self.txid, 'vout': self.vout,
                       'scriptSig': self.scriptSig.to_dict(),
                       'txinwitness': self.txinwitness,
                       'sequence': self.sequence}
        return _return
