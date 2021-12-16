from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.QtWidgets import QLabel
from narwhallet.control.shared import MShared


class animated_label(QLabel):
    def __init__(self):
        super().__init__()

        _al_center = QtCore.Qt.AlignCenter
        _transm_st = QtCore.Qt.SmoothTransformation

        self._upic = QPixmap(MShared.get_resource_path('return.png'))
        self._upic = self._upic.scaledToWidth(20, _transm_st)
        self.setPixmap(self._upic)
        self.setAlignment(_al_center)
        self.setContentsMargins(0, 0, 0, 0)
        self.setProperty('class', 'tblImg')

        self.ani = QtCore.QVariantAnimation()
        self.ani.setDuration(1000)

        self.ani.setStartValue(0.0)
        self.ani.setEndValue(360.0)
        self.ani.setLoopCount(300)
        self.ani.valueChanged.connect(self.animate)

    def animate(self, value):
        _transm_st = QtCore.Qt.SmoothTransformation

        t = QTransform()
        t.rotate(value)
        self.setPixmap(self._upic.transformed(t, _transm_st))
