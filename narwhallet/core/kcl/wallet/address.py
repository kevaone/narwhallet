

class MAddress():
    def __init__(self):
        self._address: str = ''
        self._sent: float = 0.0
        self._received: float = 0.0
        self._balance: float = 0.0
        self._unconfirmed_receive_balance: float = 0.0
        self._unconfirmed_send_balance: float = 0.0
        self._label: str = ''
        self._history: list = []
        self._input_tx: list = []
        self._output_tx: list = []
        self._namespaces: list = []
        self._is_multi_sig: bool = False
        self._multi_sig_redeem_script: str = ''
        self._multi_sig_address_indexes: list = []

    @property
    def address(self) -> str:
        return self._address

    @property
    def sent(self) -> float:
        return self._sent

    @property
    def received(self) -> float:
        return self._received

    @property
    def balance(self) -> float:
        return self._balance

    @property
    def unconfirmed_receive_balance(self) -> float:
        return self._unconfirmed_receive_balance

    @property
    def unconfirmed_send_balance(self) -> float:
        return self._unconfirmed_send_balance

    @property
    def label(self) -> str:
        return self._label

    @property
    def history(self) -> list:
        return self._history

    @property
    def input_tx(self) -> list:
        return self._input_tx

    @property
    def output_tx(self) -> list:
        return self._output_tx

    @property
    def unspent_tx(self) -> list:
        _unspent_tx = []
        _bid_test = []
        for _ns in self.namespaces:
            if 'namespace_bids' not in _ns:
                continue

            if len(_ns['namespace_bids']) == 0:
                continue

            for _bid in _ns['namespace_bids']:
                for _input in _bid['inputs']:
                    _bid_test.append((_input['txid'], _input['n']))

        for _tx in self.history:
            if 'received'in _tx or 'spent' in _tx:
                continue

            if (_tx['txid'], _tx['n']) in _bid_test:
                continue

            _unspent_tx.append(_tx)

        return _unspent_tx

    @property
    def namespaces(self) -> list:
        return self._namespaces

    @property
    def is_multi_sig(self) -> bool:
        return self._is_multi_sig

    @property
    def multi_sig_redeem_script(self) -> str:
        return self._multi_sig_redeem_script

    @property
    def multi_sig_address_indexes(self) -> list:
        return self._multi_sig_address_indexes

    def set_address(self, address: str) -> None:
        self._address = address

    def set_sent(self, sent: float) -> None:
        self._sent = sent

    def set_received(self, received: float) -> None:
        self._received = received

    def set_balance(self, balance: float) -> None:
        self._balance = balance

    def set_unconfirmed_receive_balance(self, balance: float) -> None:
        self._unconfirmed_receive_balance = balance

    def set_unconfirmed_send_balance(self, balance: float) -> None:
        self._unconfirmed_send_balance = balance

    def set_label(self, label: str) -> None:
        self._label = label

    def set_history(self, history: list) -> None:
        self._history = history

    def set_namespaces(self, namespaces) -> None:
        self._namespaces = namespaces

    def set_is_multi_sig(self, is_multi_sig) -> None:
        self._is_multi_sig = is_multi_sig

    def set_multi_sig_redeem_script(self, multi_sig_redeem_script) -> None:
        self._multi_sig_redeem_script = multi_sig_redeem_script

    def set_multi_sig_address_indexes(self, multi_sig_address_indexes) -> None:
        self._multi_sig_address_indexes = multi_sig_address_indexes

    def add_input_tx(self, tx) -> None:
        self._input_tx.append(tx)

    def add_output_tx(self, tx) -> None:
        self._output_tx.append(tx)

    def to_list(self) -> list:
        return [self.address, self.sent, self.received,
                self.balance, self.label]

    def to_dict(self) -> dict:
        return {'address': self.address, 'sent': self.sent,
                'received': self.received, 'balance': self.balance,
                'unconfirmed_receive_balance': self.unconfirmed_receive_balance,
                'unconfirmed_send_balance': self.unconfirmed_send_balance,
                'label': self.label, 'history': self.history,
                'unspent_tx': self.unspent_tx, 'namespaces': self.namespaces,
                'is_multi_sig': self.is_multi_sig,
                'multi_sig_redeem_script': self.multi_sig_redeem_script,
                'multi_sig_address_indexes': self.multi_sig_address_indexes}
