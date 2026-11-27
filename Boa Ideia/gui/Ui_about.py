# -*- coding: utf-8 -*-
"""
Janela "Sobre" do AquaPump.
Interface redesenhada em PySide6.

Os contactos e links externos estão definidos na secção CONTACT_INFO.
"""

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
)


APP_INFO = {
    "name": "AquaPump",
    "subtitle": "Dimensionamento de sistemas de bombagem de água",
    "version": "2.0.0",
    "release": "Setembro de 2025",
    "description": (
        "Ferramenta desenvolvida para apoiar o dimensionamento de sistemas "
        "de bombagem, reunindo cálculos hidráulicos e informação técnica "
        "numa interface simples e organizada."
    ),
    "developer": "Tenerife da Saugineta",
    "copyright": "© 2025 Tenerife da Saugineta. Todos os direitos reservados.",
}

# Contactos e recursos do desenvolvedor.
CONTACT_INFO = {
    "email": "tenerifenhalicale@gmail.com",
    "website": "https://www.yane.co.mz",
    "portfolio": "https://tsaugineta225.github.io/",
    "github": "https://github.com/TSaugineta225",
    "linkedin": "https://www.linkedin.com/in/tenerife-saugineta/",
}


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("AboutAquaPump")
        Dialog.setWindowTitle("Sobre o AquaPump")
        Dialog.setMinimumSize(520, 590)
        Dialog.resize(560, 650)
        Dialog.setSizeGripEnabled(True)

        Dialog.setStyleSheet("""
            QDialog {
                background: #f3f6fa;
                color: #172b4d;
                font-family: "Segoe UI", "Roboto", sans-serif;
            }
            QFrame#mainCard {
                background: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 16px;
            }
            QFrame#hero {
                background: #102a43;
                border: none;
                border-radius: 13px;
            }
            QLabel#appName {
                color: #ffffff;
                font-size: 27px;
                font-weight: 700;
            }
            QLabel#appSubtitle {
                color: #d7e5f3;
                font-size: 12px;
            }
            QLabel#versionPill {
                color: #d9f2e6;
                background: #1d604c;
                border-radius: 9px;
                padding: 5px 10px;
                font-size: 11px;
                font-weight: 600;
            }
            QLabel#sectionTitle {
                color: #102a43;
                font-size: 13px;
                font-weight: 700;
            }
            QLabel#bodyText {
                color: #526579;
                font-size: 12px;
                line-height: 1.5;
            }
            QLabel#fieldLabel {
                color: #7b8da1;
                font-size: 10px;
                font-weight: 700;
            }
            QLabel#fieldValue {
                color: #243b53;
                font-size: 12px;
                font-weight: 600;
            }
            QFrame#infoPanel {
                background: #f7f9fc;
                border: 1px solid #e8eef5;
                border-radius: 10px;
            }
            QFrame#contactPanel {
                background: #fbfcfe;
                border: 1px solid #e8eef5;
                border-radius: 10px;
            }
            QLabel#contactName {
                color: #243b53;
                font-size: 12px;
                font-weight: 600;
            }
            QLabel#contactValue {
                color: #1670b8;
                font-size: 11px;
            }
            QLabel#mutedValue {
                color: #8796a8;
                font-size: 11px;
            }
            QPushButton#closeButton {
                background: #1261a0;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 9px 24px;
                font-size: 12px;
                font-weight: 600;
            }
            QPushButton#closeButton:hover {
                background: #0e4f83;
            }
            QPushButton#closeButton:pressed {
                background: #0a3e68;
            }
        """)

        root = QVBoxLayout(Dialog)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(0)

        card = QFrame()
        card.setObjectName("mainCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(18, 18, 18, 18)
        card_layout.setSpacing(15)

        # Cabeçalho
        hero = QFrame()
        hero.setObjectName("hero")
        hero_layout = QHBoxLayout(hero)
        hero_layout.setContentsMargins(20, 19, 20, 19)
        hero_layout.setSpacing(14)

        logo = QLabel("AP")
        logo.setFixedSize(58, 58)
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setStyleSheet("""
            background: #ffffff;
            color: #102a43;
            border-radius: 14px;
            font-size: 21px;
            font-weight: 800;
        """)
        hero_layout.addWidget(logo, 0, Qt.AlignmentFlag.AlignVCenter)

        title_col = QVBoxLayout()
        title_col.setSpacing(4)
        app_name = QLabel(APP_INFO["name"])
        app_name.setObjectName("appName")
        subtitle = QLabel(APP_INFO["subtitle"])
        subtitle.setObjectName("appSubtitle")
        subtitle.setWordWrap(True)
        title_col.addWidget(app_name)
        title_col.addWidget(subtitle)
        hero_layout.addLayout(title_col, 1)

        version = QLabel(f'VERSÃO {APP_INFO["version"]}')
        version.setObjectName("versionPill")
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        version.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        hero_layout.addWidget(version, 0, Qt.AlignmentFlag.AlignTop)

        card_layout.addWidget(hero)

        # Descrição
        about_title = QLabel("Sobre a aplicação")
        about_title.setObjectName("sectionTitle")
        card_layout.addWidget(about_title)

        description = QLabel(APP_INFO["description"])
        description.setObjectName("bodyText")
        description.setWordWrap(True)
        card_layout.addWidget(description)

        # Informação da versão e autoria
        info_panel = QFrame()
        info_panel.setObjectName("infoPanel")
        info_layout = QHBoxLayout(info_panel)
        info_layout.setContentsMargins(13, 11, 13, 11)
        info_layout.setSpacing(20)

        self._add_info_field(info_layout, "DESENVOLVIDO POR", APP_INFO["developer"])
        self._add_info_field(info_layout, "LANÇAMENTO", APP_INFO["release"])
        card_layout.addWidget(info_panel)

        # Contactos
        contact_title = QLabel("Contacto e recursos")
        contact_title.setObjectName("sectionTitle")
        card_layout.addWidget(contact_title)

        contact_intro = QLabel(
            "Utilize os canais abaixo para obter informações, consultar o "
            "código-fonte ou comunicar sugestões e problemas."
        )
        contact_intro.setObjectName("bodyText")
        contact_intro.setWordWrap(True)
        card_layout.addWidget(contact_intro)

        contact_panel = QFrame()
        contact_panel.setObjectName("contactPanel")
        contact_layout = QVBoxLayout(contact_panel)
        contact_layout.setContentsMargins(13, 7, 13, 7)
        contact_layout.setSpacing(0)

        contact_rows = [
            ("Email", CONTACT_INFO["email"], "mailto:" + CONTACT_INFO["email"]),
            ("Website", "www.yane.co.mz", CONTACT_INFO["website"]),
            ("Portfólio pessoal", "tsaugineta225.github.io", CONTACT_INFO["portfolio"]),
            ("GitHub", "github.com/TSaugineta225", CONTACT_INFO["github"]),
            ("LinkedIn", "linkedin.com/in/tenerife-saugineta", CONTACT_INFO["linkedin"]),
        ]

        for index, (label, display_text, target_url) in enumerate(contact_rows):
            if index:
                line = QFrame()
                line.setFixedHeight(1)
                line.setStyleSheet("background: #e8eef5; border: none;")
                contact_layout.addWidget(line)
            self._add_contact_row(contact_layout, label, display_text, target_url)

        card_layout.addWidget(contact_panel)

        card_layout.addStretch(1)

        footer = QLabel(APP_INFO["copyright"])
        footer.setObjectName("mutedValue")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(footer)

        root.addWidget(card, 1)

        button_row = QHBoxLayout()
        button_row.setContentsMargins(0, 14, 0, 0)
        button_row.addStretch(1)
        close_button = QPushButton("Fechar")
        close_button.setObjectName("closeButton")
        close_button.setCursor(Qt.CursorShape.PointingHandCursor)
        close_button.clicked.connect(Dialog.accept)
        button_row.addWidget(close_button)
        root.addLayout(button_row)

    def _add_info_field(self, layout, label_text, value_text):
        field = QVBoxLayout()
        field.setSpacing(4)
        label = QLabel(label_text)
        label.setObjectName("fieldLabel")
        value = QLabel(value_text)
        value.setObjectName("fieldValue")
        value.setWordWrap(True)
        field.addWidget(label)
        field.addWidget(value)
        layout.addLayout(field, 1)

    def _add_contact_row(self, layout, label_text, display_text, target_url=""):
        row = QHBoxLayout()
        row.setContentsMargins(0, 8, 0, 8)
        row.setSpacing(12)

        label = QLabel(label_text)
        label.setObjectName("contactName")
        label.setMinimumWidth(105)
        row.addWidget(label)

        display = QLabel(display_text if display_text else "Não configurado")
        display.setObjectName("contactValue" if target_url else "mutedValue")
        display.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        display.setWordWrap(True)
        if target_url:
            display.setCursor(Qt.CursorShape.PointingHandCursor)
            display.setToolTip("Abrir " + label_text)
            display.mousePressEvent = (
                lambda event, target=target_url: QDesktopServices.openUrl(QUrl(target))
            )
        row.addWidget(display, 1)
        layout.addLayout(row)
