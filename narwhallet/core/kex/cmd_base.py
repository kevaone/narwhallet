class _cmd():
    @staticmethod
    def process_params(parms: list) -> str:
        _parms = '['
        for i in range(0, len(parms)):
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
                if i != len(parms) - 1:
                    _parms = _parms + ', '
        _parms = _parms + ']'

        return _parms

    @staticmethod
    def build_command(command: str, parms: list, eid: int) -> bytes:
        _parms = _cmd.process_params(parms)
        _command = '{"jsonrpc": "2.0", "method": "' + command
        _command = _command + '", "params": ' + _parms + ', "id": "' + str(eid)
        _command = _command + '" }\n'
        return _command.encode('utf-8')

    @staticmethod
    def build_web_command(command: str, parms: list, eid: int) -> bytes:
        if command == 'GET':
            _command = 'GET ' + parms[1] + ' HTTP/1.1\n'
            _command = _command + 'Host: ' + parms[0] + '\n'
            _command = _command + 'User-Agent: curl/7.54.0\n'
            _command = _command + 'Accept: */*\n'
            _command = _command + '\n'

        return _command.encode('utf-8')