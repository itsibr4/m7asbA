# -*- coding: utf-8 -*-
"""
صفحة الإعدادات - تغيير العملة والإعدادات العامة
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame,
    QComboBox, QSpinBox, QLineEdit, QFormLayout, QMessageBox, QCheckBox,
    QGroupBox, QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor

from settings import app_settings


class SettingsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()
        self._load_settings()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(0, 0, 0, 0)

        # Header
        header = QHBoxLayout()
        title = QLabel("⚙️ الإعدادات")
        title.setObjectName("pageTitle")
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        header.addWidget(title)
        header.addStretch()
        layout.addLayout(header)

        # Settings container
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(20)

        # ═══════════════════════════════════════
        # Currency Settings
        # ═══════════════════════════════════════
        currency_group = QGroupBox("💱 إعدادات العملة")
        currency_group.setObjectName("settingsGroup")
        currency_layout = QFormLayout(currency_group)
        currency_layout.setSpacing(14)
        currency_layout.setLabelAlignment(Qt.AlignRight)

        self.currency_combo = QComboBox()
        self.currency_combo.setObjectName("settingsCombo")
        self.currency_combo.setMinimumHeight(40)
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
        self.symbol_input.setMinimumHeight(40)

        self.decimals_spin = QSpinBox()
        self.decimals_spin.setObjectName("settingsSpin")
        self.decimals_spin.setRange(0, 4)
        self.decimals_spin.setMinimumHeight(36)

        currency_layout.addRow("العملة:", self.currency_combo)
        currency_layout.addRow("رمز العملة:", self.symbol_input)
        currency_layout.addRow("المنازل العشرية:", self.decimals_spin)

        scroll_layout.addWidget(currency_group)

        # ═══════════════════════════════════════
        # Display Settings
        # ═══════════════════════════════════════
        display_group = QGroupBox("📊 إعدادات العرض")
        display_group.setObjectName("settingsGroup")
        display_layout = QFormLayout(display_group)
        display_layout.setSpacing(14)
        display_layout.setLabelAlignment(Qt.AlignRight)

        self.items_per_page = QSpinBox()
        self.items_per_page.setObjectName("settingsSpin")
        self.items_per_page.setRange(10, 500)
        self.items_per_page.setValue(50)
        self.items_per_page.setMinimumHeight(36)

        self.auto_refresh = QSpinBox()
        self.auto_refresh.setObjectName("settingsSpin")
        self.auto_refresh.setRange(0, 300)
        self.auto_refresh.setSuffix(" ثانية")
        self.auto_refresh.setValue(30)
        self.auto_refresh.setMinimumHeight(36)

        display_layout.addRow("عناصر لكل صفحة:", self.items_per_page)
        display_layout.addRow("تحديث تلقائي:", self.auto_refresh)

        scroll_layout.addWidget(display_group)

        # ═══════════════════════════════════════
        # Preview
        # ═══════════════════════════════════════
        preview_group = QGroupBox("👁️ معاينة")
        preview_group.setObjectName("settingsGroup")
        preview_layout = QVBoxLayout(preview_group)

        self.preview_label = QLabel("1,250,000 د.ع")
        self.preview_label.setObjectName("previewLabel")
        self.preview_label.setFont(QFont("Segoe UI", 24, QFont.Bold))
        self.preview_label.setAlignment(Qt.AlignCenter)
        preview_layout.addWidget(self.preview_label)

        scroll_layout.addWidget(preview_group)

        # ═══════════════════════════════════════
        # Buttons
        # ═══════════════════════════════════════
        btn_row = QHBoxLayout()
        btn_row.addStretch()

        save_btn = QPushButton("💾 حفظ الإعدادات")
        save_btn.setObjectName("primaryBtn")
        save_btn.setFixedHeight(48)
        save_btn.setFont(QFont("Segoe UI", 14, QFont.Bold))
        save_btn.setCursor(Qt.PointingHandCursor)
        save_btn.clicked.connect(self.save_settings)

        reset_btn = QPushButton("🔄 استعادة الافتراضي")
        reset_btn.setObjectName("secondaryBtn")
        reset_btn.setFixedHeight(48)
        reset_btn.setCursor(Qt.PointingHandCursor)
        reset_btn.clicked.connect(self.reset_settings)

        btn_row.addWidget(reset_btn)
        btn_row.addWidget(save_btn)
        scroll_layout.addLayout(btn_row)

        scroll_layout.addStretch()
        layout.addWidget(scroll_widget)

        # Styles
        self.setStyleSheet("""
            #settingsGroup {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 16px;
                padding: 20px;
                font-weight: bold;
                font-size: 15px;
                color: #1e293b;
            }
            #settingsGroup::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px;
                color: #1e3a5f;
                font-size: 16px;
                font-weight: bold;
            }
            #settingsCombo {
                border: 2px solid #e2e8f0;
                border-radius: 10px;
                padding: 8px;
                background: #f8fafc;
                font-size: 14px;
                min-height: 24px;
                min-width: 250px;
            }
            #settingsCombo:focus {
                border: 2px solid #3b82f6;
            }
            #settingsInput {
                border: 2px solid #e2e8f0;
                border-radius: 10px;
                padding: 8px 12px;
                background: #f8fafc;
                font-size: 14px;
                min-height: 24px;
                min-width: 250px;
            }
            #settingsInput:focus {
                border: 2px solid #3b82f6;
                background: white;
            }
            #settingsSpin {
                border: 2px solid #e2e8f0;
                border-radius: 10px;
                padding: 8px;
                background: #f8fafc;
                font-size: 14px;
                min-height: 24px;
                min-width: 250px;
            }
            #settingsSpin:focus {
                border: 2px solid #3b82f6;
            }
            #previewLabel {
                color: #3b82f6;
                padding: 20px;
                background: #f8fafc;
                border-radius: 12px;
            }
            QFormLayout QLabel {
                color: #475569;
                font-size: 14px;
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
            "تم حفظ الإعدادات بنجاح!\n\nسيتم تطبيق التغييرات في الصفحات الأخرى.")

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
                "theme": "blue",
                "language": "ar",
            }
            app_settings.save()
            self._load_settings()
            QMessageBox.information(self, "تم ✅", "تم استعادة الإعدادات الافتراضية!")
