from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (QTabWidget, QWidget, QVBoxLayout, QScrollArea,
                             QLabel, QHBoxLayout, QSpacerItem, QSizePolicy,
                             QDialogButtonBox, QFrame, QPlainTextEdit,
                             QPushButton, QDialog)
from narwhallet.core.kui.ux.widgets.generator import HLSection
from narwhallet.core.kcl.transaction import MTransactionInput
from narwhallet.core.kcl.transaction import MTransactionOutput
from narwhallet.control.shared import MShared


class Ui_v_tx_dlg(QDialog):
    def setupUi(self):
        _sp_exp = QSizePolicy.Expanding
        _sp_min = QSizePolicy.Minimum
        _sp_minexp = QSizePolicy.MinimumExpanding
        _b_ok = QDialogButtonBox.Ok
        _transm_st = QtCore.Qt.SmoothTransformation
        self.verticalLayout = QVBoxLayout(self)
        self.message_pic = HLSection('', None)
        self._ppic = QPixmap(MShared.get_resource_path('plus.png'))
        self._mpic = QPixmap(MShared.get_resource_path('minus.png'))
        self.tabs = QTabWidget(self)
        self.details_tab = QWidget(self.tabs)
        self.details_tab_vl = QVBoxLayout(self.details_tab)
        self.hex_tab = QWidget(self.tabs)
        self.hex_tab_vl = QVBoxLayout(self.hex_tab)
        self.json_tab = QWidget(self.tabs)
        self.json_tab_vl = QVBoxLayout(self.json_tab)
        self.txid = HLSection('TXID:', QPlainTextEdit(self))
        self.hash = HLSection('Hash:', QPlainTextEdit(self))
        self.block_hash = HLSection('Block Hash:', QPlainTextEdit(self))
        self.inputs_show = HLSection('Inputs:', QPushButton(self))
        self.inputs_f_wrap = QFrame(self)
        self.inputs_f_wrap_vl = QVBoxLayout(self.inputs_f_wrap)
        self.inputs = QScrollArea(self)
        self.inputs_f = QFrame(self)
        self.inputs_verticalLayout = QVBoxLayout(self.inputs_f)
        self.inputs_show_data_h = QHBoxLayout()
        self.inputs_show_data = QVBoxLayout()
        self.outputs_show = HLSection('Outputs:', QPushButton(self))
        self.outputs_f_wrap = QFrame(self)
        self.outputs_f_wrap_vl = QVBoxLayout(self.outputs_f_wrap)
        self.outputs_fr = QFrame(self)
        self.outputs_f_verticalLayout = QVBoxLayout(self.outputs_fr)
        self.outputs_f = QScrollArea(self)
        self.outputs_show_data_h = QHBoxLayout()
        self.outputs_show_data = QVBoxLayout()
        self.hex_d = QPlainTextEdit(self)
        self.json_d = QPlainTextEdit(self)
        self.buttonBox = QDialogButtonBox(self)

        self.setObjectName('v_tx_dlg')
        self.setMinimumSize(QtCore.QSize(690, 550))
        self._ppic = self._ppic.scaledToWidth(15, _transm_st)
        self._mpic = self._mpic.scaledToWidth(15, _transm_st)
        self.txid.widgets[0].setMaximumHeight(28)
        self.txid.widgets[0].setReadOnly(True)
        self.txid.widgets[0].setFrameStyle(QFrame.NoFrame)
        self.hash.widgets[0].setMaximumHeight(28)
        self.hash.widgets[0].setReadOnly(True)
        self.hash.widgets[0].setFrameStyle(QFrame.NoFrame)
        self.block_hash.widgets[0].setMaximumHeight(28)
        self.block_hash.widgets[0].setReadOnly(True)
        self.block_hash.widgets[0].setFrameStyle(QFrame.NoFrame)
        self.inputs_show.widgets[0].setIcon(QIcon(self._mpic))
        self.inputs_show.widgets[0].setFlat(True)
        self.inputs.setWidgetResizable(True)
        self.inputs_f.setFrameShape(QFrame.NoFrame)
        self.outputs_show.widgets[0].setIcon(QIcon(self._mpic))
        self.outputs_show.widgets[0].setFlat(True)
        self.outputs_f.setWidgetResizable(True)
        self.outputs_f.setWidget(self.outputs_fr)
        self.outputs_fr.setFrameShape(QFrame.NoFrame)
        self.hex_d.setReadOnly(True)
        self.json_d.setReadOnly(True)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(_b_ok)

        self.tabs.addTab(self.details_tab, 'In / Out')
        self.tabs.addTab(self.hex_tab, 'Hex')
        self.tabs.addTab(self.json_tab, 'Json')
        self.verticalLayout.addWidget(self.tabs)
        self.details_tab_vl.addLayout(self.txid)
        self.details_tab_vl.addLayout(self.hash)
        self.details_tab_vl.addLayout(self.block_hash)
        self.details_tab_vl.addLayout(self.inputs_show)
        self.inputs.setWidget(self.inputs_f)
        self.inputs_f_wrap_vl.addWidget(self.inputs)
        self.details_tab_vl.addWidget(self.inputs_f_wrap)
        self.inputs_show_data_h.addLayout(self.inputs_show_data)
        self.inputs_verticalLayout.addLayout(self.inputs_show_data_h)
        self.inputs_verticalLayout.addItem(QSpacerItem(20, 20,
                                           _sp_min, _sp_minexp))
        self.details_tab_vl.addLayout(self.outputs_show)
        self.outputs_f_wrap_vl.addWidget(self.outputs_f)
        self.details_tab_vl.addWidget(self.outputs_f_wrap)
        self.outputs_show_data_h.addLayout(self.outputs_show_data)
        self.outputs_f_verticalLayout.addLayout(self.outputs_show_data_h)
        self.outputs_f_verticalLayout.addItem(QSpacerItem(20, 20,
                                              _sp_min, _sp_exp))
        self.details_tab_vl.addItem(QSpacerItem(20, 20,
                                    _sp_min, _sp_minexp))
        self.hex_tab_vl.addWidget(self.hex_d)
        self.json_tab_vl.addWidget(self.json_d)
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi()
        self.buttonBox.accepted.connect(self.accept)
        self.inputs_show.widgets[0].clicked.connect(self._display_vin)
        self.outputs_show.widgets[0].clicked.connect(self._display_vout)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate('v_tx_dlg',
                                       'Narwhallet - Transaction'))

    def add_vin(self, vin_index: int, vin: MTransactionInput):
        self.inputs_show_data.addWidget(_show_hide_frame('vin',
                                                         vin_index, vin))

    def add_vout(self, index: int, vout: MTransactionOutput):
        self.outputs_show_data.addWidget(_show_hide_frame('vout', index, vout))

    def _display_vin(self, _event):
        if self.inputs_f_wrap.isVisible() is True:
            self.inputs_f_wrap.setVisible(False)
            self.inputs_show.widgets[0].setIcon(QIcon(self._ppic))
        else:
            self.inputs_f_wrap.setVisible(True)
            self.inputs_show.widgets[0].setIcon(QIcon(self._mpic))

    def _display_vout(self, _event):
        if self.outputs_f_wrap.isVisible() is True:
            self.outputs_f_wrap.setVisible(False)
            self.outputs_show.widgets[0].setIcon(QIcon(self._ppic))
        else:
            self.outputs_f_wrap.setVisible(True)
            self.outputs_show.widgets[0].setIcon(QIcon(self._mpic))


class _show_hide_frame(QFrame):
    def __init__(self, kind: str, index: int, inp):
        super().__init__()

        self._vl_0 = QVBoxLayout(self)
        self._vl_0.setContentsMargins(8, 0, 0, 0)
        self.box = _show_hide(kind, index)
        self._vl_0.addLayout(self.box)
        self._x = self.set_frame_kind(kind, inp)
        self._vl_0.addWidget(self._x)
        self.box.pic.clicked.connect(self._display)

    @staticmethod
    def set_frame_kind(kind: str, inp):
        if kind == 'vin':
            return _tx_in(inp)

        return _tx_out(inp)

    def _display(self, _event):
        if self._x.isVisible() is True:
            self._x.setVisible(False)
            self.box.pic.setIcon(QIcon(self.box.ppic))
        else:
            self._x.setVisible(True)
            self.box.pic.setIcon(QIcon(self.box.mpic))


class _show_hide(QHBoxLayout):
    def __init__(self, kind: str, index: int):
        super().__init__()

        _sp_exp = QSizePolicy.Expanding
        _sp_min = QSizePolicy.Minimum
        _transm_st = QtCore.Qt.SmoothTransformation
        self.ppic = QPixmap(MShared.get_resource_path('plus.png'))
        self.mpic = QPixmap(MShared.get_resource_path('minus.png'))
        self.ppic = self.ppic.scaledToWidth(15, _transm_st)
        self.mpic = self.mpic.scaledToWidth(15, _transm_st)

        self.vin = QLabel()
        self.vin.setText(kind + ':')
        self.vin_index = QLabel()
        self.vin_index.setText(str(index))
        self.pic = QPushButton()

        self.pic.setIcon(QIcon(self.mpic))
        self.pic.setFlat(True)
        self.addWidget(self.vin)
        self.addWidget(self.vin_index)
        self.addWidget(self.pic)
        self.addItem(QSpacerItem(40, 20, _sp_exp, _sp_min))


class _tx_in(QScrollArea):
    def __init__(self, vin: MTransactionInput):
        super().__init__()

        self._tx_input = QFrame()
        self._tx_input.setFrameShape(QFrame.NoFrame)

        self._vl_0 = QVBoxLayout(self._tx_input)
        self._txid = HLSection('txid:', QPlainTextEdit(self))
        if vin.coinbase is not None:
            self._txid.label.setText('coinbase:')
            self._txid.widgets[0].setPlainText(str(vin.coinbase))
        else:
            self._txid.label.setText('txid:')
            self._txid.widgets[0].setPlainText(vin.txid)
        self._txid.widgets[0].setMaximumHeight(28)
        self._txid.widgets[0].setReadOnly(True)
        self._txid.widgets[0].setFrameStyle(QFrame.NoFrame)
        self._vout = HLSection('vout:', QLabel(self))
        self._vout.widgets[0].setText(str(vin.vout))
        self._scriptsig_l = HLSection('scriptSig -', None)
        self._asm = HLSection('asm:', QPlainTextEdit(self))
        self._asm.widgets[0].setPlainText(vin.scriptSig.asm)
        self._asm.widgets[0].setMaximumHeight(28)
        self._asm.widgets[0].setReadOnly(True)
        self._asm.widgets[0].setFrameStyle(QFrame.NoFrame)
        self._hex = HLSection('hex:', QPlainTextEdit(self))
        self._hex.widgets[0].setPlainText(vin.scriptSig.hex)
        self._hex.widgets[0].setMaximumHeight(28)
        self._hex.widgets[0].setReadOnly(True)
        self._hex.widgets[0].setFrameStyle(QFrame.NoFrame)
        self._txinwitness_l = HLSection('txinwitness -', None)
        self._txinwitness_0 = QPlainTextEdit()
        self._txinwitness_0.setMaximumHeight(65)
        self._txinwitness_0.setReadOnly(True)
        if len(vin.txinwitness) > 0:
            self._txinwitness_0.setPlainText(vin.txinwitness[0])
        self._txinwitness_0.setFrameStyle(QFrame.NoFrame)
        self._txinwitness_1 = QPlainTextEdit()
        if len(vin.txinwitness) > 0:
            self._txinwitness_1.setPlainText(vin.txinwitness[1])
        self._txinwitness_1.setMaximumHeight(28)
        self._txinwitness_1.setReadOnly(True)
        self._txinwitness_1.setFrameStyle(QFrame.NoFrame)
        self._sequence = HLSection('sequence -', QLabel(self))
        self._sequence.widgets[0].setText(str(vin.sequence))

        self._vl_0.addLayout(self._txid)
        if vin.coinbase is None:
            self._vl_0.addLayout(self._vout)
            self._vl_0.addLayout(self._scriptsig_l)
            self._vl_0.addLayout(self._asm)
            self._vl_0.addLayout(self._hex)
            self._vl_0.addLayout(self._txinwitness_l)
            self._vl_0.addWidget(self._txinwitness_0)
            self._vl_0.addWidget(self._txinwitness_1)
        self._vl_0.addLayout(self._sequence)

        self.setWidget(self._tx_input)
        self.setWidgetResizable(True)


class _tx_out(QScrollArea):
    def __init__(self, vout: MTransactionOutput):
        super().__init__()

        self._tx_output = QFrame()
        self._tx_output.setFrameShape(QFrame.NoFrame)

        self._vl_0 = QVBoxLayout(self._tx_output)
        self._n = HLSection('n:', QLabel(self))
        self._n.widgets[0].setText(str(vout.n))
        self._value = HLSection('value:', QLabel(self))
        self._value.widgets[0].setText(str(vout.value))
        self._scriptpubkey_l = HLSection('scriptPubKey -', None)
        self._asm = HLSection('asm:', QPlainTextEdit(self))
        self._asm.widgets[0].setPlainText(vout.scriptPubKey.asm)
        self._asm.widgets[0].setMaximumHeight(65)
        self._asm.widgets[0].setReadOnly(True)
        self._asm.widgets[0].setFrameStyle(QFrame.NoFrame)
        self._hex = HLSection('hex:', QPlainTextEdit(self))
        self._hex.widgets[0].setPlainText(vout.scriptPubKey.hex)
        self._hex.widgets[0].setMaximumHeight(65)
        self._hex.widgets[0].setReadOnly(True)
        self._hex.widgets[0].setFrameStyle(QFrame.NoFrame)
        self._reqsigs = HLSection('    reqSigs:', QLabel(self))
        self._reqsigs.widgets[0].setText(str(vout.scriptPubKey.reqSigs))
        self._type = HLSection('    type:', QLabel(self))
        self._type.widgets[0].setText(vout.scriptPubKey.type)
        self._addresses = HLSection('    addresses:', QPlainTextEdit(self))
        (self._addresses.widgets[0]
         .setPlainText(str(vout.scriptPubKey._addresses)))
        self._addresses.widgets[0].setMaximumHeight(28)
        self._addresses.widgets[0].setReadOnly(True)
        self._addresses.widgets[0].setFrameStyle(QFrame.NoFrame)

        self._vl_0.addLayout(self._n)
        self._vl_0.addLayout(self._value)
        self._vl_0.addLayout(self._scriptpubkey_l)
        self._vl_0.addLayout(self._asm)
        self._vl_0.addLayout(self._hex)
        self._vl_0.addLayout(self._reqsigs)
        self._vl_0.addLayout(self._type)
        self._vl_0.addLayout(self._addresses)

        self.setWidget(self._tx_output)
        self.setWidgetResizable(True)
