# -*- coding: utf-8 -*-
"""
إعدادات النظام - العملة والإعدادات العامة
"""
import json
import os

CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app_settings.json")

DEFAULT_SETTINGS = {
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

class Settings:
    def __init__(self):
        self.settings = DEFAULT_SETTINGS.copy()
        self.load()

    def load(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    self.settings.update(loaded)
            except:
                pass
        # Force light theme
        self.settings["theme"] = "light"

    def save(self):
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.settings, f, ensure_ascii=False, indent=2)

    def get(self, key, default=None):
        return self.settings.get(key, default)

    def set(self, key, value):
        self.settings[key] = value
        self.save()

    def format_currency(self, amount):
        symbol = self.settings["currency_symbol"]
        decimals = self.settings["decimal_places"]
        if decimals == 0:
            return f"{int(amount):,} {symbol}"
        return f"{amount:,.{decimals}f} {symbol}"

    def format_number(self, number):
        return f"{int(number):,}"

# Global instance
app_settings = Settings()
