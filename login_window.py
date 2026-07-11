# -*- coding: utf-8 -*-
"""
نافذة تسجيل الدخول - تصميم احترافي
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QFrame, QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QFont, QPixmap, QIcon, QColor


class LoginWindow(QWidget):
    login_success = Signal(dict)

    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle("تسجيل الدخول - نظام المحاسبة المتكامل")
        self.setFixedSize(480, 560)
        self.setLayoutDirection(Qt.RightToLeft)
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)
        self._build_ui()
        self._apply_styles()

    def _build_ui(self):
        # Main container with gradient background
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # Background widget
        bg_widget = QWidget()
        bg_widget.setObjectName("bgWidget")
        bg_layout = QVBoxLayout(bg_widget)
        bg_layout.setContentsMargins(40, 30, 40, 30)
        bg_layout.setSpacing(0)

        # Logo / Icon area
        logo_container = QWidget()
        logo_layout = QVBoxLayout(logo_container)
        logo_layout.setAlignment(Qt.AlignCenter)

        logo_label = QLabel("📊")
        logo_label.setObjectName("logoLabel")
        logo_label.setAlignment(Qt.AlignCenter)

        logo_layout.addWidget(logo_label)
        bg_layout.addWidget(logo_container)

        # Card container
        card = QFrame()
        card.setObjectName("loginCard")
        card.setFrameShape(QFrame.StyledPanel)

        # Add shadow effect
        shadow = QGraphicsDropShadowEffect(card)
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 60))
        shadow.setOffset(0, 8)
        card.setGraphicsEffect(shadow)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(40, 35, 40, 35)
        card_layout.setSpacing(18)

        # Title
        title = QLabel("نظام المحاسبة المتكامل")
        title.setAlignment(Qt.AlignCenter)
        title.setObjectName("loginTitle")
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))

        subtitle = QLabel("إدارة المبيعات والمخزون والأرباح")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setObjectName("loginSubtitle")

        # Separator line
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setObjectName("separator")
        sep.setFixedHeight(2)

        # Username input with icon
        user_container = QFrame()
        user_container.setObjectName("inputContainer")
        user_layout = QHBoxLayout(user_container)
        user_layout.setContentsMargins(12, 0, 12, 0)
        user_layout.setSpacing(8)

        user_icon = QLabel("👤")
        user_icon.setObjectName("inputIcon")

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("اسم المستخدم")
        self.username_input.setObjectName("loginInput")
        self.username_input.setFixedHeight(48)
        self.username_input.setClearButtonEnabled(True)

        user_layout.addWidget(user_icon)
        user_layout.addWidget(self.username_input, 1)

        # Password input with icon
        pass_container = QFrame()
        pass_container.setObjectName("inputContainer")
        pass_layout = QHBoxLayout(pass_container)
        pass_layout.setContentsMargins(12, 0, 12, 0)
        pass_layout.setSpacing(8)

        pass_icon = QLabel("🔒")
        pass_icon.setObjectName("inputIcon")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("كلمة المرور")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setObjectName("loginInput")
        self.password_input.setFixedHeight(48)
        self.password_input.setClearButtonEnabled(True)
        self.password_input.returnPressed.connect(self.attempt_login)

        pass_layout.addWidget(pass_icon)
        pass_layout.addWidget(self.password_input, 1)

        # Login button
        login_btn = QPushButton("تسجيل الدخول")
        login_btn.setObjectName("loginBtn")
        login_btn.setFixedHeight(52)
        login_btn.setCursor(Qt.PointingHandCursor)
        login_btn.clicked.connect(self.attempt_login)

        # Hint
        hint = QLabel("الحساب الافتراضي: admin / admin123")
        hint.setAlignment(Qt.AlignCenter)
        hint.setObjectName("loginHint")

        # Version
        version = QLabel("الإصدار 2.0")
        version.setAlignment(Qt.AlignCenter)
        version.setObjectName("versionLabel")

        # Add to card
        card_layout.addWidget(title)
        card_layout.addWidget(subtitle)
        card_layout.addSpacing(8)
        card_layout.addWidget(sep)
        card_layout.addSpacing(12)
        card_layout.addWidget(user_container)
        card_layout.addWidget(pass_container)
        card_layout.addSpacing(6)
        card_layout.addWidget(login_btn)
        card_layout.addSpacing(8)
        card_layout.addWidget(hint)
        card_layout.addWidget(version)

        bg_layout.addWidget(card, alignment=Qt.AlignCenter)
        outer.addWidget(bg_widget)

    def _apply_styles(self):
        self.setStyleSheet("""
            QWidget { font-family: 'Segoe UI', 'Tahoma', sans-serif; }

            #bgWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1e3a5f, stop:0.5 #2d5a87, stop:1 #1e3a5f);
            }

            #loginCard {
                background-color: #ffffff;
                border-radius: 20px;
                border: none;
                min-width: 360px;
                max-width: 400px;
            }

            #logoLabel {
                font-size: 64px;
                margin-bottom: 10px;
            }

            #loginTitle {
                color: #1e3a5f;
                font-size: 22px;
                font-weight: bold;
                margin-bottom: 4px;
            }

            #loginSubtitle {
                color: #64748b;
                font-size: 13px;
                margin-bottom: 8px;
            }

            #separator {
                background-color: #e2e8f0;
                border: none;
            }

            #inputContainer {
                background-color: #f8fafc;
                border: 2px solid #e2e8f0;
                border-radius: 12px;
                min-height: 48px;
            }

            #inputContainer:focus-within {
                border: 2px solid #3b82f6;
                background-color: #ffffff;
            }

            #inputIcon {
                font-size: 18px;
                color: #94a3b8;
            }

            #loginInput {
                border: none;
                background: transparent;
                font-size: 15px;
                color: #1e293b;
                padding: 0 4px;
            }

            #loginInput:focus {
                border: none;
            }

            #loginInput::placeholder {
                color: #94a3b8;
            }

            #loginBtn {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3b82f6, stop:1 #2563eb);
                color: white;
                border: none;
                border-radius: 12px;
                font-size: 16px;
                font-weight: bold;
                padding: 0 24px;
            }

            #loginBtn:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2563eb, stop:1 #1d4ed8);
            }

            #loginBtn:pressed {
                background: #1e40af;
            }

            #loginHint {
                color: #94a3b8;
                font-size: 11px;
                margin-top: 4px;
            }

            #versionLabel {
                color: #cbd5e1;
                font-size: 10px;
                margin-top: 8px;
            }
        """)

    def attempt_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()
        if not username or not password:
            QMessageBox.warning(self, "تنبيه", "الرجاء إدخال اسم المستخدم وكلمة المرور")
            return
        user = self.db.verify_user(username, password)
        if user:
            self.login_success.emit(user)
        else:
            QMessageBox.critical(self, "خطأ في تسجيل الدخول", 
                "اسم المستخدم أو كلمة المرور غير صحيحة\n\nيرجى التحقق من البيانات والمحاولة مرة أخرى")
            self.password_input.clear()
            self.password_input.setFocus()
