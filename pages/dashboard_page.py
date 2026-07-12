# -*- coding: utf-8 -*-
"""
صفحة لوحة التحكم (Dashboard) - تصميم احترافي
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame,
    QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView,
    QSizePolicy, QGridLayout
)
from PySide6.QtCore import Qt, QTimer, QSize
from PySide6.QtGui import QFont, QColor, QWheelEvent
from datetime import datetime, timedelta

from settings import app_settings


class WheelTableWidget(QTableWidget):
    """QTableWidget with mouse wheel scrolling support"""
    def __init__(self, rows, cols, parent=None):
        super().__init__(rows, cols, parent)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

    def wheelEvent(self, event: QWheelEvent):
        delta = event.angleDelta().y()
        scrollbar = self.verticalScrollBar()
        if scrollbar:
            scrollbar.setValue(scrollbar.value() - delta // 3)
        event.accept()


class DashboardCard(QFrame):
    def __init__(self, icon, title, value, subtitle="", color="#3b82f6", parent=None):
        super().__init__(parent)
        self.setObjectName("dashboardCard")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setMinimumHeight(120)
        self.setMaximumHeight(140)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(6)

        top = QHBoxLayout()
        self.icon_label = QLabel(icon)
        self.icon_label.setObjectName("cardIcon")
        self.icon_label.setFont(QFont("Segoe UI", 28))

        self.color_indicator = QFrame()
        self.color_indicator.setObjectName("colorIndicator")
        self.color_indicator.setFixedSize(10, 10)
        self.color_indicator.setStyleSheet(f"background: {color}; border-radius: 5px;")

        top.addWidget(self.icon_label)
        top.addStretch()
        top.addWidget(self.color_indicator)
        layout.addLayout(top)

        self.value_label = QLabel(value)
        self.value_label.setObjectName("cardValue")
        self.value_label.setFont(QFont("Segoe UI", 24, QFont.Bold))
        self.value_label.setStyleSheet(f"color: {color};")
        layout.addWidget(self.value_label)

        self.title_label = QLabel(title)
        self.title_label.setObjectName("cardTitle")
        self.title_label.setFont(QFont("Segoe UI", 11))
        layout.addWidget(self.title_label)

        if subtitle:
            self.subtitle_label = QLabel(subtitle)
            self.subtitle_label.setObjectName("cardSubtitle")
            self.subtitle_label.setFont(QFont("Segoe UI", 10))
            layout.addWidget(self.subtitle_label)

        layout.addStretch()

    def set_value(self, value):
        self.value_label.setText(value)


class DashboardPage(QWidget):
    def __init__(self, db, current_user):
        super().__init__()
        self.db = db
        self.current_user = current_user
        self._build_ui()
        self.refresh()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh)
        self.timer.start(30000)

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(14)
        layout.setContentsMargins(0, 0, 0, 0)

        # Header
        header = QHBoxLayout()
        title = QLabel("📊 لوحة التحكم")
        title.setObjectName("pageTitle")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))

        self.last_update = QLabel("🔄 الآن")
        self.last_update.setObjectName("lastUpdate")
        self.last_update.setFont(QFont("Segoe UI", 10))

        refresh_btn = QPushButton("🔄 تحديث")
        refresh_btn.setObjectName("secondaryBtn")
        refresh_btn.setFixedHeight(36)
        refresh_btn.setFont(QFont("Segoe UI", 11))
        refresh_btn.setCursor(Qt.PointingHandCursor)
        refresh_btn.clicked.connect(self.refresh)

        header.addWidget(title)
        header.addStretch()
        header.addWidget(self.last_update)
        header.addWidget(refresh_btn)
        layout.addLayout(header)

        # Stats Cards Row 1
        cards_row1 = QHBoxLayout()
        cards_row1.setSpacing(12)

        self.sales_card = DashboardCard("💰", "مبيعات اليوم", "0", "إجمالي المبيعات", "#3b82f6")
        self.profit_card = DashboardCard("💵", "ربح اليوم", "0", "صافي الربح", "#10b981")
        self.expenses_card = DashboardCard("💸", "مصاريف اليوم", "0", "المصاريف", "#ef4444")
        self.net_profit_card = DashboardCard("📊", "صافي الربح", "0", "بعد المصاريف", "#8b5cf6")

        cards_row1.addWidget(self.sales_card)
        cards_row1.addWidget(self.profit_card)
        cards_row1.addWidget(self.expenses_card)
        cards_row1.addWidget(self.net_profit_card)
        layout.addLayout(cards_row1)

        # Stats Cards Row 2
        cards_row2 = QHBoxLayout()
        cards_row2.setSpacing(12)

        self.invoices_card = DashboardCard("🧾", "فواتير اليوم", "0", "عدد الفواتير", "#f59e0b")
        self.stock_alert_card = DashboardCard("⚠️", "منتجات نافدة", "0", "تحتاج تعبئة", "#dc2626")
        self.total_products = DashboardCard("📦", "المنتجات", "0", "في النظام", "#06b6d4")
        self.total_customers = DashboardCard("👥", "العملاء", "0", "مسجلين", "#ec4899")

        cards_row2.addWidget(self.invoices_card)
        cards_row2.addWidget(self.stock_alert_card)
        cards_row2.addWidget(self.total_products)
        cards_row2.addWidget(self.total_customers)
        layout.addLayout(cards_row2)

        # Stats Cards Row 3
        cards_row3 = QHBoxLayout()
        cards_row3.setSpacing(12)

        self.total_debt = DashboardCard("📋", "الديون", "0", "على العملاء", "#dc2626")
        self.avg_margin = DashboardCard("📊", "هامش الربح", "0%", "حسب اليوم", "#8b5cf6")

        cards_row3.addWidget(self.total_debt)
        cards_row3.addWidget(self.avg_margin)
        cards_row3.addStretch()
        layout.addLayout(cards_row3)

        # Tables Section
        bottom_section = QHBoxLayout()
        bottom_section.setSpacing(12)

        # Left: Top Products Table
        left_widget = QFrame()
        left_widget.setObjectName("contentCard")
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(16, 16, 16, 16)
        left_layout.setSpacing(10)

        top_products_title = QLabel("🏆 أفضل المنتجات مبيعاً")
        top_products_title.setObjectName("sectionTitle")
        top_products_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        left_layout.addWidget(top_products_title)

        self.top_table = WheelTableWidget(0, 4)
        self.top_table.setHorizontalHeaderLabels(["المنتج", "الكمية", "المبيعات", "الربح"])
        self.top_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.top_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.top_table.setAlternatingRowColors(True)
        self.top_table.setMaximumHeight(220)
        left_layout.addWidget(self.top_table)

        bottom_section.addWidget(left_widget, 1)

        # Right: Low Stock Table
        right_widget = QFrame()
        right_widget.setObjectName("contentCard")
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(16, 16, 16, 16)
        right_layout.setSpacing(10)

        low_stock_title = QLabel("⚠️ منتجات قاربة على النفاد")
        low_stock_title.setObjectName("sectionTitle")
        low_stock_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        right_layout.addWidget(low_stock_title)

        self.low_table = WheelTableWidget(0, 3)
        self.low_table.setHorizontalHeaderLabels(["المنتج", "المتوفر", "الحد الأدنى"])
        self.low_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.low_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.low_table.setAlternatingRowColors(True)
        self.low_table.setMaximumHeight(220)
        right_layout.addWidget(self.low_table)

        bottom_section.addWidget(right_widget, 1)

        layout.addLayout(bottom_section, 1)

        self.setStyleSheet("""
            #dashboardCard {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 16px;
                min-width: 180px;
            }
            #dashboardCard:hover {
                border-color: #cbd5e1;
            }
            #cardIcon {
                font-size: 28px;
                margin-bottom: 2px;
            }
            #cardValue {
                font-size: 24px;
                font-weight: bold;
                margin-top: 2px;
            }
            #cardTitle {
                color: #64748b;
                font-size: 11px;
                font-weight: 500;
            }
            #cardSubtitle {
                color: #94a3b8;
                font-size: 10px;
            }
            #colorIndicator {
                border-radius: 5px;
            }
            #lastUpdate {
                color: #94a3b8;
                font-size: 10px;
                background: #f8fafc;
                padding: 5px 12px;
                border-radius: 16px;
                border: 1px solid #e2e8f0;
            }
            #contentCard {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 16px;
            }
        """)

    def refresh(self):
        today = datetime.now().strftime("%Y-%m-%d")
        date_from = f"{today} 00:00:00"
        date_to = f"{today} 23:59:59"

        rows, totals = self.db.profit_report(date_from, date_to)
        sales = self.db.sales_between(date_from, date_to)
        products = self.db.list_products()
        customers = self.db.list_customers()
        low_stock = self.db.low_stock_products()
        summary = self.db.profit_after_expenses(date_from, date_to)

        total_sales = totals['total_sales']
        total_profit = totals['total_profit']
        total_expenses = summary['total_expenses']
        net_profit = summary['net_profit']
        invoice_count = len(sales)
        stock_alert_count = len(low_stock)
        total_product_count = len(products)
        total_customer_count = len(customers)
        total_debt = sum(c['debt'] for c in customers)

        margin = (total_profit / total_sales * 100) if total_sales > 0 else 0

        self.sales_card.set_value(app_settings.format_currency(total_sales))
        self.profit_card.set_value(app_settings.format_currency(total_profit))
        self.expenses_card.set_value(app_settings.format_currency(total_expenses))
        self.net_profit_card.set_value(app_settings.format_currency(net_profit))
        self.invoices_card.set_value(str(invoice_count))
        self.stock_alert_card.set_value(str(stock_alert_count))
        self.total_products.set_value(str(total_product_count))
        self.total_customers.set_value(str(total_customer_count))
        self.total_debt.set_value(app_settings.format_currency(total_debt))
        self.avg_margin.set_value(f"{margin:.1f}%")

        if net_profit > 0:
            self.net_profit_card.value_label.setStyleSheet("color: #10b981;")
        elif net_profit < 0:
            self.net_profit_card.value_label.setStyleSheet("color: #ef4444;")
        else:
            self.net_profit_card.value_label.setStyleSheet("color: #64748b;")

        if total_profit > 0:
            self.profit_card.value_label.setStyleSheet("color: #10b981;")
        elif total_profit < 0:
            self.profit_card.value_label.setStyleSheet("color: #ef4444;")
        else:
            self.profit_card.value_label.setStyleSheet("color: #64748b;")

        if total_debt > 0:
            self.total_debt.value_label.setStyleSheet("color: #dc2626;")
        else:
            self.total_debt.value_label.setStyleSheet("color: #10b981;")

        self.top_table.setRowCount(min(len(rows), 5))
        for row, r in enumerate(rows[:5]):
            self.top_table.setItem(row, 0, QTableWidgetItem(r["product_name"]))
            self.top_table.setItem(row, 1, QTableWidgetItem(str(r["total_qty"])))
            self.top_table.setItem(row, 2, QTableWidgetItem(app_settings.format_currency(r["total_sales"])))

            profit_item = QTableWidgetItem(app_settings.format_currency(r["total_profit"]))
            if r['total_profit'] > 0:
                profit_item.setForeground(Qt.darkGreen)
            elif r['total_profit'] < 0:
                profit_item.setForeground(Qt.red)
            self.top_table.setItem(row, 3, profit_item)

        self.low_table.setRowCount(min(len(low_stock), 10))
        for row, p in enumerate(low_stock[:10]):
            self.low_table.setItem(row, 0, QTableWidgetItem(p["name"]))

            qty_item = QTableWidgetItem(str(p["quantity"]))
            qty_item.setForeground(Qt.red)
            qty_item.setFont(QFont("Segoe UI", 11, QFont.Bold))
            self.low_table.setItem(row, 1, qty_item)

            min_item = QTableWidgetItem(str(p["min_quantity"]))
            self.low_table.setItem(row, 2, min_item)

        self.last_update.setText(f"🔄 {datetime.now().strftime('%H:%M:%S')}")
