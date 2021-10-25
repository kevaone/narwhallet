from enum import Enum


class _error(Enum):
    def _raise(self):
        raise self.value
    connection_timeout = Exception('connection timeout')
    invalid_input_type = Exception('invalid input type')
    # raise Exception('param type mismatch')
    param_count_mismatch = Exception('param count mismatch')
