# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'config.ui'
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
    QDialogButtonBox, QFrame, QGroupBox, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QPushButton,
    QRadioButton, QScrollArea, QSizePolicy, QSpacerItem,
    QStackedWidget, QTableView, QVBoxLayout, QWidget)
import img.img_rc


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(725, 609)
        Dialog.setStyleSheet(u"QDialog {\n"
"    background-color: #f9f9f9;\n"
"    font-family: \"Segoe UI\", Roboto, sans-serif;\n"
"    font-size: 14px;\n"
"    color: #333333;\n"
"}\n"
"\n"
"QWidget {\n"
"background-color:#f9f9f9}\n"
"\n"
"QPushButton {\n"
"    background-color: #f5f5f5;\n"
"    color: #000000;\n"
"    border: 1px solid #c2c2c2;\n"
"    border-radius: 3px;\n"
"    padding: 6px 12px;\n"
"    font-size: 14px;\n"
"\n"
"\n"
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
"QRadioButton {\n"
"    spacing: 6px;\n"
"    font-family: Segoe UI, Roboto, sans-serif;\n"
"   "
                        " font-size: 14px;\n"
"    color: #333333;\n"
"}\n"
"\n"
"QRadioButton::indicator {\n"
"    width: 16px;\n"
"    height: 16px;\n"
"    border-radius: 8px;\n"
"    border: 2px solid #888888;\n"
"    background-color: #ffffff;\n"
"    transition: all 0.3s;\n"
"}\n"
"\n"
"QRadioButton::indicator:hover {\n"
"    border: 2px solid #555555;\n"
"    background-color: #f0f0f0;\n"
"}\n"
"\n"
"QRadioButton::indicator:checked {\n"
"    border: 2px solid #0078d7;  /* azul suave (cor t\u00edpica de apps profissionais) */\n"
"    background-color: #0078d7;\n"
"}\n"
"\n"
"QRadioButton::indicator:disabled {\n"
"    border: 2px solid #cccccc;\n"
"    background-color: #eeeeee;\n"
"}\n"
"\n"
"QRadioButton::indicator:checked:disabled {\n"
"    border: 2px solid #999999;\n"
"    background-color: #cccccc;\n"
"}\n"
"QRadioButton {\n"
"    spacing: 6px;\n"
"    font-family: Segoe UI, Roboto, sans-serif;\n"
"    font-size: 14px;\n"
"    color: #333333;\n"
"}\n"
"\n"
"QRadioButton::indicator {\n"
"    width: 16px;\n"
"    height: 16px"
                        ";\n"
"    border-radius: 8px;\n"
"    border: 2px solid #888888;\n"
"    background-color: #ffffff;\n"
"    transition: all 0.3s;\n"
"}\n"
"\n"
"QRadioButton::indicator:hover {\n"
"    border: 2px solid #555555;\n"
"    background-color: #f0f0f0;\n"
"}\n"
"\n"
"QRadioButton::indicator:checked {\n"
"    border: 2px solid #0078d7;  /* azul suave (cor t\u00edpica de apps profissionais) */\n"
"    background-color: #0078d7;\n"
"}\n"
"\n"
"QRadioButton::indicator:disabled {\n"
"    border: 2px solid #cccccc;\n"
"    background-color: #eeeeee;\n"
"}\n"
"\n"
"QRadioButton::indicator:checked:disabled {\n"
"    border: 2px solid #999999;\n"
"    background-color: #cccccc;\n"
"}\n"
"\n"
"/* --------- QComboBox --------- */\n"
"QComboBox {\n"
"    background-color: #ffffff;\n"
"    border: 1px solid #c5c5c5;\n"
"    border-radius: 4px;\n"
"    padding: 7px 10px;\n"
"    font-size: 14px;\n"
"    color: #212121;\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"    border: 1px solid #b0b0b0;\n"
"}\n"
"\n"
"QComboBox:focus {\n"
"    bor"
                        "der: 2px solid #0078d7;\n"
"    padding: 6px 9px;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 25px;\n"
"    border-left: 1px solid #c5c5c5;\n"
"    border-top-right-radius: 4px;\n"
"    border-bottom-right-radius: 4px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    image: url(:/img/arrow-down-1.png); \n"
"    width: 12px;\n"
"    height: 12px;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    background-color: #ffffff;\n"
"    border: 1px solid #cfcfcf;\n"
"    border-radius: 4px;\n"
"    selection-background-color: #2684ff;\n"
"    selection-color: #ffffff;\n"
"    font-family: \"Segoe UI\", Roboto, sans-serif;\n"
"}\n"
"\n"
"\n"
"/* --------- QGroupBox --------- */\n"
"QGroupBox {\n"
"    border: 1px solid #dcdcdc;\n"
"    border-radius: 6px;\n"
"    margin-top: 15px;\n"
"    background-color: transparent;\n"
"    font-size: 14px;\n"
"    color: #212121;\n"
"	padding:8px;\n"
"}\n"
"\n"
"QGroupBox::title {\n"
"    subcontr"
                        "ol-origin: margin;\n"
"    subcontrol-position: top left;\n"
"    padding: 0 10px;\n"
"    margin-top: -4px;\n"
"    background-color: transparent;\n"
"    font-family: \"Segoe UI\", \"Roboto\", sans-serif;\n"
"    font-size: 19px;\n"
"    font-weight: bold;\n"
"    color: #000000;\n"
"    \n"
"}\n"
"\n"
"/* --------- QLabel --------- */\n"
"QLabel {\n"
"    color: #333333;\n"
"    font-family: Roboto, sans-serif;\n"
"    font-size: 12px;\n"
"    padding: 2px;\n"
"}\n"
"\n"
"/* --------- QScrollArea --------- */\n"
"QScrollArea {\n"
"    background-color: transparent;\n"
"    border: none;\n"
"    font-family: \"Segoe UI\", Roboto, sans-serif;\n"
"    font-size: 14px;\n"
"    color: #333333;\n"
"}\n"
"\n"
"QScrollArea QWidget {\n"
"    background-color: transparent;\n"
"}\n"
"\n"
"/* --------- ScrollBars --------- */\n"
"QScrollBar:vertical,\n"
"QScrollBar:horizontal {\n"
"    background: rgb(231, 231, 231);\n"
"    width: 12px;\n"
"    height: 12px;\n"
"    margin: 10px 0 10px 0;\n"
"    border: none;\n"
"}\n"
""
                        "\n"
"QScrollBar::sub-page:vertical,\n"
"QScrollBar::add-page:vertical,\n"
"QScrollBar::sub-page:horizontal,\n"
"QScrollBar::add-page:horizontal {\n"
"    background: transparent;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical,\n"
"QScrollBar::handle:horizontal {\n"
"    background-color: #c0c0c0;\n"
"    min-height: 30px;\n"
"    min-width: 30px;\n"
"    margin: 2px;\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical:hover,\n"
"QScrollBar::handle:horizontal:hover {\n"
"    background-color: #a0a0a0;\n"
"}\n"
"\n"
"QScrollBar::sub-line:vertical,\n"
"QScrollBar::add-line:vertical,\n"
"QScrollBar::sub-line:horizontal,\n"
"QScrollBar::add-line:horizontal {\n"
"    background: #e1e1e1;\n"
"    height: 12px;\n"
"    width: 12px;\n"
"    border-radius: 6px;\n"
"}\n"
"\n"
"QScrollBar::up-arrow:vertical {\n"
"    image: url(:/img/arrow-up.png);\n"
"    width: 8px;\n"
"    height: 9px;\n"
"    margin: 2px;\n"
"}\n"
"\n"
"QScrollBar::down-arrow:vertical {\n"
"    image: url(:/img/arrow-down-1.png);\n"
"  "
                        "  width: 8px;\n"
"    height: 9px;\n"
"    margin: 2px;\n"
"}\n"
"\n"
"QRadioButton {\n"
"    spacing: 6px;\n"
"    font-family: Segoe UI, Roboto, sans-serif;\n"
"    font-size: 13px;\n"
"    color: #444444;\n"
"}\n"
"\n"
"QRadioButton::indicator {\n"
"    width: 12px;\n"
"    height: 12px;\n"
"    border-radius: 6px;\n"
"    border: 1.2px solid #aaaaaa;\n"
"    background-color: #f9f9f9;\n"
"}\n"
"\n"
"QRadioButton::indicator:hover {\n"
"    border: 1.2px solid #888888;\n"
"    background-color: #f0f0f0;\n"
"}\n"
"\n"
"QRadioButton::indicator:checked {\n"
"    border: 1.2px solid #4da3ff;        /* Azul mais claro */\n"
"    background-color: #4da3ff;\n"
"}\n"
"\n"
"QRadioButton::indicator:disabled {\n"
"    border: 1.2px solid #dddddd;\n"
"    background-color: #f5f5f5;\n"
"}\n"
"\n"
"QRadioButton::indicator:checked:disabled {\n"
"    border: 1.2px solid #bbbbbb;\n"
"    background-color: #dddddd;\n"
"}\n"
"\n"
"QTableView {\n"
"    background-color: #ffffff;\n"
"    alternate-background-color: #f9f9f9;\n"
""
                        "    gridline-color: #e0e0e0;\n"
"    font-family: Segoe UI, Roboto, sans-serif;\n"
"    font-size: 13px;\n"
"    color: #333333;\n"
"    selection-background-color: #cce4ff;   /* Azul bem claro na sele\u00e7\u00e3o */\n"
"    selection-color: #000000;              /* Texto preto quando selecionado */\n"
"    border: 1px solid #dcdcdc;\n"
"}\n"
"\n"
"QHeaderView::section {\n"
"    background-color: #f1f1f1;\n"
"    padding: 4px;\n"
"    border: 1px solid #dcdcdc;\n"
"    font-weight: bold;\n"
"    color: #444444;\n"
"}\n"
"\n"
"QTableView::item {\n"
"    padding: 4px;\n"
"}\n"
"\n"
"QTableView::item:selected {\n"
"    background-color: #cce4ff;\n"
"    color: #000000;\n"
"}\n"
"\n"
"QTableView QTableCornerButton::section {\n"
"    background-color: #f1f1f1;\n"
"    border: 1px solid #dcdcdc;\n"
"}\n"
"\n"
"QTableView::item:hover {\n"
"    background-color: #eaf4ff;  /* Leve azul ao passar o mouse */\n"
"}\n"
"\n"
"\n"
"")
        self.verticalLayout_2 = QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.geral = QPushButton(self.frame)
        self.geral.setObjectName(u"geral")
        self.geral.setCheckable(True)
        self.geral.setChecked(True)
        self.geral.setAutoExclusive(True)

        self.verticalLayout_3.addWidget(self.geral)

        self.unidades = QPushButton(self.frame)
        self.unidades.setObjectName(u"unidades")
        self.unidades.setCheckable(True)
        self.unidades.setAutoExclusive(True)

        self.verticalLayout_3.addWidget(self.unidades)

        self.pushButton = QPushButton(self.frame)
        self.pushButton.setObjectName(u"pushButton")

        self.verticalLayout_3.addWidget(self.pushButton)

        self.avancado = QPushButton(self.frame)
        self.avancado.setObjectName(u"avancado")
        self.avancado.setCheckable(True)
        self.avancado.setAutoExclusive(True)

        self.verticalLayout_3.addWidget(self.avancado)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)


        self.horizontalLayout.addWidget(self.frame)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setSpacing(0)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.pesquisar_label = QLabel(Dialog)
        self.pesquisar_label.setObjectName(u"pesquisar_label")
        self.pesquisar_label.setMaximumSize(QSize(30, 30))
        self.pesquisar_label.setStyleSheet(u"QLabel {\n"
"    border: 1px solig rgb(238, 238, 238);\n"
"    border-bottom: 2px solid #ccc;\n"
"    padding-left: 2px; \n"
"    height: 24px;\n"
"    font-size: 14px;\n"
"    color: #333;\n"
"    background: rgb(255, 255, 255);\n"
"    image-position: left;\n"
"}")
        self.pesquisar_label.setPixmap(QPixmap(u":/img/pesquisar.png"))
        self.pesquisar_label.setScaledContents(True)

        self.horizontalLayout_15.addWidget(self.pesquisar_label, 0, Qt.AlignmentFlag.AlignRight)

        self.pesquisar = QLineEdit(Dialog)
        self.pesquisar.setObjectName(u"pesquisar")
        self.pesquisar.setMinimumSize(QSize(200, 30))
        self.pesquisar.setMaximumSize(QSize(200, 16777215))
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

        self.horizontalLayout_15.addWidget(self.pesquisar)


        self.verticalLayout.addLayout(self.horizontalLayout_15)

        self.stackedWidget = QStackedWidget(Dialog)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.verticalLayout_4 = QVBoxLayout(self.page)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.page)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"QLabel {\n"
"    font-family: \"Segoe UI\", \"Roboto\", sans-serif;\n"
"    font-size: 15px;\n"
"    font-weight: 600; /* Semi-Bold */\n"
"    color: #000000;\n"
"\n"
"}")

        self.verticalLayout_4.addWidget(self.label)

        self.scrollArea = QScrollArea(self.page)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 540, 1065))
        self.verticalLayout_7 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.groupBox = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_5 = QVBoxLayout(self.groupBox)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setBold(False)
        font.setItalic(True)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet(u"QLabel{\n"
"    font-family: \"Segoe UI\", \"Roboto\", sans-serif;\n"
"    font-size: 14px;\n"
"      font-weight: 400; \n"
"    color: #333333;\n"
"    padding-top: 2px;\n"
"    padding-bottom: 2px;\n"
"}")

        self.verticalLayout_5.addWidget(self.label_2)

        self.line_2 = QFrame(self.groupBox)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_5.addWidget(self.line_2)

        self.radioButton = QRadioButton(self.groupBox)
        self.radioButton.setObjectName(u"radioButton")
        self.radioButton.setChecked(True)

        self.verticalLayout_5.addWidget(self.radioButton)

        self.radioButton_2 = QRadioButton(self.groupBox)
        self.radioButton_2.setObjectName(u"radioButton_2")

        self.verticalLayout_5.addWidget(self.radioButton_2)

        self.radioButton_3 = QRadioButton(self.groupBox)
        self.radioButton_3.setObjectName(u"radioButton_3")

        self.verticalLayout_5.addWidget(self.radioButton_3)


        self.verticalLayout_7.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_6 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.label_7 = QLabel(self.groupBox_2)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMaximumSize(QSize(450, 16777215))
        font1 = QFont()
        font1.setFamilies([u"Segoe UI"])
        font1.setBold(False)
        font1.setItalic(True)
        font1.setStyleStrategy(QFont.PreferAntialias)
        self.label_7.setFont(font1)
        self.label_7.setStyleSheet(u"QLabel{\n"
"    font-family: \"Segoe UI\", \"Roboto\", sans-serif;\n"
"    font-size: 14px;\n"
"      font-weight: 400; \n"
"    color: #333333;\n"
"    padding-top: 2px;\n"
"    padding-bottom: 2px;\n"
"}")

        self.verticalLayout_6.addWidget(self.label_7)

        self.line_3 = QFrame(self.groupBox_2)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_6.addWidget(self.line_3)

        self.comboBox_12 = QComboBox(self.groupBox_2)
        self.comboBox_12.addItem("")
        self.comboBox_12.addItem("")
        self.comboBox_12.addItem("")
        self.comboBox_12.addItem("")
        self.comboBox_12.addItem("")
        self.comboBox_12.addItem("")
        self.comboBox_12.setObjectName(u"comboBox_12")

        self.verticalLayout_6.addWidget(self.comboBox_12)


        self.verticalLayout_7.addWidget(self.groupBox_2)

        self.label_8 = QLabel(self.scrollAreaWidgetContents)
        self.label_8.setObjectName(u"label_8")
        font2 = QFont()
        font2.setFamilies([u"Segoe UI"])
        font2.setWeight(QFont.DemiBold)
        self.label_8.setFont(font2)
        self.label_8.setStyleSheet(u"QLabel {\n"
"    font-family: \"Segoe UI\", \"Roboto\", sans-serif;\n"
"    font-size: 15px;\n"
"    font-weight: 600; /* Semi-Bold */\n"
"    color: #000000;\n"
"\n"
"}\n"
"")

        self.verticalLayout_7.addWidget(self.label_8)

        self.label_3 = QLabel(self.scrollAreaWidgetContents)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font)
        self.label_3.setStyleSheet(u"QLabel{\n"
"    font-family: \"Segoe UI\", \"Roboto\", sans-serif;\n"
"    font-size: 14px;\n"
"      font-weight: 400; \n"
"    color: #333333;\n"
"\n"
"    padding-bottom: 2px;\n"
"}")

        self.verticalLayout_7.addWidget(self.label_3)

        self.groupBox_4 = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.verticalLayout_13 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.caudal = QLabel(self.groupBox_4)
        self.caudal.setObjectName(u"caudal")
        self.caudal.setMaximumSize(QSize(180, 16777215))

        self.horizontalLayout_6.addWidget(self.caudal)

        self.caudal_box = QComboBox(self.groupBox_4)
        self.caudal_box.setObjectName(u"caudal_box")
        self.caudal_box.setMaximumSize(QSize(250, 16777215))

        self.horizontalLayout_6.addWidget(self.caudal_box)


        self.verticalLayout_13.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.altura = QLabel(self.groupBox_4)
        self.altura.setObjectName(u"altura")
        self.altura.setMaximumSize(QSize(180, 16777215))

        self.horizontalLayout_7.addWidget(self.altura)

        self.altura_box = QComboBox(self.groupBox_4)
        self.altura_box.setObjectName(u"altura_box")
        self.altura_box.setMaximumSize(QSize(250, 16777215))

        self.horizontalLayout_7.addWidget(self.altura_box)


        self.verticalLayout_13.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.velocidade = QLabel(self.groupBox_4)
        self.velocidade.setObjectName(u"velocidade")
        self.velocidade.setMaximumSize(QSize(180, 16777215))

        self.horizontalLayout_8.addWidget(self.velocidade)

        self.velocidade_box = QComboBox(self.groupBox_4)
        self.velocidade_box.setObjectName(u"velocidade_box")
        self.velocidade_box.setMaximumSize(QSize(250, 16777215))

        self.horizontalLayout_8.addWidget(self.velocidade_box)


        self.verticalLayout_13.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.npsh = QLabel(self.groupBox_4)
        self.npsh.setObjectName(u"npsh")
        self.npsh.setMaximumSize(QSize(180, 16777215))

        self.horizontalLayout_4.addWidget(self.npsh)

        self.npsh_box = QComboBox(self.groupBox_4)
        self.npsh_box.setObjectName(u"npsh_box")
        self.npsh_box.setMaximumSize(QSize(250, 16777215))

        self.horizontalLayout_4.addWidget(self.npsh_box)


        self.verticalLayout_13.addLayout(self.horizontalLayout_4)


        self.verticalLayout_7.addWidget(self.groupBox_4)

        self.groupBox_3 = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_15 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.densidade = QLabel(self.groupBox_3)
        self.densidade.setObjectName(u"densidade")
        self.densidade.setMaximumSize(QSize(180, 16777215))

        self.horizontalLayout_3.addWidget(self.densidade)

        self.densidade_box = QComboBox(self.groupBox_3)
        self.densidade_box.setObjectName(u"densidade_box")
        self.densidade_box.setMaximumSize(QSize(250, 16777215))

        self.horizontalLayout_3.addWidget(self.densidade_box)


        self.verticalLayout_15.addLayout(self.horizontalLayout_3)


        self.verticalLayout_7.addWidget(self.groupBox_3)

        self.groupBox_6 = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.verticalLayout_16 = QVBoxLayout(self.groupBox_6)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.diametro = QLabel(self.groupBox_6)
        self.diametro.setObjectName(u"diametro")
        self.diametro.setMaximumSize(QSize(180, 16777215))

        self.horizontalLayout_13.addWidget(self.diametro)

        self.diametro_box = QComboBox(self.groupBox_6)
        self.diametro_box.setObjectName(u"diametro_box")
        self.diametro_box.setMaximumSize(QSize(250, 16777215))

        self.horizontalLayout_13.addWidget(self.diametro_box)


        self.verticalLayout_16.addLayout(self.horizontalLayout_13)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.comprimento = QLabel(self.groupBox_6)
        self.comprimento.setObjectName(u"comprimento")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comprimento.sizePolicy().hasHeightForWidth())
        self.comprimento.setSizePolicy(sizePolicy)
        self.comprimento.setMaximumSize(QSize(180, 16777215))

        self.horizontalLayout_14.addWidget(self.comprimento)

        self.comprimento_box = QComboBox(self.groupBox_6)
        self.comprimento_box.setObjectName(u"comprimento_box")
        self.comprimento_box.setMaximumSize(QSize(250, 16777215))

        self.horizontalLayout_14.addWidget(self.comprimento_box)


        self.verticalLayout_16.addLayout(self.horizontalLayout_14)


        self.verticalLayout_7.addWidget(self.groupBox_6)

        self.groupBox_5 = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.verticalLayout_10 = QVBoxLayout(self.groupBox_5)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.pressao = QLabel(self.groupBox_5)
        self.pressao.setObjectName(u"pressao")
        self.pressao.setMaximumSize(QSize(180, 16777215))

        self.horizontalLayout_11.addWidget(self.pressao)

        self.pressao_box = QComboBox(self.groupBox_5)
        self.pressao_box.setObjectName(u"pressao_box")
        self.pressao_box.setMaximumSize(QSize(250, 16777215))

        self.horizontalLayout_11.addWidget(self.pressao_box)


        self.verticalLayout_10.addLayout(self.horizontalLayout_11)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.potencia = QLabel(self.groupBox_5)
        self.potencia.setObjectName(u"potencia")
        self.potencia.setMaximumSize(QSize(180, 16777215))

        self.horizontalLayout_12.addWidget(self.potencia)

        self.potencia_box = QComboBox(self.groupBox_5)
        self.potencia_box.setObjectName(u"potencia_box")
        self.potencia_box.setMaximumSize(QSize(250, 16777215))

        self.horizontalLayout_12.addWidget(self.potencia_box)


        self.verticalLayout_10.addLayout(self.horizontalLayout_12)


        self.verticalLayout_7.addWidget(self.groupBox_5)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_4.addWidget(self.scrollArea)

        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.verticalLayout_8 = QVBoxLayout(self.page_2)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.label_5 = QLabel(self.page_2)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setStyleSheet(u"QLabel {\n"
"    font-family: \"Segoe UI\", \"Roboto\", sans-serif;\n"
"    font-size: 15px;\n"
"    font-weight: 600; /* Semi-Bold */\n"
"    color: #000000;\n"
"\n"
"}")

        self.verticalLayout_8.addWidget(self.label_5)

        self.groupBox_8 = QGroupBox(self.page_2)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.verticalLayout_11 = QVBoxLayout(self.groupBox_8)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.label_6 = QLabel(self.groupBox_8)
        self.label_6.setObjectName(u"label_6")

        self.verticalLayout_11.addWidget(self.label_6)

        self.comboBox_5 = QComboBox(self.groupBox_8)
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.comboBox_5.setObjectName(u"comboBox_5")

        self.verticalLayout_11.addWidget(self.comboBox_5)

        self.label_9 = QLabel(self.groupBox_8)
        self.label_9.setObjectName(u"label_9")

        self.verticalLayout_11.addWidget(self.label_9)

        self.comboBox_6 = QComboBox(self.groupBox_8)
        self.comboBox_6.addItem("")
        self.comboBox_6.addItem("")
        self.comboBox_6.setObjectName(u"comboBox_6")

        self.verticalLayout_11.addWidget(self.comboBox_6)


        self.verticalLayout_8.addWidget(self.groupBox_8)

        self.groupBox_7 = QGroupBox(self.page_2)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.verticalLayout_9 = QVBoxLayout(self.groupBox_7)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.radioButton_4 = QRadioButton(self.groupBox_7)
        self.radioButton_4.setObjectName(u"radioButton_4")

        self.verticalLayout_9.addWidget(self.radioButton_4)

        self.radioButton_6 = QRadioButton(self.groupBox_7)
        self.radioButton_6.setObjectName(u"radioButton_6")

        self.verticalLayout_9.addWidget(self.radioButton_6)

        self.radioButton_5 = QRadioButton(self.groupBox_7)
        self.radioButton_5.setObjectName(u"radioButton_5")

        self.verticalLayout_9.addWidget(self.radioButton_5)


        self.verticalLayout_8.addWidget(self.groupBox_7)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_8.addItem(self.verticalSpacer_2)

        self.stackedWidget.addWidget(self.page_2)
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.verticalLayout_14 = QVBoxLayout(self.page_3)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.label_4 = QLabel(self.page_3)
        self.label_4.setObjectName(u"label_4")
        font3 = QFont()
        font3.setFamilies([u"Roboto"])
        font3.setBold(True)
        self.label_4.setFont(font3)

        self.verticalLayout_14.addWidget(self.label_4)

        self.groupBox_10 = QGroupBox(self.page_3)
        self.groupBox_10.setObjectName(u"groupBox_10")
        self.verticalLayout_17 = QVBoxLayout(self.groupBox_10)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.radioButton_7 = QRadioButton(self.groupBox_10)
        self.radioButton_7.setObjectName(u"radioButton_7")
        self.radioButton_7.setChecked(True)

        self.verticalLayout_17.addWidget(self.radioButton_7)

        self.radioButton_8 = QRadioButton(self.groupBox_10)
        self.radioButton_8.setObjectName(u"radioButton_8")

        self.verticalLayout_17.addWidget(self.radioButton_8)


        self.verticalLayout_14.addWidget(self.groupBox_10)

        self.groupBox_9 = QGroupBox(self.page_3)
        self.groupBox_9.setObjectName(u"groupBox_9")
        self.verticalLayout_12 = QVBoxLayout(self.groupBox_9)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.label_10 = QLabel(self.groupBox_9)
        self.label_10.setObjectName(u"label_10")

        self.verticalLayout_12.addWidget(self.label_10)

        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.pushButton_4 = QPushButton(self.groupBox_9)
        self.pushButton_4.setObjectName(u"pushButton_4")

        self.horizontalLayout_16.addWidget(self.pushButton_4)

        self.lineEdit = QLineEdit(self.groupBox_9)
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

        self.horizontalLayout_16.addWidget(self.lineEdit)


        self.verticalLayout_12.addLayout(self.horizontalLayout_16)


        self.verticalLayout_14.addWidget(self.groupBox_9)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_14.addItem(self.verticalSpacer_3)

        self.stackedWidget.addWidget(self.page_3)
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.verticalLayout_18 = QVBoxLayout(self.page_4)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.verticalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.groupBox_11 = QGroupBox(self.page_4)
        self.groupBox_11.setObjectName(u"groupBox_11")
        self.verticalLayout_20 = QVBoxLayout(self.groupBox_11)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.verticalLayout_20.setContentsMargins(-1, 0, -1, 0)
        self.gerente_material = QTableView(self.groupBox_11)
        self.gerente_material.setObjectName(u"gerente_material")

        self.verticalLayout_20.addWidget(self.gerente_material)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.adicionar_2 = QPushButton(self.groupBox_11)
        self.adicionar_2.setObjectName(u"adicionar_2")

        self.horizontalLayout_2.addWidget(self.adicionar_2)

        self.remover_2 = QPushButton(self.groupBox_11)
        self.remover_2.setObjectName(u"remover_2")

        self.horizontalLayout_2.addWidget(self.remover_2)

        self.editar_2 = QPushButton(self.groupBox_11)
        self.editar_2.setObjectName(u"editar_2")

        self.horizontalLayout_2.addWidget(self.editar_2)

        self.salvar_2 = QPushButton(self.groupBox_11)
        self.salvar_2.setObjectName(u"salvar_2")

        self.horizontalLayout_2.addWidget(self.salvar_2)


        self.verticalLayout_20.addLayout(self.horizontalLayout_2)


        self.verticalLayout_18.addWidget(self.groupBox_11)

        self.groupBox_12 = QGroupBox(self.page_4)
        self.groupBox_12.setObjectName(u"groupBox_12")
        self.verticalLayout_19 = QVBoxLayout(self.groupBox_12)
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.verticalLayout_19.setContentsMargins(-1, 0, -1, 0)
        self.gerente_acessorio = QTableView(self.groupBox_12)
        self.gerente_acessorio.setObjectName(u"gerente_acessorio")

        self.verticalLayout_19.addWidget(self.gerente_acessorio)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.adicionar = QPushButton(self.groupBox_12)
        self.adicionar.setObjectName(u"adicionar")

        self.horizontalLayout_5.addWidget(self.adicionar)

        self.remover = QPushButton(self.groupBox_12)
        self.remover.setObjectName(u"remover")

        self.horizontalLayout_5.addWidget(self.remover)

        self.editar = QPushButton(self.groupBox_12)
        self.editar.setObjectName(u"editar")

        self.horizontalLayout_5.addWidget(self.editar)

        self.salvar = QPushButton(self.groupBox_12)
        self.salvar.setObjectName(u"salvar")

        self.horizontalLayout_5.addWidget(self.salvar)


        self.verticalLayout_19.addLayout(self.horizontalLayout_5)


        self.verticalLayout_18.addWidget(self.groupBox_12)

        self.stackedWidget.addWidget(self.page_4)

        self.verticalLayout.addWidget(self.stackedWidget)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Apply|QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok|QDialogButtonBox.StandardButton.Reset)

        self.verticalLayout_2.addWidget(self.buttonBox)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        self.stackedWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.geral.setText(QCoreApplication.translate("Dialog", u"Geral", None))
        self.unidades.setText(QCoreApplication.translate("Dialog", u"Unidades", None))
        self.pushButton.setText(QCoreApplication.translate("Dialog", u"Banco de Dados", None))
        self.avancado.setText(QCoreApplication.translate("Dialog", u"Avan\u00e7ado ", None))
        self.pesquisar_label.setText("")
        self.pesquisar.setPlaceholderText(QCoreApplication.translate("Dialog", u"Pesquisar", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Unidades", None))
        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"Padr\u00e3o de Unidades Preferencial", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Escolha entre os sistemas de unidades M\u00e9trico (SI) ou Imperial (EUA) \n"
"para configurar todas as suas prefer\u00eancias de uma vez. ", None))
        self.radioButton.setText(QCoreApplication.translate("Dialog", u"Sistema Internacional (SI / M\u00e9trico)", None))
        self.radioButton_2.setText(QCoreApplication.translate("Dialog", u"Sistema Imperial (EUA)", None))
        self.radioButton_3.setText(QCoreApplication.translate("Dialog", u"Personalizado", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Dialog", u"Precis\u00e3o (casas decimais)", None))
        self.label_7.setText(QCoreApplication.translate("Dialog", u"\n"
"Define o n\u00famero de casas decimais a serem exibidas nos c\u00e1lculos \n"
"e resultados.", None))
        self.comboBox_12.setItemText(0, QCoreApplication.translate("Dialog", u"0.00", None))
        self.comboBox_12.setItemText(1, QCoreApplication.translate("Dialog", u"0.0", None))
        self.comboBox_12.setItemText(2, QCoreApplication.translate("Dialog", u"0.000", None))
        self.comboBox_12.setItemText(3, QCoreApplication.translate("Dialog", u"0.0000", None))
        self.comboBox_12.setItemText(4, QCoreApplication.translate("Dialog", u"0.00000", None))
        self.comboBox_12.setItemText(5, QCoreApplication.translate("Dialog", u"0.000000", None))

        self.label_8.setText(QCoreApplication.translate("Dialog", u"Personaliza\u00e7\u00e3o de unidades", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"\n"
"Ajuste individualmente as unidades para cada par\u00e2metro \n"
"(ex: Caudal, Press\u00e3o, Di\u00e2metro).", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("Dialog", u"Desempenho", None))
        self.caudal.setText(QCoreApplication.translate("Dialog", u"Caudal", None))
        self.altura.setText(QCoreApplication.translate("Dialog", u"Altura Man\u00f4metrica", None))
        self.velocidade.setText(QCoreApplication.translate("Dialog", u"Velocidade de Rota\u00e7\u00e3o", None))
        self.npsh.setText(QCoreApplication.translate("Dialog", u"NPSH", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Dialog", u"Fluido", None))
        self.densidade.setText(QCoreApplication.translate("Dialog", u"Densidade", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("Dialog", u"Dimens\u00f5es F\u00edsicas", None))
        self.diametro.setText(QCoreApplication.translate("Dialog", u"Di\u00e2metro da Tubagem", None))
        self.comprimento.setText(QCoreApplication.translate("Dialog", u"Comprimento da Tubagem", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("Dialog", u"Press\u00e3o e Pot\u00eancia ", None))
        self.pressao.setText(QCoreApplication.translate("Dialog", u"Press\u00e3o", None))
        self.potencia.setText(QCoreApplication.translate("Dialog", u"Pot\u00eancia", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"Geral", None))
        self.groupBox_8.setTitle("")
        self.label_6.setText(QCoreApplication.translate("Dialog", u"Apar\u00eancia ", None))
        self.comboBox_5.setItemText(0, QCoreApplication.translate("Dialog", u"Predefini\u00e7\u00e3o do Sistema", None))
        self.comboBox_5.setItemText(1, QCoreApplication.translate("Dialog", u"Claro", None))
        self.comboBox_5.setItemText(2, QCoreApplication.translate("Dialog", u"Escuro", None))

        self.label_9.setText(QCoreApplication.translate("Dialog", u"Idioma", None))
        self.comboBox_6.setItemText(0, QCoreApplication.translate("Dialog", u"Portugu\u00eas", None))
        self.comboBox_6.setItemText(1, QCoreApplication.translate("Dialog", u"Ingl\u00eas", None))

        self.groupBox_7.setTitle(QCoreApplication.translate("Dialog", u"Modo  Gr\u00e1fico", None))
        self.radioButton_4.setText(QCoreApplication.translate("Dialog", u"Padr\u00e3o ", None))
        self.radioButton_6.setText(QCoreApplication.translate("Dialog", u"Open GL", None))
        self.radioButton_5.setText(QCoreApplication.translate("Dialog", u"DirectX", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Avan\u00e7ado ", None))
        self.groupBox_10.setTitle(QCoreApplication.translate("Dialog", u"F\u00f3rmulas Pr\u00e9-definidas/ Perdas de Carga", None))
        self.radioButton_7.setText(QCoreApplication.translate("Dialog", u"Hazen Williams", None))
        self.radioButton_8.setText(QCoreApplication.translate("Dialog", u"Darcy", None))
        self.groupBox_9.setTitle("")
        self.label_10.setText(QCoreApplication.translate("Dialog", u"Caminho para Salvar Arquivos", None))
        self.pushButton_4.setText(QCoreApplication.translate("Dialog", u"Escolha", None))
        self.groupBox_11.setTitle(QCoreApplication.translate("Dialog", u"Gerenciar Materiais de Tubula\u00e7\u00e3o", None))
        self.adicionar_2.setText(QCoreApplication.translate("Dialog", u"Adicionar Novo", None))
        self.remover_2.setText(QCoreApplication.translate("Dialog", u"Remover Selecionado", None))
        self.editar_2.setText(QCoreApplication.translate("Dialog", u"Editar", None))
        self.salvar_2.setText(QCoreApplication.translate("Dialog", u"Salvar", None))
        self.groupBox_12.setTitle(QCoreApplication.translate("Dialog", u"Gerenciar Materiais de Acess\u00f3rios ", None))
        self.adicionar.setText(QCoreApplication.translate("Dialog", u"Adicionar Novo", None))
        self.remover.setText(QCoreApplication.translate("Dialog", u"Remover Selecionado", None))
        self.editar.setText(QCoreApplication.translate("Dialog", u"Editar", None))
        self.salvar.setText(QCoreApplication.translate("Dialog", u"Salvar", None))
    # retranslateUi

