from narwhallet.core.kcl.transaction.script_pubkey import MScriptPubKey
from narwhallet.core.ksc.utils import Ut


class TransactionWitnessError(Exception):
    pass

class MTransactionWitness():
    def __init__(self):
        self._stack: list[bytes] = []
        self._PSBT_IN_WITNESS_UTXO: bytes = b''

    @property
    def stack(self) -> list:
        return self._stack

    @property
    def PSBT_IN_WITNESS_UTXO(self) -> bytes:
        return self._PSBT_IN_WITNESS_UTXO

    @property
    def size(self) -> int:
        _size = 0
        _size = _size + len(self.stack)
        for _stack_item in self.stack:
            _size = _size + len(Ut.to_cuint(len(_stack_item)))
            _size = _size + len(_stack_item)

        return _size

    def set_stack(self, stack_data: bytes | str | list) -> None:
        if isinstance(stack_data, str):
            try:
                stack_data = Ut.hex_to_bytes(stack_data)
            except Exception as Ex:
                raise TransactionWitnessError(f'Failed to set transaction witness from hex: {Ex}')
        
        _stack = []
        _stack.append(b'')
        # TODO Test stack for appended length and dropping if present
        # TODO Read stack and append items
     
        self._stack = _stack

    def add_stack_item(self, stack_data: bytes | str | list) -> None:
        if isinstance(stack_data, str):
            try:
                stack_data = Ut.hex_to_bytes(stack_data)
            except Exception as Ex:
                raise TransactionWitnessError(f'Failed to set transaction witness from hex: {Ex}')
        elif isinstance(stack_data, list):
            try:
                for _stack_item in stack_data:
                    if isinstance(_stack_item, str):
                        try:
                            _stack_item = Ut.hex_to_bytes(_stack_item)
                        except Exception as Ex:
                            raise TransactionWitnessError(f'Failed to set transaction witness from hex: {Ex}')

                    if isinstance(_stack_item, bytes):
                        self._stack.append(_stack_item)
                    else:
                        raise TransactionWitnessError(f'Failed to set transaction witness from list: {_stack_item}')
                return
            except Exception as Ex:
                raise TransactionWitnessError(f'Failed to set transaction witness from list: {Ex}')

        try:
            # TODO Test stack for appended length and dropping if present
            # self._stack.append(Ut.to_cuint(len(stack_data)))
            # TODO Read stack and append items
            self._stack.append(stack_data)
        except Exception as Ex:
            raise TransactionWitnessError()

    def set_PSBT_IN_WITNESS_UTXO(self, data: bytes) -> None:
        self._PSBT_IN_WITNESS_UTXO = data