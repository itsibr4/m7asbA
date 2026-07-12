# -*- coding: utf-8 -*-
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox,
    QSpinBox, QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView,
    QMessageBox, QAbstractItemView
)
from PySide6.QtCore import Qt

from settings import app_settings


class InventoryPage(QWidget):
    def __init__(self, db, on_change=None):
        super().__init__()
        self.db = db
        self.on_change = on_change
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(14)

        title = QLabel("إدارة المخزون")
        title.setObjectName("pageTitle")

        # تنبيهات نفاد المخزون
        self.low_stock_label = QLabel()
        self.low_stock_label.setObjectName("warningLabel")
        self.low_stock_label.setWordWrap(True)

        # نموذج إضافة حركة مخزون
        form_row = QHBoxLayout()
        self.product_combo = QComboBox()
        self.movement_combo = QComboBox()
        self.movement_combo.addItem("وارد (إضافة كمية)", "in")
        self.movement_combo.addItem("صادر (سحب كمية)", "out")
        self.movement_combo.addItem("تعديل الكمية لقيمة محددة", "adjustment")

        self.quantity_input = QSpinBox()
        self.quantity_input.setMaximum(1_000_000)

        self.note_input = QLineEdit()
        self.note_input.setPlaceholderText("ملاحظة (اختياري)")

        add_btn = QPushButton("تنفيذ الحركة")
        add_btn.setObjectName("primaryBtn")
        add_btn.clicked.connect(self.apply_movement)

        form_row.addWidget(QLabel("المنتج:"))
        form_row.addWidget(self.product_combo, 2)
        form_row.addWidget(QLabel("النوع:"))
        form_row.addWidget(self.movement_combo, 1)
        form_row.addWidget(QLabel("الكمية:"))
        form_row.addWidget(self.quantity_input, 1)
        form_row.addWidget(self.note_input, 2)
        form_row.addWidget(add_btn)

        history_title = QLabel("سجل حركة المخزون")
        history_title.setObjectName("sectionTitle")

        self.history_table = QTableWidget(0, 5)
        self.history_table.setHorizontalHeaderLabels(["المنتج", "النوع", "الكمية", "ملاحظة", "التاريخ"])
        self.history_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.history_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        layout.addWidget(title)
        layout.addWidget(self.low_stock_label)
        layout.addLayout(form_row)
        layout.addWidget(history_title)
        layout.addWidget(self.history_table)

    def refresh(self):
        self._refresh_low_stock()
        self._refresh_product_combo()
        self._refresh_history()

    def _refresh_low_stock(self):
        low = self.db.low_stock_products()
        if low:
            names = "، ".join(p["name"] for p in low)
            self.low_stock_label.setText(f"⚠ منتجات وصلت لحد النفاد: {names}")
        else:
            self.low_stock_label.setText("لا توجد منتجات بحاجة لتنبيه حاليًا ✔")

    def _refresh_product_combo(self):
        current = self.product_combo.currentData()
        self.product_combo.clear()
        for p in self.db.list_products():
            self.product_combo.addItem(f"{p['name']} (متوفر: {p['quantity']})", p["id"])
        if current:
            idx = self.product_combo.findData(current)
            if idx >= 0:
                self.product_combo.setCurrentIndex(idx)

    def _refresh_history(self):
        history = self.db.stock_history()
        self.history_table.setRowCount(len(history))
        type_labels = {"in": "وارد", "out": "صادر", "adjustment": "تعديل"}
        for row, h in enumerate(history):
            self.history_table.setItem(row, 0, QTableWidgetItem(h["product_name"]))
            self.history_table.setItem(row, 1, QTableWidgetItem(type_labels.get(h["movement_type"], h["movement_type"])))
            self.history_table.setItem(row, 2, QTableWidgetItem(str(h["quantity"])))
            self.history_table.setItem(row, 3, QTableWidgetItem(h["note"] or "-"))
            self.history_table.setItem(row, 4, QTableWidgetItem(h["created_at"]))

    def apply_movement(self):
        product_id = self.product_combo.currentData()
        if not product_id:
            QMessageBox.warning(self, "تنبيه", "الرجاء اختيار منتج")
            return
        movement_type = self.movement_combo.currentData()
        quantity = self.quantity_input.value()
        note = self.note_input.text().strip()

        if movement_type in ("in", "out") and quantity <= 0:
            QMessageBox.warning(self, "تنبيه", "الكمية يجب أن تكون أكبر من صفر")
            return

        if movement_type == "out":
            product = self.db.get_product(product_id)
            if product["quantity"] < quantity:
                QMessageBox.warning(self, "تنبيه", "الكمية المطلوب سحبها أكبر من المتوفر")
                return

        self.db.add_stock_movement(product_id, movement_type, quantity, note)
        self.quantity_input.setValue(0)
        self.note_input.clear()
        self.refresh()
        if self.on_change:
            self.on_change()
