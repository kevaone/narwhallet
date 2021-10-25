import os
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QObject
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QFrame, QHBoxLayout,
                             QLabel, QSpacerItem, QSizePolicy, QPushButton,
                             QSplitter)
from core.kui.ux.widgets.widgets import _ns_value_textedit
from core.kui.ux.widgets.namespaces_table import _namespaces_table
from core.kui.ux.widgets.namespace_keys_list import _namespace_keys_list


class Ui_NamespacesTab(QObject):
    def setupUi(self):
        _sp_exp = QSizePolicy.Policy.Expanding
        _sp_min = QSizePolicy.Policy.Minimum
        _al_center = QtCore.Qt.AlignmentFlag.AlignCenter
        _transm_st = QtCore.Qt.TransformationMode.SmoothTransformation

        self.tabNamespaces = QWidget()
        self.verticalLayout_7 = QVBoxLayout(self.tabNamespaces)
        self.frame_9 = QFrame(self.tabNamespaces)
        self.horizontalLayout_9 = QHBoxLayout(self.frame_9)
        self.ns_tab_btn_mine = QPushButton(self.frame_9)
        self.btn_fav = QPushButton(self.frame_9)
        self.btn_create = QPushButton(self.frame_9)
        self.tbl_ns = _namespaces_table('tbl_ns', self.tabNamespaces)
        self.frame_11 = QFrame(self.tabNamespaces)
        self.frame_10 = QFrame(self.frame_11)
        self.frame_12 = QFrame(self.frame_11)
        self.verticalLayout_8 = QVBoxLayout(self.frame_10)
        self.verticalLayout_9 = QVBoxLayout(self.frame_12)
        self.verticalLayout_10 = QVBoxLayout(self.frame_11)
        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_11 = QHBoxLayout()
        __path = os.path.dirname(__file__)
        _bpic = QtGui.QPixmap(os.path.join(__path, 'assets/clipboard.png'))
        _bpic = _bpic.scaledToWidth(20, _transm_st)
        self.sel_ns_sc_bvpic = QLabel()
        self.sel_ns_n_bvpic = QLabel()
        self.sel_ns = QLabel(self.tabNamespaces)
        self.sel_s = QLabel(self.tabNamespaces)
        self.sel_ns_sc = QLabel(self.tabNamespaces)
        self.sel_ns_name = QLabel(self.tabNamespaces)
        self.btn_key_add = QPushButton(self.frame_10)
        self.list_ns_keys = _namespace_keys_list('ns_tab_list_ne_keys',
                                                 self.frame_10)
        self.ns_tab_text_key_value = _ns_value_textedit('ns_tab_text_key_val',
                                                        self.frame_10)
        p = QPalette(self.ns_tab_text_key_value.palette())
        self.horizontalLayout_12 = QHBoxLayout()
        self.btn_val_save = QPushButton(self.frame_12)
        self.btn_val_edit = QPushButton(self.frame_12)
        self.btn_val_del = QPushButton(self.frame_12)
        splitter_kv = QSplitter(QtCore.Qt.Orientation.Horizontal)
        splitter_main = QSplitter(QtCore.Qt.Orientation.Vertical)

        self.tabNamespaces.setObjectName('tabNS')
        self.frame_9.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_9.setFrameShadow(QFrame.Shadow.Raised)
        self.ns_tab_btn_mine.setVisible(False)
        # self.btn_fav.setVisible(False)
        self.frame_11.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_11.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_10.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_10.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_12.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_12.setFrameShadow(QFrame.Shadow.Raised)
        self.sel_ns_sc_bvpic.setAlignment(_al_center)
        self.sel_ns_sc_bvpic.setContentsMargins(0, 0, 0, 0)
        self.sel_ns_sc_bvpic.setPixmap(_bpic)
        self.sel_ns_n_bvpic.setAlignment(_al_center)
        self.sel_ns_n_bvpic.setContentsMargins(0, 0, 0, 0)
        self.sel_ns_n_bvpic.setPixmap(_bpic)
        self.btn_key_add.setEnabled(False)
        self.ns_tab_text_key_value.setEnabled(False)
        p.setColor(QPalette.ColorRole.Text, QtCore.Qt.GlobalColor.black)
        self.ns_tab_text_key_value.setPalette(p)
        self.btn_val_save.setVisible(False)
        self.btn_val_edit.setEnabled(False)
        self.btn_val_del.setEnabled(False)
        splitter_kv.setStretchFactor(1, 1)
        splitter_main.setStretchFactor(1, 1)

        self.horizontalLayout_9.addWidget(self.ns_tab_btn_mine)
        self.horizontalLayout_9.addWidget(self.btn_fav)
        self.horizontalLayout_9.addItem(QSpacerItem(531, 20, _sp_exp, _sp_min))
        self.horizontalLayout_9.addWidget(self.btn_create)
        self.verticalLayout_7.addWidget(self.frame_9)
        self.horizontalLayout_11.addWidget(self.sel_ns)
        self.horizontalLayout_11.addWidget(self.sel_ns_sc)
        self.horizontalLayout_11.addWidget(self.sel_ns_sc_bvpic)
        self.horizontalLayout_11.addWidget(self.sel_s)
        self.horizontalLayout_11.addWidget(self.sel_ns_name)
        self.horizontalLayout_11.addWidget(self.sel_ns_n_bvpic)
        self.horizontalLayout_11.addItem(QSpacerItem(20, 20, _sp_exp, _sp_min))
        self.verticalLayout_10.addLayout(self.horizontalLayout_11)
        self.verticalLayout_8.addWidget(self.btn_key_add)
        self.verticalLayout_8.addWidget(self.list_ns_keys)
        self.verticalLayout_9.addWidget(self.ns_tab_text_key_value)
        self.horizontalLayout_12.addWidget(self.btn_val_save)
        self.horizontalLayout_12.addWidget(self.btn_val_edit)
        self.horizontalLayout_12.addWidget(self.btn_val_del)
        self.verticalLayout_9.addLayout(self.horizontalLayout_12)
        splitter_kv.addWidget(self.frame_10)
        splitter_kv.addWidget(self.frame_12)
        self.horizontalLayout_10.addWidget(splitter_kv)
        self.verticalLayout_10.addLayout(self.horizontalLayout_10)
        splitter_main.addWidget(self.tbl_ns)
        splitter_main.addWidget(self.frame_11)
        self.verticalLayout_7.addWidget(splitter_main)

        splitter_kv.setSizes([150, 300])
        splitter_main.setSizes([375, 350])

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.ns_tab_btn_mine.setText(_translate('tabNS', 'Mine'))
        self.btn_fav.setText(_translate('tabNS', 'Add Favorite'))
        self.btn_create.setText(_translate('tabNS', 'Create'))
        self.btn_key_add.setText(_translate('tabNS', 'Create'))
        self.btn_val_save.setText(_translate('tabNS', 'Save'))
        self.btn_val_edit.setText(_translate('tabNS', 'Edit'))
        self.btn_val_del.setText(_translate('tabNS', 'Delete'))
        self.sel_ns.setText(_translate('tabNS', 'Selected namespace:'))
        self.sel_s.setText(_translate('tabNS', '-'))
