# -*- coding: utf-8 -*-
"""
صفحة التقارير - تصميم احترافي مع دعم عجلة الماوس
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QDateEdit,
    QTableWidget, QTableWidgetItem, QHeaderView, QFrame, QAbstractItemView,
    QSizePolicy
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont, QColor, QWheelEvent

from settings import app_settings


class WheelTableWidget(QTableWidget):
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


class StatCard(QFrame):
    def __init__(self, icon, title, value="0", color="#3b82f6", parent=None):
        super().__init__(parent)
        self.setObjectName("statCard")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setMinimumHeight(100)
        self.setMaximumHeight(120)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(6)

        self.icon_label = QLabel(icon)
        self.icon_label.setObjectName("statIcon")
        self.icon_label.setFont(QFont("Segoe UI", 24))

        self.title_label = QLabel(title)
        self.title_label.setObjectName("statTitle")
        self.title_label.setFont(QFont("Segoe UI", 11))

        self.value_label = QLabel(value)
        self.value_label.setObjectName("statValue")
        self.value_label.setFont(QFont("Segoe UI", 22, QFont.Bold))
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
        layout.setSpacing(12)
        layout.setContentsMargins(0, 0, 0, 0)

        header = QHBoxLayout()
        title = QLabel("📈 التقارير والأرباح")
        title.setObjectName("pageTitle")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        header.addWidget(title)
        header.addStretch()
        layout.addLayout(header)

        filter_card = QFrame()
        filter_card.setObjectName("filterCard")
        filter_layout = QHBoxLayout(filter_card)
        filter_layout.setContentsMargins(16, 12, 16, 12)
        filter_layout.setSpacing(10)

        from_label = QLabel("📅 من:")
        from_label.setObjectName("filterLabel")
        from_label.setFont(QFont("Segoe UI", 11))
        self.date_from = QDateEdit(calendarPopup=True)
        self.date_from.setDate(QDate.currentDate())
        self.date_from.setObjectName("dateEdit")
        self.date_from.setMinimumHeight(32)
        self.date_from.setFont(QFont("Segoe UI", 11))

        to_label = QLabel("إلى:")
        to_label.setObjectName("filterLabel")
        to_label.setFont(QFont("Segoe UI", 11))
        self.date_to = QDateEdit(calendarPopup=True)
        self.date_to.setDate(QDate.currentDate())
        self.date_to.setObjectName("dateEdit")
        self.date_to.setMinimumHeight(32)
        self.date_to.setFont(QFont("Segoe UI", 11))

        apply_btn = QPushButton("🔍 عرض")
        apply_btn.setObjectName("primaryBtn")
        apply_btn.setFixedHeight(36)
        apply_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        apply_btn.setCursor(Qt.PointingHandCursor)
        apply_btn.clicked.connect(self.refresh)

        today_btn = QPushButton("📆 اليوم")
        today_btn.setObjectName("filterBtn")
        today_btn.setFixedHeight(36)
        today_btn.setFont(QFont("Segoe UI", 11))
        today_btn.setCursor(Qt.PointingHandCursor)
        today_btn.clicked.connect(self.set_today)

        month_btn = QPushButton("📊 الشهر")
        month_btn.setObjectName("filterBtn")
        month_btn.setFixedHeight(36)
        month_btn.setFont(QFont("Segoe UI", 11))
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
        cards_row.setSpacing(12)

        self.sales_card = StatCard("💰", "المبيعات", app_settings.format_currency(0), "#3b82f6")
        self.cost_card = StatCard("📉", "التكلفة", app_settings.format_currency(0), "#f59e0b")
        self.profit_card = StatCard("💵", "الربح", app_settings.format_currency(0), "#10b981")
        self.expenses_card = StatCard("💸", "المصاريف", app_settings.format_currency(0), "#ef4444")
        self.net_card = StatCard("📊", "صافي الربح", app_settings.format_currency(0), "#8b5cf6")

        cards_row.addWidget(self.sales_card)
        cards_row.addWidget(self.cost_card)
        cards_row.addWidget(self.profit_card)
        cards_row.addWidget(self.expenses_card)
        cards_row.addWidget(self.net_card)

        layout.addLayout(cards_row)

        table_header = QHBoxLayout()
        table_title = QLabel("📋 الأداء حسب المنتج")
        table_title.setObjectName("sectionTitle")
        table_title.setFont(QFont("Segoe UI", 14, QFont.Bold))

        self.table_count = QLabel("0 منتج")
        self.table_count.setObjectName("statBadge")
        self.table_count.setFont(QFont("Segoe UI", 11))

        table_header.addWidget(table_title)
        table_header.addStretch()
        table_header.addWidget(self.table_count)
        layout.addLayout(table_header)

        self.table = WheelTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(
            ["المنتج", "الكمية", "المبيعات", "التكلفة", "صافي الربح", "هامش الربح"]
        )
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setMinimumHeight(250)
        layout.addWidget(self.table, 1)

        self.setStyleSheet("""
            #filterCard {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 14px;
            }
            #filterLabel {
                color: #475569;
                font-size: 11px;
                font-weight: 500;
            }
            #dateEdit {
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                padding: 6px;
                background: #f8fafc;
                font-size: 11px;
                min-width: 110px;
            }
            #dateEdit:focus {
                border: 2px solid #3b82f6;
            }
            #filterBtn {
                background: #f8fafc;
                color: #475569;
                border: 1.5px solid #cbd5e1;
                border-radius: 8px;
                padding: 6px 14px;
                font-size: 11px;
                font-weight: 500;
            }
            #filterBtn:hover {
                background: #e2e8f0;
                border-color: #94a3b8;
            }
            #statBadge {
                color: #64748b;
                font-size: 11px;
                background: #f8fafc;
                padding: 6px 12px;
                border-radius: 16px;
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
        summary = self.db.profit_after_expenses(date_from, date_to)

        self.sales_card.set_value(app_settings.format_currency(totals['total_sales']))
        self.cost_card.set_value(app_settings.format_currency(totals['total_cost']))
        self.profit_card.set_value(app_settings.format_currency(totals['total_profit']))
        self.expenses_card.set_value(app_settings.format_currency(summary['total_expenses']))
        self.net_card.set_value(app_settings.format_currency(summary['net_profit']))

        if summary['net_profit'] >= 0:
            self.net_card.value_label.setStyleSheet("color: #10b981;")
        else:
            self.net_card.value_label.setStyleSheet("color: #ef4444;")

        self.table_count.setText(f"{len(rows)} منتج")

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
