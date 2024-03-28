from io import BytesIO
from typing import Tuple
from narwhallet.core.kcl.transaction.builder.sighash import SIGHASH_TYPE
from narwhallet.core.kcl.transaction.psbt_input import PsbtInput
from narwhallet.core.kcl.transaction.psbt_output import PsbtOutput
from narwhallet.core.ksc.utils import Ut
from narwhallet.core.kcl.transaction.psbt_types import record_types
from narwhallet.core.kcl.transaction.transaction_builder import MTransactionBuilder
from narwhallet.core.kcl.transaction.input import MTransactionInput
from narwhallet.core.kcl.transaction.output import MTransactionOutput


class keva_psbt():
    def __init__(self, psbt_dat: str | None = None):
        self.psbt: BytesIO | None = None
        self.size: int = -1
        self.tx = MTransactionBuilder()

        self._magic: bytes = Ut.hex_to_bytes('70736274')
        self._seperator: bytes = Ut.hex_to_bytes('ff')
        # _magic = '70736274'
        # _seperator = 'ff'
        self._PSBT_GLOBAL_UNSIGNED_TX: bytes | None = None
        self._PSBT_GLOBAL_XPUB: Tuple[bytes, bytes] | None = None
        self._PSBT_GLOBAL_TX_VERSION: bytes | None = None
        self._PSBT_GLOBAL_FALLBACK_LOCKTIME: bytes | None = None
        self._PSBT_GLOBAL_INPUT_COUNT : bytes | None= None
        self._PSBT_GLOBAL_OUTPUT_COUNT: bytes | None = None
        self._PSBT_GLOBAL_TX_MODIFIABLE: bytes | None = None
        self._PSBT_GLOBAL_SIGHASH_SINGLE_INPUTS: bytes | None = None
        self._PSBT_GLOBAL_VERSION: bytes | None = None
        self._PSBT_GLOBAL_PROPRIETARY: Tuple[bytes, bytes] | None = None

        self._inputs: list[PsbtInput] = []
        self._outputs: list[PsbtOutput] = []
        self._UNKNOWN: Tuple[int, bytes, bytes] | None = None

        if psbt_dat is not None:
            psbt_bytes = Ut.hex_to_bytes(psbt_dat)
            self.size = len(psbt_bytes)
            self.psbt = BytesIO(psbt_bytes)
        
            self.deserialize()

    @property
    def PSBT_GLOBAL_UNSIGNED_TX(self) -> bytes | None:
        return self._PSBT_GLOBAL_UNSIGNED_TX

    @property
    def PSBT_GLOBAL_XPUB(self) -> Tuple[bytes, bytes] | None:
        return self._PSBT_GLOBAL_XPUB

    @property
    def PSBT_GLOBAL_TX_VERSION(self) -> bytes | None:
        return self._PSBT_GLOBAL_TX_VERSION

    @property
    def PSBT_GLOBAL_FALLBACK_LOCKTIME(self) -> bytes | None:
        return self._PSBT_GLOBAL_FALLBACK_LOCKTIME

    @property
    def PSBT_GLOBAL_INPUT_COUNT(self) -> bytes | None:
        return self._PSBT_GLOBAL_INPUT_COUNT

    @property
    def PSBT_GLOBAL_OUTPUT_COUNT(self) -> bytes | None:
        return self._PSBT_GLOBAL_OUTPUT_COUNT

    @property
    def PSBT_GLOBAL_TX_MODIFIABLE(self) -> bytes | None:
        return self._PSBT_GLOBAL_TX_MODIFIABLE

    @property
    def PSBT_GLOBAL_SIGHASH_SINGLE_INPUTS(self) -> bytes | None:
        return self._PSBT_GLOBAL_SIGHASH_SINGLE_INPUTS

    @property
    def PSBT_GLOBAL_VERSION(self) -> bytes | None:
        return self._PSBT_GLOBAL_VERSION

    @property
    def PSBT_GLOBAL_PROPRIETARY(self) -> Tuple[bytes, bytes] | None:
        return self._PSBT_GLOBAL_PROPRIETARY

    @property
    def magic(self) -> bytes:
        return self._magic

    @property
    def seperator(self) -> bytes:
        return self._seperator

    @property
    def inputs(self) -> list[PsbtInput]:
        return self._inputs

    @property
    def outputs(self) -> list[PsbtOutput]:
        return self._outputs

    @property
    def UNKNOWN(self) -> Tuple[int, bytes, bytes] | None:
        return self._UNKNOWN

    def set_PSBT_GLOBAL_UNSIGNED_TX(self, value: bytes) -> None:
        self._PSBT_GLOBAL_UNSIGNED_TX = value

    def set_PSBT_GLOBAL_XPUB(self, key: bytes, value: bytes) -> None:
        self._PSBT_GLOBAL_XPUB = (key, value)

    def set_PSBT_GLOBAL_TX_VERSION(self, value: bytes) -> None:
        self._PSBT_GLOBAL_TX_VERSION = value

    def set_PSBT_GLOBAL_FALLBACK_LOCKTIME(self, value: bytes) -> None:
        self._PSBT_GLOBAL_FALLBACK_LOCKTIME = value

    def set_PSBT_GLOBAL_INPUT_COUNT(self, value: bytes) -> None:
        self._PSBT_GLOBAL_INPUT_COUNT = value

    def set_PSBT_GLOBAL_OUTPUT_COUNT(self, value: bytes) -> None:
        self._PSBT_GLOBAL_OUTPUT_COUNT = value

    def set_PSBT_GLOBAL_TX_MODIFIABLE(self, value: bytes) -> None:
        self._PSBT_GLOBAL_TX_MODIFIABLE = value

    def set_PSBT_GLOBAL_SIGHASH_SINGLE_INPUTS(self, value: bytes) -> None:
        self._PSBT_GLOBAL_SIGHASH_SINGLE_INPUTS = value

    def set_PSBT_GLOBAL_VERSION(self, value: bytes) -> None:
        self._PSBT_GLOBAL_VERSION = value

    def set_PSBT_GLOBAL_PROPRIETARY(self, key: bytes, value: bytes) -> None:
        self._PSBT_GLOBAL_PROPRIETARY = (key, value)

    def set_magic(self, value: bytes) -> None:
        self._magic = value

    def set_seperator(self, value: bytes) -> None:
        self._seperator = value

    def add_input(self, input: PsbtInput) -> None:
        self._inputs.append(input)

    def add_output(self, output: PsbtOutput) -> None:
        self._outputs.append(output)

    def set_inputs(self, rec_type: str, key_data: bytes, value_data: bytes) -> None:
        self.inputs[len(self.inputs) - 1].set_input(rec_type, key_data, value_data)

    def set_outputs(self, rec_type: str, key_data: bytes, value_data: bytes) -> None:
        self.outputs[len(self.outputs) - 1].set_output(rec_type, key_data, value_data)

    def set_UNKNOWN(self, rec_type, key: bytes, value: bytes) -> None:
        self._UNKNOWN = (rec_type, key, value)

    def globals_to_list(self, to_hex: bool = False) -> list[list[str | bytes | Tuple[bytes, bytes] | Tuple[int, bytes, bytes]]]:
        _globals: list[list[str | bytes | Tuple[bytes, bytes] | Tuple[int, bytes, bytes]]] = []

        if self._PSBT_GLOBAL_UNSIGNED_TX is not None:
            _globals.append(['PSBT_GLOBAL_UNSIGNED_TX', self._PSBT_GLOBAL_UNSIGNED_TX])

        if self._PSBT_GLOBAL_XPUB is not None:
            _globals.append(['PSBT_GLOBAL_XPUB', self._PSBT_GLOBAL_XPUB])

        if self._PSBT_GLOBAL_TX_VERSION is not None:
            _globals.append(['PSBT_GLOBAL_TX_VERSION', self._PSBT_GLOBAL_TX_VERSION])

        if self._PSBT_GLOBAL_FALLBACK_LOCKTIME is not None:
            _globals.append(['PSBT_GLOBAL_FALLBACK_LOCKTIME', self._PSBT_GLOBAL_FALLBACK_LOCKTIME])

        if self._PSBT_GLOBAL_INPUT_COUNT is not None:
            _globals.append(['PSBT_GLOBAL_INPUT_COUNT', self._PSBT_GLOBAL_INPUT_COUNT])

        if self._PSBT_GLOBAL_OUTPUT_COUNT is not None:
            _globals.append(['PSBT_GLOBAL_OUTPUT_COUNT', self._PSBT_GLOBAL_OUTPUT_COUNT])

        if self._PSBT_GLOBAL_TX_MODIFIABLE is not None:
            _globals.append(['PSBT_GLOBAL_TX_MODIFIABLE', self._PSBT_GLOBAL_TX_MODIFIABLE])

        if self._PSBT_GLOBAL_SIGHASH_SINGLE_INPUTS is not None:
            _globals.append(['PSBT_GLOBAL_SIGHASH_SINGLE_INPUTS', self._PSBT_GLOBAL_SIGHASH_SINGLE_INPUTS])

        if self._PSBT_GLOBAL_VERSION is not None:
            _globals.append(['PSBT_GLOBAL_VERSION', self._PSBT_GLOBAL_VERSION])

        if self._PSBT_GLOBAL_PROPRIETARY is not None:
            _globals.append(['PSBT_GLOBAL_PROPRIETARY', self._PSBT_GLOBAL_PROPRIETARY])

        if self.UNKNOWN is not None:
            _globals.append(['UNKNOWN', self.UNKNOWN])

        if to_hex is True:
            _temp: list[list[str | bytes | Tuple[bytes, bytes] | Tuple[int, bytes, bytes]]] = []
            for g in _globals:
                if isinstance(g[1], bytes):
                    _temp.append([g[0], Ut.bytes_to_hex(g[1])])
                elif len(g[1]) == 2:
                    _temp.append([g[0], Ut.bytes_to_hex(g[1][0])])
                    _temp.append([g[0], Ut.bytes_to_hex(g[1][1])])
                elif len(g[1]) == 3:
                    _temp.append([g[0], g[1][0]])
                    _temp.append([g[0], Ut.bytes_to_hex(g[1][1])])
                    _temp.append([g[0], Ut.bytes_to_hex(g[1][2])])

            _globals = _temp

        return _globals

    def to_list(self, to_hex: bool = False):
        _psbtl = []
        for _g in self.globals_to_list(to_hex):
            _psbtl.append(_g)

        for _i in self.inputs:
            for _ii in _i.to_list(to_hex):
                _psbtl.append(_ii)
        
        for _o in self.outputs:
            for _oi in _o.to_list(to_hex):
                _psbtl.append(_oi)

        return _psbtl

    def get_input(self, input: int) -> list[list[str | bytes | Tuple[bytes, bytes] | Tuple[int, bytes, bytes]]]:
        return self.inputs[input].to_list()

    def get_output(self, output: int) -> list[list[str | bytes | Tuple[bytes, bytes] | Tuple[int, bytes, bytes]]]:
        return self.outputs[output].to_list()

    def set_globals(self, rec_type: str, key_data: bytes, value_data: bytes):
        if rec_type == 'PSBT_GLOBAL_UNSIGNED_TX':
            self.set_PSBT_GLOBAL_UNSIGNED_TX(value_data)

            s_val = BytesIO(value_data)
            self.tx.set_version(s_val.read(4))
            _inputs, _ = Ut.read_csuint(s_val)
            for _ in range(_inputs):
                _vin = MTransactionInput()
                (_vin.set_txid(Ut.bytes_to_hex(
                                    Ut.reverse_bytes(s_val.read(32)))))
                _vin.set_vout(Ut.bytes_to_int(s_val.read(4), 'little'))
                _script_size, _ = Ut.read_csuint(s_val)
                _vin.set_scriptsig(s_val.read(_script_size))
                # if _vin.scriptSig.hex == '':
                #     _vin.scriptSig.set_hex(None)
                _vin.set_sequence(s_val.read(4))
                self.tx.add_vin(_vin)

            _outputs, _ = Ut.read_csuint(s_val)
            for _ in range(_outputs):
                _tx_vout = MTransactionOutput()
                _tx_vout.set_amount(s_val.read(8))
                script_size, _ = Ut.read_csuint(s_val)
                _tx_vout.set_scriptpubkey(s_val.read(script_size))
                self.tx.add_vout(_tx_vout)
            self.tx.set_locktime(s_val.read(4))

        elif rec_type == 'PSBT_GLOBAL_XPUB':
            self.set_PSBT_GLOBAL_XPUB(key_data[1:], value_data)
        elif rec_type == 'PSBT_GLOBAL_TX_VERSION':
            self.set_PSBT_GLOBAL_TX_VERSION(value_data)
        elif rec_type == 'PSBT_GLOBAL_FALLBACK_LOCKTIME':
            self.set_PSBT_GLOBAL_FALLBACK_LOCKTIME(value_data)
        elif rec_type == 'PSBT_GLOBAL_INPUT_COUNT':
            self.set_PSBT_GLOBAL_INPUT_COUNT(value_data)
        elif rec_type == 'PSBT_GLOBAL_OUTPUT_COUNT':
            self.set_PSBT_GLOBAL_OUTPUT_COUNT(value_data)
        elif rec_type == 'PSBT_GLOBAL_TX_MODIFIABLE':
            self.set_PSBT_GLOBAL_TX_MODIFIABLE(value_data)
        elif rec_type == 'PSBT_GLOBAL_SIGHASH_SINGLE_INPUTS':
            self.set_PSBT_GLOBAL_SIGHASH_SINGLE_INPUTS(value_data)
        elif rec_type == 'PSBT_GLOBAL_VERSION':
            self.set_PSBT_GLOBAL_VERSION(value_data)
        elif rec_type == 'PSBT_GLOBAL_PROPRIETARY':
            self.set_PSBT_GLOBAL_PROPRIETARY(key_data[1:], value_data)
        else:
            self.set_UNKNOWN(rec_type, key_data[1:], value_data)

    def read_vec(self, s: BytesIO) -> Tuple[int, bytes]:
        size, _ = Ut.read_csuint(s)
        return size, s.read(size)

    def deserialize(self):
        if self.psbt is None:
            raise Exception('Psbt data issue.')
        self.set_magic(self.psbt.read(4))  # _magic
        self.set_seperator(self.psbt.read(1))  # _sep
        _globals_extracted = False
        _inputs_extracted = False
        psbt_type = ''
        value_data = b''

        while True:
            key_size, key_data = self.read_vec(self.psbt)
            if key_size == 0:
                if self.psbt.tell() == self.size:
                    break

                if _globals_extracted is False:
                    _globals_extracted = True

                if _globals_extracted is True:
                    if len(self.inputs) != len(self.tx.vin):
                        _i = PsbtInput()
                        self.add_input(_i)
                    else:
                        _inputs_extracted = True

                if _inputs_extracted is True:
                    _o = PsbtOutput()
                    self.add_output(_o)
                continue

            # Read the type
            s_key = BytesIO(key_data)
            rec_type, _ = Ut.read_csuint(s_key)
            _, value_data = self.read_vec(self.psbt)

            if _globals_extracted is False:
                try:
                    psbt_type = record_types.GLOBAL(rec_type).name
                    self.set_globals(psbt_type, key_data, value_data)
                except:
                    psbt_type = 'UNKNOWN'
                    self.set_globals(rec_type, key_data, value_data)
            elif _globals_extracted is True and _inputs_extracted is False:
                try:
                    psbt_type = record_types.INPUT(rec_type).name
                    self.set_inputs(psbt_type, key_data, value_data)
                except:
                    psbt_type = 'UNKNOWN'
                    self.set_inputs(rec_type, key_data, value_data)
            else:
                try:
                    psbt_type = record_types.OUTPUT(rec_type).name
                    self.set_outputs(psbt_type, key_data, value_data)
                except:
                    psbt_type = 'UNKNOWN'
                    self.set_outputs(rec_type, key_data, value_data)

    def serialize(self) -> bytes:
        _pre: list[bytes] = []
        _pre.append(self.magic)
        _pre.append(self.seperator)

        if self.PSBT_GLOBAL_UNSIGNED_TX is not None:
            _pre.append(Ut.to_cuint(1))
            _pre.append(Ut.to_cuint(record_types.GLOBAL.PSBT_GLOBAL_UNSIGNED_TX.value))
            _tx = self.tx.serialize_tx(True)
            _pre.append(Ut.to_cuint(len(_tx)))
            _pre.append(_tx)

        if self.PSBT_GLOBAL_XPUB is not None:
            _xpub = Ut.to_cuint(record_types.GLOBAL.PSBT_GLOBAL_XPUB.value)
            _xpub = _xpub + self.PSBT_GLOBAL_XPUB[0]
            _pre.append(Ut.to_cuint(len(_xpub)))
            _pre.append(_xpub)
            _pre.append(Ut.to_cuint(len(self.PSBT_GLOBAL_XPUB[1])))
            _pre.append(self.PSBT_GLOBAL_XPUB[1])

        if self.PSBT_GLOBAL_TX_VERSION is not None:
            _pre.append(Ut.to_cuint(1))
            _pre.append(Ut.to_cuint(record_types.GLOBAL.PSBT_GLOBAL_TX_VERSION.value))
            _pre.append(Ut.to_cuint(len(self.PSBT_GLOBAL_TX_VERSION)))
            _pre.append(self.PSBT_GLOBAL_TX_VERSION)

        if self.PSBT_GLOBAL_FALLBACK_LOCKTIME is not None:
            _pre.append(Ut.to_cuint(1))
            _pre.append(Ut.to_cuint(record_types.GLOBAL.PSBT_GLOBAL_FALLBACK_LOCKTIME.value))
            _pre.append(Ut.to_cuint(len(self.PSBT_GLOBAL_FALLBACK_LOCKTIME)))
            _pre.append(self.PSBT_GLOBAL_FALLBACK_LOCKTIME)

        if self.PSBT_GLOBAL_INPUT_COUNT is not None:
            _pre.append(Ut.to_cuint(1))
            _pre.append(Ut.to_cuint(record_types.GLOBAL.PSBT_GLOBAL_INPUT_COUNT.value))
            _pre.append(Ut.to_cuint(len(self.PSBT_GLOBAL_INPUT_COUNT)))
            _pre.append(self.PSBT_GLOBAL_INPUT_COUNT)

        if self.PSBT_GLOBAL_OUTPUT_COUNT is not None:
            _pre.append(Ut.to_cuint(1))
            _pre.append(Ut.to_cuint(record_types.GLOBAL.PSBT_GLOBAL_OUTPUT_COUNT.value))
            _pre.append(Ut.to_cuint(len(self.PSBT_GLOBAL_OUTPUT_COUNT)))
            _pre.append(self.PSBT_GLOBAL_OUTPUT_COUNT)

        if self.PSBT_GLOBAL_TX_MODIFIABLE is not None:
            _pre.append(Ut.to_cuint(1))
            _pre.append(Ut.to_cuint(record_types.GLOBAL.PSBT_GLOBAL_TX_MODIFIABLE.value))
            _pre.append(Ut.to_cuint(len(self.PSBT_GLOBAL_TX_MODIFIABLE)))
            _pre.append(self.PSBT_GLOBAL_TX_MODIFIABLE)

        if self.PSBT_GLOBAL_SIGHASH_SINGLE_INPUTS is not None:
            _pre.append(Ut.to_cuint(1))
            _pre.append(Ut.to_cuint(record_types.GLOBAL.PSBT_GLOBAL_SIGHASH_SINGLE_INPUTS.value))
            _pre.append(Ut.to_cuint(len(self.PSBT_GLOBAL_SIGHASH_SINGLE_INPUTS)))
            _pre.append(self.PSBT_GLOBAL_SIGHASH_SINGLE_INPUTS)

        if self.PSBT_GLOBAL_VERSION is not None:
            _pre.append(Ut.to_cuint(1))
            _pre.append(Ut.to_cuint(record_types.GLOBAL.PSBT_GLOBAL_VERSION.value))
            _pre.append(Ut.to_cuint(len(self.PSBT_GLOBAL_VERSION)))
            _pre.append(self.PSBT_GLOBAL_VERSION)

        if self.PSBT_GLOBAL_PROPRIETARY is not None:
            _pro = Ut.to_cuint(record_types.GLOBAL.PSBT_GLOBAL_PROPRIETARY.value)
            _pro = _pro + self.PSBT_GLOBAL_PROPRIETARY[0]

            _pre.append(Ut.to_cuint(len(_pro)))
            _pre.append(_pro)
            _pre.append(Ut.to_cuint(len(self.PSBT_GLOBAL_PROPRIETARY[1])))
            _pre.append(self.PSBT_GLOBAL_PROPRIETARY[1])

        if self.UNKNOWN is not None:
            _pro = Ut.to_cuint(self.UNKNOWN[0])
            _pro = _pro + self.UNKNOWN[1]
            _pre.append(Ut.to_cuint(len(_pro)))
            _pre.append(_pro)
            _pre.append(Ut.to_cuint(len(self.UNKNOWN[2])))
            _pre.append(self.UNKNOWN[1])

        _pre.append(Ut.to_cuint(0))

        for _vin in self.inputs:
            _pre.append(_vin.serialize())

        for _vout in self.outputs:
            _pre.append(_vout.serialize())

        _spre = b''

        for p in _pre:
            _spre = _spre + p

        return _spre
