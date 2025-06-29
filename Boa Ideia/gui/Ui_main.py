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
    QLineEdit, QPushButton, QScrollArea, QSizePolicy,
    QSpacerItem, QStackedWidget, QVBoxLayout, QWidget)
from PySide6.QtWebEngineWidgets import QWebEngineView
import gui.img_rc


class Ui_AquaPump(object):
    def setupUi(self, AquaPump):
        if not AquaPump.objectName():
            AquaPump.setObjectName(u"AquaPump")
        self.view = QWebEngineView()
        AquaPump.resize(982, 635)
        AquaPump.setStyleSheet(u"/* --------- QWidget (Geral) --------- */\n"
"QWidget {\n"
"    background-color: #f9f9f9;\n"
"    font-family: \"Segoe UI\", Roboto, sans-serif;\n"
"    font-size: 14px;\n"
"    color: #333333;\n"
"}\n"
"\n"
"/* --------- QLineEdit --------- */\n"
"QLineEdit {\n"
"    background-color: #ffffff;\n"
"    border: 2px solid #d9d9d9;\n"
"    border-radius: 4px;\n"
"    padding: 6px 8px;\n"
"    font-size: 14px;\n"
"    font-family: \"Segoe UI\", Roboto, sans-serif;\n"
"    color: #2b2b2b;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border: 2px solid #95acff;\n"
"    background-color: #fcfcfc;\n"
"}\n"
"\n"
"QLineEdit:hover {\n"
"    border: 2px solid #a5baff;\n"
"    background-color: #fefefe;\n"
"}\n"
"\n"
"/* --------- QComboBox --------- */\n"
"QComboBox {\n"
"    background-color: #fdfdfd;\n"
"    border: 2px solid #d0d0d0;\n"
"    border-radius: 4px;\n"
"    padding: 6px 8px;\n"
"    font-size: 14px;\n"
"    font-family: \"Segoe UI\", Roboto, sans-serif;\n"
"    color: #2b2b2b;\n"
"}\n"
"\n"
"QComboBox:hover,\n"
""
                        "QComboBox:focus {\n"
"    border: 2px solid #95acff;\n"
"    background-color: #ffffff;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 28px;\n"
"    border-left: 1px solid #d0d0d0;\n"
"    background-color: transparent;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    image: url(:/img/arrow-down-1.png);\n"
"    width: 10px;\n"
"    height: 10px;\n"
"    margin-right: 5px;\n"
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
"/* --------- QScrollArea --------- */\n"
"QScrollArea {\n"
"    background-color: #f9f9f9;\n"
"    border: none;\n"
"    font-family: \"Segoe UI\", Roboto, sans-serif;\n"
"    font-size: 14px;\n"
"    color: #333333;\n"
"}\n"
"\n"
"QScrollArea QWidget {\n"
"    background-color"
                        ": transparent;\n"
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
"    bo"
                        "rder-radius: 6px;\n"
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
"    width: 8px;\n"
"    height: 9px;\n"
"    margin: 2px;\n"
"}\n"
"")
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
        self.pesquisa_line.setMaximumSize(QSize(500, 30))
        self.pesquisa_line.setStyleSheet(u"QLineEdit {\n"
"    border-top-left-radius: 4px;\n"
"    border-bottom-left-radius: 4px;\n"
"    border-top-right-radius: 0px;\n"
"    border-bottom-right-radius: 0px;\n"
"	border-right: 0px solid #d0d0d0;\n"
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
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 193, 352))
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

        self.projectos_recentes = QPushButton(self.projecto)
        self.projectos_recentes.setObjectName(u"projectos_recentes")
        self.projectos_recentes.setMinimumSize(QSize(0, 0))
        icon3 = QIcon()
        icon3.addFile(u":/img/recente.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.projectos_recentes.setIcon(icon3)
        self.projectos_recentes.setIconSize(QSize(16, 16))

        self.verticalLayout_3.addWidget(self.projectos_recentes)

        self.salvar_projecto = QPushButton(self.projecto)
        self.salvar_projecto.setObjectName(u"salvar_projecto")
        self.salvar_projecto.setMinimumSize(QSize(0, 0))
        icon4 = QIcon()
        icon4.addFile(u":/img/pasta.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.salvar_projecto.setIcon(icon4)
        self.salvar_projecto.setIconSize(QSize(16, 16))

        self.verticalLayout_3.addWidget(self.salvar_projecto)

        self.abrir_arquivo = QPushButton(self.projecto)
        self.abrir_arquivo.setObjectName(u"abrir_arquivo")
        self.abrir_arquivo.setMinimumSize(QSize(0, 0))
        icon5 = QIcon()
        icon5.addFile(u":/img/pasta (1).png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.abrir_arquivo.setIcon(icon5)
        self.abrir_arquivo.setIconSize(QSize(16, 16))

        self.verticalLayout_3.addWidget(self.abrir_arquivo)

        self.line = QFrame(self.projecto)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_3.addWidget(self.line)

        self.pushButton = QPushButton(self.projecto)
        self.pushButton.setObjectName(u"pushButton")
        icon6 = QIcon()
        icon6.addFile(u":/img/kml.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton.setIcon(icon6)

        self.verticalLayout_3.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(self.projecto)
        self.pushButton_2.setObjectName(u"pushButton_2")
        icon7 = QIcon()
        icon7.addFile(u":/img/arquivo-csv.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_2.setIcon(icon7)

        self.verticalLayout_3.addWidget(self.pushButton_2)

        self.pushButton_4 = QPushButton(self.projecto)
        self.pushButton_4.setObjectName(u"pushButton_4")
        icon8 = QIcon()
        icon8.addFile(u":/img/arquivo.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_4.setIcon(icon8)

        self.verticalLayout_3.addWidget(self.pushButton_4)


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
        icon9 = QIcon()
        icon9.addFile(u":/img/pdf.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.exportar_pdf.setIcon(icon9)
        self.exportar_pdf.setIconSize(QSize(16, 16))

        self.verticalLayout_6.addWidget(self.exportar_pdf)

        self.exportar_csv = QPushButton(self.exportar)
        self.exportar_csv.setObjectName(u"exportar_csv")
        self.exportar_csv.setMinimumSize(QSize(0, 36))
        self.exportar_csv.setIcon(icon7)
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
        icon10 = QIcon()
        icon10.addFile(u":/img/settings_67dp_999999_FILL1_wght400_GRAD0_opsz48.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.configuracoes.setIcon(icon10)
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
        icon11 = QIcon()
        icon11.addFile(u":/img/sair.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.sair_2.setIcon(icon11)
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
        icon12 = QIcon()
        icon12.addFile(u":/img/janelinha.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.abrir_layout_3.setIcon(icon12)
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
"}")
        icon13 = QIcon()
        icon13.addFile(u":/img/projecto.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.projeto.setIcon(icon13)
        self.projeto.setIconSize(QSize(24, 24))

        self.verticalLayout_5.addWidget(self.projeto)

        self.exportar_2 = QPushButton(self.frame_6)
        self.exportar_2.setObjectName(u"exportar_2")
        self.exportar_2.setStyleSheet(u"QPushButton {\n"
"padding-top:6px;\n"
"}")
        icon14 = QIcon()
        icon14.addFile(u":/img/exportar.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.exportar_2.setIcon(icon14)
        self.exportar_2.setIconSize(QSize(24, 24))

        self.verticalLayout_5.addWidget(self.exportar_2)

        self.relatorio_3 = QPushButton(self.frame_6)
        self.relatorio_3.setObjectName(u"relatorio_3")
        icon15 = QIcon()
        icon15.addFile(u":/img/relatorio.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.relatorio_3.setIcon(icon15)
        self.relatorio_3.setIconSize(QSize(24, 24))

        self.verticalLayout_5.addWidget(self.relatorio_3)

        self.grafico_icon = QPushButton(self.frame_6)
        self.grafico_icon.setObjectName(u"grafico_icon")
        icon16 = QIcon()
        icon16.addFile(u":/img/grafico.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.grafico_icon.setIcon(icon16)
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
        self.configuracoes_2.setIcon(icon10)
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
        self.sair_3.setIcon(icon11)
        self.sair_3.setIconSize(QSize(20, 20))

        self.verticalLayout_5.addWidget(self.sair_3)


        self.horizontalLayout_5.addWidget(self.frame_6)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.stackedWidget = QStackedWidget(AquaPump)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.verticalLayout_9 = QVBoxLayout(self.page)
        self.verticalLayout_9.setSpacing(2)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
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
        sizePolicy2.setHeightForWidth(self.comboBox_3.sizePolicy().hasHeightForWidth())
        self.comboBox_3.setSizePolicy(sizePolicy2)
        self.comboBox_3.setStyleSheet(u"")

        self.horizontalLayout_10.addWidget(self.comboBox_3)

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

        self.horizontalLayout_10.addWidget(self.comboBox)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.Vazao_2 = QLineEdit(self.page)
        self.Vazao_2.setObjectName(u"Vazao_2")
        sizePolicy2.setHeightForWidth(self.Vazao_2.sizePolicy().hasHeightForWidth())
        self.Vazao_2.setSizePolicy(sizePolicy2)
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


        self.horizontalLayout_10.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.Vazao = QLineEdit(self.page)
        self.Vazao.setObjectName(u"Vazao")
        sizePolicy2.setHeightForWidth(self.Vazao.sizePolicy().hasHeightForWidth())
        self.Vazao.setSizePolicy(sizePolicy2)
        self.Vazao.setStyleSheet(u"QLineEdit {\n"
"    border-top-left-radius: 4px;\n"
"    border-bottom-left-radius: 4px;\n"
"    border-top-right-radius: 0px;\n"
"    border-bottom-right-radius: 0px;\n"
"	border-right: 0px solid #d0d0d0;\n"
"\n"
"}\n"
"")

        self.horizontalLayout_6.addWidget(self.Vazao)

        self.icone = QComboBox(self.page)
        self.icone.setObjectName(u"icone")
        self.icone.setMaximumSize(QSize(32, 16777215))
        self.icone.setStyleSheet(u"QComboBox {\n"
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

        self.horizontalLayout_6.addWidget(self.icone)


        self.horizontalLayout_10.addLayout(self.horizontalLayout_6)


        self.verticalLayout_9.addLayout(self.horizontalLayout_10)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")

        self.horizontalLayout_14.addWidget(self.view)

        self.widget = QWidget(self.page)
        self.widget.setObjectName(u"widget")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy4)
        self.widget.setMaximumSize(QSize(0, 16777215))

        self.horizontalLayout_14.addWidget(self.widget)


        self.verticalLayout_9.addLayout(self.horizontalLayout_14)

        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.stackedWidget.addWidget(self.page_2)

        self.verticalLayout.addWidget(self.stackedWidget)


        self.horizontalLayout_5.addLayout(self.verticalLayout)


        self.verticalLayout_8.addLayout(self.horizontalLayout_5)


        self.retranslateUi(AquaPump)

        self.projecto_2.setDefault(True)


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
        self.pesquisar_2.setText("")
        self.projecto_2.setText(QCoreApplication.translate("AquaPump", u"Projecto", None))
#if QT_CONFIG(tooltip)
        self.novo_arquivo.setToolTip(QCoreApplication.translate("AquaPump", u"Novo", None))
#endif // QT_CONFIG(tooltip)
        self.novo_arquivo.setText(QCoreApplication.translate("AquaPump", u"Novo Arquivo", None))
#if QT_CONFIG(tooltip)
        self.projectos_recentes.setToolTip(QCoreApplication.translate("AquaPump", u"Projectos Recentes", None))
#endif // QT_CONFIG(tooltip)
        self.projectos_recentes.setText(QCoreApplication.translate("AquaPump", u"Projectos Recentes", None))
#if QT_CONFIG(tooltip)
        self.salvar_projecto.setToolTip(QCoreApplication.translate("AquaPump", u"Salvar Projecto", None))
#endif // QT_CONFIG(tooltip)
        self.salvar_projecto.setText(QCoreApplication.translate("AquaPump", u"Salvar Projecto", None))
#if QT_CONFIG(tooltip)
        self.abrir_arquivo.setToolTip(QCoreApplication.translate("AquaPump", u"Abrir Projecto", None))
#endif // QT_CONFIG(tooltip)
        self.abrir_arquivo.setText(QCoreApplication.translate("AquaPump", u"Abrir Arquivo", None))
        self.pushButton.setText(QCoreApplication.translate("AquaPump", u"Carregar KML", None))
        self.pushButton_2.setText(QCoreApplication.translate("AquaPump", u"Carregar CSV", None))
        self.pushButton_4.setText(QCoreApplication.translate("AquaPump", u"Carregar Shapefile", None))
        self.parametros.setText(QCoreApplication.translate("AquaPump", u"Exportar", None))
        self.exportar_pdf.setText(QCoreApplication.translate("AquaPump", u"Exportar em PDF", None))
        self.exportar_csv.setText(QCoreApplication.translate("AquaPump", u"Exportar em CSV", None))
        self.rel.setText(QCoreApplication.translate("AquaPump", u"Relat\u00f3rio ", None))
        self.grafico.setText(QCoreApplication.translate("AquaPump", u"Gr\u00e1ficos ", None))
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
        self.comboBox_3.setItemText(0, QCoreApplication.translate("AquaPump", u"PVC", None))
        self.comboBox_3.setItemText(1, QCoreApplication.translate("AquaPump", u"Polietileno", None))
        self.comboBox_3.setItemText(2, QCoreApplication.translate("AquaPump", u"A\u00e7o galvanizado (novo)", None))
        self.comboBox_3.setItemText(3, QCoreApplication.translate("AquaPump", u"Ferro fundido (novo)", None))
        self.comboBox_3.setItemText(4, QCoreApplication.translate("AquaPump", u"Ferro fundido (velho ou corro\u00eddo)", None))
        self.comboBox_3.setItemText(5, QCoreApplication.translate("AquaPump", u"Concreto liso", None))
        self.comboBox_3.setItemText(6, QCoreApplication.translate("AquaPump", u"Concreto rugoso", None))
        self.comboBox_3.setItemText(7, QCoreApplication.translate("AquaPump", u"Madeira lisa", None))
        self.comboBox_3.setItemText(8, QCoreApplication.translate("AquaPump", u"Madeira \u00e1spera", None))
        self.comboBox_3.setItemText(9, QCoreApplication.translate("AquaPump", u"Amianto-cimento", None))
        self.comboBox_3.setItemText(10, QCoreApplication.translate("AquaPump", u"Tubo de chumbo", None))
        self.comboBox_3.setItemText(11, QCoreApplication.translate("AquaPump", u"Tubo de vidro", None))

        self.comboBox.setItemText(0, QCoreApplication.translate("AquaPump", u"A\u00e7o Corrugado(chapa ondulada)", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("AquaPump", u"A\u00e7o Galvanizado", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("AquaPump", u"A\u00e7o Rebitado novo", None))
        self.comboBox.setItemText(3, QCoreApplication.translate("AquaPump", u"A\u00e7o Rebitado em uso", None))
        self.comboBox.setItemText(4, QCoreApplication.translate("AquaPump", u"A\u00e7o soldado novo", None))
        self.comboBox.setItemText(5, QCoreApplication.translate("AquaPump", u"A\u00e7o Soldado em uso", None))
        self.comboBox.setItemText(6, QCoreApplication.translate("AquaPump", u"A\u00e7o Soldado com revestimento especial", None))
        self.comboBox.setItemText(7, QCoreApplication.translate("AquaPump", u"Chumbo", None))
        self.comboBox.setItemText(8, QCoreApplication.translate("AquaPump", u"Cimento Amianto", None))
        self.comboBox.setItemText(9, QCoreApplication.translate("AquaPump", u"Cobre", None))
        self.comboBox.setItemText(10, QCoreApplication.translate("AquaPump", u"Concreto com acabamento comum", None))
        self.comboBox.setItemText(11, QCoreApplication.translate("AquaPump", u"Ferro Fundido novo", None))
        self.comboBox.setItemText(12, QCoreApplication.translate("AquaPump", u"Ferro Fundido de 15 a 20 anos de uso", None))
        self.comboBox.setItemText(13, QCoreApplication.translate("AquaPump", u"Ferro Fundido Usado", None))
        self.comboBox.setItemText(14, QCoreApplication.translate("AquaPump", u"Lat\u00e3o", None))
        self.comboBox.setItemText(15, QCoreApplication.translate("AquaPump", u"Ferro Fundido Revestido de Cimento", None))
        self.comboBox.setItemText(16, QCoreApplication.translate("AquaPump", u"Manilha Cer\u00e2mica vidrada", None))
        self.comboBox.setItemText(17, QCoreApplication.translate("AquaPump", u"Pl\u00e1stico", None))
        self.comboBox.setItemText(18, QCoreApplication.translate("AquaPump", u"Tijolos em executados", None))
        self.comboBox.setItemText(19, QCoreApplication.translate("AquaPump", u"Vidro", None))

    # retranslateUi

