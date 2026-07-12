# -*- coding: utf-8 -*-
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QDialog,
    QFormLayout, QComboBox, QDialogButtonBox, QAbstractItemView
)
from PySide6.QtCore import Qt

from settings import app_settings


class UserDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("إضافة مستخدم")
        self.setLayoutDirection(Qt.RightToLeft)
        form = QFormLayout(self)

        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.role_combo = QComboBox()
        self.role_combo.addItem("موظف", "employee")
        self.role_combo.addItem("مالك", "owner")

        form.addRow("اسم المستخدم:", self.username_input)
        form.addRow("كلمة المرور:", self.password_input)
        form.addRow("الصلاحية:", self.role_combo)

        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        form.addRow(buttons)

    def get_data(self):
        return {
            "username": self.username_input.text().strip(),
            "password": self.password_input.text(),
            "role": self.role_combo.currentData(),
        }


class UsersPage(QWidget):
    def __init__(self, db, current_user):
        super().__init__()
        self.db = db
        self.current_user = current_user
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        title = QLabel("إدارة المستخدمين")
        title.setObjectName("pageTitle")

        add_btn = QPushButton("+ إضافة مستخدم")
        add_btn.setObjectName("primaryBtn")
        add_btn.clicked.connect(self.add_user)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["اسم المستخدم", "الصلاحية", "تاريخ الإنشاء", "حذف"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        layout.addWidget(title)
        layout.addWidget(add_btn)
        layout.addWidget(self.table)

    def refresh(self):
        users = self.db.list_users()
        self.table.setRowCount(len(users))
        role_labels = {"owner": "مالك", "employee": "موظف"}
        for row, u in enumerate(users):
            self.table.setItem(row, 0, QTableWidgetItem(u["username"]))
            self.table.setItem(row, 1, QTableWidgetItem(role_labels.get(u["role"], u["role"])))
            self.table.setItem(row, 2, QTableWidgetItem(u["created_at"] or "-"))

            del_btn = QPushButton("حذف")
            if u["id"] == self.current_user["id"]:
                del_btn.setEnabled(False)
            del_btn.clicked.connect(lambda _, uid=u["id"]: self.delete_user(uid))
            self.table.setCellWidget(row, 3, del_btn)

    def add_user(self):
        dialog = UserDialog(self)
        if dialog.exec() == QDialog.Accepted:
            data = dialog.get_data()
            if not data["username"] or not data["password"]:
                QMessageBox.warning(self, "تنبيه", "اسم المستخدم وكلمة المرور مطلوبة")
                return
            try:
                self.db.add_user(**data)
            except Exception as e:
                QMessageBox.critical(self, "خطأ", f"تعذر إضافة المستخدم (ربما الاسم مكرر):\n{e}")
                return
            self.refresh()

    def delete_user(self, user_id):
        confirm = QMessageBox.question(self, "تأكيد", "هل تريد حذف هذا المستخدم؟")
        if confirm == QMessageBox.Yes:
            self.db.delete_user(user_id)
            self.refresh()
