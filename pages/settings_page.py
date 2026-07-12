# -*- coding: utf-8 -*-
"""
صفحة الإعدادات - تصميم محسن
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame,
    QComboBox, QSpinBox, QLineEdit, QFormLayout, QMessageBox, QCheckBox,
    QGroupBox, QDialog, QDialogButtonBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor

from settings import app_settings


class ChangePasswordDialog(QDialog):
    def __init__(self, parent=None, current_user=None):
        super().__init__(parent)
        self.current_user = current_user
        self.setWindowTitle("تغيير كلمة المرور")
        self.setLayoutDirection(Qt.RightToLeft)
        self.setMinimumWidth(320)

        layout = QFormLayout(self)
        layout.setSpacing(12)
        layout.setLabelAlignment(Qt.AlignRight)

        self.current_pass = QLineEdit()
        self.current_pass.setEchoMode(QLineEdit.Password)
        self.current_pass.setPlaceholderText("كلمة المرور الحالية")
        self.current_pass.setMinimumHeight(36)
        self.current_pass.setFont(QFont("Segoe UI", 12))

        self.new_pass = QLineEdit()
        self.new_pass.setEchoMode(QLineEdit.Password)
        self.new_pass.setPlaceholderText("كلمة المرور الجديدة")
        self.new_pass.setMinimumHeight(36)
        self.new_pass.setFont(QFont("Segoe UI", 12))

        self.confirm_pass = QLineEdit()
        self.confirm_pass.setEchoMode(QLineEdit.Password)
        self.confirm_pass.setPlaceholderText("تأكيد كلمة المرور")
        self.confirm_pass.setMinimumHeight(36)
        self.confirm_pass.setFont(QFont("Segoe UI", 12))

        layout.addRow("🔒 الحالية:", self.current_pass)
        layout.addRow("🔐 الجديدة:", self.new_pass)
        layout.addRow("🔐 التأكيد:", self.confirm_pass)

        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def get_data(self):
        return {
            "current": self.current_pass.text(),
            "new": self.new_pass.text(),
            "confirm": self.confirm_pass.text(),
        }


class ChangeUsernameDialog(QDialog):
    def __init__(self, parent=None, current_username=""):
        super().__init__(parent)
        self.setWindowTitle("تغيير اسم المستخدم")
        self.setLayoutDirection(Qt.RightToLeft)
        self.setMinimumWidth(320)

        layout = QFormLayout(self)
        layout.setSpacing(12)
        layout.setLabelAlignment(Qt.AlignRight)

        self.current_user = QLineEdit(current_username)
        self.current_user.setReadOnly(True)
        self.current_user.setMinimumHeight(36)
        self.current_user.setFont(QFont("Segoe UI", 12))

        self.new_username = QLineEdit()
        self.new_username.setPlaceholderText("اسم المستخدم الجديد")
        self.new_username.setMinimumHeight(36)
        self.new_username.setFont(QFont("Segoe UI", 12))

        self.password_confirm = QLineEdit()
        self.password_confirm.setEchoMode(QLineEdit.Password)
        self.password_confirm.setPlaceholderText("أدخل كلمة المرور للتأكيد")
        self.password_confirm.setMinimumHeight(36)
        self.password_confirm.setFont(QFont("Segoe UI", 12))

        layout.addRow("👤 الحالي:", self.current_user)
        layout.addRow("👤 الجديد:", self.new_username)
        layout.addRow("🔒 كلمة المرور:", self.password_confirm)

        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def get_data(self):
        return {
            "new_username": self.new_username.text().strip(),
            "password": self.password_confirm.text(),
        }


class SettingsPage(QWidget):
    def __init__(self, parent=None, db=None, current_user=None):
        super().__init__(parent)
        self.db = db
        self.current_user = current_user
        self._build_ui()
        self._load_settings()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(14)
        layout.setContentsMargins(0, 0, 0, 0)

        # Header
        header = QHBoxLayout()
        title = QLabel("⚙️ الإعدادات")
        title.setObjectName("pageTitle")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        header.addWidget(title)
        header.addStretch()
        layout.addLayout(header)

        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(14)

        # Currency Settings
        currency_group = QGroupBox("💱 إعدادات العملة")
        currency_group.setObjectName("settingsGroup")
        currency_layout = QFormLayout(currency_group)
        currency_layout.setSpacing(10)
        currency_layout.setLabelAlignment(Qt.AlignRight)

        self.currency_combo = QComboBox()
        self.currency_combo.setObjectName("settingsCombo")
        self.currency_combo.setMinimumHeight(36)
        self.currency_combo.setFont(QFont("Segoe UI", 12))
        self.currency_combo.addItem("🇮🇶 الدينار العراقي (IQD)", "IQD")
        self.currency_combo.addItem("🇺🇸 الدولار الأمريكي (USD)", "USD")
        self.currency_combo.addItem("🇸🇦 الريال السعودي (SAR)", "SAR")
        self.currency_combo.addItem("🇦🇪 الدرهم الإماراتي (AED)", "AED")
        self.currency_combo.addItem("🇰🇼 الدينار الكويتي (KWD)", "KWD")
        self.currency_combo.addItem("🇯🇴 الدينار الأردني (JOD)", "JOD")
        self.currency_combo.addItem("🇪🇬 الجنيه المصري (EGP)", "EGP")
        self.currency_combo.currentIndexChanged.connect(self.on_currency_changed)

        self.symbol_input = QLineEdit()
        self.symbol_input.setObjectName("settingsInput")
        self.symbol_input.setPlaceholderText("مثال: د.ع")
        self.symbol_input.setMinimumHeight(36)
        self.symbol_input.setFont(QFont("Segoe UI", 12))

        self.decimals_spin = QSpinBox()
        self.decimals_spin.setObjectName("settingsSpin")
        self.decimals_spin.setRange(0, 4)
        self.decimals_spin.setMinimumHeight(32)
        self.decimals_spin.setFont(QFont("Segoe UI", 12))

        currency_layout.addRow("العملة:", self.currency_combo)
        currency_layout.addRow("رمز العملة:", self.symbol_input)
        currency_layout.addRow("المنازل العشرية:", self.decimals_spin)

        scroll_layout.addWidget(currency_group)

        # Account Settings
        if self.current_user:
            account_group = QGroupBox("🔐 إعدادات الحساب")
            account_group.setObjectName("settingsGroup")
            account_layout = QVBoxLayout(account_group)
            account_layout.setSpacing(10)

            user_info = QLabel(f"المستخدم: <b>{self.current_user['username']}</b> ({self.current_user['role']})")
            user_info.setObjectName("userInfoLabel")
            user_info.setFont(QFont("Segoe UI", 12))
            account_layout.addWidget(user_info)

            btn_row = QHBoxLayout()

            change_pass_btn = QPushButton("🔐 تغيير كلمة المرور")
            change_pass_btn.setObjectName("secondaryBtn")
            change_pass_btn.setFixedHeight(40)
            change_pass_btn.setFont(QFont("Segoe UI", 11))
            change_pass_btn.setCursor(Qt.PointingHandCursor)
            change_pass_btn.clicked.connect(self.change_password)

            change_user_btn = QPushButton("👤 تغيير اسم المستخدم")
            change_user_btn.setObjectName("secondaryBtn")
            change_user_btn.setFixedHeight(40)
            change_user_btn.setFont(QFont("Segoe UI", 11))
            change_user_btn.setCursor(Qt.PointingHandCursor)
            change_user_btn.clicked.connect(self.change_username)

            btn_row.addWidget(change_pass_btn)
            btn_row.addWidget(change_user_btn)
            btn_row.addStretch()
            account_layout.addLayout(btn_row)

            scroll_layout.addWidget(account_group)

        # Display Settings
        display_group = QGroupBox("📊 إعدادات العرض")
        display_group.setObjectName("settingsGroup")
        display_layout = QFormLayout(display_group)
        display_layout.setSpacing(10)
        display_layout.setLabelAlignment(Qt.AlignRight)

        self.items_per_page = QSpinBox()
        self.items_per_page.setObjectName("settingsSpin")
        self.items_per_page.setRange(10, 500)
        self.items_per_page.setValue(50)
        self.items_per_page.setMinimumHeight(32)
        self.items_per_page.setFont(QFont("Segoe UI", 12))

        self.auto_refresh = QSpinBox()
        self.auto_refresh.setObjectName("settingsSpin")
        self.auto_refresh.setRange(0, 300)
        self.auto_refresh.setSuffix(" ثانية")
        self.auto_refresh.setValue(30)
        self.auto_refresh.setMinimumHeight(32)
        self.auto_refresh.setFont(QFont("Segoe UI", 12))

        display_layout.addRow("عناصر لكل صفحة:", self.items_per_page)
        display_layout.addRow("تحديث تلقائي:", self.auto_refresh)

        scroll_layout.addWidget(display_group)

        # Preview
        preview_group = QGroupBox("👁️ معاينة")
        preview_group.setObjectName("settingsGroup")
        preview_layout = QVBoxLayout(preview_group)

        self.preview_label = QLabel("1,250,000 د.ع")
        self.preview_label.setObjectName("previewLabel")
        self.preview_label.setFont(QFont("Segoe UI", 22, QFont.Bold))
        self.preview_label.setAlignment(Qt.AlignCenter)
        preview_layout.addWidget(self.preview_label)

        scroll_layout.addWidget(preview_group)

        # Buttons
        btn_row = QHBoxLayout()
        btn_row.addStretch()

        save_btn = QPushButton("💾 حفظ الإعدادات")
        save_btn.setObjectName("primaryBtn")
        save_btn.setFixedHeight(44)
        save_btn.setFont(QFont("Segoe UI", 13, QFont.Bold))
        save_btn.setCursor(Qt.PointingHandCursor)
        save_btn.clicked.connect(self.save_settings)

        reset_btn = QPushButton("🔄 استعادة الافتراضي")
        reset_btn.setObjectName("secondaryBtn")
        reset_btn.setFixedHeight(44)
        reset_btn.setFont(QFont("Segoe UI", 12))
        reset_btn.setCursor(Qt.PointingHandCursor)
        reset_btn.clicked.connect(self.reset_settings)

        btn_row.addWidget(reset_btn)
        btn_row.addWidget(save_btn)
        scroll_layout.addLayout(btn_row)

        scroll_layout.addStretch()
        layout.addWidget(scroll_widget)

        self.setStyleSheet("""
            #settingsGroup {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 14px;
                padding: 16px;
                font-weight: bold;
                font-size: 14px;
                color: #1e293b;
            }
            #settingsGroup::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px;
                color: #1e3a5f;
                font-size: 14px;
                font-weight: bold;
            }
            #settingsCombo {
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                padding: 6px;
                background: #f8fafc;
                font-size: 12px;
                min-height: 20px;
                min-width: 220px;
            }
            #settingsCombo:focus {
                border: 2px solid #3b82f6;
            }
            #settingsInput {
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                padding: 6px 10px;
                background: #f8fafc;
                font-size: 12px;
                min-height: 20px;
                min-width: 220px;
            }
            #settingsInput:focus {
                border: 2px solid #3b82f6;
                background: white;
            }
            #settingsSpin {
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                padding: 6px;
                background: #f8fafc;
                font-size: 12px;
                min-height: 20px;
                min-width: 220px;
            }
            #settingsSpin:focus {
                border: 2px solid #3b82f6;
            }
            #previewLabel {
                color: #3b82f6;
                padding: 16px;
                background: #f8fafc;
                border-radius: 10px;
            }
            #userInfoLabel {
                color: #475569;
                font-size: 12px;
                padding: 6px;
                background: #f8fafc;
                border-radius: 6px;
            }
            QFormLayout QLabel {
                color: #475569;
                font-size: 12px;
                font-weight: 500;
            }
        """)

    def on_currency_changed(self):
        currency_data = {
            "IQD": ("د.ع", 0),
            "USD": ("$", 2),
            "SAR": ("ر.س", 2),
            "AED": ("د.إ", 2),
            "KWD": ("د.ك", 3),
            "JOD": ("د.أ", 3),
            "EGP": ("ج.م", 2),
        }
        code = self.currency_combo.currentData()
        if code in currency_data:
            symbol, decimals = currency_data[code]
            self.symbol_input.setText(symbol)
            self.decimals_spin.setValue(decimals)
            self.update_preview()

    def update_preview(self):
        symbol = self.symbol_input.text() or "د.ع"
        decimals = self.decimals_spin.value()
        amount = 1250000
        if decimals == 0:
            preview = f"{amount:,} {symbol}"
        else:
            preview = f"{amount:,.{decimals}f} {symbol}"
        self.preview_label.setText(preview)

    def _load_settings(self):
        idx = self.currency_combo.findData(app_settings.get("currency", "IQD"))
        if idx >= 0:
            self.currency_combo.setCurrentIndex(idx)
        self.symbol_input.setText(app_settings.get("currency_symbol", "د.ع"))
        self.decimals_spin.setValue(app_settings.get("decimal_places", 0))
        self.items_per_page.setValue(app_settings.get("items_per_page", 50))
        self.auto_refresh.setValue(app_settings.get("auto_refresh", 30))
        self.update_preview()

    def save_settings(self):
        app_settings.set("currency", self.currency_combo.currentData())
        app_settings.set("currency_symbol", self.symbol_input.text())
        app_settings.set("decimal_places", self.decimals_spin.value())
        app_settings.set("items_per_page", self.items_per_page.value())
        app_settings.set("auto_refresh", self.auto_refresh.value())

        QMessageBox.information(self, "تم ✅", 
            "تم حفظ الإعدادات بنجاح!

سيتم تطبيق التغييرات في الصفحات الأخرى.")

    def reset_settings(self):
        confirm = QMessageBox.question(self, "تأكيد", 
            "هل تريد استعادة الإعدادات الافتراضية؟")
        if confirm == QMessageBox.Yes:
            import os
            config_file = os.path.join(os.path.dirname(__file__), "..", "app_settings.json")
            if os.path.exists(config_file):
                os.remove(config_file)
            app_settings.settings = {
                "currency": "IQD",
                "currency_symbol": "د.ع",
                "currency_name": "الدينار العراقي",
                "decimal_places": 0,
                "date_format": "%Y-%m-%d",
                "items_per_page": 50,
                "auto_refresh": 30,
                "theme": "light",
                "language": "ar",
            }
            app_settings.save()
            self._load_settings()
            QMessageBox.information(self, "تم ✅", "تم استعادة الإعدادات الافتراضية!")

    def change_password(self):
        if not self.db or not self.current_user:
            QMessageBox.warning(self, "تنبيه", "لا يوجد اتصال بقاعدة البيانات")
            return

        dialog = ChangePasswordDialog(self, self.current_user)
        if dialog.exec() == QDialog.Accepted:
            data = dialog.get_data()
            if not data["current"] or not data["new"]:
                QMessageBox.warning(self, "تنبيه", "جميع الحقول مطلوبة")
                return
            if data["new"] != data["confirm"]:
                QMessageBox.warning(self, "تنبيه", "كلمة المرور الجديدة غير متطابقة")
                return
            user = self.db.verify_user(self.current_user["username"], data["current"])
            if not user:
                QMessageBox.critical(self, "خطأ", "كلمة المرور الحالية غير صحيحة")
                return
            self.db.update_user_password(self.current_user["id"], data["new"])
            QMessageBox.information(self, "تم ✅", "تم تغيير كلمة المرور بنجاح!")

    def change_username(self):
        if not self.db or not self.current_user:
            QMessageBox.warning(self, "تنبيه", "لا يوجد اتصال بقاعدة البيانات")
            return

        dialog = ChangeUsernameDialog(self, self.current_user["username"])
        if dialog.exec() == QDialog.Accepted:
            data = dialog.get_data()
            if not data["new_username"]:
                QMessageBox.warning(self, "تنبيه", "اسم المستخدم الجديد مطلوب")
                return
            user = self.db.verify_user(self.current_user["username"], data["password"])
            if not user:
                QMessageBox.critical(self, "خطأ", "كلمة المرور غير صحيحة")
                return
            try:
                self.db.update_username(self.current_user["id"], data["new_username"])
                self.current_user["username"] = data["new_username"]
                QMessageBox.information(self, "تم ✅", 
                    f"تم تغيير اسم المستخدم بنجاح!

الاسم الجديد: {data['new_username']}

📝 يرجى تسجيل الخروج وإعادة الدخول.")
            except Exception as e:
                QMessageBox.critical(self, "خطأ", f"تعذر تغيير اسم المستخدم:
{e}")
