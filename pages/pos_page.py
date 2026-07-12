# -*- coding: utf-8 -*-
"""
صفحة نقطة البيع - تصميم احترافي مع الدينار العراقي
+ عرض نوع المنتج وسنة الإصدار
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QComboBox, QMessageBox,
    QDoubleSpinBox, QListWidget, QListWidgetItem, QAbstractItemView, QFrame,
    QGraphicsDropShadowEffect, QSizePolicy, QScrollArea
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QColor

from settings import app_settings


class POSPage(QWidget):
    def __init__(self, db, current_user):
        super().__init__()
        self.db = db
        self.current_user = current_user
        self.cart = []
        self._build_ui()
        self.refresh_products()
        self.refresh_customers()

    def _build_ui(self):
        root = QHBoxLayout(self)
        root.setSpacing(20)
        root.setContentsMargins(0, 0, 0, 0)

        # ═══════════════════════════════════════
        # الجهة اليسرى: البحث والمنتجات
        # ═══════════════════════════════════════
        left_card = QFrame()
        left_card.setObjectName("contentCard")
        left = QVBoxLayout(left_card)
        left.setContentsMargins(20, 20, 20, 20)
        left.setSpacing(14)

        header = QHBoxLayout()
        title = QLabel("🛒 نقطة البيع")
        title.setObjectName("pageTitle")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        header.addWidget(title)
        header.addStretch()
        left.addLayout(header)

        search_container = QFrame()
        search_container.setObjectName("searchContainer")
        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(12, 4, 12, 4)
        search_layout.setSpacing(8)

        search_icon = QLabel("🔍")
        search_icon.setObjectName("searchIcon")

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("ابحث بالاسم أو الباركود...")
        self.search_input.setObjectName("searchBox")
        self.search_input.setFixedHeight(44)
        self.search_input.textChanged.connect(self.refresh_products)
        self.search_input.returnPressed.connect(self.try_barcode_add)

        search_layout.addWidget(search_icon)
        search_layout.addWidget(self.search_input, 1)
        left.addWidget(search_container)

        products_header = QLabel("📦 المنتجات المتاحة")
        products_header.setObjectName("sectionTitle")
        left.addWidget(products_header)

        # Scrollable products list for many items
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background: transparent; border: none;")

        self.products_list = QListWidget()
        self.products_list.setObjectName("productsList")
        self.products_list.setSpacing(4)
        self.products_list.itemDoubleClicked.connect(self.add_selected_to_cart)
        self.products_list.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.products_list.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        scroll.setWidget(self.products_list)
        left.addWidget(scroll, 1)

        stats_row = QHBoxLayout()
        self.products_count = QLabel("المنتجات: 0")
        self.products_count.setObjectName("quickStat")
        stats_row.addWidget(self.products_count)
        stats_row.addStretch()
        left.addLayout(stats_row)

        root.addWidget(left_card, 3)

        # ═══════════════════════════════════════
        # الجهة اليمنى: السلة والدفع
        # ═══════════════════════════════════════
        right_card = QFrame()
        right_card.setObjectName("contentCard")
        right = QVBoxLayout(right_card)
        right.setContentsMargins(20, 20, 20, 20)
        right.setSpacing(14)

        cart_header = QHBoxLayout()
        cart_title = QLabel("🧾 الفاتورة الحالية")
        cart_title.setObjectName("sectionTitle")
        cart_title.setFont(QFont("Segoe UI", 16, QFont.Bold))

        clear_btn = QPushButton("🗑️ إفراغ")
        clear_btn.setObjectName("dangerBtn")
        clear_btn.setFixedHeight(32)
        clear_btn.setCursor(Qt.PointingHandCursor)
        clear_btn.clicked.connect(self.clear_cart)

        cart_header.addWidget(cart_title)
        cart_header.addWidget(clear_btn)
        right.addLayout(cart_header)

        # Scrollable cart table
        cart_scroll = QScrollArea()
        cart_scroll.setWidgetResizable(True)
        cart_scroll.setFrameShape(QFrame.NoFrame)
        cart_scroll.setStyleSheet("background: transparent; border: none;")

        self.cart_table = QTableWidget(0, 4)
        self.cart_table.setHorizontalHeaderLabels(["المنتج", "الكمية", "السعر", "الإجمالي"])
        self.cart_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.cart_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.cart_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.cart_table.setAlternatingRowColors(True)
        self.cart_table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.cart_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        cart_scroll.setWidget(self.cart_table)
        right.addWidget(cart_scroll, 1)

        remove_btn = QPushButton("❌ حذف المنتج المحدد")
        remove_btn.setObjectName("secondaryBtn")
        remove_btn.setCursor(Qt.PointingHandCursor)
        remove_btn.clicked.connect(self.remove_selected_from_cart)
        right.addWidget(remove_btn)

        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setStyleSheet("color: #e2e8f0; background: #e2e8f0; max-height: 1px;")
        right.addWidget(divider)

        options_frame = QFrame()
        options_frame.setObjectName("optionsFrame")
        options_layout = QVBoxLayout(options_frame)
        options_layout.setSpacing(12)

        customer_row = QHBoxLayout()
        customer_label = QLabel("👤 العميل:")
        customer_label.setObjectName("optionLabel")
        self.customer_combo = QComboBox()
        self.customer_combo.setObjectName("customerCombo")
        self.customer_combo.addItem("بدون عميل", None)
        self.customer_combo.setMinimumHeight(36)

        customer_row.addWidget(customer_label)
        customer_row.addWidget(self.customer_combo, 1)
        options_layout.addLayout(customer_row)

        payment_row = QHBoxLayout()
        payment_label = QLabel("💳 طريقة الدفع:")
        payment_label.setObjectName("optionLabel")
        self.payment_combo = QComboBox()
        self.payment_combo.setObjectName("paymentCombo")
        self.payment_combo.addItem("💵 كاش", "cash")
        self.payment_combo.addItem("💳 شبكة", "card")
        self.payment_combo.addItem("📋 آجل (على العميل)", "credit")
        self.payment_combo.setMinimumHeight(36)

        payment_row.addWidget(payment_label)
        payment_row.addWidget(self.payment_combo, 1)
        options_layout.addLayout(payment_row)

        discount_row = QHBoxLayout()
        discount_label = QLabel("🏷️ الخصم:")
        discount_label.setObjectName("optionLabel")
        self.discount_input = QDoubleSpinBox()
        self.discount_input.setObjectName("discountInput")
        self.discount_input.setPrefix(app_settings.get("currency_symbol", "د.ع") + " ")
        self.discount_input.setMaximum(100000000)
        self.discount_input.setDecimals(app_settings.get("decimal_places", 0))
        self.discount_input.setMinimumHeight(36)
        self.discount_input.valueChanged.connect(self.update_totals)

        discount_row.addWidget(discount_label)
        discount_row.addWidget(self.discount_input, 1)
        options_layout.addLayout(discount_row)

        right.addWidget(options_frame)

        total_frame = QFrame()
        total_frame.setObjectName("totalFrame")
        total_layout = QVBoxLayout(total_frame)
        total_layout.setSpacing(8)

        self.subtotal_label = QLabel("المجموع: " + app_settings.format_currency(0))
        self.subtotal_label.setObjectName("subtotalLabel")
        self.subtotal_label.setAlignment(Qt.AlignCenter)

        self.discount_display = QLabel("الخصم: " + app_settings.format_currency(0))
        self.discount_display.setObjectName("discountLabel")
        self.discount_display.setAlignment(Qt.AlignCenter)

        self.total_label = QLabel("الإجمالي: " + app_settings.format_currency(0))
        self.total_label.setObjectName("totalLabel")
        self.total_label.setAlignment(Qt.AlignCenter)
        self.total_label.setFont(QFont("Segoe UI", 22, QFont.Bold))

        total_layout.addWidget(self.subtotal_label)
        total_layout.addWidget(self.discount_display)
        total_layout.addWidget(self.total_label)

        right.addWidget(total_frame)

        confirm_btn = QPushButton("✅ إتمام عملية البيع")
        confirm_btn.setObjectName("primaryBtn")
        confirm_btn.setFixedHeight(56)
        confirm_btn.setFont(QFont("Segoe UI", 15, QFont.Bold))
        confirm_btn.setCursor(Qt.PointingHandCursor)
        confirm_btn.clicked.connect(self.confirm_sale)
        right.addWidget(confirm_btn)

        root.addWidget(right_card, 2)

        self.setStyleSheet("""
            #contentCard {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 20px;
            }
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
            #quickStat {
                color: #64748b;
                font-size: 12px;
                background: #f8fafc;
                padding: 6px 14px;
                border-radius: 20px;
            }
            #optionLabel {
                color: #475569;
                font-size: 13px;
                font-weight: 500;
                min-width: 90px;
            }
            #customerCombo, #paymentCombo, #discountInput {
                border: 2px solid #e2e8f0;
                border-radius: 10px;
                padding: 8px;
                background: white;
                font-size: 13px;
            }
            #customerCombo:focus, #paymentCombo:focus, #discountInput:focus {
                border: 2px solid #3b82f6;
            }
            #optionsFrame {
                background: #f8fafc;
                border-radius: 14px;
                padding: 8px;
            }
            #totalFrame {
                background: #f8fafc;
                border-radius: 16px;
                padding: 16px;
                border: 2px solid #e2e8f0;
            }
            #subtotalLabel {
                color: #64748b;
                font-size: 14px;
            }
            #discountLabel {
                color: #ef4444;
                font-size: 14px;
            }
            #totalLabel {
                color: #1e3a5f;
                font-size: 26px;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 12px 8px;
            }
        """)

    def refresh_products(self):
        self.products_list.clear()
        search = self.search_input.text().strip()
        products = self.db.list_products(search if search else None)

        self.products_count.setText(f"المنتجات: {len(products)}")

        for p in products:
            # Build label with new fields
            extra_info = ""
            if p.get("product_type"):
                extra_info += f" | النوع: {p['product_type']}"
            if p.get("year"):
                extra_info += f" | سنة: {p['year']}"

            label = f"{p['name']}{extra_info}   |   السعر: {app_settings.format_currency(p['sale_price'])}   |   المتوفر: {p['quantity']}"
            item = QListWidgetItem(label)
            item.setData(Qt.UserRole, p)
            if p["quantity"] <= 0:
                item.setForeground(Qt.red)
                item.setText(label + " ⚠️ نفذت الكمية")
            elif p["quantity"] <= p["min_quantity"]:
                item.setForeground(Qt.darkYellow)
                item.setText(label + " ⚠️ قارب على النفاد")
            self.products_list.addItem(item)

    def refresh_customers(self):
        self.customer_combo.clear()
        self.customer_combo.addItem("بدون عميل", None)
        for c in self.db.list_customers():
            debt_info = f" (دين: {app_settings.format_currency(c['debt'])})" if c['debt'] > 0 else ""
            self.customer_combo.addItem(f"{c['name']}{debt_info}", c["id"])

    def try_barcode_add(self):
        code = self.search_input.text().strip()
        product = self.db.get_product_by_barcode(code)
        if product:
            self.add_to_cart(product)
            self.search_input.clear()
        else:
            QMessageBox.warning(self, "تنبيه", "لم يتم العثور على منتج بهذا الباركود")

    def add_selected_to_cart(self, item):
        product = item.data(Qt.UserRole)
        self.add_to_cart(product)

    def add_to_cart(self, product):
        if product["quantity"] <= 0:
            QMessageBox.warning(self, "تنبيه", "الكمية غير متوفرة بالمخزون")
            return
        for line in self.cart:
            if line["product_id"] == product["id"]:
                if line["quantity"] + 1 > product["quantity"]:
                    QMessageBox.warning(self, "تنبيه", "لا توجد كمية كافية بالمخزون")
                    return
                line["quantity"] += 1
                self._refresh_cart_table()
                return
        self.cart.append({
            "product_id": product["id"],
            "name": product["name"],
            "quantity": 1,
            "unit_price": product["sale_price"],
            "unit_cost": product["purchase_price"],
            "available": product["quantity"],
        })
        self._refresh_cart_table()

    def remove_selected_from_cart(self):
        row = self.cart_table.currentRow()
        if row < 0:
            QMessageBox.information(self, "معلومة", "الرجاء تحديد منتج من السلة أولا")
            return
        del self.cart[row]
        self._refresh_cart_table()

    def clear_cart(self):
        if not self.cart:
            return
        confirm = QMessageBox.question(self, "تأكيد", "هل تريد إفراغ السلة؟")
        if confirm == QMessageBox.Yes:
            self.cart = []
            self.discount_input.setValue(0)
            self._refresh_cart_table()

    def _refresh_cart_table(self):
        self.cart_table.setRowCount(len(self.cart))
        for row, line in enumerate(self.cart):
            self.cart_table.setItem(row, 0, QTableWidgetItem(line["name"]))
            self.cart_table.setItem(row, 1, QTableWidgetItem(str(line["quantity"])))
            self.cart_table.setItem(row, 2, QTableWidgetItem(app_settings.format_currency(line["unit_price"])))
            total = line["quantity"] * line["unit_price"]
            self.cart_table.setItem(row, 3, QTableWidgetItem(app_settings.format_currency(total)))
        self.update_totals()

    def update_totals(self):
        subtotal = sum(l["quantity"] * l["unit_price"] for l in self.cart)
        discount = self.discount_input.value()
        total = max(subtotal - discount, 0)

        self.subtotal_label.setText(f"المجموع: {app_settings.format_currency(subtotal)}")
        self.discount_display.setText(f"الخصم: {app_settings.format_currency(discount)}")
        self.total_label.setText(f"الإجمالي: {app_settings.format_currency(total)}")

    def confirm_sale(self):
        if not self.cart:
            QMessageBox.warning(self, "تنبيه", "الفاتورة فارغة")
            return
        payment_method = self.payment_combo.currentData()
        customer_id = self.customer_combo.currentData()
        if payment_method == "credit" and not customer_id:
            QMessageBox.warning(self, "تنبيه", "طريقة الدفع آجل تحتاج اختيار عميل")
            return
        discount = self.discount_input.value()
        try:
            self.db.create_sale(
                items=self.cart,
                payment_method=payment_method,
                user_id=self.current_user["id"],
                customer_id=customer_id,
                discount=discount,
            )
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء حفظ الفاتورة:\n{e}")
            return

        QMessageBox.information(self, "تم ✅", "تم إتمام عملية البيع بنجاح")
        self.cart = []
        self.discount_input.setValue(0)
        self._refresh_cart_table()
        self.refresh_products()
