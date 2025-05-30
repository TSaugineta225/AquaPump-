# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QHBoxLayout,
    QLayout, QLineEdit, QPushButton, QScrollArea,
    QSizePolicy, QSpacerItem, QSplitter, QStackedWidget,
    QVBoxLayout, QWidget)
import gui.img_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(892, 601)
        Form.setStyleSheet(u"/* --------- QLineEdit --------- */\n"
"QLineEdit {\n"
"    background-color: #ffffff;\n"
"    border: 2px solid #b3b3b3;\n"
"    border-radius: 5px;\n"
"    padding: 5px;\n"
"    font-size: 14px;\n"
"    font-family: Roboto;\n"
"    color: #333333;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border: 2px solid #0078d7;\n"
"    background-color: #f0f8ff;\n"
"}\n"
"\n"
"QLineEdit:hover {\n"
"    border: 2px solid #0078d7;\n"
"}\n"
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
"    width: 10p"
                        "x;\n"
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
"")
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.frame = QFrame(Form)
        self.frame.setObjectName(u"frame")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setStyleSheet(u"QPushButton {\n"
"background-color: transparent;\n"
"font-family: Roboto;\n"
"font-size:10pt;\n"
"border: none;\n"
"border-radius:3px\n"
"\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"background-color:	#D9D9D6\n"
"}")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, -1, -1)
        self.arquivo = QPushButton(self.frame)
        self.arquivo.setObjectName(u"arquivo")
        self.arquivo.setMinimumSize(QSize(55, 28))
        self.arquivo.setMaximumSize(QSize(55, 16777215))
        self.arquivo.setStyleSheet(u"")

        self.horizontalLayout.addWidget(self.arquivo)

        self.config = QPushButton(self.frame)
        self.config.setObjectName(u"config")
        self.config.setMinimumSize(QSize(60, 28))
        self.config.setMaximumSize(QSize(87, 16777215))

        self.horizontalLayout.addWidget(self.config)

        self.relatorio = QPushButton(self.frame)
        self.relatorio.setObjectName(u"relatorio")
        self.relatorio.setMinimumSize(QSize(60, 28))
        self.relatorio.setMaximumSize(QSize(60, 16777215))
        self.relatorio.setStyleSheet(u"")

        self.horizontalLayout.addWidget(self.relatorio)

        self.ajuda = QPushButton(self.frame)
        self.ajuda.setObjectName(u"ajuda")
        self.ajuda.setMinimumSize(QSize(45, 28))
        self.ajuda.setMaximumSize(QSize(45, 16777215))

        self.horizontalLayout.addWidget(self.ajuda)


        self.horizontalLayout_3.addWidget(self.frame)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.splitter = QSplitter(Form)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.frame_3 = QFrame(self.splitter)
        self.frame_3.setObjectName(u"frame_3")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy1)
        self.frame_3.setMinimumSize(QSize(0, 0))
        self.frame_3.setMaximumSize(QSize(0, 16777215))
        self.frame_3.setStyleSheet(u"QFrame {\n"
"    background-color: #F9F9F9;\n"
"    border: 1px solid #DDDDDD;\n"
"    border-radius: 6px;\n"
"    padding: 2px;\n"
"	padding-top: 0px;\n"
"}\n"
"\n"
"\n"
"QPushButton {\n"
"background-color: transparent;\n"
"font-family: Roboto;\n"
"font-size:10pt;\n"
"border: none;\n"
"border-radius:3px\n"
"\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"background-color:		#D9D9D6\n"
"}\n"
"\n"
"QLabel {\n"
"font-family: Roboto;\n"
"font-size:10pt;\n"
"\n"
"}\n"
"QDoubleSpinBox {\n"
"    background-color: #FFFFFF;\n"
"    border: 2px solid #CCCCCC;\n"
"    border-radius: 6px;\n"
"    padding: 2px 6px;\n"
"    font-size: 14px;\n"
"    color: #333333;\n"
"}\n"
"\n"
"\n"
"/* --------- QScrollArea --------- */\n"
"QScrollArea {\n"
"    background-color: transparent;\n"
"    border: none;\n"
"}\n"
"\n"
"/* Viewport transparente tamb\u00e9m */\n"
"QScrollArea > QWidget > QWidget {\n"
"    background-color: transparent;\n"
"}\n"
"\n"
"/* --------- Scrollbars --------- */\n"
"QScrollBar:vertical, QScrollBar:horizontal {\n"
""
                        "    background: rgba(0, 0, 0, 0);  /* Transparente */\n"
"    width: 10px;\n"
"    height: 10px;\n"
"    margin: 2px;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical, QScrollBar::handle:horizontal {\n"
"    background-color: #c0c0c0;\n"
"    border-radius: 5px;\n"
"    min-height: 20px;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical:hover, QScrollBar::handle:horizontal:hover {\n"
"    background-color: #a0a0a0;\n"
"}\n"
"\n"
"/* --------- Bot\u00f5es de rolagem --------- */\n"
"QScrollBar::sub-line:vertical, QScrollBar::add-line:vertical,\n"
"QScrollBar::sub-line:horizontal, QScrollBar::add-line:horizontal {\n"
"    background: none;\n"
"    border: none;\n"
"    width: 12px;\n"
"    height: 12px;\n"
"}\n"
"\n"
"QScrollBar::sub-line:vertical {\n"
"    subcontrol-position: top;\n"
"}\n"
"\n"
"QScrollBar::add-line:vertical {\n"
"    subcontrol-position: bottom;\n"
"}\n"
"\n"
"QScrollBar::sub-line:horizontal {\n"
"    subcontrol-position: left;\n"
"}\n"
"\n"
"QScrollBar::add-line:horizontal {\n"
"    subcontrol-position: "
                        "right;\n"
"}\n"
"\n"
"QScrollBar::up-arrow {\n"
"    image: url(:/img/arrow-up.png);\n"
"    width: 8px;\n"
"    height: 8px;\n"
"}\n"
"\n"
"\n"
" QScrollBar::down-arrow {\n"
"    image: url(:/img/arrow-down-1.png);\n"
"    width: 8px;\n"
"    height: 8px;\n"
"}\n"
"\n"
"\n"
"/* --------- Canto entre as barras --------- */\n"
"QScrollBar::corner {\n"
"    background: transparent;\n"
"}\n"
"\n"
"")
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_3)
        self.verticalLayout_2.setSpacing(15)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 3, 0, -1)
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.abrir_layout_2 = QPushButton(self.frame_3)
        self.abrir_layout_2.setObjectName(u"abrir_layout_2")
        self.abrir_layout_2.setStyleSheet(u"QPushButton {\n"
"background-color: transparent;\n"
"font-family: Roboto;\n"
"font-size:10pt;\n"
"border: none;\n"
"border-radius:2px\n"
"\n"
"}\n"
"\n"
"")
        icon = QIcon()
        icon.addFile(u":/img/sidebar-left.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.abrir_layout_2.setIcon(icon)
        self.abrir_layout_2.setIconSize(QSize(26, 26))

        self.horizontalLayout_8.addWidget(self.abrir_layout_2)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_2)

        self.dimensionar_2 = QPushButton(self.frame_3)
        self.dimensionar_2.setObjectName(u"dimensionar_2")
        icon1 = QIcon()
        icon1.addFile(u":/img/scale-3d.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.dimensionar_2.setIcon(icon1)
        self.dimensionar_2.setIconSize(QSize(24, 24))

        self.horizontalLayout_8.addWidget(self.dimensionar_2)

        self.mapa_2 = QPushButton(self.frame_3)
        self.mapa_2.setObjectName(u"mapa_2")
        icon2 = QIcon()
        icon2.addFile(u":/img/mind-map.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.mapa_2.setIcon(icon2)
        self.mapa_2.setIconSize(QSize(24, 24))

        self.horizontalLayout_8.addWidget(self.mapa_2)


        self.verticalLayout_2.addLayout(self.horizontalLayout_8)

        self.scrollArea = QScrollArea(self.frame_3)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 182, 353))
        self.verticalLayout_4 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.pushButton_5 = QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_5.setObjectName(u"pushButton_5")
        self.pushButton_5.setStyleSheet(u"QPushButton {\n"
"	background-color: rgb(240, 240, 240);\n"
"padding: 5px\n"
"}\n"
"QPushButton:hover {\n"
"background-color:		#D9D9D6\n"
"}\n"
"")
        self.pushButton_5.setCheckable(True)

        self.verticalLayout_4.addWidget(self.pushButton_5)

        self.projecto = QFrame(self.scrollAreaWidgetContents)
        self.projecto.setObjectName(u"projecto")
        self.projecto.setMaximumSize(QSize(16777215, 0))
        self.projecto.setStyleSheet(u"QFrame {\n"
"    background-color: #F9F9F9;\n"
"    border: 1px solid rgb(249, 249, 249);\n"
"    border-radius: 6px;\n"
"    padding: 7px;\n"
"	padding-top: 0px;\n"
"}\n"
"QPushButton {\n"
"text-align: left;\n"
"padding: 8px 5px;\n"
"}")
        self.projecto.setFrameShape(QFrame.Shape.StyledPanel)
        self.projecto.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.projecto)
        self.verticalLayout_3.setSpacing(11)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, -1, -1)
        self.novo_arquivo = QPushButton(self.projecto)
        self.novo_arquivo.setObjectName(u"novo_arquivo")
        self.novo_arquivo.setMinimumSize(QSize(0, 36))
        icon3 = QIcon()
        icon3.addFile(u":/img/novo-arquivo.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.novo_arquivo.setIcon(icon3)
        self.novo_arquivo.setIconSize(QSize(16, 16))

        self.verticalLayout_3.addWidget(self.novo_arquivo)

        self.projectos_recentes = QPushButton(self.projecto)
        self.projectos_recentes.setObjectName(u"projectos_recentes")
        self.projectos_recentes.setMinimumSize(QSize(0, 36))
        icon4 = QIcon()
        icon4.addFile(u":/img/recente.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.projectos_recentes.setIcon(icon4)
        self.projectos_recentes.setIconSize(QSize(16, 16))

        self.verticalLayout_3.addWidget(self.projectos_recentes)

        self.salvar_projecto = QPushButton(self.projecto)
        self.salvar_projecto.setObjectName(u"salvar_projecto")
        self.salvar_projecto.setMinimumSize(QSize(0, 36))
        icon5 = QIcon()
        icon5.addFile(u":/img/pasta.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.salvar_projecto.setIcon(icon5)
        self.salvar_projecto.setIconSize(QSize(16, 16))

        self.verticalLayout_3.addWidget(self.salvar_projecto)

        self.abrir_arquivo = QPushButton(self.projecto)
        self.abrir_arquivo.setObjectName(u"abrir_arquivo")
        self.abrir_arquivo.setMinimumSize(QSize(0, 36))
        icon6 = QIcon()
        icon6.addFile(u":/img/pasta (1).png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.abrir_arquivo.setIcon(icon6)
        self.abrir_arquivo.setIconSize(QSize(16, 16))

        self.verticalLayout_3.addWidget(self.abrir_arquivo)


        self.verticalLayout_4.addWidget(self.projecto)

        self.parametros = QPushButton(self.scrollAreaWidgetContents)
        self.parametros.setObjectName(u"parametros")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.parametros.sizePolicy().hasHeightForWidth())
        self.parametros.setSizePolicy(sizePolicy2)
        self.parametros.setMinimumSize(QSize(0, 25))
        self.parametros.setStyleSheet(u"QPushButton {\n"
"	background-color: rgb(240, 240, 240);\n"
"padding: 5px\n"
"}\n"
"QPushButton:hover {\n"
"background-color:		#D9D9D6\n"
"}\n"
"")
        self.parametros.setCheckable(True)

        self.verticalLayout_4.addWidget(self.parametros)

        self.exportar = QFrame(self.scrollAreaWidgetContents)
        self.exportar.setObjectName(u"exportar")
        self.exportar.setMaximumSize(QSize(16777215, 0))
        self.exportar.setStyleSheet(u"QFrame {\n"
"    background-color: #F9F9F9;\n"
"    border: 1px solid rgb(249, 249, 249);\n"
"    border-radius: 6px;\n"
"    padding: 7px;\n"
"	padding-top:0px;\n"
"}\n"
"\n"
"QPushButton {\n"
"text-align: left;\n"
"padding: 8px 5px;\n"
"}")
        self.exportar.setFrameShape(QFrame.Shape.StyledPanel)
        self.exportar.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.exportar)
        self.verticalLayout_6.setSpacing(11)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, -1, 0)
        self.exportar_pdf = QPushButton(self.exportar)
        self.exportar_pdf.setObjectName(u"exportar_pdf")
        self.exportar_pdf.setMinimumSize(QSize(0, 36))
        icon7 = QIcon()
        icon7.addFile(u":/img/pdf.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.exportar_pdf.setIcon(icon7)
        self.exportar_pdf.setIconSize(QSize(16, 16))

        self.verticalLayout_6.addWidget(self.exportar_pdf)

        self.exportar_csv = QPushButton(self.exportar)
        self.exportar_csv.setObjectName(u"exportar_csv")
        self.exportar_csv.setMinimumSize(QSize(0, 36))
        icon8 = QIcon()
        icon8.addFile(u":/img/arquivo-csv.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.exportar_csv.setIcon(icon8)
        self.exportar_csv.setIconSize(QSize(16, 16))

        self.verticalLayout_6.addWidget(self.exportar_csv)


        self.verticalLayout_4.addWidget(self.exportar)

        self.pushButton_3 = QPushButton(self.scrollAreaWidgetContents)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setStyleSheet(u"	QPushButton {\n"
"background-color: rgb(240, 240, 240);\n"
"padding: 5px\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"background-color:		#D9D9D6\n"
"}")
        self.pushButton_3.setCheckable(True)

        self.verticalLayout_4.addWidget(self.pushButton_3)

        self.verticalSpacer = QSpacerItem(20, 225, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_2.addWidget(self.scrollArea)

        self.configuracoes = QPushButton(self.frame_3)
        self.configuracoes.setObjectName(u"configuracoes")
        sizePolicy2.setHeightForWidth(self.configuracoes.sizePolicy().hasHeightForWidth())
        self.configuracoes.setSizePolicy(sizePolicy2)
        self.configuracoes.setMinimumSize(QSize(0, 25))
        self.configuracoes.setStyleSheet(u"QPushButton {\n"
"text-align: left;\n"
"padding: 8px 2px;\n"
"}")
        icon9 = QIcon()
        icon9.addFile(u":/img/settings.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.configuracoes.setIcon(icon9)
        self.configuracoes.setIconSize(QSize(20, 20))

        self.verticalLayout_2.addWidget(self.configuracoes)

        self.sair_2 = QPushButton(self.frame_3)
        self.sair_2.setObjectName(u"sair_2")
        sizePolicy2.setHeightForWidth(self.sair_2.sizePolicy().hasHeightForWidth())
        self.sair_2.setSizePolicy(sizePolicy2)
        self.sair_2.setMinimumSize(QSize(100, 25))
        self.sair_2.setStyleSheet(u"QPushButton {\n"
"text-align: left;\n"
"padding: 8px 2px;\n"
"}")
        icon10 = QIcon()
        icon10.addFile(u":/img/log-out.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.sair_2.setIcon(icon10)
        self.sair_2.setIconSize(QSize(20, 20))

        self.verticalLayout_2.addWidget(self.sair_2)

        self.splitter.addWidget(self.frame_3)
        self.stackedWidget = QStackedWidget(self.splitter)
        self.stackedWidget.setObjectName(u"stackedWidget")
        sizePolicy2.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy2)
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.verticalLayout_5 = QVBoxLayout(self.page)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(11)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.fechar_layout_2 = QPushButton(self.page)
        self.fechar_layout_2.setObjectName(u"fechar_layout_2")
        self.fechar_layout_2.setStyleSheet(u"QPushButton {\n"
"background-color: transparent;\n"
"font-family: Roboto;\n"
"font-size:10pt;\n"
"border: none;\n"
"border-radius:2px\n"
"\n"
"}\n"
"\n"
"")
        self.fechar_layout_2.setIcon(icon)
        self.fechar_layout_2.setIconSize(QSize(26, 26))

        self.horizontalLayout_2.addWidget(self.fechar_layout_2)

        self.comboBox = QComboBox(self.page)
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

        self.horizontalLayout_2.addWidget(self.comboBox)

        self.comboBox_3 = QComboBox(self.page)
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

        self.horizontalLayout_2.addWidget(self.comboBox_3)

        self.lineEdit_2 = QLineEdit(self.page)
        self.lineEdit_2.setObjectName(u"lineEdit_2")

        self.horizontalLayout_2.addWidget(self.lineEdit_2)

        self.lineEdit_3 = QLineEdit(self.page)
        self.lineEdit_3.setObjectName(u"lineEdit_3")

        self.horizontalLayout_2.addWidget(self.lineEdit_3)


        self.verticalLayout_5.addLayout(self.horizontalLayout_2)

        self.widget = QWidget(self.page)
        self.widget.setObjectName(u"widget")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy3)

        self.verticalLayout_5.addWidget(self.widget)

        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.stackedWidget.addWidget(self.page_2)
        self.splitter.addWidget(self.stackedWidget)

        self.horizontalLayout_4.addWidget(self.splitter)


        self.verticalLayout.addLayout(self.horizontalLayout_4)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.arquivo.setText(QCoreApplication.translate("Form", u"Arquivo", None))
        self.config.setText(QCoreApplication.translate("Form", u"Editar", None))
        self.relatorio.setText(QCoreApplication.translate("Form", u"Relat\u00f3rio ", None))
        self.ajuda.setText(QCoreApplication.translate("Form", u"Ajuda", None))
#if QT_CONFIG(tooltip)
        self.abrir_layout_2.setToolTip(QCoreApplication.translate("Form", u"Fechar Barra Lateral", None))
#endif // QT_CONFIG(tooltip)
        self.abrir_layout_2.setText("")
        self.dimensionar_2.setText("")
        self.mapa_2.setText("")
        self.pushButton_5.setText(QCoreApplication.translate("Form", u"Projecto", None))
#if QT_CONFIG(tooltip)
        self.novo_arquivo.setToolTip(QCoreApplication.translate("Form", u"Novo", None))
#endif // QT_CONFIG(tooltip)
        self.novo_arquivo.setText(QCoreApplication.translate("Form", u"Novo Arquivo", None))
#if QT_CONFIG(tooltip)
        self.projectos_recentes.setToolTip(QCoreApplication.translate("Form", u"Projectos Recentes", None))
#endif // QT_CONFIG(tooltip)
        self.projectos_recentes.setText(QCoreApplication.translate("Form", u"Projectos Recentes", None))
#if QT_CONFIG(tooltip)
        self.salvar_projecto.setToolTip(QCoreApplication.translate("Form", u"Salvar Projecto", None))
#endif // QT_CONFIG(tooltip)
        self.salvar_projecto.setText(QCoreApplication.translate("Form", u"Salvar Projecto", None))
#if QT_CONFIG(tooltip)
        self.abrir_arquivo.setToolTip(QCoreApplication.translate("Form", u"Abrir Projecto", None))
#endif // QT_CONFIG(tooltip)
        self.abrir_arquivo.setText(QCoreApplication.translate("Form", u"Abrir Arquivo", None))
        self.parametros.setText(QCoreApplication.translate("Form", u"Exportar", None))
        self.exportar_pdf.setText(QCoreApplication.translate("Form", u"Exportar em PDF", None))
        self.exportar_csv.setText(QCoreApplication.translate("Form", u"Exportar em CSV", None))
        self.pushButton_3.setText(QCoreApplication.translate("Form", u"Relat\u00f3rio ", None))
        self.configuracoes.setText(QCoreApplication.translate("Form", u"Configura\u00e7\u00f5es ", None))
        self.sair_2.setText(QCoreApplication.translate("Form", u"Sair", None))
#if QT_CONFIG(tooltip)
        self.fechar_layout_2.setToolTip(QCoreApplication.translate("Form", u"Fechar Barra Lateral", None))
#endif // QT_CONFIG(tooltip)
        self.fechar_layout_2.setText("")
        self.comboBox.setItemText(0, QCoreApplication.translate("Form", u"A\u00e7o Corrugado(chapa ondulada)", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("Form", u"A\u00e7o Galvanizado", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("Form", u"A\u00e7o Rebitado novo", None))
        self.comboBox.setItemText(3, QCoreApplication.translate("Form", u"A\u00e7o Rebitado em uso", None))
        self.comboBox.setItemText(4, QCoreApplication.translate("Form", u"A\u00e7o soldado novo", None))
        self.comboBox.setItemText(5, QCoreApplication.translate("Form", u"A\u00e7o Soldado em uso", None))
        self.comboBox.setItemText(6, QCoreApplication.translate("Form", u"A\u00e7o Soldado com revestimento especial", None))
        self.comboBox.setItemText(7, QCoreApplication.translate("Form", u"Chumbo", None))
        self.comboBox.setItemText(8, QCoreApplication.translate("Form", u"Cimento Amianto", None))
        self.comboBox.setItemText(9, QCoreApplication.translate("Form", u"Cobre", None))
        self.comboBox.setItemText(10, QCoreApplication.translate("Form", u"Concreto com acabamento comum", None))
        self.comboBox.setItemText(11, QCoreApplication.translate("Form", u"Ferro Fundido novo", None))
        self.comboBox.setItemText(12, QCoreApplication.translate("Form", u"Ferro Fundido de 15 a 20 anos de uso", None))
        self.comboBox.setItemText(13, QCoreApplication.translate("Form", u"Ferro Fundido Usado", None))
        self.comboBox.setItemText(14, QCoreApplication.translate("Form", u"Lat\u00e3o", None))
        self.comboBox.setItemText(15, QCoreApplication.translate("Form", u"Ferro Fundido Revestido de Cimento", None))
        self.comboBox.setItemText(16, QCoreApplication.translate("Form", u"Manilha Cer\u00e2mica vidrada", None))
        self.comboBox.setItemText(17, QCoreApplication.translate("Form", u"Pl\u00e1stico", None))
        self.comboBox.setItemText(18, QCoreApplication.translate("Form", u"Tijolos em executados", None))
        self.comboBox.setItemText(19, QCoreApplication.translate("Form", u"Vidro", None))

        self.comboBox_3.setItemText(0, QCoreApplication.translate("Form", u"PVC", None))
        self.comboBox_3.setItemText(1, QCoreApplication.translate("Form", u"Polietileno", None))
        self.comboBox_3.setItemText(2, QCoreApplication.translate("Form", u"A\u00e7o galvanizado (novo)", None))
        self.comboBox_3.setItemText(3, QCoreApplication.translate("Form", u"Ferro fundido (novo)", None))
        self.comboBox_3.setItemText(4, QCoreApplication.translate("Form", u"Ferro fundido (velho ou corro\u00eddo)", None))
        self.comboBox_3.setItemText(5, QCoreApplication.translate("Form", u"Concreto liso", None))
        self.comboBox_3.setItemText(6, QCoreApplication.translate("Form", u"Concreto rugoso", None))
        self.comboBox_3.setItemText(7, QCoreApplication.translate("Form", u"Madeira lisa", None))
        self.comboBox_3.setItemText(8, QCoreApplication.translate("Form", u"Madeira \u00e1spera", None))
        self.comboBox_3.setItemText(9, QCoreApplication.translate("Form", u"Amianto-cimento", None))
        self.comboBox_3.setItemText(10, QCoreApplication.translate("Form", u"Tubo de chumbo", None))
        self.comboBox_3.setItemText(11, QCoreApplication.translate("Form", u"Tubo de vidro", None))

    # retranslateUi

