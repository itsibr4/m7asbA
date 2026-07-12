# -*- coding: utf-8 -*-
"""
صفحة المنتجات - تصميم احترافي مع الدينار العراقي ودعم +1000 منتج
+ حقول إضافية: نوع المنتج، سنة الإصدار
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QDialog,
    QFormLayout, QDoubleSpinBox, QSpinBox, QDialogButtonBox, QAbstractItemView,
    QFrame, QGraphicsDropShadowEffect, QScrollArea, QComboBox
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QColor

from settings import app_settings


class ProductDialog(QDialog):
    def __init__(self, parent=None, product=None):
        super().__init__(parent)
        self.setWindowTitle("إضافة منتج جديد" if product is None else "تعديل منتج")
        self.setLayoutDirection(Qt.RightToLeft)
        self.setMinimumWidth(420)
        self.setMinimumHeight(560)
        self.product = product

        self._build_ui()
        self._apply_dialog_styles()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)

        header = QLabel("📦 إضافة منتج جديد" if self.product is None else "✏️ تعديل منتج")
        header.setObjectName("dialogHeader")
        header.setFont(QFont("Segoe UI", 18, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)

        form = QFormLayout()
        form.setSpacing(14)
        form.setLabelAlignment(Qt.AlignRight)
        form.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)

        self.name_input = QLineEdit(self.product["name"] if self.product else "")
        self.name_input.setPlaceholderText("أدخل اسم المنتج")
        self.name_input.setObjectName("dialogInput")
        self.name_input.setMinimumHeight(40)

        self.barcode_input = QLineEdit(self.product["barcode"] if self.product and self.product["barcode"] else "")
        self.barcode_input.setPlaceholderText("أدخل الباركود (اختياري)")
        self.barcode_input.setObjectName("dialogInput")
        self.barcode_input.setMinimumHeight(40)

        self.category_input = QLineEdit(self.product["category"] if self.product and self.product["category"] else "")
        self.category_input.setPlaceholderText("أدخل التصنيف (اختياري)")
        self.category_input.setObjectName("dialogInput")
        self.category_input.setMinimumHeight(40)

        # NEW: Product Type
        self.product_type_input = QLineEdit(self.product["product_type"] if self.product and self.product.get("product_type") else "")
        self.product_type_input.setPlaceholderText("مثال: إلكترونيات، ملابس، أدوات...")
        self.product_type_input.setObjectName("dialogInput")
        self.product_type_input.setMinimumHeight(40)

        # NEW: Year
        self.year_input = QSpinBox()
        self.year_input.setRange(1900, 2100)
        self.year_input.setValue(self.product["year"] if self.product and self.product.get("year") else 2026)
        self.year_input.setObjectName("dialogSpin")
        self.year_input.setMinimumHeight(36)

        symbol = app_settings.get("currency_symbol", "د.ع")
        decimals = app_settings.get("decimal_places", 0)

        self.purchase_price = QDoubleSpinBox()
        self.purchase_price.setMaximum(1_000_000_000)
        self.purchase_price.setValue(self.product["purchase_price"] if self.product else 0)
        self.purchase_price.setSuffix(f" {symbol}")
        self.purchase_price.setDecimals(decimals)
        self.purchase_price.setObjectName("dialogSpin")
        self.purchase_price.setMinimumHeight(36)

        self.sale_price = QDoubleSpinBox()
        self.sale_price.setMaximum(1_000_000_000)
        self.sale_price.setValue(self.product["sale_price"] if self.product else 0)
        self.sale_price.setSuffix(f" {symbol}")
        self.sale_price.setDecimals(decimals)
        self.sale_price.setObjectName("dialogSpin")
        self.sale_price.setMinimumHeight(36)

        self.quantity = QSpinBox()
        self.quantity.setMaximum(1_000_000_000)
        self.quantity.setValue(self.product["quantity"] if self.product else 0)
        self.quantity.setObjectName("dialogSpin")
        self.quantity.setMinimumHeight(36)

        self.min_quantity = QSpinBox()
        self.min_quantity.setMaximum(1_000_000_000)
        self.min_quantity.setValue(self.product["min_quantity"] if self.product else 0)
        self.min_quantity.setObjectName("dialogSpin")
        self.min_quantity.setMinimumHeight(36)

        form.addRow("🏷️ اسم المنتج:", self.name_input)
        form.addRow("📊 الباركود:", self.barcode_input)
        form.addRow("📁 التصنيف:", self.category_input)
        form.addRow("📂 نوع المنتج:", self.product_type_input)
        form.addRow("📅 سنة الإصدار:", self.year_input)
        form.addRow(f"💰 سعر الشراء ({symbol}):", self.purchase_price)
        form.addRow(f"💵 سعر البيع ({symbol}):", self.sale_price)
        form.addRow("📦 الكمية:", self.quantity)
        form.addRow("⚠️ حد التنبيه:", self.min_quantity)

        layout.addLayout(form)
        layout.addStretch()

        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _apply_dialog_styles(self):
        self.setStyleSheet("""
            QDialog { background: #ffffff; }
            #dialogHeader {
                color: #1e3a5f;
                margin-bottom: 8px;
            }
            #dialogInput {
                border: 2px solid #e2e8f0;
                border-radius: 10px;
                padding: 8px 12px;
                background: #f8fafc;
                font-size: 14px;
                color: #1e293b;
                min-height: 24px;
            }
            #dialogInput:focus {
                border: 2px solid #3b82f6;
                background: #ffffff;
            }
            #dialogInput::placeholder {
                color: #94a3b8;
            }
            #dialogSpin {
                border: 2px solid #e2e8f0;
                border-radius: 10px;
                padding: 8px;
                background: #f8fafc;
                font-size: 14px;
                min-height: 24px;
            }
            #dialogSpin:focus {
                border: 2px solid #3b82f6;
            }
            QFormLayout QLabel {
                color: #475569;
                font-size: 13px;
                font-weight: 500;
            }
            QDialogButtonBox QPushButton {
                padding: 10px 24px;
                border-radius: 10px;
                font-weight: 500;
                font-size: 14px;
                min-width: 100px;
            }
            QDialogButtonBox QPushButton[text="Save"] {
                background: #3b82f6;
                color: white;
                border: none;
            }
            QDialogButtonBox QPushButton[text="Save"]:hover {
                background: #2563eb;
            }
            QDialogButtonBox QPushButton[text="Cancel"] {
                background: #f1f5f9;
                color: #475569;
                border: 1.5px solid #cbd5e1;
            }
            QDialogButtonBox QPushButton[text="Cancel"]:hover {
                background: #e2e8f0;
            }
        """)

    def get_data(self):
        return {
            "name": self.name_input.text().strip(),
            "barcode": self.barcode_input.text().strip() or None,
            "category": self.category_input.text().strip(),
            "product_type": self.product_type_input.text().strip(),
            "year": self.year_input.value(),
            "purchase_price": self.purchase_price.value(),
            "sale_price": self.sale_price.value(),
            "quantity": self.quantity.value(),
            "min_quantity": self.min_quantity.value(),
        }


class ProductsPage(QWidget):
    def __init__(self, db, on_change=None):
        super().__init__()
        self.db = db
        self.on_change = on_change
        self.current_page = 0
        self.items_per_page = app_settings.get("items_per_page", 50)
        self.all_products = []
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(0, 0, 0, 0)

        # Header
        header = QHBoxLayout()
        title = QLabel("📦 إدارة المنتجات")
        title.setObjectName("pageTitle")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))

        self.product_count = QLabel("إجمالي المنتجات: 0")
        self.product_count.setObjectName("statBadge")

        header.addWidget(title)
        header.addStretch()
        header.addWidget(self.product_count)
        layout.addLayout(header)

        # Search and add button row
        top_row = QHBoxLayout()
        top_row.setSpacing(12)

        search_container = QFrame()
        search_container.setObjectName("searchContainer")
        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(12, 4, 12, 4)
        search_layout.setSpacing(8)

        search_icon = QLabel("🔍")
        search_icon.setObjectName("searchIcon")

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("ابحث بالاسم أو الباركود أو النوع...")
        self.search_input.setObjectName("searchBox")
        self.search_input.setFixedHeight(44)
        self.search_input.textChanged.connect(self.on_search)

        search_layout.addWidget(search_icon)
        search_layout.addWidget(self.search_input, 1)

        add_btn = QPushButton("+ إضافة منتج")
        add_btn.setObjectName("primaryBtn")
        add_btn.setFixedHeight(44)
        add_btn.setCursor(Qt.PointingHandCursor)
        add_btn.clicked.connect(self.add_product)

        top_row.addWidget(search_container, 1)
        top_row.addWidget(add_btn)
        layout.addLayout(top_row)

        # Table with scrollbars
        table_scroll = QScrollArea()
        table_scroll.setWidgetResizable(True)
        table_scroll.setFrameShape(QFrame.NoFrame)
        table_scroll.setStyleSheet("background: transparent; border: none;")

        self.table = QTableWidget(0, 10)
        self.table.setHorizontalHeaderLabels(
            ["المنتج", "الباركود", "التصنيف", "النوع", "السنة", "سعر الشراء", "سعر البيع", "الكمية", "تعديل", "حذف"]
        )
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        table_scroll.setWidget(self.table)
        layout.addWidget(table_scroll, 1)

        # Pagination
        pagination = QHBoxLayout()
        pagination.setSpacing(8)

        self.prev_btn = QPushButton("◀ السابق")
        self.prev_btn.setObjectName("paginationBtn")
        self.prev_btn.setFixedHeight(36)
        self.prev_btn.setCursor(Qt.PointingHandCursor)
        self.prev_btn.clicked.connect(self.prev_page)

        self.page_label = QLabel("صفحة 1 من 1")
        self.page_label.setObjectName("pageLabel")
        self.page_label.setAlignment(Qt.AlignCenter)

        self.next_btn = QPushButton("التالي ▶")
        self.next_btn.setObjectName("paginationBtn")
        self.next_btn.setFixedHeight(36)
        self.next_btn.setCursor(Qt.PointingHandCursor)
        self.next_btn.clicked.connect(self.next_page)

        self.page_size_combo = QComboBox()
        self.page_size_combo.setObjectName("pageSizeCombo")
        self.page_size_combo.addItems(["25", "50", "100", "200", "500"])
        self.page_size_combo.setCurrentText(str(self.items_per_page))
        self.page_size_combo.currentTextChanged.connect(self.on_page_size_changed)
        self.page_size_combo.setFixedHeight(36)

        pagination.addWidget(self.prev_btn)
        pagination.addWidget(self.page_label, 1)
        pagination.addWidget(self.next_btn)
        pagination.addWidget(QLabel("عرض:"))
        pagination.addWidget(self.page_size_combo)

        layout.addLayout(pagination)

        # Page styles
        self.setStyleSheet("""
            #searchContainer {
                background: #f8fafc;
                border: 2px solid #e2e8f0;
                border-radius: 14px;
            }
            #searchContainer:focus-within {
                border: 2px solid #3b82f6;
                background: white;
            }
            #searchIcon {
                font-size: 18px;
                color: #94a3b8;
            }
            #statBadge {
                color: #64748b;
                font-size: 13px;
                background: #f8fafc;
                padding: 8px 16px;
                border-radius: 20px;
                border: 1px solid #e2e8f0;
            }
            #paginationBtn {
                background: #f8fafc;
                color: #475569;
                border: 1.5px solid #cbd5e1;
                border-radius: 10px;
                padding: 8px 16px;
                font-size: 13px;
                font-weight: 500;
                min-width: 80px;
            }
            #paginationBtn:hover {
                background: #e2e8f0;
                border-color: #94a3b8;
            }
            #paginationBtn:disabled {
                background: #f1f5f9;
                color: #cbd5e1;
                border-color: #e2e8f0;
            }
            #pageLabel {
                color: #475569;
                font-size: 14px;
                font-weight: 500;
            }
            #pageSizeCombo {
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                padding: 4px;
                background: white;
                font-size: 13px;
                min-width: 60px;
            }
        """)

    def on_search(self):
        self.current_page = 0
        self.refresh()

    def on_page_size_changed(self, text):
        self.items_per_page = int(text)
        self.current_page = 0
        self.refresh()

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.refresh_table_page()

    def next_page(self):
        total_pages = (len(self.all_products) + self.items_per_page - 1) // self.items_per_page
        if self.current_page < total_pages - 1:
            self.current_page += 1
            self.refresh_table_page()

    def refresh(self):
        search = self.search_input.text().strip()
        self.all_products = self.db.list_products(search if search else None)
        self.product_count.setText(f"إجمالي المنتجات: {len(self.all_products)}")
        self.refresh_table_page()

    def refresh_table_page(self):
        total_pages = max(1, (len(self.all_products) + self.items_per_page - 1) // self.items_per_page)
        self.page_label.setText(f"صفحة {self.current_page + 1} من {total_pages}")

        self.prev_btn.setEnabled(self.current_page > 0)
        self.next_btn.setEnabled(self.current_page < total_pages - 1)

        start = self.current_page * self.items_per_page
        end = start + self.items_per_page
        page_products = self.all_products[start:end]

        self.table.setRowCount(len(page_products))
        for row, p in enumerate(page_products):
            self.table.setItem(row, 0, QTableWidgetItem(p["name"]))
            self.table.setItem(row, 1, QTableWidgetItem(p["barcode"] or "-"))
            self.table.setItem(row, 2, QTableWidgetItem(p["category"] or "-"))
            self.table.setItem(row, 3, QTableWidgetItem(p.get("product_type") or "-"))

            year_val = p.get("year")
            self.table.setItem(row, 4, QTableWidgetItem(str(year_val) if year_val else "-"))

            self.table.setItem(row, 5, QTableWidgetItem(app_settings.format_currency(p["purchase_price"])))
            self.table.setItem(row, 6, QTableWidgetItem(app_settings.format_currency(p["sale_price"])))

            qty_item = QTableWidgetItem(str(p["quantity"]))
            if p["quantity"] <= 0:
                qty_item.setForeground(Qt.red)
                qty_item.setText(f"{p['quantity']} ⚠️")
            elif p["quantity"] <= p["min_quantity"]:
                qty_item.setForeground(Qt.darkYellow)
                qty_item.setText(f"{p['quantity']} ⚠️")
            self.table.setItem(row, 7, qty_item)

            edit_btn = QPushButton("✏️ تعديل")
            edit_btn.setObjectName("secondaryBtn")
            edit_btn.setFixedHeight(32)
            edit_btn.setCursor(Qt.PointingHandCursor)
            edit_btn.clicked.connect(lambda _, pid=p["id"]: self.edit_product(pid))
            self.table.setCellWidget(row, 8, edit_btn)

            del_btn = QPushButton("🗑️ حذف")
            del_btn.setObjectName("dangerBtn")
            del_btn.setFixedHeight(32)
            del_btn.setCursor(Qt.PointingHandCursor)
            del_btn.clicked.connect(lambda _, pid=p["id"]: self.delete_product(pid))
            self.table.setCellWidget(row, 9, del_btn)

    def add_product(self):
        dialog = ProductDialog(self)
        if dialog.exec() == QDialog.Accepted:
            data = dialog.get_data()
            if not data["name"]:
                QMessageBox.warning(self, "تنبيه", "اسم المنتج مطلوب")
                return
            try:
                self.db.add_product(**data)
            except Exception as e:
                QMessageBox.critical(self, "خطأ", f"تعذر إضافة المنتج:\n{e}")
                return
            self.refresh()
            if self.on_change:
                self.on_change()

    def edit_product(self, product_id):
        product = self.db.get_product(product_id)
        dialog = ProductDialog(self, product=product)
        if dialog.exec() == QDialog.Accepted:
            data = dialog.get_data()
            self.db.update_product(product_id, **data)
            self.refresh()
            if self.on_change:
                self.on_change()

    def delete_product(self, product_id):
        confirm = QMessageBox.question(self, "تأكيد الحذف", 
            "هل تريد حذف هذا المنتج؟\n\n⚠️ هذا الإجراء لا يمكن التراجع عنه")
        if confirm == QMessageBox.Yes:
            self.db.delete_product(product_id)
            self.refresh()
            if self.on_change:
                self.on_change()
