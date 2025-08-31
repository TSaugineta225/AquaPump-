# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainRpkcLI.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
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
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QComboBox, QFrame,
    QGroupBox, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QPushButton, QRadioButton, QScrollArea,
    QSizePolicy, QSpacerItem, QSplitter, QStackedWidget,
    QTableView, QToolButton, QVBoxLayout, QWidget)
from PySide6.QtWebEngineWidgets import QWebEngineView
import img.img_rc

class Ui_AquaPump(object):
    def setupUi(self, AquaPump):
        if not AquaPump.objectName():
            AquaPump.setObjectName(u"AquaPump")
        AquaPump.resize(1165, 749)
        self.view = QWebEngineView(self)
        AquaPump.setStyleSheet(u"")
        self.layoutWidget = QWidget(AquaPump)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(0, 0, 100, 30))
        self.verticalLayout_12 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8 = QVBoxLayout(AquaPump)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.frame_2 = QFrame(AquaPump)
        self.frame_2.setObjectName(u"frame_2")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setStyleSheet(u"QPushButton {\n"
"background-color: transparent;\n"
"font-family: Roboto;\n"
"font-size:10pt;\n"
"border: none;\n"
"border-radius:3px;\n"
"padding:0px\n"
"\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"background-color:	#D9D9D6\n"
"}")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, -1, -1)
        self.arquivo_2 = QPushButton(self.frame_2)
        self.arquivo_2.setObjectName(u"arquivo_2")
        self.arquivo_2.setMinimumSize(QSize(55, 28))
        self.arquivo_2.setMaximumSize(QSize(55, 16777215))
        self.arquivo_2.setStyleSheet(u"")

        self.horizontalLayout_2.addWidget(self.arquivo_2)

        self.config_2 = QPushButton(self.frame_2)
        self.config_2.setObjectName(u"config_2")
        self.config_2.setMinimumSize(QSize(60, 28))
        self.config_2.setMaximumSize(QSize(87, 16777215))

        self.horizontalLayout_2.addWidget(self.config_2)

        self.relatorio_2 = QPushButton(self.frame_2)
        self.relatorio_2.setObjectName(u"relatorio_2")
        self.relatorio_2.setMinimumSize(QSize(60, 28))
        self.relatorio_2.setMaximumSize(QSize(60, 16777215))
        self.relatorio_2.setStyleSheet(u"")

        self.horizontalLayout_2.addWidget(self.relatorio_2)

        self.ajuda_2 = QPushButton(self.frame_2)
        self.ajuda_2.setObjectName(u"ajuda_2")
        self.ajuda_2.setMinimumSize(QSize(45, 28))
        self.ajuda_2.setMaximumSize(QSize(45, 16777215))

        self.horizontalLayout_2.addWidget(self.ajuda_2)


        self.horizontalLayout_4.addWidget(self.frame_2)

        self.horizontalSpacer_2 = QSpacerItem(40, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)


        self.verticalLayout_8.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.frame_4 = QFrame(AquaPump)
        self.frame_4.setObjectName(u"frame_4")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.frame_4.sizePolicy().hasHeightForWidth())
        self.frame_4.setSizePolicy(sizePolicy1)
        self.frame_4.setMinimumSize(QSize(0, 0))
        self.frame_4.setMaximumSize(QSize(0, 16777215))
        self.frame_4.setStyleSheet(u"QFrame {\n"
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
        self.frame_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_4)
        self.verticalLayout_2.setSpacing(15)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 3, 0, -1)
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.abrir_layout_2 = QPushButton(self.frame_4)
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
        icon.addFile(u":/img/left_panel_close_67dp_999999_FILL1_wght400_GRAD0_opsz48.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.abrir_layout_2.setIcon(icon)
        self.abrir_layout_2.setIconSize(QSize(26, 26))

        self.horizontalLayout_8.addWidget(self.abrir_layout_2)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_3)


        self.verticalLayout_2.addLayout(self.horizontalLayout_8)

        self.frame_3 = QFrame(self.frame_4)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setStyleSheet(u"QFrame {\n"
"background-color:transparent;\n"
"border:none\n"
"\n"
"}")
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pesquisa_line = QLineEdit(self.frame_3)
        self.pesquisa_line.setObjectName(u"pesquisa_line")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.pesquisa_line.sizePolicy().hasHeightForWidth())
        self.pesquisa_line.setSizePolicy(sizePolicy2)
        self.pesquisa_line.setMinimumSize(QSize(0, 30))
        self.pesquisa_line.setMaximumSize(QSize(500, 30))
        self.pesquisa_line.setStyleSheet(u"QLineEdit {\n"
"    border-top-left-radius: 4px;\n"
"    border-bottom-left-radius: 4px;\n"
"    border-top-right-radius: 0px;\n"
"    border-bottom-right-radius: 0px;\n"
"	border-right: 0px solid #d0d0d0;\n"
"	font-size: 14px;\n"
"padding:0px;\n"
"\n"
"}\n"
"")

        self.horizontalLayout_3.addWidget(self.pesquisa_line)

        self.pesquisar_2 = QPushButton(self.frame_3)
        self.pesquisar_2.setObjectName(u"pesquisar_2")
        self.pesquisar_2.setMaximumSize(QSize(32, 30))
        self.pesquisar_2.setStyleSheet(u"QPushButton {\n"
"    border-top: 2px solid #d0d0d0;\n"
"    border-top-left-radius: 0px;\n"
"    border-bottom-left-radius: 0px;\n"
"    border-top-right-radius: 4px;\n"
"    border-bottom-right-radius: 4px;\n"
"border-left:1px solid #d0d0d0;\n"
" border-bottom: 2px solid #d0d0d0;\n"
" border-right: 2px solid #d0d0d0;\n"
"\n"
"}\n"
"")
        icon1 = QIcon()
        icon1.addFile(u":/img/search.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pesquisar_2.setIcon(icon1)
        self.pesquisar_2.setIconSize(QSize(25, 20))

        self.horizontalLayout_3.addWidget(self.pesquisar_2)


        self.verticalLayout_2.addWidget(self.frame_3)

        self.scrollArea = QScrollArea(self.frame_4)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setStyleSheet(u"/* --------- QPushButton --------- */\n"
"QPushButton {\n"
"    color: #000000;\n"
"    border: none;\n"
"    border-radius: 3px;\n"
"    padding: 6px 12px;\n"
"    font-size: 14px;\n"
"    font-family: Roboto;\n"
"	background-color: rgb(240, 240, 240);\n"
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
"    background-color: rgb(220, 220, 220);\n"
"}\n"
"")
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 177, 405))
        self.verticalLayout_4 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.projecto_2 = QPushButton(self.scrollAreaWidgetContents)
        self.projecto_2.setObjectName(u"projecto_2")
        self.projecto_2.setStyleSheet(u"")
        self.projecto_2.setCheckable(True)
        self.projecto_2.setAutoDefault(True)
        self.projecto_2.setFlat(True)

        self.verticalLayout_4.addWidget(self.projecto_2)

        self.projecto = QFrame(self.scrollAreaWidgetContents)
        self.projecto.setObjectName(u"projecto")
        self.projecto.setMaximumSize(QSize(16777215, 0))
        self.projecto.setStyleSheet(u"QFrame {\n"
"    background-color: transparent;\n"
"    border: none;\n"
"    border-radius: 6px;\n"
"    padding: 7px;\n"
"	padding-top: 0px;\n"
"}\n"
"QPushButton {\n"
"text-align: left;\n"
"padding: 8px 5px;\n"
"}\n"
"\n"
"QFrame {\n"
"    background-color: transparent;\n"
"    border: 1px solid rgb(249, 249, 249);\n"
"    border-radius: 6px;\n"
"    padding: 7px;\n"
"	padding-top:0px;\n"
"}\n"
"\n"
"/* --------- QPushButton --------- */\n"
"QPushButton {\n"
"    background-color: transparent;\n"
"    color: #000000;\n"
"    border: none;\n"
"    border-radius: 3px;\n"
"    padding: 6px 12px;\n"
"    font-size: 12px;\n"
"    font-family: Roboto;\n"
"	text-align: left;\n"
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
"")
        self.projecto.setFrameShape(QFrame.Shape.StyledPanel)
        self.projecto.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.projecto)
        self.verticalLayout_3.setSpacing(11)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, -1, -1)
        self.novo_arquivo = QPushButton(self.projecto)
        self.novo_arquivo.setObjectName(u"novo_arquivo")
        self.novo_arquivo.setMinimumSize(QSize(0, 0))
        icon2 = QIcon()
        icon2.addFile(u":/img/novo-arquivo.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.novo_arquivo.setIcon(icon2)
        self.novo_arquivo.setIconSize(QSize(16, 16))

        self.verticalLayout_3.addWidget(self.novo_arquivo)

        self.salvar_projecto = QPushButton(self.projecto)
        self.salvar_projecto.setObjectName(u"salvar_projecto")
        self.salvar_projecto.setMinimumSize(QSize(0, 0))
        icon3 = QIcon()
        icon3.addFile(u":/img/pasta.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.salvar_projecto.setIcon(icon3)
        self.salvar_projecto.setIconSize(QSize(16, 16))

        self.verticalLayout_3.addWidget(self.salvar_projecto)

        self.abrir_arquivo = QPushButton(self.projecto)
        self.abrir_arquivo.setObjectName(u"abrir_arquivo")
        self.abrir_arquivo.setMinimumSize(QSize(0, 0))
        icon4 = QIcon()
        icon4.addFile(u":/img/pasta (1).png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.abrir_arquivo.setIcon(icon4)
        self.abrir_arquivo.setIconSize(QSize(16, 16))

        self.verticalLayout_3.addWidget(self.abrir_arquivo)

        self.line = QFrame(self.projecto)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_3.addWidget(self.line)


        self.verticalLayout_4.addWidget(self.projecto)

        self.parametros = QPushButton(self.scrollAreaWidgetContents)
        self.parametros.setObjectName(u"parametros")
        sizePolicy2.setHeightForWidth(self.parametros.sizePolicy().hasHeightForWidth())
        self.parametros.setSizePolicy(sizePolicy2)
        self.parametros.setMinimumSize(QSize(0, 0))
        self.parametros.setStyleSheet(u"")
        self.parametros.setCheckable(True)

        self.verticalLayout_4.addWidget(self.parametros)

        self.exportar = QFrame(self.scrollAreaWidgetContents)
        self.exportar.setObjectName(u"exportar")
        self.exportar.setMaximumSize(QSize(16777215, 0))
        self.exportar.setStyleSheet(u"QFrame {\n"
"    background-color: transparent;\n"
"    border: 1px solid rgb(249, 249, 249);\n"
"    border-radius: 6px;\n"
"    padding: 7px;\n"
"	padding-top:0px;\n"
"}\n"
"\n"
"QPushButton {\n"
"text-align: left;\n"
"padding: 8px 5px;\n"
"}\n"
"/* --------- QPushButton --------- */\n"
"QPushButton {\n"
"    background-color: transparent;\n"
"    color: #000000;\n"
"    border: none;\n"
"    border-radius: 3px;\n"
"    padding: 6px 12px;\n"
"    font-size: 12px;\n"
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
"")
        self.exportar.setFrameShape(QFrame.Shape.StyledPanel)
        self.exportar.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.exportar)
        self.verticalLayout_6.setSpacing(11)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, -1, 0)
        self.exportar_pdf = QPushButton(self.exportar)
        self.exportar_pdf.setObjectName(u"exportar_pdf")
        self.exportar_pdf.setMinimumSize(QSize(0, 36))
        icon5 = QIcon()
        icon5.addFile(u":/img/pdf.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.exportar_pdf.setIcon(icon5)
        self.exportar_pdf.setIconSize(QSize(16, 16))

        self.verticalLayout_6.addWidget(self.exportar_pdf)

        self.exportar_csv = QPushButton(self.exportar)
        self.exportar_csv.setObjectName(u"exportar_csv")
        self.exportar_csv.setMinimumSize(QSize(0, 36))
        icon6 = QIcon()
        icon6.addFile(u":/img/arquivo-csv.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.exportar_csv.setIcon(icon6)
        self.exportar_csv.setIconSize(QSize(16, 16))

        self.verticalLayout_6.addWidget(self.exportar_csv)


        self.verticalLayout_4.addWidget(self.exportar)

        self.rel = QPushButton(self.scrollAreaWidgetContents)
        self.rel.setObjectName(u"rel")
        self.rel.setStyleSheet(u"")
        self.rel.setCheckable(True)

        self.verticalLayout_4.addWidget(self.rel)

        self.grafico = QPushButton(self.scrollAreaWidgetContents)
        self.grafico.setObjectName(u"grafico")

        self.verticalLayout_4.addWidget(self.grafico)

        self.verticalSpacer = QSpacerItem(20, 225, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_2.addWidget(self.scrollArea)

        self.pushButton_3 = QPushButton(self.frame_4)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setStyleSheet(u"QPushButton {\n"
"text-align: left;\n"
"padding: 8px 2px;\n"
"}\n"
"\n"
"QPushButton {\n"
"    background-color: transparent;\n"
"    color: #000000;\n"
"    border: none;\n"
"    border-radius: 3px;\n"
"    padding: 6px 12px;\n"
"    font-size: 14px;\n"
"    font-family: Roboto;\n"
"	text-align: left;\n"
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
"")
        icon7 = QIcon()
        icon7.addFile(u":/img/star.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_3.setIcon(icon7)
        self.pushButton_3.setIconSize(QSize(20, 20))

        self.verticalLayout_2.addWidget(self.pushButton_3)

        self.configuracoes = QPushButton(self.frame_4)
        self.configuracoes.setObjectName(u"configuracoes")
        sizePolicy2.setHeightForWidth(self.configuracoes.sizePolicy().hasHeightForWidth())
        self.configuracoes.setSizePolicy(sizePolicy2)
        self.configuracoes.setMinimumSize(QSize(0, 25))
        self.configuracoes.setStyleSheet(u"QPushButton {\n"
"text-align: left;\n"
"padding: 8px 2px;\n"
"}\n"
"\n"
"QPushButton {\n"
"    background-color: transparent;\n"
"    color: #000000;\n"
"    border: none;\n"
"    border-radius: 3px;\n"
"    padding: 6px 12px;\n"
"    font-size: 14px;\n"
"    font-family: Roboto;\n"
"	text-align: left;\n"
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
"")
        icon8 = QIcon()
        icon8.addFile(u":/img/settings_67dp_999999_FILL1_wght400_GRAD0_opsz48.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.configuracoes.setIcon(icon8)
        self.configuracoes.setIconSize(QSize(20, 20))

        self.verticalLayout_2.addWidget(self.configuracoes)

        self.sair_2 = QPushButton(self.frame_4)
        self.sair_2.setObjectName(u"sair_2")
        sizePolicy2.setHeightForWidth(self.sair_2.sizePolicy().hasHeightForWidth())
        self.sair_2.setSizePolicy(sizePolicy2)
        self.sair_2.setMinimumSize(QSize(100, 25))
        self.sair_2.setStyleSheet(u"QPushButton {\n"
"text-align: left;\n"
"padding: 8px 2px;\n"
"}\n"
"\n"
"QPushButton {\n"
"    background-color: transparent;\n"
"    color: #000000;\n"
"    border: none;\n"
"    border-radius: 3px;\n"
"    padding: 6px 12px;\n"
"    font-size: 14px;\n"
"    font-family: Roboto;\n"
"	text-align: left;\n"
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
"")
        icon9 = QIcon()
        icon9.addFile(u":/img/sair.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.sair_2.setIcon(icon9)
        self.sair_2.setIconSize(QSize(20, 20))

        self.verticalLayout_2.addWidget(self.sair_2)


        self.horizontalLayout_5.addWidget(self.frame_4)

        self.frame_6 = QFrame(AquaPump)
        self.frame_6.setObjectName(u"frame_6")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.frame_6.sizePolicy().hasHeightForWidth())
        self.frame_6.setSizePolicy(sizePolicy3)
        self.frame_6.setMinimumSize(QSize(0, 0))
        self.frame_6.setMaximumSize(QSize(50, 16777215))
        self.frame_6.setStyleSheet(u"QFrame {\n"
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
        self.frame_6.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame_6)
        self.verticalLayout_5.setSpacing(15)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 3, 0, -1)
        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.abrir_layout_3 = QPushButton(self.frame_6)
        self.abrir_layout_3.setObjectName(u"abrir_layout_3")
        self.abrir_layout_3.setStyleSheet(u"QPushButton {\n"
"background-color: transparent;\n"
"font-family: Roboto;\n"
"font-size:10pt;\n"
"border: none;\n"
"border-radius:2px\n"
"\n"
"}\n"
"\n"
"")
        icon10 = QIcon()
        icon10.addFile(u":/img/janelinha.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.abrir_layout_3.setIcon(icon10)
        self.abrir_layout_3.setIconSize(QSize(26, 26))

        self.horizontalLayout_9.addWidget(self.abrir_layout_3)


        self.verticalLayout_5.addLayout(self.horizontalLayout_9)

        self.frame_7 = QFrame(self.frame_6)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setStyleSheet(u"QFrame {\n"
"background-color:transparent;\n"
"border:none\n"
"\n"
"}")
        self.frame_7.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_11 = QHBoxLayout(self.frame_7)
        self.horizontalLayout_11.setSpacing(0)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(0, -1, 0, -1)
        self.pesquisar_3 = QPushButton(self.frame_7)
        self.pesquisar_3.setObjectName(u"pesquisar_3")
        self.pesquisar_3.setMaximumSize(QSize(32, 25))
        self.pesquisar_3.setStyleSheet(u"")
        self.pesquisar_3.setIcon(icon1)
        self.pesquisar_3.setIconSize(QSize(28, 28))

        self.horizontalLayout_11.addWidget(self.pesquisar_3)


        self.verticalLayout_5.addWidget(self.frame_7)

        self.projeto = QPushButton(self.frame_6)
        self.projeto.setObjectName(u"projeto")
        self.projeto.setStyleSheet(u"QPushButton {\n"
"padding-top:8px;\n"
"padding-bottom:5px\n"
"}")
        icon11 = QIcon()
        icon11.addFile(u":/img/projecto.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.projeto.setIcon(icon11)
        self.projeto.setIconSize(QSize(24, 24))

        self.verticalLayout_5.addWidget(self.projeto)

        self.exportar_2 = QPushButton(self.frame_6)
        self.exportar_2.setObjectName(u"exportar_2")
        self.exportar_2.setStyleSheet(u"padding-top:5px;\n"
"padding-bottom:5px")
        icon12 = QIcon()
        icon12.addFile(u":/img/exportar.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.exportar_2.setIcon(icon12)
        self.exportar_2.setIconSize(QSize(24, 24))

        self.verticalLayout_5.addWidget(self.exportar_2)

        self.relatorio_3 = QPushButton(self.frame_6)
        self.relatorio_3.setObjectName(u"relatorio_3")
        self.relatorio_3.setStyleSheet(u"padding-top:5px;\n"
"padding-bottom:5px")
        icon13 = QIcon()
        icon13.addFile(u":/img/relatorio.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.relatorio_3.setIcon(icon13)
        self.relatorio_3.setIconSize(QSize(24, 24))

        self.verticalLayout_5.addWidget(self.relatorio_3)

        self.grafico_icon = QPushButton(self.frame_6)
        self.grafico_icon.setObjectName(u"grafico_icon")
        self.grafico_icon.setStyleSheet(u"padding-top:5px;\n"
"padding-bottom:5px")
        icon14 = QIcon()
        icon14.addFile(u":/img/grafico.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.grafico_icon.setIcon(icon14)
        self.grafico_icon.setIconSize(QSize(24, 24))

        self.verticalLayout_5.addWidget(self.grafico_icon)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_2)

        self.configuracoes_2 = QPushButton(self.frame_6)
        self.configuracoes_2.setObjectName(u"configuracoes_2")
        sizePolicy2.setHeightForWidth(self.configuracoes_2.sizePolicy().hasHeightForWidth())
        self.configuracoes_2.setSizePolicy(sizePolicy2)
        self.configuracoes_2.setMinimumSize(QSize(0, 25))
        self.configuracoes_2.setStyleSheet(u"QPushButton {\n"
"text-align: left;\n"
"padding: 8px 2px;\n"
"}\n"
"\n"
"QPushButton {\n"
"    background-color: transparent;\n"
"    color: #000000;\n"
"    border: none;\n"
"    border-radius: 3px;\n"
"    padding: 6px 12px;\n"
"    font-size: 14px;\n"
"    font-family: Roboto;\n"
"	text-align: left;\n"
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
"")
        self.configuracoes_2.setIcon(icon8)
        self.configuracoes_2.setIconSize(QSize(20, 20))

        self.verticalLayout_5.addWidget(self.configuracoes_2)

        self.sair_3 = QPushButton(self.frame_6)
        self.sair_3.setObjectName(u"sair_3")
        sizePolicy2.setHeightForWidth(self.sair_3.sizePolicy().hasHeightForWidth())
        self.sair_3.setSizePolicy(sizePolicy2)
        self.sair_3.setMinimumSize(QSize(0, 25))
        self.sair_3.setStyleSheet(u"QPushButton {\n"
"text-align: left;\n"
"padding: 8px 2px;\n"
"}\n"
"\n"
"QPushButton {\n"
"    background-color: transparent;\n"
"    color: #000000;\n"
"    border: none;\n"
"    border-radius: 3px;\n"
"    padding: 6px 12px;\n"
"    font-size: 14px;\n"
"    font-family: Roboto;\n"
"	text-align: left;\n"
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
"")
        self.sair_3.setIcon(icon9)
        self.sair_3.setIconSize(QSize(20, 20))

        self.verticalLayout_5.addWidget(self.sair_3)


        self.horizontalLayout_5.addWidget(self.frame_6)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.stackedWidget = QStackedWidget(AquaPump)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.verticalLayout_7 = QVBoxLayout(self.page)
        self.verticalLayout_7.setSpacing(2)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.darcy = QComboBox(self.page)
        self.darcy.setObjectName(u"darcy")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.darcy.sizePolicy().hasHeightForWidth())
        self.darcy.setSizePolicy(sizePolicy4)
        self.darcy.setMinimumSize(QSize(0, 0))
        self.darcy.setMaximumSize(QSize(450, 16777215))
        self.darcy.setStyleSheet(u"")

        self.horizontalLayout.addWidget(self.darcy)

        self.hazen_will = QComboBox(self.page)
        self.hazen_will.setObjectName(u"hazen_will")
        self.hazen_will.setMinimumSize(QSize(0, 30))
        self.hazen_will.setMaximumSize(QSize(450, 16777215))
        self.hazen_will.setStyleSheet(u"")

        self.horizontalLayout.addWidget(self.hazen_will)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.Vazao_2 = QLineEdit(self.page)
        self.Vazao_2.setObjectName(u"Vazao_2")
        sizePolicy.setHeightForWidth(self.Vazao_2.sizePolicy().hasHeightForWidth())
        self.Vazao_2.setSizePolicy(sizePolicy)
        self.Vazao_2.setStyleSheet(u"QLineEdit {\n"
"    border-top-left-radius: 4px;\n"
"    border-bottom-left-radius: 4px;\n"
"    border-top-right-radius: 0px;\n"
"    border-bottom-right-radius: 0px;\n"
"	border-right: 0px solid #d0d0d0;\n"
"\n"
"}\n"
"")

        self.horizontalLayout_7.addWidget(self.Vazao_2)

        self.icone_2 = QComboBox(self.page)
        self.icone_2.setObjectName(u"icone_2")
        self.icone_2.setMaximumSize(QSize(32, 16777215))
        self.icone_2.setStyleSheet(u"QComboBox {\n"
"    border-top: 2px solid #d0d0d0;\n"
"    border-top-left-radius: 0px;\n"
"    border-bottom-left-radius: 0px;\n"
"    border-top-right-radius: 4px;\n"
"    border-bottom-right-radius: 4px;\n"
"border-left:0px solid #d0d0d0;\n"
" border-bottom: 2px solid #d0d0d0;\n"
" border-right: 2px solid #d0d0d0;\n"
"\n"
"}\n"
"")

        self.horizontalLayout_7.addWidget(self.icone_2)


        self.horizontalLayout.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.Vazao = QLineEdit(self.page)
        self.Vazao.setObjectName(u"Vazao")
        sizePolicy.setHeightForWidth(self.Vazao.sizePolicy().hasHeightForWidth())
        self.Vazao.setSizePolicy(sizePolicy)
        self.Vazao.setStyleSheet(u"QLineEdit {\n"
"    border-radius: 4px;\n"
"\n"
"\n"
"}\n"
"")

        self.horizontalLayout_6.addWidget(self.Vazao)


        self.horizontalLayout.addLayout(self.horizontalLayout_6)


        self.verticalLayout_7.addLayout(self.horizontalLayout)

        self.splitter_2 = QSplitter(self.page)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Orientation.Horizontal)
        self.splitter = QSplitter(self.splitter_2)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Orientation.Vertical)
        self.splitter.addWidget(self.view)
        self.widget_2 = QWidget(self.splitter)
        self.widget_2.setObjectName(u"widget_2")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy5)
        self.widget_2.setMaximumSize(QSize(16777215, 0))
        self.widget_2.setStyleSheet(u"")
        self.verticalLayout_11 = QVBoxLayout(self.widget_2)
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(9, -1, 9, -1)
        self.fechar_perfil = QToolButton(self.widget_2)
        self.fechar_perfil.setObjectName(u"fechar_perfil")
        icon15 = QIcon()
        icon15.addFile(u":/img/bottom.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.fechar_perfil.setIcon(icon15)
        self.fechar_perfil.setIconSize(QSize(24, 24))

        self.horizontalLayout_13.addWidget(self.fechar_perfil)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_5)

        self.opcoes_perfil = QToolButton(self.widget_2)
        self.opcoes_perfil.setObjectName(u"opcoes_perfil")
        self.opcoes_perfil.setStyleSheet(u"padding-right: 15px")
        icon16 = QIcon()
        icon16.addFile(u":/img/opcoes.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.opcoes_perfil.setIcon(icon16)
        self.opcoes_perfil.setIconSize(QSize(24, 24))

        self.horizontalLayout_13.addWidget(self.opcoes_perfil)

        self.expandir_2 = QToolButton(self.widget_2)
        self.expandir_2.setObjectName(u"expandir_2")
        icon17 = QIcon()
        icon17.addFile(u":/img/zoom.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.expandir_2.setIcon(icon17)
        self.expandir_2.setIconSize(QSize(24, 24))

        self.horizontalLayout_13.addWidget(self.expandir_2)


        self.verticalLayout_11.addLayout(self.horizontalLayout_13)

        self.grafico_2 = QFrame(self.widget_2)
        self.grafico_2.setObjectName(u"grafico_2")
        self.grafico_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.grafico_2.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout_11.addWidget(self.grafico_2)

        self.splitter.addWidget(self.widget_2)
        self.splitter_2.addWidget(self.splitter)
        self.janel_direita = QWidget(self.splitter_2)
        self.janel_direita.setObjectName(u"janel_direita")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.janel_direita.sizePolicy().hasHeightForWidth())
        self.janel_direita.setSizePolicy(sizePolicy6)
        self.janel_direita.setMaximumSize(QSize(0, 16777215))
        self.janel_direita.setStyleSheet(u"")
        self.verticalLayout_9 = QVBoxLayout(self.janel_direita)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.fechar_lateral_2 = QToolButton(self.janel_direita)
        self.fechar_lateral_2.setObjectName(u"fechar_lateral_2")
        icon18 = QIcon()
        icon18.addFile(u":/img/right_panel_close.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.fechar_lateral_2.setIcon(icon18)
        self.fechar_lateral_2.setIconSize(QSize(24, 24))

        self.horizontalLayout_12.addWidget(self.fechar_lateral_2)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_6)

        self.label_2 = QLabel(self.janel_direita)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setStyleSheet(u"color: rgb(181, 181, 181);")

        self.horizontalLayout_12.addWidget(self.label_2)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_7)

        self.definicoes_direita_2 = QToolButton(self.janel_direita)
        self.definicoes_direita_2.setObjectName(u"definicoes_direita_2")
        self.definicoes_direita_2.setStyleSheet(u"padding-right: 15px")
        self.definicoes_direita_2.setIcon(icon16)
        self.definicoes_direita_2.setIconSize(QSize(24, 24))

        self.horizontalLayout_12.addWidget(self.definicoes_direita_2)

        self.actualizar_grafico = QToolButton(self.janel_direita)
        self.actualizar_grafico.setObjectName(u"actualizar_grafico")
        icon19 = QIcon()
        icon19.addFile(u":/img/refresh.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actualizar_grafico.setIcon(icon19)
        self.actualizar_grafico.setIconSize(QSize(20, 20))

        self.horizontalLayout_12.addWidget(self.actualizar_grafico)

        self.expandir_3 = QToolButton(self.janel_direita)
        self.expandir_3.setObjectName(u"expandir_3")
        self.expandir_3.setIcon(icon17)
        self.expandir_3.setIconSize(QSize(24, 24))

        self.horizontalLayout_12.addWidget(self.expandir_3)


        self.verticalLayout_9.addLayout(self.horizontalLayout_12)

        self.stackedWidget_3 = QStackedWidget(self.janel_direita)
        self.stackedWidget_3.setObjectName(u"stackedWidget_3")
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.horizontalLayout_14 = QHBoxLayout(self.page_3)
        self.horizontalLayout_14.setSpacing(0)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.altura = QWidget(self.page_3)
        self.altura.setObjectName(u"altura")

        self.horizontalLayout_14.addWidget(self.altura)

        self.stackedWidget_3.addWidget(self.page_3)
        self.page_5 = QWidget()
        self.page_5.setObjectName(u"page_5")
        self.horizontalLayout_15 = QHBoxLayout(self.page_5)
        self.horizontalLayout_15.setSpacing(0)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.potencia = QWidget(self.page_5)
        self.potencia.setObjectName(u"potencia")

        self.horizontalLayout_15.addWidget(self.potencia)

        self.stackedWidget_3.addWidget(self.page_5)
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.verticalLayout_10 = QVBoxLayout(self.page_4)
        self.verticalLayout_10.setSpacing(0)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.rendimento = QWidget(self.page_4)
        self.rendimento.setObjectName(u"rendimento")

        self.verticalLayout_10.addWidget(self.rendimento)

        self.stackedWidget_3.addWidget(self.page_4)

        self.verticalLayout_9.addWidget(self.stackedWidget_3)

        self.splitter_2.addWidget(self.janel_direita)

        self.verticalLayout_7.addWidget(self.splitter_2)

        self.stackedWidget.addWidget(self.page)
        self.definicoes_2 = QWidget()
        self.definicoes_2.setObjectName(u"definicoes_2")
        self.verticalLayout_32 = QVBoxLayout(self.definicoes_2)
        self.verticalLayout_32.setObjectName(u"verticalLayout_32")
        self.frame = QFrame(self.definicoes_2)
        self.frame.setObjectName(u"frame")
        self.frame.setStyleSheet(u"")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_27 = QHBoxLayout(self.frame)
        self.horizontalLayout_27.setSpacing(0)
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.horizontalLayout_27.setContentsMargins(-1, 0, -1, -1)
        self.label_11 = QLabel(self.frame)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setStyleSheet(u"QLabel {\n"
"    font-family: \"Segoe UI\", \"Roboto\", sans-serif;\n"
"    font-size: 22px;\n"
"    font-weight: 600; /* Semi-Bold */\n"
"    color: rgb(166, 166, 166);\n"
"\n"
"}")

        self.horizontalLayout_27.addWidget(self.label_11)


        self.verticalLayout_32.addWidget(self.frame)

        self.splitter_3 = QSplitter(self.definicoes_2)
        self.splitter_3.setObjectName(u"splitter_3")
        self.splitter_3.setOrientation(Qt.Orientation.Horizontal)
        self.scrollArea_3 = QScrollArea(self.splitter_3)
        self.scrollArea_3.setObjectName(u"scrollArea_3")
        sizePolicy2.setHeightForWidth(self.scrollArea_3.sizePolicy().hasHeightForWidth())
        self.scrollArea_3.setSizePolicy(sizePolicy2)
        self.scrollArea_3.setMaximumSize(QSize(350, 16777215))
        self.scrollArea_3.setStyleSheet(u"QFrame {\n"
"    background-color: #F9F9F9;\n"
"    border: 1px solid #DDDDDD;\n"
"    border-radius: 6px;\n"
"    padding: 2px;\n"
"	padding-top: 0px;\n"
"}\n"
"\n"
"\n"
"QPushButton {\n"
"    background-color: #f5f5f5;\n"
"    color: #000000;\n"
"    border:none;\n"
"    border-radius: 3px;\n"
"    padding: 6px 12px;\n"
"    font-size: 14px;\n"
"	text-align: left\n"
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
"")
        self.scrollArea_3.setWidgetResizable(True)
        self.scrollAreaWidgetContents_3 = QWidget()
        self.scrollAreaWidgetContents_3.setObjectName(u"scrollAreaWidgetContents_3")
        self.scrollAreaWidgetContents_3.setGeometry(QRect(0, 0, 212, 605))
        self.verticalLayout_14 = QVBoxLayout(self.scrollAreaWidgetContents_3)
        self.verticalLayout_14.setSpacing(10)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.verticalLayout_14.setContentsMargins(12, -1, 12, -1)
        self.geral = QPushButton(self.scrollAreaWidgetContents_3)
        self.geral.setObjectName(u"geral")
        self.geral.setMinimumSize(QSize(0, 0))
        self.geral.setMaximumSize(QSize(20000, 16777215))
        icon20 = QIcon()
        icon20.addFile(u":/img/geral.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.geral.setIcon(icon20)
        self.geral.setIconSize(QSize(16, 16))
        self.geral.setCheckable(True)
        self.geral.setChecked(True)
        self.geral.setAutoExclusive(True)

        self.verticalLayout_14.addWidget(self.geral)

        self.unidades = QPushButton(self.scrollAreaWidgetContents_3)
        self.unidades.setObjectName(u"unidades")
        icon21 = QIcon()
        icon21.addFile(u":/img/unidades.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.unidades.setIcon(icon21)
        self.unidades.setIconSize(QSize(16, 16))
        self.unidades.setCheckable(True)
        self.unidades.setAutoExclusive(True)

        self.verticalLayout_14.addWidget(self.unidades)

        self.banco_dados = QPushButton(self.scrollAreaWidgetContents_3)
        self.banco_dados.setObjectName(u"banco_dados")
        icon22 = QIcon()
        icon22.addFile(u":/img/dados.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.banco_dados.setIcon(icon22)
        self.banco_dados.setCheckable(True)
        self.banco_dados.setAutoExclusive(True)

        self.verticalLayout_14.addWidget(self.banco_dados)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_14.addItem(self.verticalSpacer_3)

        self.scrollArea_3.setWidget(self.scrollAreaWidgetContents_3)
        self.splitter_3.addWidget(self.scrollArea_3)
        self.layoutWidget1 = QWidget(self.splitter_3)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.verticalLayout_27 = QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_27.setObjectName(u"verticalLayout_27")
        self.verticalLayout_27.setContentsMargins(0, 0, 0, 0)
        self.janela_definicoes = QStackedWidget(self.layoutWidget1)
        self.janela_definicoes.setObjectName(u"janela_definicoes")
        sizePolicy5.setHeightForWidth(self.janela_definicoes.sizePolicy().hasHeightForWidth())
        self.janela_definicoes.setSizePolicy(sizePolicy5)
        self.geral_2 = QWidget()
        self.geral_2.setObjectName(u"geral_2")
        self.verticalLayout_16 = QVBoxLayout(self.geral_2)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.label_5 = QLabel(self.geral_2)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setStyleSheet(u"QLabel {\n"
"    font-family: \"Segoe UI\", \"Roboto\", sans-serif;\n"
"    font-size: 20px;\n"
"    font-weight: 600; /* Semi-Bold */\n"
"    color: rgb(166, 166, 166);\n"
"\n"
"}")

        self.verticalLayout_16.addWidget(self.label_5)

        self.groupBox_8 = QGroupBox(self.geral_2)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.verticalLayout_15 = QVBoxLayout(self.groupBox_8)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.label_6 = QLabel(self.groupBox_8)
        self.label_6.setObjectName(u"label_6")

        self.verticalLayout_15.addWidget(self.label_6)

        self.comboBox_5 = QComboBox(self.groupBox_8)
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.comboBox_5.setObjectName(u"comboBox_5")

        self.verticalLayout_15.addWidget(self.comboBox_5)

        self.label_9 = QLabel(self.groupBox_8)
        self.label_9.setObjectName(u"label_9")

        self.verticalLayout_15.addWidget(self.label_9)

        self.comboBox_6 = QComboBox(self.groupBox_8)
        self.comboBox_6.addItem("")
        self.comboBox_6.addItem("")
        self.comboBox_6.setObjectName(u"comboBox_6")

        self.verticalLayout_15.addWidget(self.comboBox_6)


        self.verticalLayout_16.addWidget(self.groupBox_8)

        self.groupBox_13 = QGroupBox(self.geral_2)
        self.groupBox_13.setObjectName(u"groupBox_13")
        self.verticalLayout_21 = QVBoxLayout(self.groupBox_13)
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.radioButton_9 = QRadioButton(self.groupBox_13)
        self.radioButton_9.setObjectName(u"radioButton_9")
        self.radioButton_9.setChecked(True)

        self.verticalLayout_21.addWidget(self.radioButton_9)

        self.radioButton_10 = QRadioButton(self.groupBox_13)
        self.radioButton_10.setObjectName(u"radioButton_10")

        self.verticalLayout_21.addWidget(self.radioButton_10)


        self.verticalLayout_16.addWidget(self.groupBox_13)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_16.addItem(self.verticalSpacer_4)

        self.janela_definicoes.addWidget(self.geral_2)
        self.Banco = QWidget()
        self.Banco.setObjectName(u"Banco")
        self.verticalLayout_29 = QVBoxLayout(self.Banco)
        self.verticalLayout_29.setSpacing(9)
        self.verticalLayout_29.setObjectName(u"verticalLayout_29")
        self.Banco_dados = QLabel(self.Banco)
        self.Banco_dados.setObjectName(u"Banco_dados")
        self.Banco_dados.setStyleSheet(u"QLabel {\n"
"    font-family: \"Segoe UI\", \"Roboto\", sans-serif;\n"
"    font-size: 20px;\n"
"    font-weight: 600; /* Semi-Bold */\n"
"    color: rgb(166, 166, 166);\n"
"\n"
"}")

        self.verticalLayout_29.addWidget(self.Banco_dados)

        self.groupBox_11 = QGroupBox(self.Banco)
        self.groupBox_11.setObjectName(u"groupBox_11")
        self.verticalLayout_24 = QVBoxLayout(self.groupBox_11)
        self.verticalLayout_24.setObjectName(u"verticalLayout_24")
        self.verticalLayout_24.setContentsMargins(-1, 0, -1, 0)
        self.gerente_material = QTableView(self.groupBox_11)
        self.gerente_material.setObjectName(u"gerente_material")

        self.verticalLayout_24.addWidget(self.gerente_material)

        self.horizontalLayout_25 = QHBoxLayout()
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.adicionar_2 = QPushButton(self.groupBox_11)
        self.adicionar_2.setObjectName(u"adicionar_2")
        self.adicionar_2.setStyleSheet(u"    padding: 6px 12px;")

        self.horizontalLayout_25.addWidget(self.adicionar_2)

        self.remover_2 = QPushButton(self.groupBox_11)
        self.remover_2.setObjectName(u"remover_2")
        self.remover_2.setStyleSheet(u"    padding: 6px 12px;")

        self.horizontalLayout_25.addWidget(self.remover_2)

        self.editar_2 = QPushButton(self.groupBox_11)
        self.editar_2.setObjectName(u"editar_2")
        self.editar_2.setStyleSheet(u"    padding: 6px 12px;")

        self.horizontalLayout_25.addWidget(self.editar_2)

        self.salvar_2 = QPushButton(self.groupBox_11)
        self.salvar_2.setObjectName(u"salvar_2")
        self.salvar_2.setStyleSheet(u"    padding: 6px 12px;")

        self.horizontalLayout_25.addWidget(self.salvar_2)


        self.verticalLayout_24.addLayout(self.horizontalLayout_25)


        self.verticalLayout_29.addWidget(self.groupBox_11)

        self.groupBox_12 = QGroupBox(self.Banco)
        self.groupBox_12.setObjectName(u"groupBox_12")
        self.verticalLayout_25 = QVBoxLayout(self.groupBox_12)
        self.verticalLayout_25.setObjectName(u"verticalLayout_25")
        self.verticalLayout_25.setContentsMargins(-1, 0, -1, 0)
        self.gerente_acessorio = QTableView(self.groupBox_12)
        self.gerente_acessorio.setObjectName(u"gerente_acessorio")

        self.verticalLayout_25.addWidget(self.gerente_acessorio)

        self.horizontalLayout_26 = QHBoxLayout()
        self.horizontalLayout_26.setObjectName(u"horizontalLayout_26")
        self.adicionar = QPushButton(self.groupBox_12)
        self.adicionar.setObjectName(u"adicionar")
        self.adicionar.setStyleSheet(u"    padding: 6px 12px;")

        self.horizontalLayout_26.addWidget(self.adicionar)

        self.remover = QPushButton(self.groupBox_12)
        self.remover.setObjectName(u"remover")
        self.remover.setStyleSheet(u"    padding: 6px 12px;")

        self.horizontalLayout_26.addWidget(self.remover)

        self.editar = QPushButton(self.groupBox_12)
        self.editar.setObjectName(u"editar")
        self.editar.setStyleSheet(u"    padding: 6px 12px;")

        self.horizontalLayout_26.addWidget(self.editar)

        self.salvar = QPushButton(self.groupBox_12)
        self.salvar.setObjectName(u"salvar")
        self.salvar.setStyleSheet(u"    padding: 6px 12px;")

        self.horizontalLayout_26.addWidget(self.salvar)


        self.verticalLayout_25.addLayout(self.horizontalLayout_26)


        self.verticalLayout_29.addWidget(self.groupBox_12)

        self.janela_definicoes.addWidget(self.Banco)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.verticalLayout_31 = QVBoxLayout(self.page_2)
        self.verticalLayout_31.setObjectName(u"verticalLayout_31")
        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_31.addItem(self.verticalSpacer_5)

        self.janela_definicoes.addWidget(self.page_2)
        self.unidade = QWidget()
        self.unidade.setObjectName(u"unidade")
        self.verticalLayout_13 = QVBoxLayout(self.unidade)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.label = QLabel(self.unidade)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"QLabel {\n"
"    font-family: \"Segoe UI\", \"Roboto\", sans-serif;\n"
"    font-size: 20px;\n"
"    font-weight: 600; /* Semi-Bold */\n"
"    color: rgb(166, 166, 166);\n"
"\n"
"}")

        self.verticalLayout_13.addWidget(self.label)

        self.scrollArea_4 = QScrollArea(self.unidade)
        self.scrollArea_4.setObjectName(u"scrollArea_4")
        self.scrollArea_4.setStyleSheet(u"QFrame {\n"
"    background-color: #FFFFFF;\n"
"    border: none;\n"
"\n"
"    padding: 2px;\n"
"	padding-top: 0px;\n"
"}\n"
"")
        self.scrollArea_4.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.scrollArea_4.setWidgetResizable(True)
        self.scrollAreaWidgetContents_4 = QWidget()
        self.scrollAreaWidgetContents_4.setObjectName(u"scrollAreaWidgetContents_4")
        self.scrollAreaWidgetContents_4.setGeometry(QRect(0, 0, 796, 822))
        self.verticalLayout_28 = QVBoxLayout(self.scrollAreaWidgetContents_4)
        self.verticalLayout_28.setSpacing(30)
        self.verticalLayout_28.setObjectName(u"verticalLayout_28")
        self.groupBox = QGroupBox(self.scrollAreaWidgetContents_4)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_17 = QVBoxLayout(self.groupBox)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setBold(False)
        font.setItalic(True)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet(u"QLabel{\n"
"    font-family: \"Segoe UI\", \"Roboto\", sans-serif;\n"
"    font-size: 14px;\n"
"      font-weight: 400; \n"
"    color: #333333;\n"
"    padding-top: 2px;\n"
"    padding-bottom: 2px;\n"
"}")

        self.verticalLayout_17.addWidget(self.label_3)

        self.line_2 = QFrame(self.groupBox)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_17.addWidget(self.line_2)

        self.radioButton = QRadioButton(self.groupBox)
        self.radioButton.setObjectName(u"radioButton")
        self.radioButton.setChecked(True)

        self.verticalLayout_17.addWidget(self.radioButton)

        self.radioButton_2 = QRadioButton(self.groupBox)
        self.radioButton_2.setObjectName(u"radioButton_2")

        self.verticalLayout_17.addWidget(self.radioButton_2)

        self.radioButton_3 = QRadioButton(self.groupBox)
        self.radioButton_3.setObjectName(u"radioButton_3")

        self.verticalLayout_17.addWidget(self.radioButton_3)


        self.verticalLayout_28.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.scrollAreaWidgetContents_4)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_19 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
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

        self.verticalLayout_19.addWidget(self.label_7)

        self.line_3 = QFrame(self.groupBox_2)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_19.addWidget(self.line_3)

        self.comboBox_12 = QComboBox(self.groupBox_2)
        self.comboBox_12.addItem("")
        self.comboBox_12.addItem("")
        self.comboBox_12.addItem("")
        self.comboBox_12.addItem("")
        self.comboBox_12.addItem("")
        self.comboBox_12.addItem("")
        self.comboBox_12.setObjectName(u"comboBox_12")
        sizePolicy2.setHeightForWidth(self.comboBox_12.sizePolicy().hasHeightForWidth())
        self.comboBox_12.setSizePolicy(sizePolicy2)

        self.verticalLayout_19.addWidget(self.comboBox_12)


        self.verticalLayout_28.addWidget(self.groupBox_2)

        self.label_8 = QLabel(self.scrollAreaWidgetContents_4)
        self.label_8.setObjectName(u"label_8")
        font2 = QFont()
        font2.setFamilies([u"Segoe UI"])
        font2.setWeight(QFont.DemiBold)
        self.label_8.setFont(font2)
        self.label_8.setStyleSheet(u"QLabel {\n"
"    font-family: \"Segoe UI\", \"Roboto\", sans-serif;\n"
"    font-size: 15px;\n"
"    font-weight: 600; /* Semi-Bold */\n"
"    color: rgb(161, 161, 161);\n"
"\n"
"}\n"
"")

        self.verticalLayout_28.addWidget(self.label_8)

        self.label_4 = QLabel(self.scrollAreaWidgetContents_4)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font)
        self.label_4.setStyleSheet(u"QLabel{\n"
"    font-family: \"Segoe UI\", \"Roboto\", sans-serif;\n"
"    font-size: 14px;\n"
"      font-weight: 400; \n"
"    color: #333333;\n"
"\n"
"    padding-bottom: 2px;\n"
"}")

        self.verticalLayout_28.addWidget(self.label_4)

        self.groupBox_4 = QGroupBox(self.scrollAreaWidgetContents_4)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.verticalLayout_20 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.caudal = QLabel(self.groupBox_4)
        self.caudal.setObjectName(u"caudal")
        self.caudal.setMaximumSize(QSize(180, 16777215))

        self.horizontalLayout_16.addWidget(self.caudal)

        self.caudal_box = QComboBox(self.groupBox_4)
        self.caudal_box.setObjectName(u"caudal_box")
        sizePolicy2.setHeightForWidth(self.caudal_box.sizePolicy().hasHeightForWidth())
        self.caudal_box.setSizePolicy(sizePolicy2)
        self.caudal_box.setMaximumSize(QSize(500, 16777215))

        self.horizontalLayout_16.addWidget(self.caudal_box)


        self.verticalLayout_20.addLayout(self.horizontalLayout_16)

        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.altura_2 = QLabel(self.groupBox_4)
        self.altura_2.setObjectName(u"altura_2")
        self.altura_2.setMaximumSize(QSize(180, 16777215))

        self.horizontalLayout_17.addWidget(self.altura_2)

        self.altura_box = QComboBox(self.groupBox_4)
        self.altura_box.setObjectName(u"altura_box")
        sizePolicy2.setHeightForWidth(self.altura_box.sizePolicy().hasHeightForWidth())
        self.altura_box.setSizePolicy(sizePolicy2)
        self.altura_box.setMaximumSize(QSize(500, 16777215))

        self.horizontalLayout_17.addWidget(self.altura_box)


        self.verticalLayout_20.addLayout(self.horizontalLayout_17)

        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.npsh = QLabel(self.groupBox_4)
        self.npsh.setObjectName(u"npsh")
        self.npsh.setMaximumSize(QSize(180, 16777215))

        self.horizontalLayout_19.addWidget(self.npsh)

        self.npsh_box = QComboBox(self.groupBox_4)
        self.npsh_box.setObjectName(u"npsh_box")
        self.npsh_box.setMaximumSize(QSize(500, 16777215))

        self.horizontalLayout_19.addWidget(self.npsh_box)


        self.verticalLayout_20.addLayout(self.horizontalLayout_19)


        self.verticalLayout_28.addWidget(self.groupBox_4)

        self.groupBox_6 = QGroupBox(self.scrollAreaWidgetContents_4)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.verticalLayout_22 = QVBoxLayout(self.groupBox_6)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.horizontalLayout_21 = QHBoxLayout()
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.diametro = QLabel(self.groupBox_6)
        self.diametro.setObjectName(u"diametro")
        self.diametro.setMaximumSize(QSize(180, 16777215))

        self.horizontalLayout_21.addWidget(self.diametro)

        self.diametro_box = QComboBox(self.groupBox_6)
        self.diametro_box.setObjectName(u"diametro_box")
        self.diametro_box.setMaximumSize(QSize(500, 16777215))

        self.horizontalLayout_21.addWidget(self.diametro_box)


        self.verticalLayout_22.addLayout(self.horizontalLayout_21)

        self.horizontalLayout_22 = QHBoxLayout()
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.comprimento = QLabel(self.groupBox_6)
        self.comprimento.setObjectName(u"comprimento")
        sizePolicy7 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.comprimento.sizePolicy().hasHeightForWidth())
        self.comprimento.setSizePolicy(sizePolicy7)
        self.comprimento.setMaximumSize(QSize(180, 16777215))

        self.horizontalLayout_22.addWidget(self.comprimento)

        self.comprimento_box = QComboBox(self.groupBox_6)
        self.comprimento_box.setObjectName(u"comprimento_box")
        self.comprimento_box.setMaximumSize(QSize(500, 16777215))

        self.horizontalLayout_22.addWidget(self.comprimento_box)


        self.verticalLayout_22.addLayout(self.horizontalLayout_22)


        self.verticalLayout_28.addWidget(self.groupBox_6)

        self.groupBox_5 = QGroupBox(self.scrollAreaWidgetContents_4)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.verticalLayout_23 = QVBoxLayout(self.groupBox_5)
        self.verticalLayout_23.setObjectName(u"verticalLayout_23")
        self.horizontalLayout_24 = QHBoxLayout()
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.potencia_2 = QLabel(self.groupBox_5)
        self.potencia_2.setObjectName(u"potencia_2")
        self.potencia_2.setMaximumSize(QSize(180, 16777215))

        self.horizontalLayout_24.addWidget(self.potencia_2)

        self.potencia_box = QComboBox(self.groupBox_5)
        self.potencia_box.setObjectName(u"potencia_box")
        self.potencia_box.setMaximumSize(QSize(500, 16777215))

        self.horizontalLayout_24.addWidget(self.potencia_box)


        self.verticalLayout_23.addLayout(self.horizontalLayout_24)


        self.verticalLayout_28.addWidget(self.groupBox_5)

        self.scrollArea_4.setWidget(self.scrollAreaWidgetContents_4)

        self.verticalLayout_13.addWidget(self.scrollArea_4)

        self.janela_definicoes.addWidget(self.unidade)

        self.verticalLayout_27.addWidget(self.janela_definicoes)

        self.frame_8 = QFrame(self.layoutWidget1)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setStyleSheet(u"QPushButton {\n"
"    background-color: #f5f5f5;\n"
"    color: #000000;\n"
"    border: 1px solid #c2c2c2;\n"
"    border-radius: 3px;\n"
"    padding: 6px 12px;\n"
"    font-size: 14px;\n"
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
"}")
        self.frame_8.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_10 = QHBoxLayout(self.frame_8)
        self.horizontalLayout_10.setSpacing(12)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(0, -1, -1, 0)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer)

        self.voltar = QPushButton(self.frame_8)
        self.voltar.setObjectName(u"voltar")

        self.horizontalLayout_10.addWidget(self.voltar)

        self.cancelar = QPushButton(self.frame_8)
        self.cancelar.setObjectName(u"cancelar")

        self.horizontalLayout_10.addWidget(self.cancelar)

        self.aplicar = QPushButton(self.frame_8)
        self.aplicar.setObjectName(u"aplicar")

        self.horizontalLayout_10.addWidget(self.aplicar)


        self.verticalLayout_27.addWidget(self.frame_8)

        self.splitter_3.addWidget(self.layoutWidget1)

        self.verticalLayout_32.addWidget(self.splitter_3)

        self.stackedWidget.addWidget(self.definicoes_2)

        self.verticalLayout.addWidget(self.stackedWidget)


        self.horizontalLayout_5.addLayout(self.verticalLayout)


        self.verticalLayout_8.addLayout(self.horizontalLayout_5)


        self.retranslateUi(AquaPump)

        self.projecto_2.setDefault(True)
        self.stackedWidget.setCurrentIndex(0)
        self.stackedWidget_3.setCurrentIndex(1)
        self.janela_definicoes.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(AquaPump)
    # setupUi

    def retranslateUi(self, AquaPump):
        AquaPump.setWindowTitle(QCoreApplication.translate("AquaPump", u"Form", None))
        self.arquivo_2.setText(QCoreApplication.translate("AquaPump", u"Arquivo", None))
        self.config_2.setText(QCoreApplication.translate("AquaPump", u"Editar", None))
        self.relatorio_2.setText(QCoreApplication.translate("AquaPump", u"Relat\u00f3rio ", None))
        self.ajuda_2.setText(QCoreApplication.translate("AquaPump", u"Ajuda", None))
#if QT_CONFIG(tooltip)
        self.abrir_layout_2.setToolTip(QCoreApplication.translate("AquaPump", u"Fechar Barra Lateral", None))
#endif // QT_CONFIG(tooltip)
        self.abrir_layout_2.setText("")
        self.pesquisa_line.setPlaceholderText(QCoreApplication.translate("AquaPump", u"Pesquisar", None))
        self.pesquisar_2.setText("")
        self.projecto_2.setText(QCoreApplication.translate("AquaPump", u"Projecto", None))
#if QT_CONFIG(tooltip)
        self.novo_arquivo.setToolTip(QCoreApplication.translate("AquaPump", u"Novo", None))
#endif // QT_CONFIG(tooltip)
        self.novo_arquivo.setText(QCoreApplication.translate("AquaPump", u"Novo Arquivo", None))
#if QT_CONFIG(tooltip)
        self.salvar_projecto.setToolTip(QCoreApplication.translate("AquaPump", u"Salvar Projecto", None))
#endif // QT_CONFIG(tooltip)
        self.salvar_projecto.setText(QCoreApplication.translate("AquaPump", u"Salvar Projecto", None))
#if QT_CONFIG(tooltip)
        self.abrir_arquivo.setToolTip(QCoreApplication.translate("AquaPump", u"Abrir Projecto", None))
#endif // QT_CONFIG(tooltip)
        self.abrir_arquivo.setText(QCoreApplication.translate("AquaPump", u"Abrir Arquivo", None))
        self.parametros.setText(QCoreApplication.translate("AquaPump", u"Exportar", None))
        self.exportar_pdf.setText(QCoreApplication.translate("AquaPump", u"Exportar em PDF", None))
        self.exportar_csv.setText(QCoreApplication.translate("AquaPump", u"Exportar em CSV", None))
        self.rel.setText(QCoreApplication.translate("AquaPump", u"Selec\u00e7\u00e3o de Bombas", None))
        self.grafico.setText(QCoreApplication.translate("AquaPump", u"Gr\u00e1ficos ", None))
        self.pushButton_3.setText(QCoreApplication.translate("AquaPump", u"Actualizar (PRO)", None))
        self.configuracoes.setText(QCoreApplication.translate("AquaPump", u"Configura\u00e7\u00f5es ", None))
        self.sair_2.setText(QCoreApplication.translate("AquaPump", u"Sair", None))
#if QT_CONFIG(tooltip)
        self.abrir_layout_3.setToolTip(QCoreApplication.translate("AquaPump", u"Abrir Barra Lateral", None))
#endif // QT_CONFIG(tooltip)
        self.abrir_layout_3.setText("")
        self.pesquisar_3.setText("")
        self.projeto.setText("")
        self.exportar_2.setText("")
        self.relatorio_3.setText("")
        self.grafico_icon.setText("")
        self.configuracoes_2.setText("")
        self.sair_3.setText("")
        self.fechar_perfil.setText("")
        self.opcoes_perfil.setText("")
        self.expandir_2.setText("")
#if QT_CONFIG(tooltip)
        self.fechar_lateral_2.setToolTip(QCoreApplication.translate("AquaPump", u"Fechar Janela", None))
#endif // QT_CONFIG(tooltip)
        self.fechar_lateral_2.setText("")
        self.label_2.setText(QCoreApplication.translate("AquaPump", u" Curva H vs Q (Altura vs Vaz\u00e3o) ", None))
#if QT_CONFIG(tooltip)
        self.definicoes_direita_2.setToolTip(QCoreApplication.translate("AquaPump", u"Alterne o grafico exibido", None))
#endif // QT_CONFIG(tooltip)
        self.definicoes_direita_2.setText("")
#if QT_CONFIG(tooltip)
        self.actualizar_grafico.setToolTip(QCoreApplication.translate("AquaPump", u"Actualizar Gr\u00e1ficos", None))
#endif // QT_CONFIG(tooltip)
        self.actualizar_grafico.setText("")
        self.expandir_3.setText("")
        self.label_11.setText(QCoreApplication.translate("AquaPump", u"Defini\u00e7\u00f5es", None))
        self.geral.setText(QCoreApplication.translate("AquaPump", u"Geral", None))
        self.unidades.setText(QCoreApplication.translate("AquaPump", u"Unidades", None))
        self.banco_dados.setText(QCoreApplication.translate("AquaPump", u"Banco de Dados", None))
        self.label_5.setText(QCoreApplication.translate("AquaPump", u"Geral", None))
        self.groupBox_8.setTitle("")
        self.label_6.setText(QCoreApplication.translate("AquaPump", u"Apar\u00eancia ", None))
        self.comboBox_5.setItemText(0, QCoreApplication.translate("AquaPump", u"Predefini\u00e7\u00e3o do Sistema", None))
        self.comboBox_5.setItemText(1, QCoreApplication.translate("AquaPump", u"Claro", None))
        self.comboBox_5.setItemText(2, QCoreApplication.translate("AquaPump", u"Escuro", None))

        self.label_9.setText(QCoreApplication.translate("AquaPump", u"Idioma", None))
        self.comboBox_6.setItemText(0, QCoreApplication.translate("AquaPump", u"Portugu\u00eas", None))
        self.comboBox_6.setItemText(1, QCoreApplication.translate("AquaPump", u"Ingl\u00eas", None))

        self.groupBox_13.setTitle(QCoreApplication.translate("AquaPump", u"F\u00f3rmulas Pr\u00e9-definidas/ Perdas de Carga", None))
        self.radioButton_9.setText(QCoreApplication.translate("AquaPump", u"Hazen Williams", None))
        self.radioButton_10.setText(QCoreApplication.translate("AquaPump", u"Darcy", None))
        self.Banco_dados.setText(QCoreApplication.translate("AquaPump", u"Banco de Dados", None))
        self.groupBox_11.setTitle(QCoreApplication.translate("AquaPump", u"Gerenciar Materiais de Tubula\u00e7\u00e3o", None))
        self.adicionar_2.setText(QCoreApplication.translate("AquaPump", u"Adicionar Novo", None))
        self.remover_2.setText(QCoreApplication.translate("AquaPump", u"Remover Selecionado", None))
        self.editar_2.setText(QCoreApplication.translate("AquaPump", u"Editar", None))
        self.salvar_2.setText(QCoreApplication.translate("AquaPump", u"Salvar", None))
        self.groupBox_12.setTitle(QCoreApplication.translate("AquaPump", u"Gerenciar Materiais de Acess\u00f3rios ", None))
        self.adicionar.setText(QCoreApplication.translate("AquaPump", u"Adicionar Novo", None))
        self.remover.setText(QCoreApplication.translate("AquaPump", u"Remover Selecionado", None))
        self.editar.setText(QCoreApplication.translate("AquaPump", u"Editar", None))
        self.salvar.setText(QCoreApplication.translate("AquaPump", u"Salvar", None))
        self.label.setText(QCoreApplication.translate("AquaPump", u"Unidades", None))
        self.groupBox.setTitle(QCoreApplication.translate("AquaPump", u"Padr\u00e3o de Unidades Preferencial", None))
        self.label_3.setText(QCoreApplication.translate("AquaPump", u"Escolha entre os sistemas de unidades M\u00e9trico (SI) ou Imperial (EUA) para configurar todas as suas prefer\u00eancias de uma vez. ", None))
        self.radioButton.setText(QCoreApplication.translate("AquaPump", u"Sistema Internacional (SI / M\u00e9trico)", None))
        self.radioButton_2.setText(QCoreApplication.translate("AquaPump", u"Sistema Imperial (EUA)", None))
        self.radioButton_3.setText(QCoreApplication.translate("AquaPump", u"Personalizado", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("AquaPump", u"Precis\u00e3o (casas decimais)", None))
        self.label_7.setText(QCoreApplication.translate("AquaPump", u"\n"
"Define o n\u00famero de casas decimais a serem exibidas nos c\u00e1lculos \n"
"e resultados.", None))
        self.comboBox_12.setItemText(0, QCoreApplication.translate("AquaPump", u"0.00", None))
        self.comboBox_12.setItemText(1, QCoreApplication.translate("AquaPump", u"0.0", None))
        self.comboBox_12.setItemText(2, QCoreApplication.translate("AquaPump", u"0.000", None))
        self.comboBox_12.setItemText(3, QCoreApplication.translate("AquaPump", u"0.0000", None))
        self.comboBox_12.setItemText(4, QCoreApplication.translate("AquaPump", u"0.00000", None))
        self.comboBox_12.setItemText(5, QCoreApplication.translate("AquaPump", u"0.000000", None))

        self.label_8.setText(QCoreApplication.translate("AquaPump", u"Personaliza\u00e7\u00e3o de unidades", None))
        self.label_4.setText(QCoreApplication.translate("AquaPump", u"\n"
"Ajuste individualmente as unidades para cada par\u00e2metro \n"
"(ex: Caudal, Press\u00e3o, Di\u00e2metro).", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("AquaPump", u"Desempenho", None))
        self.caudal.setText(QCoreApplication.translate("AquaPump", u"Caudal", None))
        self.altura_2.setText(QCoreApplication.translate("AquaPump", u"Altura Man\u00f4metrica", None))
        self.npsh.setText(QCoreApplication.translate("AquaPump", u"NPSH", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("AquaPump", u"Dimens\u00f5es F\u00edsicas", None))
        self.diametro.setText(QCoreApplication.translate("AquaPump", u"Di\u00e2metro da Tubagem", None))
        self.comprimento.setText(QCoreApplication.translate("AquaPump", u"Comprimento da Tubagem", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("AquaPump", u"Pot\u00eancia ", None))
        self.potencia_2.setText(QCoreApplication.translate("AquaPump", u"Pot\u00eancia", None))
        self.voltar.setText(QCoreApplication.translate("AquaPump", u"Voltar", None))
        self.cancelar.setText(QCoreApplication.translate("AquaPump", u"Cancelar", None))
        self.aplicar.setText(QCoreApplication.translate("AquaPump", u"Aplicar", None))
    # retranslateUi

