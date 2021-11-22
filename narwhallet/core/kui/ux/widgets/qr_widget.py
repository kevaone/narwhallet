# https://stackoverflow.com/questions/20452486/create-qr-code-in-python-pyqt
import qrcode
from PyQt5 import QtCore
from PyQt5.QtGui import QImage, QPainter, QPixmap


class QRImage(qrcode.image.base.BaseImage):
    def __init__(self, border=1, width=250, box_size=10):
        self.border = border
        self.width = width
        self.box_size = box_size
        size = (width + border * 2) * box_size
        self._image = QImage(
            size, size, QImage.Format_RGB16)
        self._image.fill(QtCore.Qt.white)

    @staticmethod
    def make(text, image_factory):
        return qrcode.make(text, image_factory=image_factory).pixmap()

    def pixmap(self):
        return QPixmap.fromImage(self._image)

    def drawrect(self, row, col):
        painter = QPainter(self._image)
        painter.fillRect(
            (col + self.border) * self.box_size,
            (row + self.border) * self.box_size,
            self.box_size, self.box_size,
            QtCore.Qt.GlobalColor.black)

    def save(self, stream, kind=None):
        pass
