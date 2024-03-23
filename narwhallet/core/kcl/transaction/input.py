from typing import List
from narwhallet.core.kcl.transaction.script_sig import MScriptSig
from narwhallet.core.ksc.utils import Ut


class TransactionInputError(Exception):
    pass

class MTransactionInput():
    def __init__(self):
        self._idx: int = -1
        self._type: str = ''
        self._coinbase: str = ''
        
        self._txinwitness: List[str] = []
        
        self.tb_address: int = -1
        self.tb_address_chain: int = -1
        self.tb_value: int = -1

        self._txid: bytes = b''
        self._vout: bytes = b''
        self._scriptsig: MScriptSig = MScriptSig()
        self._sequence: bytes = self.set_sequence(b'\xff\xff\xff\xff')

    @property
    def coinbase(self) -> str:
        return self._coinbase

    @property
    def txid(self) -> bytes:
        return self._txid

    @property
    def vout(self) -> bytes:
        return self._vout

    @property
    def scriptsig(self) -> MScriptSig:
        return self._scriptsig

    @property
    def txinwitness(self) -> List[str]:
        return self._txinwitness

    @property
    def sequence(self) -> bytes:
        return self._sequence

    @property
    def size(self) -> int:
        _size = 0
        _size = _size + len(self.txid)
        _size = _size + len(self.vout)
        _size = _size + self.scriptsig.size
        _size = _size + len(self.sequence)

        return _size

    def set_coinbase(self, coinbase: str) -> None:
        self._coinbase = coinbase

    def set_txid(self, txid: bytes | str) -> None:
        if isinstance(txid, str):
            try:
                txid = Ut.hex_to_bytes(txid)
            except Exception as Ex:
                raise TransactionInputError(f'Failed to set transaction input txid from hex: {Ex}')

        self._txid = txid

    def set_vout(self, vout: bytes | str | int) -> None:
        if isinstance(vout, str):
            try:
                vout = Ut.hex_to_bytes(vout)
            except Exception as Ex:
                raise TransactionInputError(f'Failed to set transaction input vout from hex: {Ex}')
        elif isinstance(vout, int):
            try:
                vout = Ut.int_to_bytes(vout, 4, 'little')
            except Exception as Ex:
                raise TransactionInputError(f'Failed to set transaction input vout from int: {Ex}')

        if len(vout) != 4:
            raise TransactionInputError(f'Failed to set transaction input vout: Input vout is 4 bytes, {len(vout)} bytes supplied.')

        self._vout = vout

    def set_scriptsig(self, script: bytes | str) -> None:
        self.scriptsig.set_script(script)

    def set_txinwitness(self, txinwitness: List[str]) -> None:
        self._txinwitness = txinwitness

    def set_sequence(self, sequence: bytes | str) -> bytes:
        if isinstance(sequence, str):
            sequence = Ut.hex_to_bytes(sequence)

        if sequence not in (b'\xff\xff\xff\xff', b'\xfd\xff\xff\xff', b'\xfe\xff\xff\xff'):
            if (sequence < b'\x00\x00@\x00' and sequence > b'\xff\xff@\x00') \
                and (sequence < b'\x00\x00\x00\x00' and sequence > b'\xff\xff\x00\x00'):
                
                raise TransactionInputError(f'Failed to set transaction input sequence: Unsupported unsupported sequence, {Ut.bytes_to_hex(sequence)}.')

        self._sequence = sequence
        return self._sequence

    # def from_sql(self, vin):
    #     self._idx = vin[0]
    #     self.set_txid(vin[1])
    #     self.set_vout(vin[2])
    #     self.scriptSig.set_asm(vin[3])
    #     self.scriptSig.set_hex(vin[4])
    #     self._type = vin[5]
    #     if vin[6] != '':
    #         self.set_coinbase(vin[6])
    #     if vin[7] != '':
    #         self.set_txinwitness(json.loads(vin[7]))
    #     self.set_sequence(vin[8])

    # def from_json(self, json: dict):
    #     # TODO Refine this, hack to support cache changing
    #     if 'coinbase' in json:
    #         if json['coinbase'] != '':
    #             self.set_coinbase(json['coinbase'])
    #         else:
    #             self.set_txid(json['txid'])
    #             self.set_vout(json['vout'])
    #             self.scriptSig.from_json(json['scriptSig'])
    #             self.set_txinwitness(json['txinwitness'])
    #     else:
    #         self.set_txid(json['txid'])
    #         self.set_vout(json['vout'])
    #         self.scriptSig.from_json(json['scriptSig'])
    #         if 'txinwitness' in json:
    #             self.set_txinwitness(json['txinwitness'])
    #     self.set_sequence(json['sequence'])

    # def to_list(self) -> list:
    #     return [self.txid, self.vout, self.scriptSig,
    #             self.txinwitness, self.sequence]

    # def to_dict(self) -> dict:
    #     if self.coinbase != '':
    #         _return = {'coinbase': self.coinbase, 'txid': self.txid,
    #                    'vout': self.vout,
    #                    'scriptSig': self.scriptSig.to_dict(),
    #                    'txinwitness': self.txinwitness,
    #                    'sequence': self.sequence}
    #     else:
    #         _return = {'txid': self.txid, 'vout': self.vout,
    #                    'scriptSig': self.scriptSig.to_dict(),
    #                    'txinwitness': self.txinwitness,
    #                    'sequence': self.sequence}
    #     return _return
