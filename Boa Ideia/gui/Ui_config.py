# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'def.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialog,
    QDialogButtonBox, QFrame, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QRadioButton, QSizePolicy,
    QSpacerItem, QStackedWidget, QVBoxLayout, QWidget)
import gui.img_rc

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(535, 437)
        Dialog.setStyleSheet(u"QPushButton {\n"
"    background-color: #f5f5f5;\n"
"    color: #000000;\n"
"    border: 1px solid #c2c2c2;\n"
"    border-radius: 3px;\n"
"    padding: 6px 12px;\n"
"    font-size: 14px;\n"
"    font-family: Roboto;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #e0e0e0;\n"
"    border: 1px solid #e0e0e0;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #d0d0d0;\n"
"    border: 1px solid #888888;\n"
"}\n"
"\n"
"QPushButton:checked {\n"
"    border-top-left-radius: 0px;\n"
"    border-bottom-left-radius: 0px;\n"
"    border-top-right-radius: 3px;\n"
"    border-bottom-right-radius: 3px;\n"
"    border-left: 3px solid rgb(0, 85, 255);\n"
"    background-color: rgb(220, 220, 220);\n"
"}\n"
"\n"
"\n"
"\n"
"QRadioButton {\n"
"    spacing: 6px;\n"
"}\n"
"\n"
"QRadioButton::indicator {\n"
"    width: 24px;\n"
"    height: 24px;\n"
"}\n"
"/* --------- QComboBox --------- */\n"
"QComboBox {\n"
"    background-color: #ffffff;\n"
"    border: 2px solid #b3b3b3;\n"
"    border-radius: 5px;\n"
""
                        "    padding: 5px;\n"
"    font-size: 14px;\n"
"    font-family: Roboto;\n"
"    color: #333333;\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"    border: 2px solid #0078d7;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 25px;\n"
"    border-left: 1px solid #b3b3b3;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    image: url(:/img/arrow-down-1.png);\n"
"    width: 10px;\n"
"    height: 10px;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    background-color: #ffffff;\n"
"    border: 1px solid #b3b3b3;\n"
"    border-radius: 5px;\n"
"    selection-background-color: #0078d7;\n"
"    selection-color: #ffffff;\n"
"}\n"
"\n"
"\n"
"/* --------- QTableWidget --------- */\n"
"QTableWidget {\n"
"    background-color: #ffffff;\n"
"    border: 1px solid #dcdcdc;\n"
"    border-radius: 3px;\n"
"    font-family: Roboto;\n"
"    font-size: 10pt;\n"
"    gridline-color: #e0e0e0;\n"
"    selection-background-color: #0078d7;\n"
"    selection-color: #ffff"
                        "ff;\n"
"}\n"
"\n"
"QTableWidget::item:hover {\n"
"    background-color: #f0f0f0;\n"
"}\n"
"\n"
"QHeaderView::section {\n"
"    background-color: #eaeaea;\n"
"    color: #333333;\n"
"    padding: 4px;\n"
"    border: none;\n"
"    border-right: 1px solid #dcdcdc;\n"
"    font-weight: bold;\n"
"    font-family: Roboto;\n"
"    font-size: 10pt;\n"
"}\n"
"\n"
"QHeaderView::section:horizontal {\n"
"    border-top-left-radius: 3px;\n"
"    border-top-right-radius: 3px;\n"
"}\n"
"\n"
"QHeaderView::section:vertical {\n"
"    border-top-left-radius: 3px;\n"
"    border-bottom-left-radius: 3px;\n"
"}\n"
"\n"
"QTableCornerButton::section {\n"
"    background-color: #eaeaea;\n"
"    border: none;\n"
"}\n"
"\n"
"\n"
"\n"
"/* --------- QLabel --------- */\n"
"QLabel {\n"
"    color: #333333;\n"
"    font-family: Roboto, sans-serif;\n"
"    font-size: 14px;\n"
"    padding: 2px;\n"
"}\n"
"")
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.pushButton = QPushButton(self.frame)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setCheckable(True)
        self.pushButton.setChecked(True)
        self.pushButton.setAutoExclusive(True)

        self.verticalLayout_3.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(self.frame)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setCheckable(True)
        self.pushButton_2.setAutoExclusive(True)

        self.verticalLayout_3.addWidget(self.pushButton_2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)


        self.horizontalLayout.addWidget(self.frame)

        self.frame_2 = QFrame(Dialog)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.pesquisar = QLineEdit(self.frame_2)
        self.pesquisar.setObjectName(u"pesquisar")
        self.pesquisar.setStyleSheet(u"QLineEdit {\n"
"    border: 1px solig rgb(238, 238, 238);\n"
"    border-bottom: 2px solid #ccc;\n"
"    padding-left: 2px; \n"
"    height: 24px;\n"
"    font-size: 14px;\n"
"    color: #333;\n"
"    background: rgb(255, 255, 255);\n"
"    image-position: left;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border-bottom: 2px solid #2979ff;\n"
"    outline: none;\n"
"}\n"
"")
        self.pesquisar.setEchoMode(QLineEdit.EchoMode.Normal)

        self.verticalLayout_2.addWidget(self.pesquisar, 0, Qt.AlignmentFlag.AlignRight)

        self.stackedWidget = QStackedWidget(self.frame_2)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.verticalLayout_5 = QVBoxLayout(self.page)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label_2 = QLabel(self.page)
        self.label_2.setObjectName(u"label_2")
        font = QFont()
        font.setFamilies([u"Roboto"])
        font.setBold(True)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet(u"")

        self.verticalLayout_5.addWidget(self.label_2)

        self.frame_3 = QFrame(self.page)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame_3)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label = QLabel(self.frame_3)
        self.label.setObjectName(u"label")

        self.verticalLayout_4.addWidget(self.label)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.radioButton = QRadioButton(self.frame_3)
        self.radioButton.setObjectName(u"radioButton")

        self.horizontalLayout_2.addWidget(self.radioButton)

        self.radioButton_2 = QRadioButton(self.frame_3)
        self.radioButton_2.setObjectName(u"radioButton_2")

        self.horizontalLayout_2.addWidget(self.radioButton_2)

        self.radioButton_3 = QRadioButton(self.frame_3)
        self.radioButton_3.setObjectName(u"radioButton_3")

        self.horizontalLayout_2.addWidget(self.radioButton_3)


        self.verticalLayout_4.addLayout(self.horizontalLayout_2)

        self.frame_4 = QFrame(self.frame_3)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.frame_4)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.label_4 = QLabel(self.frame_4)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_6.addWidget(self.label_4)


        self.verticalLayout_4.addWidget(self.frame_4)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.pushButton_3 = QPushButton(self.frame_3)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.horizontalLayout_7.addWidget(self.pushButton_3)

        self.lineEdit = QLineEdit(self.frame_3)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setStyleSheet(u"QLineEdit {\n"
"    background-color: #ffffff;\n"
"    border: 1px solid #c2c2c2;\n"
"    border-radius: 6px;\n"
"    padding: 6px;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border: 1px solid #0078d7;\n"
"    background-color: #f0f8ff;\n"
"}\n"
"\n"
"QLineEdit:hover {\n"
"    border: 1px solid #0078d7;\n"
"}")

        self.horizontalLayout_7.addWidget(self.lineEdit)


        self.verticalLayout_4.addLayout(self.horizontalLayout_7)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_2)


        self.verticalLayout_5.addWidget(self.frame_3)

        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.verticalLayout_7 = QVBoxLayout(self.page_2)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.label_3 = QLabel(self.page_2)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font)

        self.verticalLayout_7.addWidget(self.label_3)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_5 = QLabel(self.page_2)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_3.addWidget(self.label_5)

        self.comboBox = QComboBox(self.page_2)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")

        self.horizontalLayout_3.addWidget(self.comboBox)


        self.verticalLayout_7.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_6 = QLabel(self.page_2)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_4.addWidget(self.label_6)

        self.comboBox_2 = QComboBox(self.page_2)
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.setObjectName(u"comboBox_2")

        self.horizontalLayout_4.addWidget(self.comboBox_2)


        self.verticalLayout_7.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_7 = QLabel(self.page_2)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_5.addWidget(self.label_7)

        self.comboBox_3 = QComboBox(self.page_2)
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.setObjectName(u"comboBox_3")

        self.horizontalLayout_5.addWidget(self.comboBox_3)


        self.verticalLayout_7.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_8 = QLabel(self.page_2)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_6.addWidget(self.label_8)

        self.comboBox_4 = QComboBox(self.page_2)
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.setObjectName(u"comboBox_4")

        self.horizontalLayout_6.addWidget(self.comboBox_4)


        self.verticalLayout_7.addLayout(self.horizontalLayout_6)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer_3)

        self.stackedWidget.addWidget(self.page_2)

        self.verticalLayout_2.addWidget(self.stackedWidget)


        self.horizontalLayout.addWidget(self.frame_2)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok|QDialogButtonBox.StandardButton.RestoreDefaults)

        self.verticalLayout.addWidget(self.buttonBox, 0, Qt.AlignmentFlag.AlignRight)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.pushButton.setText(QCoreApplication.translate("Dialog", u"Geral", None))
        self.pushButton_2.setText(QCoreApplication.translate("Dialog", u"Unidades", None))
        self.pesquisar.setPlaceholderText(QCoreApplication.translate("Dialog", u"Pesquisar", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Geral", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Apar\u00eancia ", None))
        self.radioButton.setText(QCoreApplication.translate("Dialog", u"Escuro", None))
        self.radioButton_2.setText(QCoreApplication.translate("Dialog", u"Claro", None))
        self.radioButton_3.setText(QCoreApplication.translate("Dialog", u"Automatico", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Caminho para Salvar Arquivos", None))
        self.pushButton_3.setText(QCoreApplication.translate("Dialog", u"Escolha", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Unidades", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"Vaz\u00e3o ", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("Dialog", u"m3\u2044s", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("Dialog", u"L/s", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("Dialog", u"m3/dia", None))

        self.label_6.setText(QCoreApplication.translate("Dialog", u"Comprimento", None))
        self.comboBox_2.setItemText(0, QCoreApplication.translate("Dialog", u"Metros", None))
        self.comboBox_2.setItemText(1, QCoreApplication.translate("Dialog", u"Cent\u00edmetros", None))
        self.comboBox_2.setItemText(2, QCoreApplication.translate("Dialog", u"Mil\u00edmetros ", None))

        self.label_7.setText(QCoreApplication.translate("Dialog", u"Di\u00e2metro ", None))
        self.comboBox_3.setItemText(0, QCoreApplication.translate("Dialog", u"Metros", None))
        self.comboBox_3.setItemText(1, QCoreApplication.translate("Dialog", u"Mil\u00edmetros ", None))
        self.comboBox_3.setItemText(2, QCoreApplication.translate("Dialog", u"Polegadas", None))

        self.label_8.setText(QCoreApplication.translate("Dialog", u"Pot\u00eancia ", None))
        self.comboBox_4.setItemText(0, QCoreApplication.translate("Dialog", u"Watt", None))
        self.comboBox_4.setItemText(1, QCoreApplication.translate("Dialog", u"Cavalo Vapor", None))

    # retranslateUi

