# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'aboutIFgrSf.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QFrame, QHBoxLayout, QLabel, QSizePolicy,
    QVBoxLayout, QWidget)
import img.img_rc

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(400, 300)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setStyleSheet(u"QWidget {\n"
"    background-color: #ffffff;\n"
"    font-family: \"Segoe UI\", Roboto, sans-serif;\n"
"    color: #333333;\n"
"}\n"
"\n"
"QPushButton {\n"
"    background-color: #f5f5f5;\n"
"    color: #000000;\n"
"    border: 1px solid #c2c2c2;\n"
"    border-radius: 3px;\n"
"    font-size: 14px;\n"
"width:50px;\n"
"height: 25px;\n"
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
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.frame_2 = QFrame(self.frame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMaximumSize(QSize(70, 16777215))
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.frame_2)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(16777215, 40))
        self.label.setPixmap(QPixmap(u":/img/logo_principal.png"))
        self.label.setScaledContents(True)

        self.verticalLayout_2.addWidget(self.label)


        self.horizontalLayout.addWidget(self.frame_2)

        self.frame_3 = QFrame(self.frame)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame_3)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label_2 = QLabel(self.frame_3)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setStyleSheet(u"QLabel {\n"
"color: #000000;\n"
"    font-family: Roboto;\n"
"    font-size: 14px;\n"
"}")

        self.verticalLayout_5.addWidget(self.label_2)

        self.label_3 = QLabel(self.frame_3)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setStyleSheet(u"QLabel {\n"
"    font-family: Roboto;\n"
"    font-size: 11px;\n"
"}")

        self.verticalLayout_5.addWidget(self.label_3)


        self.horizontalLayout.addWidget(self.frame_3)


        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.frame_4 = QFrame(self.frame)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_4)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_4 = QLabel(self.frame_4)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setStyleSheet(u"QLabel {\n"
"    font-family: Roboto;\n"
"    font-size: 11px;\n"
"}")

        self.verticalLayout_3.addWidget(self.label_4)

        self.label_5 = QLabel(self.frame_4)
        self.label_5.setObjectName(u"label_5")
        font = QFont()
        font.setFamilies([u"Roboto"])
        self.label_5.setFont(font)
        self.label_5.setStyleSheet(u"QLabel {\n"
"    font-family: Roboto;\n"
"    font-size: 9px;\n"
"}")

        self.verticalLayout_3.addWidget(self.label_5)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_6 = QLabel(self.frame_4)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMaximumSize(QSize(15, 15))
        self.label_6.setPixmap(QPixmap(u":/img/giti.png"))
        self.label_6.setScaledContents(True)

        self.horizontalLayout_2.addWidget(self.label_6)

        self.git = QLabel(self.frame_4)
        self.git.setObjectName(u"git")
        self.git.setStyleSheet(u"QLabel {\n"
"    font-family: Roboto;\n"
"    font-size: 12px;\n"
"}")
        self.git.setOpenExternalLinks(True)

        self.horizontalLayout_2.addWidget(self.git)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_7 = QLabel(self.frame_4)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMaximumSize(QSize(15, 15))
        self.label_7.setPixmap(QPixmap(u":/img/linkedin.png"))
        self.label_7.setScaledContents(True)

        self.horizontalLayout_3.addWidget(self.label_7)

        self.link = QLabel(self.frame_4)
        self.link.setObjectName(u"link")
        self.link.setStyleSheet(u"QLabel {\n"
"    font-family: Roboto;\n"
"    font-size: 12px;\n"
"}")
        self.link.setOpenExternalLinks(True)

        self.horizontalLayout_3.addWidget(self.link)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_8 = QLabel(self.frame_4)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMaximumSize(QSize(15, 15))
        self.label_8.setPixmap(QPixmap(u":/img/social.png"))
        self.label_8.setScaledContents(True)

        self.horizontalLayout_4.addWidget(self.label_8)

        self.redit = QLabel(self.frame_4)
        self.redit.setObjectName(u"redit")
        self.redit.setStyleSheet(u"QLabel {\n"
"    font-family: Roboto;\n"
"    font-size: 12px;\n"
"}")
        self.redit.setOpenExternalLinks(True)

        self.horizontalLayout_4.addWidget(self.redit)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)

        self.label_12 = QLabel(self.frame_4)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setFont(font)
        self.label_12.setStyleSheet(u"QLabel {\n"
"    font-family: Roboto;\n"
"    font-size: 9px;\n"
"}")

        self.verticalLayout_3.addWidget(self.label_12, 0, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignVCenter)


        self.verticalLayout_4.addWidget(self.frame_4)


        self.verticalLayout.addWidget(self.frame)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setMinimumSize(QSize(29, 0))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText("")
        self.label_2.setText(QCoreApplication.translate("Dialog", u"AquaPump", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Vers\u00e3o 1.0.0 (Lan\u00e7amento de Setembro 2025)", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Desenvolvido por: <span style=\" font-weight:700;\">Tenerife da Saugineta</span></p></body></html>", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"Para mais informa\u00e7\u00f5es visite:", None))
        self.label_6.setText("")
        self.git.setText(QCoreApplication.translate("Dialog", u"GitHub", None))
        self.label_7.setText("")
        self.link.setText(QCoreApplication.translate("Dialog", u"LinkeIn", None))
        self.label_8.setText("")
        self.redit.setText(QCoreApplication.translate("Dialog", u"Redit", None))
        self.label_12.setText(QCoreApplication.translate("Dialog", u"\u00a9 2025 Tenerife da Saugineta. Todos os direitos reservados.", None))
    # retranslateUi

