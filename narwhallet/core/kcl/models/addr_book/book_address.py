class MBookAddress():
    def __init__(self):
        self._coin: str = None
        self._name: str = None
        self._address: str = None
        self._sent: float = 0.0
        self._received: float = 0.0
        self._label: str = None
        self._history: list = []
        self._input_tx: list = []
        self._output_tx: list = []

    @property
    def coin(self) -> str:
        return self._coin

    @property
    def name(self) -> str:
        return self._name

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

    def set_coin(self, coin: str) -> None:
        self._coin = coin

    def set_name(self, name: str) -> None:
        self._name = name

    def set_address(self, address: str) -> None:
        self._address = address

    def set_sent(self, sent: float) -> None:
        self._sent = sent

    def set_received(self, received: float) -> None:
        self._received = received

    def set_label(self, label: str) -> None:
        self._label = label

    def set_history(self, history: list) -> None:
        self._history = history

    def add_input_tx(self, tx) -> None:
        self._input_tx.append(tx)

    def add_output_tx(self, tx) -> None:
        self._output_tx.append(tx)

    def to_list(self) -> list:
        return [self.coin, self.name, self.address,
                self.sent, self.received, self.label]

    def to_dict(self) -> dict:
        return {'coin': self.coin, 'name': self.name,
                'address': self.address, 'sent': self.sent,
                'received': self.received, 'label': self.label}
