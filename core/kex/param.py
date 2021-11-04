from enum import Enum
from core.kex.ex import error


class _param(Enum):
    def resolve(self, param) -> str:
        self.test_input_type(param)
        _return = param
        if isinstance(param, bool):
            if param is True:
                _return = 'true'
            else:
                _return = 'false'

        if not isinstance(param, str):
            _return = str(param)

        return _return

    def test_input_type(self, param):
        if self.value[0] != type(param):
            error.invalid_input_type.raise_error()

    def describe(self) -> dict:
        _d = {
            'name': self.name,
            'type': self.value
        }
        return _d


class ElXparams(_param):
    # TODO Create type objects for the various params
    client_name = str
    protocol_version = float
    features = str
    address = str
    scripthash = str
    height = int
    chk_height = int
    start_height = int
    count = int
    number = int
    raw = str
    rawtx = str
    tx_hash = str
    verbose = bool
    tx_pos = int
    merkle = bool
    # index = int
    min_tx_num = int
    tx_hashes = str
    namespace_info = str
