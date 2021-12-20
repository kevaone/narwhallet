from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (QTabWidget, QWidget, QVBoxLayout, QScrollArea,
                             QLabel, QHBoxLayout, QSpacerItem, QSizePolicy,
                             QDialogButtonBox, QFrame, QPlainTextEdit,
                             QPushButton, QDialog)

from narwhallet.core.kcl.models.transaction_input import MTransactionInput
from narwhallet.core.kcl.models.transaction_output import MTransactionOutput
from narwhallet.control.shared import MShared


class Ui_v_tx_dlg(QDialog):
    def setupUi(self):
        _sp_exp = QSizePolicy.Expanding
        _sp_min = QSizePolicy.Minimum
        _sp_minexp = QSizePolicy.MinimumExpanding
        _b_ok = QDialogButtonBox.Ok
        _transm_st = QtCore.Qt.SmoothTransformation
        self.verticalLayout = QVBoxLayout(self)
        self._ppic = QPixmap(MShared.get_resource_path('plus.png'))
        self._mpic = QPixmap(MShared.get_resource_path('minus.png'))
        self.tabs = QTabWidget(self)
        self.details_tab = QWidget(self.tabs)
        self.details_tab_vl = QVBoxLayout(self.details_tab)
        self.hex_tab = QWidget(self.tabs)
        self.hex_tab_vl = QVBoxLayout(self.hex_tab)
        self.json_tab = QWidget(self.tabs)
        self.json_tab_vl = QVBoxLayout(self.json_tab)
        self.txid_hl = QHBoxLayout()
        self.txid_label = QLabel(self)
        self.txid_d = QPlainTextEdit(self)
        self.hash_hl = QHBoxLayout()
        self.hash_label = QLabel(self)
        self.hash_d = QPlainTextEdit(self)
        self.blockhash_hl = QHBoxLayout()
        self.blockhash_label = QLabel(self)
        self.blockhash_d = QPlainTextEdit(self)
        self.inputs_show = QHBoxLayout()
        self.inputs_show_label = QLabel(self)
        self.inputs_show_img = QPushButton(self)
        self.inputs_f_wrap = QFrame(self)
        self.inputs_f_wrap_vl = QVBoxLayout(self.inputs_f_wrap)
        self.inputs = QScrollArea(self)
        self.inputs_f = QFrame(self)
        self.inputs_verticalLayout = QVBoxLayout(self.inputs_f)
        self.inputs_show_data_h = QHBoxLayout()
        self.inputs_show_data = QVBoxLayout()
        self.outputs_show = QHBoxLayout()
        self.outputs_show_label = QLabel(self)
        self.outputs_show_img = QPushButton(self)
        self.outputs_f_wrap = QFrame(self)
        self.outputs_f_wrap_vl = QVBoxLayout(self.outputs_f_wrap)
        self.outputs_fr = QFrame(self)
        self.outputs_f_verticalLayout = QVBoxLayout(self.outputs_fr)
        self.outputs_f = QScrollArea(self)
        self.outputs_show_data_h = QHBoxLayout()
        self.outputs_show_data = QVBoxLayout()
        self.hex_hl = QHBoxLayout()
        self.hex_label = QLabel(self)
        self.hex_d = QPlainTextEdit(self)
        self.json_d = QPlainTextEdit(self)
        self.buttonBox = QDialogButtonBox(self)

        self.setObjectName('v_tx_dlg')
        self.setMinimumSize(QtCore.QSize(690, 550))
        self._ppic = self._ppic.scaledToWidth(15, _transm_st)
        self._mpic = self._mpic.scaledToWidth(15, _transm_st)
        self.txid_d.setMaximumHeight(28)
        self.txid_d.setReadOnly(True)
        self.txid_d.setFrameStyle(QFrame.NoFrame)
        self.hash_d.setMaximumHeight(28)
        self.hash_d.setReadOnly(True)
        self.hash_d.setFrameStyle(QFrame.NoFrame)
        self.blockhash_d.setMaximumHeight(28)
        self.blockhash_d.setReadOnly(True)
        self.blockhash_d.setFrameStyle(QFrame.NoFrame)
        self.inputs_show_img.setIcon(QIcon(self._mpic))
        self.inputs_show_img.setFlat(True)
        self.inputs.setWidgetResizable(True)
        self.inputs_f.setFrameShape(QFrame.NoFrame)
        self.outputs_show_img.setIcon(QIcon(self._mpic))
        self.outputs_show_img.setFlat(True)
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
        self.txid_hl.addWidget(self.txid_label)
        self.txid_hl.addWidget(self.txid_d)
        self.details_tab_vl.addLayout(self.txid_hl)
        self.hash_hl.addWidget(self.hash_label)
        self.hash_hl.addWidget(self.hash_d)
        self.details_tab_vl.addLayout(self.hash_hl)
        self.blockhash_hl.addWidget(self.blockhash_label)
        self.blockhash_hl.addWidget(self.blockhash_d)
        self.details_tab_vl.addLayout(self.blockhash_hl)
        self.inputs_show.addWidget(self.inputs_show_label)
        self.inputs_show.addWidget(self.inputs_show_img)
        self.inputs_show.addItem(QSpacerItem(40, 20, _sp_exp, _sp_min))
        self.details_tab_vl.addLayout(self.inputs_show)
        self.inputs.setWidget(self.inputs_f)
        self.inputs_f_wrap_vl.addWidget(self.inputs)
        self.details_tab_vl.addWidget(self.inputs_f_wrap)
        self.inputs_show_data_h.addLayout(self.inputs_show_data)
        self.inputs_verticalLayout.addLayout(self.inputs_show_data_h)
        self.inputs_verticalLayout.addItem(QSpacerItem(20, 20,
                                           _sp_min, _sp_minexp))
        self.outputs_show.addWidget(self.outputs_show_label)
        self.outputs_show.addWidget(self.outputs_show_img)
        self.outputs_show.addItem(QSpacerItem(40, 20, _sp_exp, _sp_min))
        self.details_tab_vl.addLayout(self.outputs_show)
        self.outputs_f_wrap_vl.addWidget(self.outputs_f)
        self.details_tab_vl.addWidget(self.outputs_f_wrap)
        self.outputs_show_data_h.addLayout(self.outputs_show_data)
        self.outputs_f_verticalLayout.addLayout(self.outputs_show_data_h)
        self.outputs_f_verticalLayout.addItem(QSpacerItem(20, 20,
                                              _sp_min, _sp_exp))
        self.details_tab_vl.addItem(QSpacerItem(20, 20,
                                    _sp_min, _sp_minexp))
        self.hex_hl.addWidget(self.hex_label)
        self.hex_tab_vl.addLayout(self.hex_hl)
        self.hex_tab_vl.addWidget(self.hex_d)
        self.json_tab_vl.addWidget(self.json_d)
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi()
        self.buttonBox.accepted.connect(self.accept)
        self.inputs_show_img.clicked.connect(self._display_vin)
        self.outputs_show_img.clicked.connect(self._display_vout)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate('v_tx_dlg',
                                       'Narwhallet - Transaction'))
        self.txid_label.setText(_translate('v_tx_dlg', 'TX:'))
        self.hash_label.setText(_translate('v_tx_dlg', 'Hash:'))
        self.blockhash_label.setText(_translate('v_tx_dlg', 'Block Hash:'))
        self.inputs_show_label.setText(_translate('v_tx_dlg', 'Inputs'))
        self.outputs_show_label.setText(_translate('v_tx_dlg', 'Outputs'))
        self.hex_label.setText(_translate('v_tx_dlg', 'HEX:'))

    def add_vin(self, vin_index: int, vin: MTransactionInput):
        self.inputs_show_data.addWidget(_show_hide_frame('vin',
                                                         vin_index, vin))

    def add_vout(self, index: int, vout: MTransactionOutput):
        self.outputs_show_data.addWidget(_show_hide_frame('vout', index, vout))

    def _display_vin(self, _event):
        if self.inputs_f_wrap.isVisible() is True:
            self.inputs_f_wrap.setVisible(False)
            self.inputs_show_img.setIcon(QIcon(self._ppic))
        else:
            self.inputs_f_wrap.setVisible(True)
            self.inputs_show_img.setIcon(QIcon(self._mpic))

    def _display_vout(self, _event):
        if self.outputs_f_wrap.isVisible() is True:
            self.outputs_f_wrap.setVisible(False)
            self.outputs_show_img.setIcon(QIcon(self._ppic))
        else:
            self.outputs_f_wrap.setVisible(True)
            self.outputs_show_img.setIcon(QIcon(self._mpic))


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

        _sp_exp = QSizePolicy.Expanding
        _sp_min = QSizePolicy.Minimum

        self._tx_input = QFrame()
        self._tx_input.setFrameShape(QFrame.NoFrame)

        self._vl_0 = QVBoxLayout(self._tx_input)
        self._hl_0 = QHBoxLayout()
        self._hl_0a = QHBoxLayout()
        self._hl_1 = QHBoxLayout()
        self._hl_2 = QHBoxLayout()
        self._hl_3 = QHBoxLayout()
        self._hl_4 = QHBoxLayout()
        self._hl_5 = QHBoxLayout()
        self._hl_5a = QHBoxLayout()
        self._hl_5b = QHBoxLayout()
        self._hl_6 = QHBoxLayout()

        self._txid_l = QLabel()
        self._txid = QPlainTextEdit()
        if vin.coinbase is not None:
            self._txid_l.setText('coinbase:')
            self._txid.setPlainText(vin.coinbase)
        else:
            self._txid_l.setText('txid:')
            self._txid.setPlainText(vin.txid)
        self._txid.setMaximumHeight(28)
        self._txid.setReadOnly(True)
        self._txid.setFrameStyle(QFrame.NoFrame)
        self._vout_l = QLabel()
        self._vout_l.setText('vout:')
        self._vout = QLabel()
        self._vout.setText(str(vin.vout))
        self._scriptsig_l = QLabel()
        self._scriptsig_l.setText('scriptSig -')
        self._asm_l = QLabel()
        self._asm_l.setText('asm:')
        self._asm = QPlainTextEdit()
        self._asm.setPlainText(vin.scriptSig.asm)
        self._asm.setMaximumHeight(28)
        self._asm.setReadOnly(True)
        self._asm.setFrameStyle(QFrame.NoFrame)
        self._hex_l = QLabel()
        self._hex_l.setText('hex:')
        self._hex = QPlainTextEdit()
        self._hex.setPlainText(vin.scriptSig.hex)
        self._hex.setMaximumHeight(28)
        self._hex.setReadOnly(True)
        self._hex.setFrameStyle(QFrame.NoFrame)
        self._txinwitness_l = QLabel()
        self._txinwitness_l.setText('txinwitness -')
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
        self._sequence_l = QLabel()
        self._sequence_l.setText('sequence:')
        self._sequence = QLabel()
        self._sequence.setText(str(vin.sequence))

        self._hl_0.addWidget(self._txid_l)
        self._hl_0.addItem(QSpacerItem(40, 20, _sp_exp, _sp_min))
        self._hl_0a.addWidget(self._txid)
        self._hl_1.addWidget(self._vout_l)
        self._hl_1.addWidget(self._vout)
        self._hl_1.addItem(QSpacerItem(40, 20, _sp_exp, _sp_min))
        self._hl_2.addWidget(self._scriptsig_l)
        self._hl_3.addWidget(self._asm_l)
        self._hl_3.addWidget(self._asm)
        self._hl_4.addWidget(self._hex_l)
        self._hl_4.addWidget(self._hex)
        self._hl_5.addWidget(self._txinwitness_l)
        self._hl_5a.addWidget(self._txinwitness_0)
        self._hl_5b.addWidget(self._txinwitness_1)
        self._hl_6.addWidget(self._sequence_l)
        self._hl_6.addWidget(self._sequence)
        self._hl_6.addItem(QSpacerItem(40, 20, _sp_exp, _sp_min))

        self._vl_0.addLayout(self._hl_0)
        self._vl_0.addLayout(self._hl_0a)
        if vin.coinbase is None:
            self._vl_0.addLayout(self._hl_1)
            self._vl_0.addLayout(self._hl_2)
            self._vl_0.addLayout(self._hl_3)
            self._vl_0.addLayout(self._hl_4)
            self._vl_0.addLayout(self._hl_5)
            self._vl_0.addLayout(self._hl_5a)
            self._vl_0.addLayout(self._hl_5b)
        self._vl_0.addLayout(self._hl_6)

        self.setWidget(self._tx_input)
        self.setWidgetResizable(True)


class _tx_out(QScrollArea):
    def __init__(self, vout: MTransactionOutput):
        super().__init__()

        _sp_exp = QSizePolicy.Expanding
        _sp_min = QSizePolicy.Minimum
        self._tx_output = QFrame()
        self._tx_output.setFrameShape(QFrame.NoFrame)

        self._vl_0 = QVBoxLayout(self._tx_output)
        self._hl_0 = QHBoxLayout()
        self._hl_1 = QHBoxLayout()
        self._hl_2 = QHBoxLayout()
        self._hl_3 = QHBoxLayout()
        self._hl_4 = QHBoxLayout()
        self._hl_5 = QHBoxLayout()
        self._hl_6 = QHBoxLayout()
        self._hl_7 = QHBoxLayout()

        self._n_l = QLabel()
        self._n_l.setText('n:')
        self._n = QLabel()
        self._n.setText(str(vout.n))
        self._value_l = QLabel()
        self._value_l.setText('value:')
        self._value = QLabel()
        self._value.setText(str(vout.value))
        self._scriptpubkey_l = QLabel()
        self._scriptpubkey_l.setText('scriptPubKey -')
        self._asm_l = QLabel()
        self._asm_l.setText('    asm:')
        self._asm = QPlainTextEdit()
        self._asm.setPlainText(vout.scriptPubKey.asm)
        self._asm.setMaximumHeight(65)
        self._asm.setReadOnly(True)
        self._asm.setFrameStyle(QFrame.NoFrame)
        self._hex_l = QLabel()
        self._hex_l.setText('    hex:')
        self._hex = QPlainTextEdit()
        self._hex.setPlainText(vout.scriptPubKey.hex)
        self._hex.setMaximumHeight(65)
        self._hex.setReadOnly(True)
        self._hex.setFrameStyle(QFrame.NoFrame)
        self._reqsigs_l = QLabel()
        self._reqsigs_l.setText('    reqSigs:')
        self._reqsigs = QLabel()
        self._reqsigs.setText(str(vout.scriptPubKey.reqSigs))
        self._type_l = QLabel()
        self._type_l.setText('    type:')
        self._type = QLabel()
        self._type.setText(vout.scriptPubKey.type)
        self._addresses_l = QLabel()
        self._addresses_l.setText('    addresses:')
        self._addresses = QPlainTextEdit()
        self._addresses.setPlainText(str(vout.scriptPubKey._addresses))
        self._addresses.setMaximumHeight(28)
        self._addresses.setReadOnly(True)
        self._addresses.setFrameStyle(QFrame.NoFrame)

        self._hl_0.addWidget(self._n_l)
        self._hl_0.addWidget(self._n)
        self._hl_0.addItem(QSpacerItem(40, 20, _sp_exp, _sp_min))
        self._hl_1.addWidget(self._value_l)
        self._hl_1.addWidget(self._value)
        self._hl_1.addItem(QSpacerItem(40, 20, _sp_exp, _sp_min))
        self._hl_2.addWidget(self._scriptpubkey_l)
        self._hl_3.addWidget(self._asm_l)
        self._hl_3.addWidget(self._asm)
        self._hl_4.addWidget(self._hex_l)
        self._hl_4.addWidget(self._hex)
        self._hl_5.addWidget(self._reqsigs_l)
        self._hl_5.addWidget(self._reqsigs)
        self._hl_5.addItem(QSpacerItem(40, 20, _sp_exp, _sp_min))
        self._hl_6.addWidget(self._type_l)
        self._hl_6.addWidget(self._type)
        self._hl_6.addItem(QSpacerItem(40, 20, _sp_exp, _sp_min))
        self._hl_7.addWidget(self._addresses_l)
        self._hl_7.addWidget(self._addresses)

        self._vl_0.addLayout(self._hl_0)
        self._vl_0.addLayout(self._hl_1)
        self._vl_0.addLayout(self._hl_2)
        self._vl_0.addLayout(self._hl_3)
        self._vl_0.addLayout(self._hl_4)
        self._vl_0.addLayout(self._hl_5)
        self._vl_0.addLayout(self._hl_6)
        self._vl_0.addLayout(self._hl_7)

        self.setWidget(self._tx_output)
        self.setWidgetResizable(True)
