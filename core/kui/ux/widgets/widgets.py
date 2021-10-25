from PyQt5.QtWidgets import QComboBox, QPlainTextEdit


class _QComboBox(QComboBox):
    def __init__(self):
        super().__init__()


class _ns_value_textedit(QPlainTextEdit):
    def __init__(self, name: str, QWidget):
        super().__init__()
        self.name = name
