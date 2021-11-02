import struct
from io import BytesIO

from core.ksc.utils import Ut

from core.kcl.models.psbt_types import record_types
from core.kcl.models.transaction_builder import MTransactionBuilder
from core.kcl.models.transaction_input import MTransactionInput
from core.kcl.models.script_sig import MScriptSig
from core.kcl.models.transaction_output import MTransactionOutput


class keva_psbt():
    def __init__(self, psbt_dat):
        self.psbt = None
        self.tx = MTransactionBuilder()
        self.psbt_records = []
        self.psbt_inputs = 0
        self.psbt_outputs = 0
        self.prep_psbt_data(psbt_dat)

    def read_csuint(self, s):
        size = struct.unpack('<B', s.read(1))[0]
        if size == 253:
            _return = struct.unpack('<H', s.read(2))[0]
        elif size == 254:
            _return = struct.unpack('<I', s.read(4))[0]
        elif size == 255:
            _return = struct.unpack('<Q', s.read(8))[0]
        else:
            _return = size
        return _return

    def read_vec(self, s):
        size = self.read_csuint(s)
        return size, s.read(size)

    def deserialize_map(self, psbt, scope):
        psbt_type = ''
        # value_size = ''
        value_data = b''

        while True:
            key_size, key_data = self.read_vec(psbt)
            if key_size == 0:
                break

            # Read the type
            s_key = BytesIO(key_data)
            rec_type = self.read_csuint(s_key)

            _is_tx = False
            if (rec_type == record_types.GLOBAL.PSBT_GLOBAL_UNSIGNED_TX.value
               and scope == 'GLOBAL'):
                _is_tx = True
                psbt_type = record_types.GLOBAL.PSBT_GLOBAL_UNSIGNED_TX.name
            elif record_types.INPUT.has_value(rec_type):
                psbt_type = record_types.INPUT(rec_type).name
            elif record_types.OUTPUT.has_value(rec_type):
                psbt_type = record_types.OUTPUT(rec_type).name
            else:
                psbt_type = 'UNKNOWN'

            # TODO Deal with proprietary types
            # if rec_type == '252':

            _, value_data = self.read_vec(psbt)
            if _is_tx:
                s_val = BytesIO(value_data)
                self.tx.set_version(Ut.bytes_to_int(s_val.read(4), 'little'))

                self.psbt_inputs = self.read_csuint(s_val)
                for _ in range(self.psbt_inputs):
                    _tx_vin = MTransactionInput()
                    _tx_vin_script_sig = MScriptSig()
                    _tx_vin.set_txid(Ut.bytes_to_hex(Ut.reverse_bytes(s_val.read(32))))
                    _tx_vin.set_vout(Ut.bytes_to_int(s_val.read(4), 'little'))
                    _script_size = self.read_csuint(s_val)
                    _tx_vin_script_sig.set_hex(Ut.bytes_to_hex(s_val.read(_script_size)))
                    if _tx_vin_script_sig.hex == '':
                        _tx_vin_script_sig.set_hex(None)
                    _tx_vin.set_scriptSig(_tx_vin_script_sig)
                    _tx_vin.set_sequence(Ut.bytes_to_hex(s_val.read(4)))
                    self.tx.add_vin(_tx_vin)

                self.psbt_outputs = self.read_csuint(s_val)
                for _ in range(self.psbt_outputs):
                    _tx_vout = MTransactionOutput()
                    _tx_vout.set_value(Ut.bytes_to_int(s_val.read(8), 'little'))
                    script_size = self.read_csuint(s_val)
                    _tx_vout.scriptPubKey.set_asm(Ut.bytes_to_hex(s_val.read(script_size)))
                    self.tx.add_vout(_tx_vout)
                self.tx.set_locktime(Ut.bytes_to_int(s_val.read(4), 'little'))

            self.psbt_records.append([psbt_type, key_data, value_data])

    def prep_psbt_data(self, psbt):
        psbt_bytes = Ut.hex_to_bytes(psbt)
        self.psbt = BytesIO(psbt_bytes)
        _ = self.psbt.read(4)  # _magic
        _ = self.psbt.read(1)  # _sep
        self.get_global_tx()

    def get_global_tx(self):
        self.deserialize_map(self.psbt, 'GLOBAL')
        self.get_psbt_inputs()

    def get_psbt_inputs(self):
        for _ in range(self.psbt_inputs):
            self.deserialize_map(self.psbt, 'INPUT')
        self.get_psbt_outputs()

    def get_psbt_outputs(self):
        for _ in range(self.psbt_outputs):
            self.deserialize_map(self.psbt, 'OUTPUT')

    def toDict(self) -> dict:
        _records = []
        for record in self.psbt_records:
            _record = []
            for entry in record:
                if isinstance(entry, bytes) is True:
                    _record.append(Ut.bytes_to_hex(entry))
                else:
                    _record.append(entry)
            _records.append(_record)

        return {'psbt_inputs': self.psbt_inputs,
                'psbt_outputs': self.psbt_outputs,
                'psbt_records': _records,
                'tx': self.tx.toDict()
                }

# _test_psbt_dat = ''
# KL = keva_psbt(_test_psbt_dat)
# print(KL.toDict())
