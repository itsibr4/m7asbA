# -*- coding: utf-8 -*-
"""
صفحة المطور - للتواصل والدعم
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QGraphicsDropShadowEffect, QScrollArea
)
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QFont, QColor, QDesktopServices


class DeveloperPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignCenter)

        # Main card
        card = QFrame()
        card.setObjectName("devCard")
        card.setMaximumWidth(600)
        card.setMinimumWidth(500)

        shadow = QGraphicsDropShadowEffect(card)
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 50))
        shadow.setOffset(0, 8)
        card.setGraphicsEffect(shadow)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(40, 40, 40, 40)
        card_layout.setSpacing(20)
        card_layout.setAlignment(Qt.AlignCenter)

        # Icon
        icon = QLabel("👨‍💻")
        icon.setObjectName("devIcon")
        icon.setAlignment(Qt.AlignCenter)
        icon.setFont(QFont("Segoe UI", 64))
        card_layout.addWidget(icon)

        # Title
        title = QLabel("المطور")
        title.setObjectName("devTitle")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        card_layout.addWidget(title)

        # Subtitle
        subtitle = QLabel("نظام المحاسبة المتكامل")
        subtitle.setObjectName("devSubtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setFont(QFont("Segoe UI", 14))
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
        info_layout.setSpacing(16)
        info_layout.setAlignment(Qt.AlignCenter)

        # Telegram
        telegram_row = QHBoxLayout()
        telegram_icon = QLabel("📱")
        telegram_icon.setFont(QFont("Segoe UI", 20))
        telegram_label = QLabel("Telegram:")
        telegram_label.setObjectName("contactLabel")
        telegram_value = QLabel("@developer_username")
        telegram_value.setObjectName("contactValue")
        telegram_value.setTextInteractionFlags(Qt.TextSelectableByMouse)
        telegram_row.addWidget(telegram_icon)
        telegram_row.addWidget(telegram_label)
        telegram_row.addWidget(telegram_value)
        telegram_row.addStretch()
        info_layout.addLayout(telegram_row)

        # Email
        email_row = QHBoxLayout()
        email_icon = QLabel("📧")
        email_icon.setFont(QFont("Segoe UI", 20))
        email_label = QLabel("Email:")
        email_label.setObjectName("contactLabel")
        email_value = QLabel("developer@example.com")
        email_value.setObjectName("contactValue")
        email_value.setTextInteractionFlags(Qt.TextSelectableByMouse)
        email_row.addWidget(email_icon)
        email_row.addWidget(email_label)
        email_row.addWidget(email_value)
        email_row.addStretch()
        info_layout.addLayout(email_row)

        # Phone
        phone_row = QHBoxLayout()
        phone_icon = QLabel("☎️")
        phone_icon.setFont(QFont("Segoe UI", 20))
        phone_label = QLabel("Phone:")
        phone_label.setObjectName("contactLabel")
        phone_value = QLabel("+964 770 123 4567")
        phone_value.setObjectName("contactValue")
        phone_value.setTextInteractionFlags(Qt.TextSelectableByMouse)
        phone_row.addWidget(phone_icon)
        phone_row.addWidget(phone_label)
        phone_row.addWidget(phone_value)
        phone_row.addStretch()
        info_layout.addLayout(phone_row)

        card_layout.addWidget(info_frame)

        # Buttons
        btn_row = QHBoxLayout()
        btn_row.setSpacing(12)

        telegram_btn = QPushButton("📱 فتح Telegram")
        telegram_btn.setObjectName("contactBtn")
        telegram_btn.setFixedHeight(48)
        telegram_btn.setCursor(Qt.PointingHandCursor)
        telegram_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://t.me/itsibr44")))

        email_btn = QPushButton("📧 إرسال بريد")
        email_btn.setObjectName("contactBtn")
        email_btn.setFixedHeight(48)
        email_btn.setCursor(Qt.PointingHandCursor)
        email_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("itslh44@gmail.com")))

        btn_row.addWidget(telegram_btn)
        btn_row.addWidget(email_btn)
        card_layout.addLayout(btn_row)

        # Version
        version = QLabel("الإصدار 2.0 - 2026")
        version.setObjectName("versionLabel")
        version.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(version)

        layout.addStretch()
        layout.addWidget(card, alignment=Qt.AlignCenter)
        layout.addStretch()

        self.setStyleSheet("""
            #devCard {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 24px;
            }
            #devIcon {
                font-size: 64px;
                margin-bottom: 8px;
            }
            #devTitle {
                color: #1e3a5f;
                font-size: 24px;
                font-weight: bold;
            }
            #devSubtitle {
                color: #64748b;
                font-size: 14px;
            }
            #devSep {
                background-color: #e2e8f0;
                border: none;
                margin: 8px 40px;
            }
            #contactLabel {
                color: #64748b;
                font-size: 14px;
                font-weight: 500;
                min-width: 80px;
            }
            #contactValue {
                color: #1e293b;
                font-size: 14px;
                font-weight: bold;
                background: #f8fafc;
                padding: 6px 12px;
                border-radius: 8px;
                border: 1px solid #e2e8f0;
            }
            #contactBtn {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3b82f6, stop:1 #2563eb);
                color: white;
                border: none;
                border-radius: 12px;
                font-size: 14px;
                font-weight: bold;
                padding: 0 24px;
            }
            #contactBtn:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2563eb, stop:1 #1d4ed8);
            }
            #versionLabel {
                color: #94a3b8;
                font-size: 12px;
                margin-top: 12px;
            }
        """)
