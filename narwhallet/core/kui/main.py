from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication as QApp
from PyQt5.QtWidgets import QMainWindow

from narwhallet._version import __version__
from narwhallet.control.shared import MShared
from narwhallet.core.kui.ux.main_window import Ui_MainWindow

if hasattr(Qt, 'AA_EnableHighDpiScaling'):
    QApp.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)

if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
    QApp.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)


class NarwhalletUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setObjectName('MainWindow')
        self.resize(858, 806)
        self.setWindowTitle('Narwhallet ' + __version__)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(MShared.get_resource_path('narwhal.png')))
