# -*- coding: utf-8 -*-
"""
صفحة التقارير - تصميم احترافي مع الدينار العراقي
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QDateEdit,
    QTableWidget, QTableWidgetItem, QHeaderView, QFrame, QAbstractItemView,
    QGraphicsDropShadowEffect, QSizePolicy, QScrollArea
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont, QColor

from settings import app_settings


class StatCard(QFrame):
    def __init__(self, icon, title, value="0", color="#3b82f6", parent=None):
        super().__init__(parent)
        self.setObjectName("statCard")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(8)

        self.icon_label = QLabel(icon)
        self.icon_label.setObjectName("statIcon")
        self.icon_label.setFont(QFont("Segoe UI", 32))

        self.title_label = QLabel(title)
        self.title_label.setObjectName("statTitle")

        self.value_label = QLabel(value)
        self.value_label.setObjectName("statValue")
        self.value_label.setFont(QFont("Segoe UI", 26, QFont.Bold))
        self.value_label.setStyleSheet(f"color: {color};")

        layout.addWidget(self.icon_label)
        layout.addWidget(self.title_label)
        layout.addWidget(self.value_label)

    def set_value(self, value):
        self.value_label.setText(value)


class ReportsPage(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(0, 0, 0, 0)

        header = QHBoxLayout()
        title = QLabel("📈 التقارير والأرباح")
        title.setObjectName("pageTitle")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        header.addWidget(title)
        header.addStretch()
        layout.addLayout(header)

        filter_card = QFrame()
        filter_card.setObjectName("filterCard")
        filter_layout = QHBoxLayout(filter_card)
        filter_layout.setContentsMargins(20, 16, 20, 16)
        filter_layout.setSpacing(12)

        from_label = QLabel("📅 من:")
        from_label.setObjectName("filterLabel")
        self.date_from = QDateEdit(calendarPopup=True)
        self.date_from.setDate(QDate.currentDate())
        self.date_from.setObjectName("dateEdit")
        self.date_from.setMinimumHeight(36)

        to_label = QLabel("إلى:")
        to_label.setObjectName("filterLabel")
        self.date_to = QDateEdit(calendarPopup=True)
        self.date_to.setDate(QDate.currentDate())
        self.date_to.setObjectName("dateEdit")
        self.date_to.setMinimumHeight(36)

        apply_btn = QPushButton("🔍 عرض التقرير")
        apply_btn.setObjectName("primaryBtn")
        apply_btn.setFixedHeight(40)
        apply_btn.setCursor(Qt.PointingHandCursor)
        apply_btn.clicked.connect(self.refresh)

        today_btn = QPushButton("📆 اليوم")
        today_btn.setObjectName("filterBtn")
        today_btn.setFixedHeight(40)
        today_btn.setCursor(Qt.PointingHandCursor)
        today_btn.clicked.connect(self.set_today)

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
        filter_layout.addWidget(today_btn)
        filter_layout.addWidget(month_btn)
        filter_layout.addStretch()

        layout.addWidget(filter_card)

        cards_row = QHBoxLayout()
        cards_row.setSpacing(16)

        self.sales_card = StatCard("💰", "إجمالي المبيعات", app_settings.format_currency(0), "#3b82f6")
        self.cost_card = StatCard("📉", "إجمالي التكلفة", app_settings.format_currency(0), "#f59e0b")
        self.profit_card = StatCard("💵", "صافي الربح", app_settings.format_currency(0), "#10b981")
        self.margin_card = StatCard("📊", "هامش الربح", "0%", "#8b5cf6")

        cards_row.addWidget(self.sales_card)
        cards_row.addWidget(self.cost_card)
        cards_row.addWidget(self.profit_card)
        cards_row.addWidget(self.margin_card)

        layout.addLayout(cards_row)

        table_header = QHBoxLayout()
        table_title = QLabel("📋 الأداء حسب المنتج")
        table_title.setObjectName("sectionTitle")
        table_title.setFont(QFont("Segoe UI", 16, QFont.Bold))

        self.table_count = QLabel("عدد المنتجات: 0")
        self.table_count.setObjectName("statBadge")

        table_header.addWidget(table_title)
        table_header.addStretch()
        table_header.addWidget(self.table_count)
        layout.addLayout(table_header)

        # Scrollable table
        table_scroll = QScrollArea()
        table_scroll.setWidgetResizable(True)
        table_scroll.setFrameShape(QFrame.NoFrame)
        table_scroll.setStyleSheet("background: transparent; border: none;")

        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(
            ["المنتج", "الكمية المباعة", "المبيعات", "التكلفة", "صافي الربح", "هامش الربح"]
        )
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        table_scroll.setWidget(self.table)
        layout.addWidget(table_scroll, 1)

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
            #dateEdit {
                border: 2px solid #e2e8f0;
                border-radius: 10px;
                padding: 8px;
                background: #f8fafc;
                font-size: 13px;
                min-width: 130px;
            }
            #dateEdit:focus {
                border: 2px solid #3b82f6;
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
        """)

    def set_today(self):
        today = QDate.currentDate()
        self.date_from.setDate(today)
        self.date_to.setDate(today)
        self.refresh()

    def set_this_month(self):
        today = QDate.currentDate()
        self.date_from.setDate(QDate(today.year(), today.month(), 1))
        self.date_to.setDate(today)
        self.refresh()

    def refresh(self):
        date_from = self.date_from.date().toString("yyyy-MM-dd") + " 00:00:00"
        date_to = self.date_to.date().toString("yyyy-MM-dd") + " 23:59:59"
        rows, totals = self.db.profit_report(date_from, date_to)

        self.sales_card.set_value(app_settings.format_currency(totals['total_sales']))
        self.cost_card.set_value(app_settings.format_currency(totals['total_cost']))
        self.profit_card.set_value(app_settings.format_currency(totals['total_profit']))

        margin = (totals['total_profit'] / totals['total_sales'] * 100) if totals['total_sales'] > 0 else 0
        self.margin_card.set_value(f"{margin:.1f}%")

        self.table_count.setText(f"عدد المنتجات: {len(rows)}")

        self.table.setRowCount(len(rows))
        for row, r in enumerate(rows):
            self.table.setItem(row, 0, QTableWidgetItem(r["product_name"]))
            self.table.setItem(row, 1, QTableWidgetItem(str(r["total_qty"])))
            self.table.setItem(row, 2, QTableWidgetItem(app_settings.format_currency(r["total_sales"])))
            self.table.setItem(row, 3, QTableWidgetItem(app_settings.format_currency(r["total_cost"])))

            profit_item = QTableWidgetItem(app_settings.format_currency(r["total_profit"]))
            if r['total_profit'] > 0:
                profit_item.setForeground(Qt.darkGreen)
            elif r['total_profit'] < 0:
                profit_item.setForeground(Qt.red)
            self.table.setItem(row, 4, profit_item)

            item_margin = (r['total_profit'] / r['total_sales'] * 100) if r['total_sales'] > 0 else 0
            margin_item = QTableWidgetItem(f"{item_margin:.1f}%")
            if item_margin > 20:
                margin_item.setForeground(Qt.darkGreen)
            elif item_margin < 5:
                margin_item.setForeground(Qt.darkRed)
            self.table.setItem(row, 5, margin_item)
