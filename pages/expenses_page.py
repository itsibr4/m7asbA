# -*- coding: utf-8 -*-
"""
صفحة المصاريف الشهرية
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QDialog,
    QFormLayout, QDoubleSpinBox, QDateEdit, QDialogButtonBox, QAbstractItemView,
    QFrame, QGraphicsDropShadowEffect, QScrollArea
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont, QColor

from settings import app_settings


class ExpenseDialog(QDialog):
    def __init__(self, parent=None, expense=None):
        super().__init__(parent)
        self.setWindowTitle("إضافة مصروف" if expense is None else "تعديل مصروف")
        self.setLayoutDirection(Qt.RightToLeft)
        self.setMinimumWidth(400)
        self.expense = expense

        layout = QFormLayout(self)
        layout.setSpacing(14)
        layout.setLabelAlignment(Qt.AlignRight)

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("مثال: إيجار المحل، كهرباء، رواتب...")
        self.title_input.setMinimumHeight(40)

        self.amount_input = QDoubleSpinBox()
        self.amount_input.setMaximum(100_000_000)
        self.amount_input.setSuffix(f" {app_settings.get('currency_symbol', 'د.ع')}")
        self.amount_input.setDecimals(app_settings.get('decimal_places', 0))
        self.amount_input.setMinimumHeight(36)

        self.date_input = QDateEdit(calendarPopup=True)
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setMinimumHeight(36)

        self.note_input = QLineEdit()
        self.note_input.setPlaceholderText("ملاحظة اختيارية...")
        self.note_input.setMinimumHeight(40)

        layout.addRow("🏷️ عنوان المصروف:", self.title_input)
        layout.addRow(f"💰 المبلغ ({app_settings.get('currency_symbol', 'د.ع')}):", self.amount_input)
        layout.addRow("📅 التاريخ:", self.date_input)
        layout.addRow("📝 ملاحظة:", self.note_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

        if expense:
            self.title_input.setText(expense.get("title", ""))
            self.amount_input.setValue(expense.get("amount", 0))
            if expense.get("expense_date"):
                try:
                    d = QDate.fromString(expense["expense_date"][:10], "yyyy-MM-dd")
                    if d.isValid():
                        self.date_input.setDate(d)
                except:
                    pass
            self.note_input.setText(expense.get("note", ""))

    def get_data(self):
        return {
            "title": self.title_input.text().strip(),
            "amount": self.amount_input.value(),
            "expense_date": self.date_input.date().toString("yyyy-MM-dd"),
            "note": self.note_input.text().strip(),
        }


class ExpensesPage(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(0, 0, 0, 0)

        # Header
        header = QHBoxLayout()
        title = QLabel("💸 المصاريف الشهرية")
        title.setObjectName("pageTitle")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))

        self.total_label = QLabel("إجمالي المصاريف: 0")
        self.total_label.setObjectName("statBadge")

        header.addWidget(title)
        header.addStretch()
        header.addWidget(self.total_label)
        layout.addLayout(header)

        # Filter row
        filter_card = QFrame()
        filter_card.setObjectName("filterCard")
        filter_layout = QHBoxLayout(filter_card)
        filter_layout.setContentsMargins(20, 16, 20, 16)
        filter_layout.setSpacing(12)

        from_label = QLabel("📅 من:")
        from_label.setObjectName("filterLabel")
        self.date_from = QDateEdit(calendarPopup=True)
        self.date_from.setDate(QDate.currentDate().addMonths(-1))
        self.date_from.setMinimumHeight(36)

        to_label = QLabel("إلى:")
        to_label.setObjectName("filterLabel")
        self.date_to = QDateEdit(calendarPopup=True)
        self.date_to.setDate(QDate.currentDate())
        self.date_to.setMinimumHeight(36)

        apply_btn = QPushButton("🔍 عرض")
        apply_btn.setObjectName("primaryBtn")
        apply_btn.setFixedHeight(40)
        apply_btn.setCursor(Qt.PointingHandCursor)
        apply_btn.clicked.connect(self.refresh)

        month_btn = QPushButton("📊 هذا الشهر")
        month_btn.setObjectName("filterBtn")
        month_btn.setFixedHeight(40)
        month_btn.setCursor(Qt.PointingHandCursor)
        month_btn.clicked.connect(self.set_this_month)

        filter_layout.addWidget(from_label)
        filter_layout.addWidget(self.date_from)
        filter_layout.addWidget(to_label)
        filter_layout.addWidget(self.date_to)
        filter_layout.addWidget(apply_btn)
        filter_layout.addWidget(month_btn)
        filter_layout.addStretch()

        layout.addWidget(filter_card)

        # Add button
        add_btn = QPushButton("+ إضافة مصروف")
        add_btn.setObjectName("primaryBtn")
        add_btn.setFixedHeight(44)
        add_btn.setCursor(Qt.PointingHandCursor)
        add_btn.clicked.connect(self.add_expense)
        layout.addWidget(add_btn)

        # Table
        table_scroll = QScrollArea()
        table_scroll.setWidgetResizable(True)
        table_scroll.setFrameShape(QFrame.NoFrame)
        table_scroll.setStyleSheet("background: transparent; border: none;")

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["العنوان", "المبلغ", "التاريخ", "الملاحظة", "حذف"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)

        table_scroll.setWidget(self.table)
        layout.addWidget(table_scroll, 1)

        # Summary card
        summary_card = QFrame()
        summary_card.setObjectName("summaryCard")
        summary_layout = QHBoxLayout(summary_card)
        summary_layout.setContentsMargins(20, 16, 20, 16)

        self.summary_sales = QLabel("المبيعات: 0")
        self.summary_sales.setObjectName("summaryLabel")
        self.summary_profit = QLabel("الربح الإجمالي: 0")
        self.summary_profit.setObjectName("summaryLabel")
        self.summary_expenses = QLabel("المصاريف: 0")
        self.summary_expenses.setObjectName("summaryLabel")
        self.summary_net = QLabel("صافي الربح: 0")
        self.summary_net.setObjectName("summaryLabel")
        self.summary_net.setFont(QFont("Segoe UI", 14, QFont.Bold))

        summary_layout.addWidget(self.summary_sales)
        summary_layout.addWidget(self.summary_profit)
        summary_layout.addWidget(self.summary_expenses)
        summary_layout.addWidget(self.summary_net)
        summary_layout.addStretch()

        layout.addWidget(summary_card)

        self.setStyleSheet("""
            #filterCard {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 16px;
            }
            #filterLabel {
                color: #475569;
                font-size: 13px;
                font-weight: 500;
            }
            #filterBtn {
                background: #f8fafc;
                color: #475569;
                border: 1.5px solid #cbd5e1;
                border-radius: 10px;
                padding: 8px 16px;
                font-size: 13px;
                font-weight: 500;
            }
            #filterBtn:hover {
                background: #e2e8f0;
                border-color: #94a3b8;
            }
            #statBadge {
                color: #64748b;
                font-size: 13px;
                background: #f8fafc;
                padding: 8px 16px;
                border-radius: 20px;
                border: 1px solid #e2e8f0;
            }
            #summaryCard {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 16px;
            }
            #summaryLabel {
                color: #475569;
                font-size: 14px;
                font-weight: 500;
                padding: 8px 16px;
                background: #f8fafc;
                border-radius: 10px;
                margin: 0 4px;
            }
        """)

    def set_this_month(self):
        today = QDate.currentDate()
        self.date_from.setDate(QDate(today.year(), today.month(), 1))
        self.date_to.setDate(today)
        self.refresh()

    def refresh(self):
        date_from = self.date_from.date().toString("yyyy-MM-dd") + " 00:00:00"
        date_to = self.date_to.date().toString("yyyy-MM-dd") + " 23:59:59"

        expenses = self.db.list_expenses(date_from, date_to)
        self.table.setRowCount(len(expenses))
        total = 0

        for row, e in enumerate(expenses):
            self.table.setItem(row, 0, QTableWidgetItem(e["title"]))
            amount_item = QTableWidgetItem(app_settings.format_currency(e["amount"]))
            amount_item.setForeground(Qt.red)
            self.table.setItem(row, 1, amount_item)
            self.table.setItem(row, 2, QTableWidgetItem(e["expense_date"][:10] if e["expense_date"] else "-"))
            self.table.setItem(row, 3, QTableWidgetItem(e["note"] or "-"))

            del_btn = QPushButton("🗑️ حذف")
            del_btn.setObjectName("dangerBtn")
            del_btn.setFixedHeight(32)
            del_btn.clicked.connect(lambda _, eid=e["id"]: self.delete_expense(eid))
            self.table.setCellWidget(row, 4, del_btn)
            total += e["amount"]

        self.total_label.setText(f"إجمالي المصاريف: {app_settings.format_currency(total)}")

        # Update summary
        summary = self.db.profit_after_expenses(date_from, date_to)
        self.summary_sales.setText(f"💰 المبيعات: {app_settings.format_currency(summary['total_sales'])}")
        self.summary_profit.setText(f"📈 الربح الإجمالي: {app_settings.format_currency(summary['gross_profit'])}")
        self.summary_expenses.setText(f"💸 المصاريف: {app_settings.format_currency(summary['total_expenses'])}")
        self.summary_net.setText(f"💵 صافي الربح: {app_settings.format_currency(summary['net_profit'])}")

        if summary['net_profit'] >= 0:
            self.summary_net.setStyleSheet("color: #10b981; font-weight: bold; font-size: 14px; padding: 8px 16px; background: #f8fafc; border-radius: 10px;")
        else:
            self.summary_net.setStyleSheet("color: #ef4444; font-weight: bold; font-size: 14px; padding: 8px 16px; background: #f8fafc; border-radius: 10px;")

    def add_expense(self):
        dialog = ExpenseDialog(self)
        if dialog.exec() == QDialog.Accepted:
            data = dialog.get_data()
            if not data["title"]:
                QMessageBox.warning(self, "تنبيه", "عنوان المصروف مطلوب")
                return
            self.db.add_expense(**data)
            self.refresh()

    def delete_expense(self, expense_id):
        confirm = QMessageBox.question(self, "تأكيد", "هل تريد حذف هذا المصروف؟")
        if confirm == QMessageBox.Yes:
            self.db.delete_expense(expense_id)
            self.refresh()
