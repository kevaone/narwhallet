from PyQt5 import QtCore
from PyQt5.QtWidgets import QPushButton


class DelayPushButton(QPushButton):
    def __init__(self, text, delay):
        super().__init__()

        self._track = -1
        self._text = text
        self._delay = delay
        self.setText(self._text)

        self.ani = QtCore.QVariantAnimation()
        self.ani.setDuration(self._delay * 1000)
        self.ani.setStartValue(0)
        self.ani.setEndValue(self._delay * 1000)
        self.ani.setLoopCount(1)
        self.ani.valueChanged.connect(self.count_down)

    def count_down(self, value):
        _value = int(value / 1000)
        if self._track != _value:
            self._track = _value
            _d = self._delay - self._track

            if _d == 0:
                self.setText(self._text)
                self.setEnabled(True)
            else:
                self.setText(self._text + ' (' + str(_d) + ')')
                self.setEnabled(False)
