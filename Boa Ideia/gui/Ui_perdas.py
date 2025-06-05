# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'untitled.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QAbstractItemView, QAbstractScrollArea, QApplication,
    QComboBox, QDialog, QDialogButtonBox, QFrame,
    QGroupBox, QHBoxLayout, QHeaderView, QPushButton,
    QRadioButton, QSizePolicy, QSpacerItem, QStackedWidget,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)
import gui.img_rc

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(550, 427)
        Dialog.setStyleSheet(u"/* --------- QPushButton --------- */\n"
"QPushButton {\n"
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
"/* --------- QLabel --------- */\n"
"QLabel {\n"
"    font-family: Roboto;\n"
"    font-size: 10pt;\n"
"    color: #333333;\n"
"}\n"
"\n"
"\n"
"/* --------- QGroupBox --------- */\n"
"QGroupBox {\n"
"    background-color: transparent;\n"
"    bord"
                        "er: 1px solid #dcdcdc;\n"
"    border-radius: 3px;\n"
"    margin-top: 10px;\n"
"    padding: 10px;\n"
"    font-family: \"Roboto\";\n"
"    font-size: 13px;\n"
"}\n"
"\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left;\n"
"    padding: 0 3px;\n"
"    background-color: transparent;\n"
"    color: rgb(0, 0, 0);\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"\n"
"/* --------- QComboBox --------- */\n"
"QComboBox {\n"
"    background-color: #ffffff;\n"
"    border: 2px solid #b3b3b3;\n"
"    border-radius: 5px;\n"
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
""
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
"    selection-color: #ffffff;\n"
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
""
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
"/* --------- QScrollBar --------- */\n"
"QScrollBar:vertical, QScrollBar:horizontal {\n"
"    background: rgb(231, 231, 231);\n"
"    width: 12px;\n"
"    height: 12px;\n"
"    margin: 10px 0 10px 0;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical, QScrollBar::handle:horizontal {\n"
"    background-color: #c0c0c0;\n"
"    min-height: 30px;\n"
"    margin: 2px;\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical:hover, QScrollBar::handle:horizontal:hover {\n"
"    background-color: #909090;\n"
"}\n"
"\n"
"QScrollBar::sub-line:vertical, QScrollBar::add-line:vertical,\n"
"QScrollBar::sub-line:horizontal, QScrollBar::add-line:horizontal {\n"
"    background: #e1e1e1;\n"
"    height: 12px;\n"
"    width: 12px;\n"
"    border-radius: 6px;\n"
"}\n"
"\n"
"QScrollBar:"
                        ":add-line:vertical:hover, QScrollBar::add-line:horizontal:hover {\n"
"    background: #c0c0c0;\n"
"}\n"
"\n"
"QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical,\n"
"QScrollBar::left-arrow:horizontal, QScrollBar::right-arrow:horizontal {\n"
"    image: url(:/img/arrow-up.png); /* Ajuste conforme necess\u00e1rio */\n"
"    width: 8px;\n"
"    height: 9px;\n"
"    margin: 2px;\n"
"}\n"
"")
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame)
        self.verticalLayout_5.setSpacing(9)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, -1, 0, 0)
        self.botao_succao = QPushButton(self.frame)
        self.botao_succao.setObjectName(u"botao_succao")
        self.botao_succao.setMinimumSize(QSize(0, 25))
        self.botao_succao.setCheckable(True)
        self.botao_succao.setChecked(True)
        self.botao_succao.setAutoExclusive(True)

        self.verticalLayout_5.addWidget(self.botao_succao)

        self.botao_recalque = QPushButton(self.frame)
        self.botao_recalque.setObjectName(u"botao_recalque")
        self.botao_recalque.setMinimumSize(QSize(0, 25))
        self.botao_recalque.setCheckable(True)
        self.botao_recalque.setAutoExclusive(True)

        self.verticalLayout_5.addWidget(self.botao_recalque)

        self.botao_metodo = QPushButton(self.frame)
        self.botao_metodo.setObjectName(u"botao_metodo")
        self.botao_metodo.setMinimumSize(QSize(65, 25))
        self.botao_metodo.setCheckable(True)
        self.botao_metodo.setAutoExclusive(True)

        self.verticalLayout_5.addWidget(self.botao_metodo)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer)


        self.horizontalLayout.addWidget(self.frame)

        self.stackedWidget = QStackedWidget(Dialog)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.verticalLayout_6 = QVBoxLayout(self.page)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.groupBox_4 = QGroupBox(self.page)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.verticalLayout_8 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.comboBox = QComboBox(self.groupBox_4)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setMinimumSize(QSize(0, 30))
        self.comboBox.setStyleSheet(u"")

        self.verticalLayout_8.addWidget(self.comboBox)

        self.comboBox_3 = QComboBox(self.groupBox_4)
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.setObjectName(u"comboBox_3")
        self.comboBox_3.setStyleSheet(u"")

        self.verticalLayout_8.addWidget(self.comboBox_3)


        self.verticalLayout_6.addWidget(self.groupBox_4)

        self.groupBox = QGroupBox(self.page)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.tabela_1 = QTableWidget(self.groupBox)
        if (self.tabela_1.columnCount() < 2):
            self.tabela_1.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.tabela_1.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tabela_1.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        if (self.tabela_1.rowCount() < 25):
            self.tabela_1.setRowCount(25)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tabela_1.setItem(0, 0, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tabela_1.setItem(0, 1, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tabela_1.setItem(1, 0, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tabela_1.setItem(1, 1, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tabela_1.setItem(2, 0, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tabela_1.setItem(2, 1, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.tabela_1.setItem(3, 0, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.tabela_1.setItem(3, 1, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.tabela_1.setItem(4, 0, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.tabela_1.setItem(4, 1, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.tabela_1.setItem(5, 0, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.tabela_1.setItem(5, 1, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.tabela_1.setItem(6, 0, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.tabela_1.setItem(6, 1, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        self.tabela_1.setItem(7, 0, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        self.tabela_1.setItem(7, 1, __qtablewidgetitem17)
        __qtablewidgetitem18 = QTableWidgetItem()
        self.tabela_1.setItem(8, 0, __qtablewidgetitem18)
        __qtablewidgetitem19 = QTableWidgetItem()
        self.tabela_1.setItem(8, 1, __qtablewidgetitem19)
        __qtablewidgetitem20 = QTableWidgetItem()
        self.tabela_1.setItem(9, 0, __qtablewidgetitem20)
        __qtablewidgetitem21 = QTableWidgetItem()
        self.tabela_1.setItem(9, 1, __qtablewidgetitem21)
        __qtablewidgetitem22 = QTableWidgetItem()
        self.tabela_1.setItem(10, 0, __qtablewidgetitem22)
        __qtablewidgetitem23 = QTableWidgetItem()
        self.tabela_1.setItem(10, 1, __qtablewidgetitem23)
        __qtablewidgetitem24 = QTableWidgetItem()
        self.tabela_1.setItem(11, 0, __qtablewidgetitem24)
        __qtablewidgetitem25 = QTableWidgetItem()
        self.tabela_1.setItem(11, 1, __qtablewidgetitem25)
        __qtablewidgetitem26 = QTableWidgetItem()
        self.tabela_1.setItem(12, 0, __qtablewidgetitem26)
        __qtablewidgetitem27 = QTableWidgetItem()
        self.tabela_1.setItem(12, 1, __qtablewidgetitem27)
        __qtablewidgetitem28 = QTableWidgetItem()
        self.tabela_1.setItem(13, 0, __qtablewidgetitem28)
        __qtablewidgetitem29 = QTableWidgetItem()
        self.tabela_1.setItem(13, 1, __qtablewidgetitem29)
        __qtablewidgetitem30 = QTableWidgetItem()
        self.tabela_1.setItem(14, 0, __qtablewidgetitem30)
        __qtablewidgetitem31 = QTableWidgetItem()
        self.tabela_1.setItem(14, 1, __qtablewidgetitem31)
        __qtablewidgetitem32 = QTableWidgetItem()
        self.tabela_1.setItem(15, 0, __qtablewidgetitem32)
        __qtablewidgetitem33 = QTableWidgetItem()
        self.tabela_1.setItem(15, 1, __qtablewidgetitem33)
        __qtablewidgetitem34 = QTableWidgetItem()
        self.tabela_1.setItem(16, 0, __qtablewidgetitem34)
        __qtablewidgetitem35 = QTableWidgetItem()
        self.tabela_1.setItem(16, 1, __qtablewidgetitem35)
        __qtablewidgetitem36 = QTableWidgetItem()
        self.tabela_1.setItem(17, 0, __qtablewidgetitem36)
        __qtablewidgetitem37 = QTableWidgetItem()
        self.tabela_1.setItem(17, 1, __qtablewidgetitem37)
        __qtablewidgetitem38 = QTableWidgetItem()
        self.tabela_1.setItem(18, 0, __qtablewidgetitem38)
        __qtablewidgetitem39 = QTableWidgetItem()
        self.tabela_1.setItem(18, 1, __qtablewidgetitem39)
        __qtablewidgetitem40 = QTableWidgetItem()
        self.tabela_1.setItem(19, 0, __qtablewidgetitem40)
        __qtablewidgetitem41 = QTableWidgetItem()
        self.tabela_1.setItem(19, 1, __qtablewidgetitem41)
        __qtablewidgetitem42 = QTableWidgetItem()
        self.tabela_1.setItem(20, 0, __qtablewidgetitem42)
        __qtablewidgetitem43 = QTableWidgetItem()
        self.tabela_1.setItem(20, 1, __qtablewidgetitem43)
        __qtablewidgetitem44 = QTableWidgetItem()
        self.tabela_1.setItem(21, 0, __qtablewidgetitem44)
        __qtablewidgetitem45 = QTableWidgetItem()
        self.tabela_1.setItem(21, 1, __qtablewidgetitem45)
        __qtablewidgetitem46 = QTableWidgetItem()
        self.tabela_1.setItem(22, 0, __qtablewidgetitem46)
        __qtablewidgetitem47 = QTableWidgetItem()
        self.tabela_1.setItem(22, 1, __qtablewidgetitem47)
        __qtablewidgetitem48 = QTableWidgetItem()
        self.tabela_1.setItem(23, 0, __qtablewidgetitem48)
        __qtablewidgetitem49 = QTableWidgetItem()
        self.tabela_1.setItem(23, 1, __qtablewidgetitem49)
        __qtablewidgetitem50 = QTableWidgetItem()
        self.tabela_1.setItem(24, 0, __qtablewidgetitem50)
        __qtablewidgetitem51 = QTableWidgetItem()
        self.tabela_1.setItem(24, 1, __qtablewidgetitem51)
        self.tabela_1.setObjectName(u"tabela_1")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabela_1.sizePolicy().hasHeightForWidth())
        self.tabela_1.setSizePolicy(sizePolicy)
        self.tabela_1.setMaximumSize(QSize(16777215, 500))
        self.tabela_1.setStyleSheet(u"QTableView::header{\n"
"	background-color: rgb(227, 227, 227);\n"
"border: 1px solid rgb(227, 227, 227)\n"
"}\n"
"\n"
"QScrollBar:vertical {\n"
"    border: none;\n"
"    background: #f0f0f0;\n"
"    width: 12px;\n"
"    margin: 3px;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical {\n"
"    background: rgb(206, 206, 206);\n"
"    min-height: 20px;\n"
"    border-radius: 6px;\n"
"}\n"
"\n"
"QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {\n"
"    height: 0px;\n"
"    width: 0px;\n"
"    background: none;\n"
"}\n"
"\n"
"QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"    background: rgb(248, 248, 248);\n"
"}\n"
"\n"
"QScrollBar:horizontal {\n"
"    border: none;\n"
"    background: rgb(255, 255, 255);\n"
"    height: 12px;\n"
"    margin: 3px;\n"
"}\n"
"\n"
"QScrollBar::handle:horizontal {\n"
"    background: rgb(206, 206, 206) ;\n"
"    min-width: 20px;\n"
"    border-radius: 6px;\n"
"}\n"
"\n"
"QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {\n"
"    height: 0px;\n"
""
                        "    width: 0px;\n"
"    background: none;\n"
"}\n"
"\n"
"QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {\n"
"    background: rgb(248, 248, 248);\n"
"}\n"
"\n"
"")
        self.tabela_1.setInputMethodHints(Qt.InputMethodHint.ImhDigitsOnly)
        self.tabela_1.setFrameShape(QFrame.Shape.Box)
        self.tabela_1.setFrameShadow(QFrame.Shadow.Sunken)
        self.tabela_1.setLineWidth(1)
        self.tabela_1.setMidLineWidth(0)
        self.tabela_1.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.tabela_1.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.tabela_1.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.tabela_1.setEditTriggers(QAbstractItemView.EditTrigger.AllEditTriggers)
        self.tabela_1.setDragEnabled(True)
        self.tabela_1.setAlternatingRowColors(True)
        self.tabela_1.setTextElideMode(Qt.TextElideMode.ElideNone)
        self.tabela_1.setRowCount(25)
        self.tabela_1.horizontalHeader().setVisible(True)
        self.tabela_1.horizontalHeader().setCascadingSectionResizes(True)
        self.tabela_1.horizontalHeader().setMinimumSectionSize(60)
        self.tabela_1.horizontalHeader().setProperty(u"showSortIndicator", False)
        self.tabela_1.horizontalHeader().setStretchLastSection(False)
        self.tabela_1.verticalHeader().setCascadingSectionResizes(False)

        self.verticalLayout_2.addWidget(self.tabela_1)


        self.verticalLayout_6.addWidget(self.groupBox)

        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.verticalLayout_4 = QVBoxLayout(self.page_2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.groupBox_3 = QGroupBox(self.page_2)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_7 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.comboBox_2 = QComboBox(self.groupBox_3)
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.setObjectName(u"comboBox_2")
        self.comboBox_2.setMinimumSize(QSize(0, 30))
        self.comboBox_2.setStyleSheet(u"")

        self.verticalLayout_7.addWidget(self.comboBox_2)

        self.comboBox_4 = QComboBox(self.groupBox_3)
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.setObjectName(u"comboBox_4")
        self.comboBox_4.setStyleSheet(u"")

        self.verticalLayout_7.addWidget(self.comboBox_4)


        self.verticalLayout_4.addWidget(self.groupBox_3)

        self.groupBox_2 = QGroupBox(self.page_2)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 10, 0, 0)
        self.tabela_2 = QTableWidget(self.groupBox_2)
        if (self.tabela_2.columnCount() < 2):
            self.tabela_2.setColumnCount(2)
        __qtablewidgetitem52 = QTableWidgetItem()
        self.tabela_2.setHorizontalHeaderItem(0, __qtablewidgetitem52)
        __qtablewidgetitem53 = QTableWidgetItem()
        self.tabela_2.setHorizontalHeaderItem(1, __qtablewidgetitem53)
        if (self.tabela_2.rowCount() < 25):
            self.tabela_2.setRowCount(25)
        __qtablewidgetitem54 = QTableWidgetItem()
        self.tabela_2.setItem(0, 0, __qtablewidgetitem54)
        __qtablewidgetitem55 = QTableWidgetItem()
        self.tabela_2.setItem(0, 1, __qtablewidgetitem55)
        __qtablewidgetitem56 = QTableWidgetItem()
        self.tabela_2.setItem(1, 0, __qtablewidgetitem56)
        __qtablewidgetitem57 = QTableWidgetItem()
        self.tabela_2.setItem(1, 1, __qtablewidgetitem57)
        __qtablewidgetitem58 = QTableWidgetItem()
        self.tabela_2.setItem(2, 0, __qtablewidgetitem58)
        __qtablewidgetitem59 = QTableWidgetItem()
        self.tabela_2.setItem(2, 1, __qtablewidgetitem59)
        __qtablewidgetitem60 = QTableWidgetItem()
        self.tabela_2.setItem(3, 0, __qtablewidgetitem60)
        __qtablewidgetitem61 = QTableWidgetItem()
        self.tabela_2.setItem(3, 1, __qtablewidgetitem61)
        __qtablewidgetitem62 = QTableWidgetItem()
        self.tabela_2.setItem(4, 0, __qtablewidgetitem62)
        __qtablewidgetitem63 = QTableWidgetItem()
        self.tabela_2.setItem(4, 1, __qtablewidgetitem63)
        __qtablewidgetitem64 = QTableWidgetItem()
        self.tabela_2.setItem(5, 0, __qtablewidgetitem64)
        __qtablewidgetitem65 = QTableWidgetItem()
        self.tabela_2.setItem(5, 1, __qtablewidgetitem65)
        __qtablewidgetitem66 = QTableWidgetItem()
        self.tabela_2.setItem(6, 0, __qtablewidgetitem66)
        __qtablewidgetitem67 = QTableWidgetItem()
        self.tabela_2.setItem(6, 1, __qtablewidgetitem67)
        __qtablewidgetitem68 = QTableWidgetItem()
        self.tabela_2.setItem(7, 0, __qtablewidgetitem68)
        __qtablewidgetitem69 = QTableWidgetItem()
        self.tabela_2.setItem(7, 1, __qtablewidgetitem69)
        __qtablewidgetitem70 = QTableWidgetItem()
        self.tabela_2.setItem(8, 0, __qtablewidgetitem70)
        __qtablewidgetitem71 = QTableWidgetItem()
        self.tabela_2.setItem(8, 1, __qtablewidgetitem71)
        __qtablewidgetitem72 = QTableWidgetItem()
        self.tabela_2.setItem(9, 0, __qtablewidgetitem72)
        __qtablewidgetitem73 = QTableWidgetItem()
        self.tabela_2.setItem(9, 1, __qtablewidgetitem73)
        __qtablewidgetitem74 = QTableWidgetItem()
        self.tabela_2.setItem(10, 0, __qtablewidgetitem74)
        __qtablewidgetitem75 = QTableWidgetItem()
        self.tabela_2.setItem(10, 1, __qtablewidgetitem75)
        __qtablewidgetitem76 = QTableWidgetItem()
        self.tabela_2.setItem(11, 0, __qtablewidgetitem76)
        __qtablewidgetitem77 = QTableWidgetItem()
        self.tabela_2.setItem(11, 1, __qtablewidgetitem77)
        __qtablewidgetitem78 = QTableWidgetItem()
        self.tabela_2.setItem(12, 0, __qtablewidgetitem78)
        __qtablewidgetitem79 = QTableWidgetItem()
        self.tabela_2.setItem(12, 1, __qtablewidgetitem79)
        __qtablewidgetitem80 = QTableWidgetItem()
        self.tabela_2.setItem(13, 0, __qtablewidgetitem80)
        __qtablewidgetitem81 = QTableWidgetItem()
        self.tabela_2.setItem(13, 1, __qtablewidgetitem81)
        __qtablewidgetitem82 = QTableWidgetItem()
        self.tabela_2.setItem(14, 0, __qtablewidgetitem82)
        __qtablewidgetitem83 = QTableWidgetItem()
        self.tabela_2.setItem(14, 1, __qtablewidgetitem83)
        __qtablewidgetitem84 = QTableWidgetItem()
        self.tabela_2.setItem(15, 0, __qtablewidgetitem84)
        __qtablewidgetitem85 = QTableWidgetItem()
        self.tabela_2.setItem(15, 1, __qtablewidgetitem85)
        __qtablewidgetitem86 = QTableWidgetItem()
        self.tabela_2.setItem(16, 0, __qtablewidgetitem86)
        __qtablewidgetitem87 = QTableWidgetItem()
        self.tabela_2.setItem(16, 1, __qtablewidgetitem87)
        __qtablewidgetitem88 = QTableWidgetItem()
        self.tabela_2.setItem(17, 0, __qtablewidgetitem88)
        __qtablewidgetitem89 = QTableWidgetItem()
        self.tabela_2.setItem(17, 1, __qtablewidgetitem89)
        __qtablewidgetitem90 = QTableWidgetItem()
        self.tabela_2.setItem(18, 0, __qtablewidgetitem90)
        __qtablewidgetitem91 = QTableWidgetItem()
        self.tabela_2.setItem(18, 1, __qtablewidgetitem91)
        __qtablewidgetitem92 = QTableWidgetItem()
        self.tabela_2.setItem(19, 0, __qtablewidgetitem92)
        __qtablewidgetitem93 = QTableWidgetItem()
        self.tabela_2.setItem(19, 1, __qtablewidgetitem93)
        __qtablewidgetitem94 = QTableWidgetItem()
        self.tabela_2.setItem(20, 0, __qtablewidgetitem94)
        __qtablewidgetitem95 = QTableWidgetItem()
        self.tabela_2.setItem(20, 1, __qtablewidgetitem95)
        __qtablewidgetitem96 = QTableWidgetItem()
        self.tabela_2.setItem(21, 0, __qtablewidgetitem96)
        __qtablewidgetitem97 = QTableWidgetItem()
        self.tabela_2.setItem(21, 1, __qtablewidgetitem97)
        __qtablewidgetitem98 = QTableWidgetItem()
        self.tabela_2.setItem(22, 0, __qtablewidgetitem98)
        __qtablewidgetitem99 = QTableWidgetItem()
        self.tabela_2.setItem(22, 1, __qtablewidgetitem99)
        __qtablewidgetitem100 = QTableWidgetItem()
        self.tabela_2.setItem(23, 0, __qtablewidgetitem100)
        __qtablewidgetitem101 = QTableWidgetItem()
        self.tabela_2.setItem(23, 1, __qtablewidgetitem101)
        __qtablewidgetitem102 = QTableWidgetItem()
        self.tabela_2.setItem(24, 0, __qtablewidgetitem102)
        __qtablewidgetitem103 = QTableWidgetItem()
        self.tabela_2.setItem(24, 1, __qtablewidgetitem103)
        self.tabela_2.setObjectName(u"tabela_2")
        sizePolicy.setHeightForWidth(self.tabela_2.sizePolicy().hasHeightForWidth())
        self.tabela_2.setSizePolicy(sizePolicy)
        self.tabela_2.setMaximumSize(QSize(16777215, 500))
        self.tabela_2.setStyleSheet(u"QTableView::header{\n"
"	background-color: rgb(227, 227, 227);\n"
"border: 1px solid rgb(227, 227, 227)\n"
"}\n"
"\n"
"QScrollBar:vertical {\n"
"    border: none;\n"
"    background: #f0f0f0;\n"
"    width: 12px;\n"
"    margin: 3px;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical {\n"
"    background: rgb(206, 206, 206);\n"
"    min-height: 20px;\n"
"    border-radius: 6px;\n"
"}\n"
"\n"
"QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {\n"
"    height: 0px;\n"
"    width: 0px;\n"
"    background: none;\n"
"}\n"
"\n"
"QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"    background: rgb(248, 248, 248);\n"
"}\n"
"\n"
"QScrollBar:horizontal {\n"
"    border: none;\n"
"    background: rgb(255, 255, 255);\n"
"    height: 12px;\n"
"    margin: 3px;\n"
"}\n"
"\n"
"QScrollBar::handle:horizontal {\n"
"    background: rgb(206, 206, 206) ;\n"
"    min-width: 20px;\n"
"    border-radius: 6px;\n"
"}\n"
"\n"
"QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {\n"
"    height: 0px;\n"
""
                        "    width: 0px;\n"
"    background: none;\n"
"}\n"
"\n"
"QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {\n"
"    background: rgb(248, 248, 248);\n"
"}\n"
"\n"
"")
        self.tabela_2.setInputMethodHints(Qt.InputMethodHint.ImhDigitsOnly)
        self.tabela_2.setFrameShape(QFrame.Shape.Box)
        self.tabela_2.setFrameShadow(QFrame.Shadow.Sunken)
        self.tabela_2.setLineWidth(1)
        self.tabela_2.setMidLineWidth(0)
        self.tabela_2.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.tabela_2.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.tabela_2.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.tabela_2.setEditTriggers(QAbstractItemView.EditTrigger.AllEditTriggers)
        self.tabela_2.setDragEnabled(True)
        self.tabela_2.setAlternatingRowColors(True)
        self.tabela_2.setTextElideMode(Qt.TextElideMode.ElideNone)
        self.tabela_2.setRowCount(25)
        self.tabela_2.horizontalHeader().setVisible(True)
        self.tabela_2.horizontalHeader().setCascadingSectionResizes(True)
        self.tabela_2.horizontalHeader().setMinimumSectionSize(60)
        self.tabela_2.horizontalHeader().setProperty(u"showSortIndicator", False)
        self.tabela_2.horizontalHeader().setStretchLastSection(False)
        self.tabela_2.verticalHeader().setCascadingSectionResizes(False)

        self.verticalLayout_3.addWidget(self.tabela_2)


        self.verticalLayout_4.addWidget(self.groupBox_2)

        self.stackedWidget.addWidget(self.page_2)
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.verticalLayout_9 = QVBoxLayout(self.page_3)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.groupBox_5 = QGroupBox(self.page_3)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.verticalLayout_10 = QVBoxLayout(self.groupBox_5)
        self.verticalLayout_10.setSpacing(12)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.darcy = QRadioButton(self.groupBox_5)
        self.darcy.setObjectName(u"darcy")
        self.darcy.setChecked(True)

        self.verticalLayout_10.addWidget(self.darcy)

        self.wiliams = QRadioButton(self.groupBox_5)
        self.wiliams.setObjectName(u"wiliams")

        self.verticalLayout_10.addWidget(self.wiliams)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_10.addItem(self.verticalSpacer_2)


        self.verticalLayout_9.addWidget(self.groupBox_5)

        self.stackedWidget.addWidget(self.page_3)

        self.horizontalLayout.addWidget(self.stackedWidget)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStyleSheet(u"")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.botao_succao.setText(QCoreApplication.translate("Dialog", u"Suc\u00e7\u00e3o ", None))
        self.botao_recalque.setText(QCoreApplication.translate("Dialog", u"Recalque", None))
        self.botao_metodo.setText(QCoreApplication.translate("Dialog", u"M\u00e9todo ", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("Dialog", u"Material da Tubula\u00e7\u00e3o ", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("Dialog", u"A\u00e7o Corrugado(chapa ondulada)", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("Dialog", u"A\u00e7o Galvanizado", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("Dialog", u"A\u00e7o Rebitado novo", None))
        self.comboBox.setItemText(3, QCoreApplication.translate("Dialog", u"A\u00e7o Rebitado em uso", None))
        self.comboBox.setItemText(4, QCoreApplication.translate("Dialog", u"A\u00e7o soldado novo", None))
        self.comboBox.setItemText(5, QCoreApplication.translate("Dialog", u"A\u00e7o Soldado em uso", None))
        self.comboBox.setItemText(6, QCoreApplication.translate("Dialog", u"A\u00e7o Soldado com revestimento especial", None))
        self.comboBox.setItemText(7, QCoreApplication.translate("Dialog", u"Chumbo", None))
        self.comboBox.setItemText(8, QCoreApplication.translate("Dialog", u"Cimento Amianto", None))
        self.comboBox.setItemText(9, QCoreApplication.translate("Dialog", u"Cobre", None))
        self.comboBox.setItemText(10, QCoreApplication.translate("Dialog", u"Concreto com acabamento comum", None))
        self.comboBox.setItemText(11, QCoreApplication.translate("Dialog", u"Ferro Fundido novo", None))
        self.comboBox.setItemText(12, QCoreApplication.translate("Dialog", u"Ferro Fundido de 15 a 20 anos de uso", None))
        self.comboBox.setItemText(13, QCoreApplication.translate("Dialog", u"Ferro Fundido Usado", None))
        self.comboBox.setItemText(14, QCoreApplication.translate("Dialog", u"Lat\u00e3o", None))
        self.comboBox.setItemText(15, QCoreApplication.translate("Dialog", u"Ferro Fundido Revestido de Cimento", None))
        self.comboBox.setItemText(16, QCoreApplication.translate("Dialog", u"Manilha Cer\u00e2mica vidrada", None))
        self.comboBox.setItemText(17, QCoreApplication.translate("Dialog", u"Pl\u00e1stico", None))
        self.comboBox.setItemText(18, QCoreApplication.translate("Dialog", u"Tijolos em executados", None))
        self.comboBox.setItemText(19, QCoreApplication.translate("Dialog", u"Vidro", None))

        self.comboBox_3.setItemText(0, QCoreApplication.translate("Dialog", u"PVC", None))
        self.comboBox_3.setItemText(1, QCoreApplication.translate("Dialog", u"Polietileno", None))
        self.comboBox_3.setItemText(2, QCoreApplication.translate("Dialog", u"A\u00e7o galvanizado (novo)", None))
        self.comboBox_3.setItemText(3, QCoreApplication.translate("Dialog", u"Ferro fundido (novo)", None))
        self.comboBox_3.setItemText(4, QCoreApplication.translate("Dialog", u"Ferro fundido (velho ou corro\u00eddo)", None))
        self.comboBox_3.setItemText(5, QCoreApplication.translate("Dialog", u"Concreto liso", None))
        self.comboBox_3.setItemText(6, QCoreApplication.translate("Dialog", u"Concreto rugoso", None))
        self.comboBox_3.setItemText(7, QCoreApplication.translate("Dialog", u"Madeira lisa", None))
        self.comboBox_3.setItemText(8, QCoreApplication.translate("Dialog", u"Madeira \u00e1spera", None))
        self.comboBox_3.setItemText(9, QCoreApplication.translate("Dialog", u"Amianto-cimento", None))
        self.comboBox_3.setItemText(10, QCoreApplication.translate("Dialog", u"Tubo de chumbo", None))
        self.comboBox_3.setItemText(11, QCoreApplication.translate("Dialog", u"Tubo de vidro", None))

        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"Perdas de Cargas Localizadas", None))
        ___qtablewidgetitem = self.tabela_1.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Dialog", u"Acess\u00f3rio ", None));
        ___qtablewidgetitem1 = self.tabela_1.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Dialog", u"Quantidade", None));

        __sortingEnabled = self.tabela_1.isSortingEnabled()
        self.tabela_1.setSortingEnabled(False)
        ___qtablewidgetitem2 = self.tabela_1.item(0, 0)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Dialog", u"Amplia\u00e7\u00e3o Gradua", None));
        ___qtablewidgetitem3 = self.tabela_1.item(0, 1)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Dialog", u"0", None));
        ___qtablewidgetitem4 = self.tabela_1.item(1, 0)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Dialog", u"Comporta Aberta", None));
        ___qtablewidgetitem5 = self.tabela_1.item(1, 1)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("Dialog", u"0", None));
        ___qtablewidgetitem6 = self.tabela_1.item(2, 0)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("Dialog", u"Controlador de Vaz\u00e3o", None));
        ___qtablewidgetitem7 = self.tabela_1.item(2, 1)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("Dialog", u"0", None));
        ___qtablewidgetitem8 = self.tabela_1.item(3, 0)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("Dialog", u"Cotovelo ou joelho de 45", None));
        ___qtablewidgetitem9 = self.tabela_1.item(3, 1)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("Dialog", u"0", None));
        ___qtablewidgetitem10 = self.tabela_1.item(4, 0)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("Dialog", u"Cotovelo ou joelho de 90", None));
        ___qtablewidgetitem11 = self.tabela_1.item(4, 1)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("Dialog", u"0", None));
        ___qtablewidgetitem12 = self.tabela_1.item(5, 0)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("Dialog", u"            Crivo", None));
        ___qtablewidgetitem13 = self.tabela_1.item(5, 1)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("Dialog", u"0", None));
        ___qtablewidgetitem14 = self.tabela_1.item(6, 0)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("Dialog", u"Curva de 22.5", None));
        ___qtablewidgetitem15 = self.tabela_1.item(6, 1)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("Dialog", u"0", None));
        ___qtablewidgetitem16 = self.tabela_1.item(7, 0)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("Dialog", u"Curva 45", None));
        ___qtablewidgetitem17 = self.tabela_1.item(7, 1)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("Dialog", u"0", None));
        ___qtablewidgetitem18 = self.tabela_1.item(8, 0)
        ___qtablewidgetitem18.setText(QCoreApplication.translate("Dialog", u"Curva 90", None));
        ___qtablewidgetitem19 = self.tabela_1.item(8, 1)
        ___qtablewidgetitem19.setText(QCoreApplication.translate("Dialog", u"0", None));
        ___qtablewidgetitem20 = self.tabela_1.item(9, 0)
        ___qtablewidgetitem20.setText(QCoreApplication.translate("Dialog", u"Entrada de Borda", None));
        ___qtablewidgetitem21 = self.tabela_1.item(9, 1)
        ___qtablewidgetitem21.setText(QCoreApplication.translate("Dialog", u"0", None));
        ___qtablewidgetitem22 = self.tabela_1.item(10, 0)
        ___qtablewidgetitem22.setText(QCoreApplication.translate("Dialog", u"Entrada Normal", None));
        ___qtablewidgetitem23 = self.tabela_1.item(10, 1)
        ___qtablewidgetitem23.setText(QCoreApplication.translate("Dialog", u"0", None));
        ___qtablewidgetitem24 = self.tabela_1.item(11, 0)
        ___qtablewidgetitem24.setText(QCoreApplication.translate("Dialog", u"Jun\u00e7\u00e3o", None));
        ___qtablewidgetitem25 = self.tabela_1.item(11, 1)
        ___qtablewidgetitem25.setText(QCoreApplication.translate("Dialog", u"0", None));
        ___qtablewidgetitem26 = self.tabela_1.item(12, 0)
        ___qtablewidgetitem26.setText(QCoreApplication.translate("Dialog", u"Medidor Venturi", None));
        ___qtablewidgetitem27 = self.tabela_1.item(12, 1)
        ___qtablewidgetitem27.setText(QCoreApplication.translate("Dialog", u"0", None));
        ___qtablewidgetitem28 = self.tabela_1.item(13, 0)
        ___qtablewidgetitem28.setText(QCoreApplication.translate("Dialog", u"Pequena Deriva\u00e7\u00e3o", None));
        ___qtablewidgetitem29 = self.tabela_1.item(13, 1)
        ___qtablewidgetitem29.setText(QCoreApplication.translate("Dialog", u"0", None));
        ___qtablewidgetitem30 = self.tabela_1.item(14, 0)
        ___qtablewidgetitem30.setText(QCoreApplication.translate("Dialog", u"Redu\u00e7\u00e3o Gradual", None));
        ___qtablewidgetitem31 = self.tabela_1.item(14, 1)
        ___qtablewidgetitem31.setText(QCoreApplication.translate("Dialog", u"0", None));
        ___qtablewidgetitem32 = self.tabela_1.item(15, 0)
        ___qtablewidgetitem32.setText(QCoreApplication.translate("Dialog", u"Sa\u00edda de Canaliza\u00e7\u00e3o", None));
        ___qtablewidgetitem33 = self.tabela_1.item(15, 1)
        ___qtablewidgetitem33.setText(QCoreApplication.translate("Dialog", u"0", None));
        ___qtablewidgetitem34 = self.tabela_1.item(16, 0)
        ___qtablewidgetitem34.setText(QCoreApplication.translate("Dialog", u"T\u00ea de Passagem directa", None));
        ___qtablewidgetitem35 = self.tabela_1.item(16, 1)
        ___qtablewidgetitem35.setText(QCoreApplication.translate("Dialog", u"0", None));
        ___qtablewidgetitem36 = self.tabela_1.item(17, 0)
        ___qtablewidgetitem36.setText(QCoreApplication.translate("Dialog", u"T\u00ea de saida Bilateral", None));
        ___qtablewidgetitem37 = self.tabela_1.item(17, 1)
        ___qtablewidgetitem37.setText(QCoreApplication.translate("Dialog", u"0", None));
        ___qtablewidgetitem38 = self.tabela_1.item(18, 0)
        ___qtablewidgetitem38.setText(QCoreApplication.translate("Dialog", u"T\u00ea de saida de lado", None));
        ___qtablewidgetitem39 = self.tabela_1.item(18, 1)
        ___qtablewidgetitem39.setText(QCoreApplication.translate("Dialog", u"0", None));
        ___qtablewidgetitem40 = self.tabela_1.item(19, 0)
        ___qtablewidgetitem40.setText(QCoreApplication.translate("Dialog", u"V\u00e1lvula Borboleta", None));
        ___qtablewidgetitem41 = self.tabela_1.item(19, 1)
        ___qtablewidgetitem41.setText(QCoreApplication.translate("Dialog", u"0", None));
        ___qtablewidgetitem42 = self.tabela_1.item(20, 0)
        ___qtablewidgetitem42.setText(QCoreApplication.translate("Dialog", u"V\u00e1lvula de \u00e2ngulo aberta", None));
        ___qtablewidgetitem43 = self.tabela_1.item(20, 1)
        ___qtablewidgetitem43.setText(QCoreApplication.translate("Dialog", u"0", None));
        ___qtablewidgetitem44 = self.tabela_1.item(21, 0)
        ___qtablewidgetitem44.setText(QCoreApplication.translate("Dialog", u"V\u00e1lvula de gaveta aberta", None));
        ___qtablewidgetitem45 = self.tabela_1.item(21, 1)
        ___qtablewidgetitem45.setText(QCoreApplication.translate("Dialog", u"0", None));
        ___qtablewidgetitem46 = self.tabela_1.item(22, 0)
        ___qtablewidgetitem46.setText(QCoreApplication.translate("Dialog", u"V\u00e1lvula de p\u00e9", None));
        ___qtablewidgetitem47 = self.tabela_1.item(22, 1)
        ___qtablewidgetitem47.setText(QCoreApplication.translate("Dialog", u"0", None));
        ___qtablewidgetitem48 = self.tabela_1.item(23, 0)
        ___qtablewidgetitem48.setText(QCoreApplication.translate("Dialog", u"V\u00e1lvula de reten\u00e7\u00e3o", None));
        ___qtablewidgetitem49 = self.tabela_1.item(23, 1)
        ___qtablewidgetitem49.setText(QCoreApplication.translate("Dialog", u"0", None));
        ___qtablewidgetitem50 = self.tabela_1.item(24, 0)
        ___qtablewidgetitem50.setText(QCoreApplication.translate("Dialog", u"V\u00e1lvula globo aberta", None));
        ___qtablewidgetitem51 = self.tabela_1.item(24, 1)
        ___qtablewidgetitem51.setText(QCoreApplication.translate("Dialog", u"0", None));
        self.tabela_1.setSortingEnabled(__sortingEnabled)

        self.groupBox_3.setTitle(QCoreApplication.translate("Dialog", u"Material da Tubula\u00e7\u00e3o ", None))
        self.comboBox_2.setItemText(0, QCoreApplication.translate("Dialog", u"A\u00e7o Corrugado(chapa ondulada)", None))
        self.comboBox_2.setItemText(1, QCoreApplication.translate("Dialog", u"A\u00e7o Galvanizado", None))
        self.comboBox_2.setItemText(2, QCoreApplication.translate("Dialog", u"A\u00e7o Rebitado novo", None))
        self.comboBox_2.setItemText(3, QCoreApplication.translate("Dialog", u"A\u00e7o Rebitado em uso", None))
        self.comboBox_2.setItemText(4, QCoreApplication.translate("Dialog", u"A\u00e7o soldado novo", None))
        self.comboBox_2.setItemText(5, QCoreApplication.translate("Dialog", u"A\u00e7o Soldado em uso", None))
        self.comboBox_2.setItemText(6, QCoreApplication.translate("Dialog", u"A\u00e7o Soldado com revestimento especial", None))
        self.comboBox_2.setItemText(7, QCoreApplication.translate("Dialog", u"Chumbo", None))
        self.comboBox_2.setItemText(8, QCoreApplication.translate("Dialog", u"Cimento Amianto", None))
        self.comboBox_2.setItemText(9, QCoreApplication.translate("Dialog", u"Cobre", None))
        self.comboBox_2.setItemText(10, QCoreApplication.translate("Dialog", u"Concreto com acabamento comum", None))
        self.comboBox_2.setItemText(11, QCoreApplication.translate("Dialog", u"Ferro Fundido novo", None))
        self.comboBox_2.setItemText(12, QCoreApplication.translate("Dialog", u"Ferro Fundido de 15 a 20 anos de uso", None))
        self.comboBox_2.setItemText(13, QCoreApplication.translate("Dialog", u"Ferro Fundido Usado", None))
        self.comboBox_2.setItemText(14, QCoreApplication.translate("Dialog", u"Lat\u00e3o", None))
        self.comboBox_2.setItemText(15, QCoreApplication.translate("Dialog", u"Ferro Fundido Revestido de Cimento", None))
        self.comboBox_2.setItemText(16, QCoreApplication.translate("Dialog", u"Manilha Cer\u00e2mica vidrada", None))
        self.comboBox_2.setItemText(17, QCoreApplication.translate("Dialog", u"Pl\u00e1stico", None))
        self.comboBox_2.setItemText(18, QCoreApplication.translate("Dialog", u"Tijolos em executados", None))
        self.comboBox_2.setItemText(19, QCoreApplication.translate("Dialog", u"Vidro", None))

        self.comboBox_4.setItemText(0, QCoreApplication.translate("Dialog", u"PVC", None))
        self.comboBox_4.setItemText(1, QCoreApplication.translate("Dialog", u"Polietileno", None))
        self.comboBox_4.setItemText(2, QCoreApplication.translate("Dialog", u"A\u00e7o galvanizado (novo)", None))
        self.comboBox_4.setItemText(3, QCoreApplication.translate("Dialog", u"Ferro fundido (novo)", None))
        self.comboBox_4.setItemText(4, QCoreApplication.translate("Dialog", u"Ferro fundido (velho ou corro\u00eddo)", None))
        self.comboBox_4.setItemText(5, QCoreApplication.translate("Dialog", u"Concreto liso", None))
        self.comboBox_4.setItemText(6, QCoreApplication.translate("Dialog", u"Concreto rugoso", None))
        self.comboBox_4.setItemText(7, QCoreApplication.translate("Dialog", u"Madeira lisa", None))
        self.comboBox_4.setItemText(8, QCoreApplication.translate("Dialog", u"Madeira \u00e1spera", None))
        self.comboBox_4.setItemText(9, QCoreApplication.translate("Dialog", u"Amianto-cimento", None))
        self.comboBox_4.setItemText(10, QCoreApplication.translate("Dialog", u"Tubo de chumbo", None))
        self.comboBox_4.setItemText(11, QCoreApplication.translate("Dialog", u"Tubo de vidro", None))

        self.groupBox_2.setTitle(QCoreApplication.translate("Dialog", u"Perdas de Cargas Localizadas", None))
        ___qtablewidgetitem52 = self.tabela_2.horizontalHeaderItem(0)
        ___qtablewidgetitem52.setText(QCoreApplication.translate("Dialog", u"Acess\u00f3rio ", None));
        ___qtablewidgetitem53 = self.tabela_2.horizontalHeaderItem(1)
        ___qtablewidgetitem53.setText(QCoreApplication.translate("Dialog", u"Quantidade", None));

        __sortingEnabled1 = self.tabela_2.isSortingEnabled()
        self.tabela_2.setSortingEnabled(False)
        ___qtablewidgetitem54 = self.tabela_2.item(0, 0)
        ___qtablewidgetitem54.setText(QCoreApplication.translate("Dialog", u"Amplia\u00e7\u00e3o Gradua", None));
        ___qtablewidgetitem55 = self.tabela_2.item(0, 1)
        ___qtablewidgetitem55.setText(QCoreApplication.translate("Dialog", u"0", None));
        ___qtablewidgetitem56 = self.tabela_2.item(1, 0)
        ___qtablewidgetitem56.setText(QCoreApplication.translate("Dialog", u"Comporta Aberta", None));
        ___qtablewidgetitem57 = self.tabela_2.item(1, 1)
        ___qtablewidgetitem57.setText(QCoreApplication.translate("Dialog", u"0", None));
        ___qtablewidgetitem58 = self.tabela_2.item(2, 0)
        ___qtablewidgetitem58.setText(QCoreApplication.translate("Dialog", u"Controlador de Vaz\u00e3o", None));
        ___qtablewidgetitem59 = self.tabela_2.item(2, 1)
        ___qtablewidgetitem59.setText(QCoreApplication.translate("Dialog", u"0", None));
        ___qtablewidgetitem60 = self.tabela_2.item(3, 0)
        ___qtablewidgetitem60.setText(QCoreApplication.translate("Dialog", u"Cotovelo ou joelho de 45", None));
        ___qtablewidgetitem61 = self.tabela_2.item(3, 1)
        ___qtablewidgetitem61.setText(QCoreApplication.translate("Dialog", u"0", None));
        ___qtablewidgetitem62 = self.tabela_2.item(4, 0)
        ___qtablewidgetitem62.setText(QCoreApplication.translate("Dialog", u"Cotovelo ou joelho de 90", None));
        ___qtablewidgetitem63 = self.tabela_2.item(4, 1)
        ___qtablewidgetitem63.setText(QCoreApplication.translate("Dialog", u"0", None));
        ___qtablewidgetitem64 = self.tabela_2.item(5, 0)
        ___qtablewidgetitem64.setText(QCoreApplication.translate("Dialog", u"            Crivo", None));
        ___qtablewidgetitem65 = self.tabela_2.item(5, 1)
        ___qtablewidgetitem65.setText(QCoreApplication.translate("Dialog", u"0", None));
        ___qtablewidgetitem66 = self.tabela_2.item(6, 0)
        ___qtablewidgetitem66.setText(QCoreApplication.translate("Dialog", u"Curva de 22.5", None));
        ___qtablewidgetitem67 = self.tabela_2.item(6, 1)
        ___qtablewidgetitem67.setText(QCoreApplication.translate("Dialog", u"0", None));
        ___qtablewidgetitem68 = self.tabela_2.item(7, 0)
        ___qtablewidgetitem68.setText(QCoreApplication.translate("Dialog", u"Curva 45", None));
        ___qtablewidgetitem69 = self.tabela_2.item(7, 1)
        ___qtablewidgetitem69.setText(QCoreApplication.translate("Dialog", u"0", None));
        ___qtablewidgetitem70 = self.tabela_2.item(8, 0)
        ___qtablewidgetitem70.setText(QCoreApplication.translate("Dialog", u"Curva 90", None));
        ___qtablewidgetitem71 = self.tabela_2.item(8, 1)
        ___qtablewidgetitem71.setText(QCoreApplication.translate("Dialog", u"0", None));
        ___qtablewidgetitem72 = self.tabela_2.item(9, 0)
        ___qtablewidgetitem72.setText(QCoreApplication.translate("Dialog", u"Entrada de Borda", None));
        ___qtablewidgetitem73 = self.tabela_2.item(9, 1)
        ___qtablewidgetitem73.setText(QCoreApplication.translate("Dialog", u"0", None));
        ___qtablewidgetitem74 = self.tabela_2.item(10, 0)
        ___qtablewidgetitem74.setText(QCoreApplication.translate("Dialog", u"Entrada Normal", None));
        ___qtablewidgetitem75 = self.tabela_2.item(10, 1)
        ___qtablewidgetitem75.setText(QCoreApplication.translate("Dialog", u"0", None));
        ___qtablewidgetitem76 = self.tabela_2.item(11, 0)
        ___qtablewidgetitem76.setText(QCoreApplication.translate("Dialog", u"Jun\u00e7\u00e3o", None));
        ___qtablewidgetitem77 = self.tabela_2.item(11, 1)
        ___qtablewidgetitem77.setText(QCoreApplication.translate("Dialog", u"0", None));
        ___qtablewidgetitem78 = self.tabela_2.item(12, 0)
        ___qtablewidgetitem78.setText(QCoreApplication.translate("Dialog", u"Medidor Venturi", None));
        ___qtablewidgetitem79 = self.tabela_2.item(12, 1)
        ___qtablewidgetitem79.setText(QCoreApplication.translate("Dialog", u"0", None));
        ___qtablewidgetitem80 = self.tabela_2.item(13, 0)
        ___qtablewidgetitem80.setText(QCoreApplication.translate("Dialog", u"Pequena Deriva\u00e7\u00e3o", None));
        ___qtablewidgetitem81 = self.tabela_2.item(13, 1)
        ___qtablewidgetitem81.setText(QCoreApplication.translate("Dialog", u"0", None));
        ___qtablewidgetitem82 = self.tabela_2.item(14, 0)
        ___qtablewidgetitem82.setText(QCoreApplication.translate("Dialog", u"Redu\u00e7\u00e3o Gradual", None));
        ___qtablewidgetitem83 = self.tabela_2.item(14, 1)
        ___qtablewidgetitem83.setText(QCoreApplication.translate("Dialog", u"0", None));
        ___qtablewidgetitem84 = self.tabela_2.item(15, 0)
        ___qtablewidgetitem84.setText(QCoreApplication.translate("Dialog", u"Sa\u00edda de Canaliza\u00e7\u00e3o", None));
        ___qtablewidgetitem85 = self.tabela_2.item(15, 1)
        ___qtablewidgetitem85.setText(QCoreApplication.translate("Dialog", u"0", None));
        ___qtablewidgetitem86 = self.tabela_2.item(16, 0)
        ___qtablewidgetitem86.setText(QCoreApplication.translate("Dialog", u"T\u00ea de Passagem directa", None));
        ___qtablewidgetitem87 = self.tabela_2.item(16, 1)
        ___qtablewidgetitem87.setText(QCoreApplication.translate("Dialog", u"0", None));
        ___qtablewidgetitem88 = self.tabela_2.item(17, 0)
        ___qtablewidgetitem88.setText(QCoreApplication.translate("Dialog", u"T\u00ea de saida Bilateral", None));
        ___qtablewidgetitem89 = self.tabela_2.item(17, 1)
        ___qtablewidgetitem89.setText(QCoreApplication.translate("Dialog", u"0", None));
        ___qtablewidgetitem90 = self.tabela_2.item(18, 0)
        ___qtablewidgetitem90.setText(QCoreApplication.translate("Dialog", u"T\u00ea de saida de lado", None));
        ___qtablewidgetitem91 = self.tabela_2.item(18, 1)
        ___qtablewidgetitem91.setText(QCoreApplication.translate("Dialog", u"0", None));
        ___qtablewidgetitem92 = self.tabela_2.item(19, 0)
        ___qtablewidgetitem92.setText(QCoreApplication.translate("Dialog", u"V\u00e1lvula Borboleta", None));
        ___qtablewidgetitem93 = self.tabela_2.item(19, 1)
        ___qtablewidgetitem93.setText(QCoreApplication.translate("Dialog", u"0", None));
        ___qtablewidgetitem94 = self.tabela_2.item(20, 0)
        ___qtablewidgetitem94.setText(QCoreApplication.translate("Dialog", u"V\u00e1lvula de \u00e2ngulo aberta", None));
        ___qtablewidgetitem95 = self.tabela_2.item(20, 1)
        ___qtablewidgetitem95.setText(QCoreApplication.translate("Dialog", u"0", None));
        ___qtablewidgetitem96 = self.tabela_2.item(21, 0)
        ___qtablewidgetitem96.setText(QCoreApplication.translate("Dialog", u"V\u00e1lvula de gaveta aberta", None));
        ___qtablewidgetitem97 = self.tabela_2.item(21, 1)
        ___qtablewidgetitem97.setText(QCoreApplication.translate("Dialog", u"0", None));
        ___qtablewidgetitem98 = self.tabela_2.item(22, 0)
        ___qtablewidgetitem98.setText(QCoreApplication.translate("Dialog", u"V\u00e1lvula de p\u00e9", None));
        ___qtablewidgetitem99 = self.tabela_2.item(22, 1)
        ___qtablewidgetitem99.setText(QCoreApplication.translate("Dialog", u"0", None));
        ___qtablewidgetitem100 = self.tabela_2.item(23, 0)
        ___qtablewidgetitem100.setText(QCoreApplication.translate("Dialog", u"V\u00e1lvula de reten\u00e7\u00e3o", None));
        ___qtablewidgetitem101 = self.tabela_2.item(23, 1)
        ___qtablewidgetitem101.setText(QCoreApplication.translate("Dialog", u"0", None));
        ___qtablewidgetitem102 = self.tabela_2.item(24, 0)
        ___qtablewidgetitem102.setText(QCoreApplication.translate("Dialog", u"V\u00e1lvula globo aberta", None));
        ___qtablewidgetitem103 = self.tabela_2.item(24, 1)
        ___qtablewidgetitem103.setText(QCoreApplication.translate("Dialog", u"0", None));
        self.tabela_2.setSortingEnabled(__sortingEnabled1)

        self.groupBox_5.setTitle(QCoreApplication.translate("Dialog", u"M\u00e9todo perdas de Carga Distribu\u00eddas ", None))
        self.darcy.setText(QCoreApplication.translate("Dialog", u"Darcy-Weiss Bach ", None))
        self.wiliams.setText(QCoreApplication.translate("Dialog", u"Hazen Wiliams", None))
    # retranslateUi

