from narwhallet.core.ksc.utils import Ut


class TransactionScriptPubKeyError(Exception):
    pass

class MScriptPubKey():
    def __init__(self):
        self._script: bytes = b''

    @property
    def script(self) -> bytes:
        return self._script

    @property
    def size(self) -> int:
        _size = 0
        _size = _size + len(Ut.to_cuint(len(self._script)))
        _size = _size + len(self._script)

        return _size

    def set_script(self, script: bytes | str) -> None:
        if isinstance(script, str):
            try:
                script = Ut.hex_to_bytes(script)
            except Exception as Ex:
                raise TransactionScriptPubKeyError(f'Failed to set transaction scriptsig from hex: {Ex}')

        # TODO: Add script validation

        self._script = script
