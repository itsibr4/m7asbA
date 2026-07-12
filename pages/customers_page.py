# -*- coding: utf-8 -*-
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QDialog,
    QFormLayout, QDoubleSpinBox, QDialogButtonBox, QAbstractItemView
)
from PySide6.QtCore import Qt

from settings import app_settings


class CustomerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("إضافة عميل")
        self.setLayoutDirection(Qt.RightToLeft)
        form = QFormLayout(self)

        self.name_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.debt_input = QDoubleSpinBox()
        self.debt_input.setMaximum(1_000_000)

        form.addRow("اسم العميل:", self.name_input)
        form.addRow("رقم الجوال:", self.phone_input)
        form.addRow("دين مبدئي:", self.debt_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        form.addRow(buttons)

    def get_data(self):
        return {
            "name": self.name_input.text().strip(),
            "phone": self.phone_input.text().strip(),
            "debt": self.debt_input.value(),
        }


class CustomersPage(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        title = QLabel("إدارة العملاء")
        title.setObjectName("pageTitle")

        top_row = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("ابحث بالاسم أو الجوال...")
        self.search_input.setObjectName("searchBox")
        self.search_input.textChanged.connect(self.refresh)

        add_btn = QPushButton("+ إضافة عميل")
        add_btn.setObjectName("primaryBtn")
        add_btn.clicked.connect(self.add_customer)

        top_row.addWidget(self.search_input, 1)
        top_row.addWidget(add_btn)

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["الاسم", "الجوال", "الدين المستحق", "تسديد", "حذف"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        layout.addWidget(title)
        layout.addLayout(top_row)
        layout.addWidget(self.table)

    def refresh(self):
        search = self.search_input.text().strip()
        customers = self.db.list_customers(search if search else None)
        self.table.setRowCount(len(customers))
        for row, c in enumerate(customers):
            self.table.setItem(row, 0, QTableWidgetItem(c["name"]))
            self.table.setItem(row, 1, QTableWidgetItem(c["phone"] or "-"))
            debt_item = QTableWidgetItem(app_settings.format_currency(c["debt"]))
            if c["debt"] > 0:
                debt_item.setForeground(Qt.red)
            self.table.setItem(row, 2, debt_item)

            pay_btn = QPushButton("تسديد الكل")
            pay_btn.clicked.connect(lambda _, cid=c["id"], debt=c["debt"]: self.settle_debt(cid, debt))
            self.table.setCellWidget(row, 3, pay_btn)

            del_btn = QPushButton("حذف")
            del_btn.clicked.connect(lambda _, cid=c["id"]: self.delete_customer(cid))
            self.table.setCellWidget(row, 4, del_btn)

    def add_customer(self):
        dialog = CustomerDialog(self)
        if dialog.exec() == QDialog.Accepted:
            data = dialog.get_data()
            if not data["name"]:
                QMessageBox.warning(self, "تنبيه", "اسم العميل مطلوب")
                return
            self.db.add_customer(**data)
            self.refresh()

    def settle_debt(self, customer_id, debt):
        if debt <= 0:
            QMessageBox.information(self, "معلومة", "لا يوجد دين مستحق على هذا العميل")
            return
        confirm = QMessageBox.question(self, "تأكيد", f"تأكيد تسديد مبلغ {app_settings.format_currency(debt)}؟")
        if confirm == QMessageBox.Yes:
            self.db.update_customer_debt(customer_id, -debt)
            self.refresh()

    def delete_customer(self, customer_id):
        confirm = QMessageBox.question(self, "تأكيد", "هل تريد حذف هذا العميل؟")
        if confirm == QMessageBox.Yes:
            self.db.delete_customer(customer_id)
            self.refresh()
