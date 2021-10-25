# from PyQt5 import QtCore
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QWidget


class Ui_NFTMarketTab(QObject):
    def setupUi(self):
        self.tabNFT = QWidget()
        self.tabNFT.setObjectName('tabNFT')

    def retranslateUi(self):
        # _translate = QtCore.QCoreApplication.translate
        pass
