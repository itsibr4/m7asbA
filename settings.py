# -*- coding: utf-8 -*-
"""
إعدادات النظام - العملة والإعدادات العامة + نظام الثيمات
"""
import json
import os

CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app_settings.json")

DEFAULT_SETTINGS = {
    "currency": "IQD",           # العملة: IQD, USD, SAR, etc.
    "currency_symbol": "د.ع",     # رمز العملة
    "currency_name": "الدينار العراقي",
    "decimal_places": 0,          # عدد المنازل العشرية (0 للدينار)
    "date_format": "%Y-%m-%d",
    "items_per_page": 50,         # عدد العناصر في الصفحة
    "auto_refresh": 30,           # التحديث التلقائي (ثواني)
    "theme": "dark",              # dark أو light
    "language": "ar",             # اللغة
}

# ═══════════════════════════════════════
# أنظمة الألوان - Dark & Light
# ═══════════════════════════════════════

LIGHT_THEME = {
    "name": "light",
    "bg_primary": "#f1f5f9",
    "bg_secondary": "#ffffff",
    "bg_card": "#ffffff",
    "text_primary": "#1e293b",
    "text_secondary": "#64748b",
    "text_muted": "#94a3b8",
    "border": "#e2e8f0",
    "border_focus": "#3b82f6",
    "sidebar_bg": "#1e293b",
    "sidebar_text": "#cbd5e1",
    "sidebar_text_active": "#ffffff",
    "sidebar_hover": "#334155",
    "accent": "#3b82f6",
    "success": "#10b981",
    "warning": "#f59e0b",
    "danger": "#ef4444",
    "input_bg": "#f8fafc",
    "table_header": "#f8fafc",
    "table_alt": "#f8fafc",
    "shadow": "rgba(0,0,0,0.05)",
    "gradient_start": "#3b82f6",
    "gradient_end": "#2563eb",
}

DARK_THEME = {
    "name": "dark",
    "bg_primary": "#0f172a",
    "bg_secondary": "#1e293b",
    "bg_card": "#1e293b",
    "text_primary": "#f1f5f9",
    "text_secondary": "#94a3b8",
    "text_muted": "#64748b",
    "border": "#334155",
    "border_focus": "#60a5fa",
    "sidebar_bg": "#020617",
    "sidebar_text": "#94a3b8",
    "sidebar_text_active": "#ffffff",
    "sidebar_hover": "#1e293b",
    "accent": "#60a5fa",
    "success": "#34d399",
    "warning": "#fbbf24",
    "danger": "#f87171",
    "input_bg": "#334155",
    "table_header": "#1e293b",
    "table_alt": "#27354f",
    "shadow": "rgba(0,0,0,0.3)",
    "gradient_start": "#3b82f6",
    "gradient_end": "#60a5fa",
}

class Settings:
    def __init__(self):
        self.settings = DEFAULT_SETTINGS.copy()
        self.load()
        self._theme = DARK_THEME if self.settings.get("theme") == "dark" else LIGHT_THEME

    @property
    def theme(self):
        return self._theme

    def load(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    self.settings.update(loaded)
            except:
                pass
        self._theme = DARK_THEME if self.settings.get("theme") == "dark" else LIGHT_THEME

    def save(self):
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.settings, f, ensure_ascii=False, indent=2)

    def get(self, key, default=None):
        return self.settings.get(key, default)

    def set(self, key, value):
        self.settings[key] = value
        if key == "theme":
            self._theme = DARK_THEME if value == "dark" else LIGHT_THEME
        self.save()

    def format_currency(self, amount):
        """تنسيق المبلغ بالعملة المختارة"""
        symbol = self.settings["currency_symbol"]
        decimals = self.settings["decimal_places"]
        if decimals == 0:
            return f"{int(amount):,} {symbol}"
        return f"{amount:,.{decimals}f} {symbol}"

    def format_number(self, number):
        """تنسيق الرقم بفواصل الآلاف"""
        return f"{int(number):,}"

# Global instance
app_settings = Settings()
