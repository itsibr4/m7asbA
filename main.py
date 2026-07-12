# -*- coding: utf-8 -*-
"""
نظام إدارة المبيعات - نقطة تشغيل البرنامج
"""
import sys
import os

# Add current directory to path so 'pages' package can be found
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication

from database import Database
from login_window import LoginWindow
from main_window import MainWindow


class AppController:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.db = Database()
        self.login_window = None
        self.main_window = None
        self.show_login()

    def show_login(self):
        self.login_window = LoginWindow(self.db)
        self.login_window.login_success.connect(self.show_main_window)
        self.login_window.show()

    def show_main_window(self, user):
        self.login_window.close()
        self.main_window = MainWindow(self.db, user, on_logout=self.show_login)
        self.main_window.show()

    def run(self):
        sys.exit(self.app.exec())


if __name__ == "__main__":
    controller = AppController()
    controller.run()
