from enum import Enum
from narwhallet.core.kex.ex import error


class _cmd(Enum):
    def describe(self) -> dict:
        _d = {
            'command': self.value[0],
            'params': self.value[1]
        }
        return _d

    def process_params(self, parms: list) -> str:
        _p_len = len(self.value[1])

        if len(parms) == _p_len:
            _parms = '['
            for i in range(_p_len):
                # TODO Extend a validator for complex types
                if isinstance(parms[i], self.value[1][i].value):
                    if isinstance(parms[i], bool):
                        if parms[i] is True:
                            parms[i] = 'true'
                        else:
                            parms[i] = 'false'
                        _parms = _parms + parms[i]
                    else:
                        if not isinstance(parms[i], str):
                            parms[i] = str(parms[i])
                        _parms = _parms + '"' + parms[i] + '"'
                        if i != _p_len - 1:
                            _parms = _parms + ', '
                else:
                    error.invalid_input_type.raise_error()
            _parms = _parms + ']'
        else:
            error.param_count_mismatch.raise_error()

        return _parms

    def build_command(self, parms: list, eid: int) -> bytes:
        _parms = self.process_params(parms)
        _command = '{"jsonrpc": "2.0", "method": "' + self.value[0]
        _command = _command + '", "params": ' + _parms + ', "id": "' + str(eid)
        _command = _command + '" }\n'
        return _command.encode('utf-8')
