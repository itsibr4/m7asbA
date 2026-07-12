# -*- coding: utf-8 -*-
"""
صفحة المطور - للتواصل والدعم
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
)
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QFont, QDesktopServices


class DeveloperPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignCenter)

        # Main card
        card = QFrame()
        card.setObjectName("devCard")
        card.setMaximumWidth(520)
        card.setMinimumWidth(450)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(32, 32, 32, 32)
        card_layout.setSpacing(16)
        card_layout.setAlignment(Qt.AlignCenter)

        # Icon
        icon = QLabel("👨‍💻")
        icon.setObjectName("devIcon")
        icon.setAlignment(Qt.AlignCenter)
        icon.setFont(QFont("Segoe UI", 52))
        card_layout.addWidget(icon)

        # Title
        title = QLabel("المطور")
        title.setObjectName("devTitle")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        card_layout.addWidget(title)

        # Subtitle
        subtitle = QLabel("نظام المحاسبة المتكامل")
        subtitle.setObjectName("devSubtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setFont(QFont("Segoe UI", 13))
        card_layout.addWidget(subtitle)

        # Separator
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setObjectName("devSep")
        sep.setFixedHeight(2)
        card_layout.addWidget(sep)

        # Contact info
        info_frame = QFrame()
        info_layout = QVBoxLayout(info_frame)
        info_layout.setSpacing(12)
        info_layout.setAlignment(Qt.AlignCenter)

        # Telegram
        telegram_row = QHBoxLayout()
        telegram_icon = QLabel("📱")
        telegram_icon.setFont(QFont("Segoe UI", 18))
        telegram_label = QLabel("Telegram:")
        telegram_label.setObjectName("contactLabel")
        telegram_label.setFont(QFont("Segoe UI", 12))
        telegram_value = QLabel("@developer_username")
        telegram_value.setObjectName("contactValue")
        telegram_value.setFont(QFont("Segoe UI", 12, QFont.Bold))
        telegram_value.setTextInteractionFlags(Qt.TextSelectableByMouse)
        telegram_row.addWidget(telegram_icon)
        telegram_row.addWidget(telegram_label)
        telegram_row.addWidget(telegram_value)
        telegram_row.addStretch()
        info_layout.addLayout(telegram_row)

        # Email
        email_row = QHBoxLayout()
        email_icon = QLabel("📧")
        email_icon.setFont(QFont("Segoe UI", 18))
        email_label = QLabel("Email:")
        email_label.setObjectName("contactLabel")
        email_label.setFont(QFont("Segoe UI", 12))
        email_value = QLabel("developer@example.com")
        email_value.setObjectName("contactValue")
        email_value.setFont(QFont("Segoe UI", 12, QFont.Bold))
        email_value.setTextInteractionFlags(Qt.TextSelectableByMouse)
        email_row.addWidget(email_icon)
        email_row.addWidget(email_label)
        email_row.addWidget(email_value)
        email_row.addStretch()
        info_layout.addLayout(email_row)

        # Phone
        phone_row = QHBoxLayout()
        phone_icon = QLabel("☎️")
        phone_icon.setFont(QFont("Segoe UI", 18))
        phone_label = QLabel("Phone:")
        phone_label.setObjectName("contactLabel")
        phone_label.setFont(QFont("Segoe UI", 12))
        phone_value = QLabel("+964 770 123 4567")
        phone_value.setObjectName("contactValue")
        phone_value.setFont(QFont("Segoe UI", 12, QFont.Bold))
        phone_value.setTextInteractionFlags(Qt.TextSelectableByMouse)
        phone_row.addWidget(phone_icon)
        phone_row.addWidget(phone_label)
        phone_row.addWidget(phone_value)
        phone_row.addStretch()
        info_layout.addLayout(phone_row)

        card_layout.addWidget(info_frame)

        # Buttons
        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)

        telegram_btn = QPushButton("📱 فتح Telegram")
        telegram_btn.setObjectName("contactBtn")
        telegram_btn.setFixedHeight(44)
        telegram_btn.setFont(QFont("Segoe UI", 12, QFont.Bold))
        telegram_btn.setCursor(Qt.PointingHandCursor)
        telegram_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://t.me/developer_username")))

        email_btn = QPushButton("📧 إرسال بريد")
        email_btn.setObjectName("contactBtn")
        email_btn.setFixedHeight(44)
        email_btn.setFont(QFont("Segoe UI", 12, QFont.Bold))
        email_btn.setCursor(Qt.PointingHandCursor)
        email_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("mailto:developer@example.com")))

        btn_row.addWidget(telegram_btn)
        btn_row.addWidget(email_btn)
        card_layout.addLayout(btn_row)

        # Version
        version = QLabel("الإصدار 2.0 - 2026")
        version.setObjectName("versionLabel")
        version.setAlignment(Qt.AlignCenter)
        version.setFont(QFont("Segoe UI", 11))
        card_layout.addWidget(version)

        layout.addStretch()
        layout.addWidget(card, alignment=Qt.AlignCenter)
        layout.addStretch()

        self.setStyleSheet("""
            #devCard {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 20px;
            }
            #devIcon {
                font-size: 52px;
                margin-bottom: 6px;
            }
            #devTitle {
                color: #1e3a5f;
                font-size: 22px;
                font-weight: bold;
            }
            #devSubtitle {
                color: #64748b;
                font-size: 13px;
            }
            #devSep {
                background-color: #e2e8f0;
                border: none;
                margin: 6px 30px;
            }
            #contactLabel {
                color: #64748b;
                font-size: 12px;
                font-weight: 500;
                min-width: 70px;
            }
            #contactValue {
                color: #1e293b;
                font-size: 12px;
                font-weight: bold;
                background: #f8fafc;
                padding: 5px 10px;
                border-radius: 6px;
                border: 1px solid #e2e8f0;
            }
            #contactBtn {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3b82f6, stop:1 #2563eb);
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 12px;
                font-weight: bold;
                padding: 0 20px;
            }
            #contactBtn:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2563eb, stop:1 #1d4ed8);
            }
            #versionLabel {
                color: #94a3b8;
                font-size: 11px;
                margin-top: 10px;
            }
        """)
