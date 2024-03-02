class MNSKeyReply():
    def __init__(self, data):
        self._address: str = ''
        self._block: int = -1
        self._date: str = ''
        self._dkey: str = ''
        self._dtype: str = ''
        self._dvalue: str = ''
        self._key: str = ''
        self._key_shortcode: int = -1
        self._op: str = ''
        self._name: str = ''
        self._namespaceid: str = ''
        self._root_shortcode: int = -1
        # self._replies: list = []
        self._timestamp: int = -1
        self._txid: str = ''
        self._value: str = ''

        self.set_address(data['addr'])
        self.set_block(data['block'])
        self.set_date(data['time'], data['timestamp'])        
        self.set_dkey(data['dkey'])
        self.set_dvalue(data['dvalue'])
        self.set_dtype(data['dtype'])
        self.set_key(data['key'])
        self.set_key_shortcode(data['key_shortcode'])
        self.set_name(data['name'])
        self.set_namespaceid(data['dnsid'])
        self.set_op(data['type'])
        # self.set_replies(data['replies'])
        self.set_root_shortcode(data['root_shortcode'])
        self.set_txid(data['txid'])
        self.set_value(data['value'])

    @property
    def address(self) -> str:
        return self._address

    @property
    def block(self) -> int:
        return self._block

    @property
    def date(self) -> tuple[str, int]:
        return self._date, self._timestamp

    @property
    def dkey(self) -> str:
        return self._dkey

    @property
    def dtype(self) -> str:
        return self._dtype

    @property
    def dvalue(self) -> str:
        return self._dvalue

    @property
    def key(self) -> str:
        return self._key

    @property
    def key_shortcode(self) -> int:
        return self._key_shortcode

    @property
    def name(self) -> str:
        return self._name

    @property
    def namespaceid(self) -> str:
        return self._namespaceid

    @property
    def op(self) -> str:
        return self._op

    # @property
    # def replies(self) -> list:
    #     return self._replies

    @property
    def root_shortcode(self) -> int:
        return self._root_shortcode

    @property
    def txid(self) -> str:
        return self._txid

    @property
    def value(self) -> str:
        return self._value

    def set_address(self, address: str) -> None:
        self._address = address

    def set_block(self, block: int) -> None:
        self._block = block

    def set_date(self, date: str, timestamp: int) -> None:
        self._date = date
        self._timestamp = timestamp

    def set_dkey(self, dkey: str) -> None:
        self._dkey = dkey

    def set_dtype(self, dtype: str) -> None:
        self._dtype = dtype

    def set_dvalue(self, dvalue: str) -> None:
        self._dvalue = dvalue

    def set_key(self, key: str) -> None:
        self._key = key

    def set_key_shortcode(self, key_shortcode: int) -> None:
        self._key_shortcode = key_shortcode

    # def set_replies(self, replies: list) -> None:
    #     for _reply in replies:
    #         self._replies.append(MNSKeyReply(_reply))

    def set_name(self, name: str) -> None:
        self._name = name

    def set_namespaceid(self, namespaceid: str) -> None:
        self._namespaceid = namespaceid

    def set_op(self, op: str) -> None:
        self._op = op
    
    def set_root_shortcode(self, root_shortcode: int) -> None:
        self._root_shortcode = root_shortcode

    def set_txid(self, txid: str) -> None:
        self._txid = txid

    def set_value(self, value: str) -> None:
        self._value = value

    def to_list(self) -> list:
        return [self.date, self.key, self.value]

    def to_dict(self) -> dict:
        return {'date': self.date, 'key': self.key, 'value': self.value}
