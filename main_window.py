# -*- coding: utf-8 -*-
"""
النافذة الرئيسية - تصميم احترافي مع sidebar متقدم و Dashboard
"""
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QStackedWidget, QFrame, QGraphicsDropShadowEffect, QSizePolicy
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QColor, QIcon

from pages.dashboard_page import DashboardPage
from pages.pos_page import POSPage
from pages.products_page import ProductsPage
from pages.inventory_page import InventoryPage
from pages.reports_page import ReportsPage
from pages.customers_page import CustomersPage
from pages.users_page import UsersPage
from pages.settings_page import SettingsPage


class NavButton(QPushButton):
    """زر تنقل مخصص بتصميم احترافي"""
    def __init__(self, icon, text, parent=None):
        super().__init__(parent)
        self.setText(f"  {icon}  {text}")
        self.setObjectName("navBtn")
        self.setCheckable(True)
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(48)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)


class MainWindow(QMainWindow):
    def __init__(self, db, current_user, on_logout):
        super().__init__()
        self.db = db
        self.current_user = current_user
        self.on_logout = on_logout

        self.setWindowTitle("نظام المحاسبة المتكامل - إدارة المبيعات والمخزون")
        self.resize(1500, 900)
        self.setLayoutDirection(Qt.RightToLeft)
        self.setMinimumSize(1200, 750)

        self._build_ui()
        self._apply_styles()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ═══════════════════════════════════════
        # الشريط الجانبي (Sidebar)
        # ═══════════════════════════════════════
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(260)
        side_layout = QVBoxLayout(sidebar)
        side_layout.setContentsMargins(0, 0, 0, 20)
        side_layout.setSpacing(0)

        # Header section with brand
        header = QFrame()
        header.setObjectName("sidebarHeader")
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(20, 24, 20, 20)
        header_layout.setSpacing(8)

        brand_icon = QLabel("📊")
        brand_icon.setObjectName("brandIcon")
        brand_icon.setAlignment(Qt.AlignCenter)

        brand = QLabel("نظام المحاسبة")
        brand.setObjectName("brand")
        brand.setAlignment(Qt.AlignCenter)

        brand_sub = QLabel("المتكامل")
        brand_sub.setObjectName("brandSub")
        brand_sub.setAlignment(Qt.AlignCenter)

        header_layout.addWidget(brand_icon)
        header_layout.addWidget(brand)
        header_layout.addWidget(brand_sub)

        side_layout.addWidget(header)

        # Separator
        sep1 = QFrame()
        sep1.setFrameShape(QFrame.HLine)
        sep1.setObjectName("sidebarSep")
        side_layout.addWidget(sep1)

        # User info section
        user_frame = QFrame()
        user_frame.setObjectName("userFrame")
        user_layout = QVBoxLayout(user_frame)
        user_layout.setContentsMargins(20, 16, 20, 16)
        user_layout.setSpacing(6)

        user_avatar = QLabel("👤")
        user_avatar.setObjectName("userAvatar")
        user_avatar.setAlignment(Qt.AlignCenter)

        user_name = QLabel(f"{self.current_user['username']}")
        user_name.setObjectName("userName")
        user_name.setAlignment(Qt.AlignCenter)

        role_labels = {"owner": "👑 المالك", "employee": "🧑‍💼 موظف"}
        user_role = QLabel(role_labels.get(self.current_user['role'], self.current_user['role']))
        user_role.setObjectName("userRole")
        user_role.setAlignment(Qt.AlignCenter)

        user_layout.addWidget(user_avatar)
        user_layout.addWidget(user_name)
        user_layout.addWidget(user_role)

        side_layout.addWidget(user_frame)

        # Separator
        sep2 = QFrame()
        sep2.setFrameShape(QFrame.HLine)
        sep2.setObjectName("sidebarSep")
        side_layout.addWidget(sep2)

        # Navigation buttons
        nav_container = QWidget()
        nav_layout = QVBoxLayout(nav_container)
        nav_layout.setContentsMargins(16, 12, 16, 12)
        nav_layout.setSpacing(6)

        self.nav_buttons = []
        self.page_indices = {}

        def make_nav_button(icon, text, index):
            btn = NavButton(icon, text)
            btn.clicked.connect(lambda: self.switch_page(index))
            nav_layout.addWidget(btn)
            self.nav_buttons.append(btn)
            self.page_indices[btn] = index
            return btn

        side_layout.addWidget(nav_container)

        # ═══════════════════════════════════════
        # الصفحات (Stacked Widget)
        # ═══════════════════════════════════════
        self.stack = QStackedWidget()
        self.stack.setObjectName("mainStack")

        self.dashboard_page = DashboardPage(self.db, self.current_user)
        self.pos_page = POSPage(self.db, self.current_user)
        self.products_page = ProductsPage(self.db, on_change=self.pos_page.refresh_products)
        self.inventory_page = InventoryPage(self.db, on_change=self._refresh_all_stock_views)
        self.reports_page = ReportsPage(self.db)
        self.customers_page = CustomersPage(self.db)
        self.settings_page = SettingsPage()

        self.stack.addWidget(self.dashboard_page)   # 0
        self.stack.addWidget(self.pos_page)         # 1
        self.stack.addWidget(self.products_page)    # 2
        self.stack.addWidget(self.inventory_page)   # 3
        self.stack.addWidget(self.reports_page)     # 4
        self.stack.addWidget(self.customers_page)   # 5
        self.stack.addWidget(self.settings_page)    # 6

        make_nav_button("📊", "لوحة التحكم", 0)
        make_nav_button("🛒", "نقطة البيع", 1)
        make_nav_button("📦", "المنتجات", 2)
        make_nav_button("📊", "المخزون", 3)

        is_owner = self.current_user["role"] == "owner"
        if is_owner:
            make_nav_button("📈", "التقارير والأرباح", 4)
        make_nav_button("👥", "العملاء", 5)
        make_nav_button("⚙️", "الإعدادات", 6)

        if is_owner:
            self.users_page = UsersPage(self.db, self.current_user)
            self.stack.addWidget(self.users_page)  # 7
            make_nav_button("🔐", "المستخدمين", 7)

        nav_layout.addStretch()
        side_layout.addStretch()

        # Logout section at bottom
        logout_frame = QFrame()
        logout_frame.setObjectName("logoutFrame")
        logout_layout = QVBoxLayout(logout_frame)
        logout_layout.setContentsMargins(16, 12, 16, 0)
        logout_layout.setSpacing(8)

        logout_btn = QPushButton("🚪  تسجيل الخروج")
        logout_btn.setObjectName("logoutBtn")
        logout_btn.setCursor(Qt.PointingHandCursor)
        logout_btn.setFixedHeight(44)
        logout_btn.clicked.connect(self.handle_logout)

        logout_layout.addWidget(logout_btn)
        side_layout.addWidget(logout_frame)

        # ═══════════════════════════════════════
        # المحتوى الرئيسي (Content Area)
        # ═══════════════════════════════════════
        content_widget = QWidget()
        content_widget.setObjectName("contentWidget")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(24, 20, 24, 20)
        content_layout.setSpacing(16)

        # Top bar with breadcrumb
        top_bar = QFrame()
        top_bar.setObjectName("topBar")
        top_bar_layout = QHBoxLayout(top_bar)
        top_bar_layout.setContentsMargins(16, 12, 16, 12)

        self.page_title = QLabel("📊 لوحة التحكم")
        self.page_title.setObjectName("pageTitle")
        self.page_title.setFont(QFont("Segoe UI", 18, QFont.Bold))

        date_label = QLabel("📅 " + __import__('datetime').datetime.now().strftime("%Y-%m-%d"))
        date_label.setObjectName("dateLabel")

        top_bar_layout.addWidget(self.page_title)
        top_bar_layout.addStretch()
        top_bar_layout.addWidget(date_label)

        content_layout.addWidget(top_bar)
        content_layout.addWidget(self.stack, 1)

        root.addWidget(sidebar)
        root.addWidget(content_widget, 1)

        self.switch_page(0)

    def switch_page(self, index):
        self.stack.setCurrentIndex(index)

        # Update nav button states
        for btn in self.nav_buttons:
            btn.setChecked(False)
            btn.setProperty("active", False)
            btn.style().unpolish(btn)
            btn.style().polish(btn)

        if index < len(self.nav_buttons):
            self.nav_buttons[index].setChecked(True)
            self.nav_buttons[index].setProperty("active", True)
            self.nav_buttons[index].style().unpolish(self.nav_buttons[index])
            self.nav_buttons[index].style().polish(self.nav_buttons[index])

        # Update page title
        page_titles = {
            0: "📊 لوحة التحكم",
            1: "🛒 نقطة البيع",
            2: "📦 إدارة المنتجات", 
            3: "📊 إدارة المخزون",
            4: "📈 التقارير والأرباح",
            5: "👥 إدارة العملاء",
            6: "⚙️ الإعدادات",
            7: "🔐 إدارة المستخدمين"
        }
        self.page_title.setText(page_titles.get(index, ""))

        # Refresh page data
        widget = self.stack.currentWidget()
        if hasattr(widget, "refresh"):
            widget.refresh()
        if widget is self.pos_page:
            self.pos_page.refresh_products()
            self.pos_page.refresh_customers()

    def _refresh_all_stock_views(self):
        self.pos_page.refresh_products()
        self.products_page.refresh()

    def handle_logout(self):
        self.close()
        self.on_logout()

    def _apply_styles(self):
        self.setStyleSheet("""
            /* ═══════════════════════════════════════
               الألوان الرئيسية:
               Primary: #1e3a5f (أزرق داكن محاسبي)
               Secondary: #3b82f6 (أزرق فاتح)
               Accent: #10b981 (أخضر نجاح)
               Warning: #f59e0b (أصفر تحذير)
               Danger: #ef4444 (أحمر خطأ)
               Background: #f1f5f9 (رمادي فاتح)
               ═══════════════════════════════════════ */

            QWidget { 
                font-family: 'Segoe UI', 'Tahoma', sans-serif; 
                font-size: 13px; 
            }

            /* ═══ Sidebar ═══ */
            #sidebar { 
                background-color: #1e293b; 
                border-right: 1px solid #334155;
            }

            #sidebarHeader {
                background-color: transparent;
            }

            #brandIcon {
                font-size: 42px;
                margin-bottom: 4px;
            }

            #brand { 
                color: #ffffff; 
                font-size: 18px; 
                font-weight: bold; 
            }

            #brandSub { 
                color: #94a3b8; 
                font-size: 12px; 
                margin-top: -4px;
            }

            #sidebarSep {
                color: #334155;
                background-color: #334155;
                max-height: 1px;
                margin: 0 20px;
            }

            #userFrame {
                background-color: transparent;
            }

            #userAvatar {
                font-size: 36px;
                margin-bottom: 4px;
            }

            #userName { 
                color: #f1f5f9; 
                font-size: 14px; 
                font-weight: bold; 
            }

            #userRole { 
                color: #94a3b8; 
                font-size: 11px; 
                background-color: #334155;
                border-radius: 12px;
                padding: 4px 12px;
                max-width: 100px;
            }

            #navBtn {
                text-align: right;
                color: #cbd5e1;
                background: transparent;
                border: none;
                padding: 0 16px;
                border-radius: 12px;
                font-size: 14px;
                font-weight: 500;
            }

            #navBtn:hover { 
                background-color: #334155; 
                color: #ffffff; 
            }

            #navBtn:checked { 
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3b82f6, stop:1 #2563eb);
                color: white; 
                font-weight: bold; 
            }

            #navBtn:checked:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2563eb, stop:1 #1d4ed8);
            }

            #logoutFrame {
                background-color: transparent;
                border-top: 1px solid #334155;
                margin-top: 8px;
                padding-top: 8px;
            }

            #logoutBtn {
                color: #f87171;
                background: transparent;
                border: 1.5px solid #7f1d1d;
                border-radius: 10px;
                padding: 10px;
                font-size: 13px;
                font-weight: 500;
            }

            #logoutBtn:hover { 
                background-color: #7f1d1d; 
                color: white; 
            }

            /* ═══ Content Area ═══ */
            #contentWidget {
                background-color: #f1f5f9;
            }

            #topBar {
                background-color: #ffffff;
                border-radius: 16px;
                border: 1px solid #e2e8f0;
            }

            #pageTitle { 
                color: #1e293b; 
                font-size: 20px; 
                font-weight: bold; 
            }

            #dateLabel {
                color: #64748b;
                font-size: 13px;
                background-color: #f8fafc;
                padding: 6px 14px;
                border-radius: 20px;
                border: 1px solid #e2e8f0;
            }

            #mainStack {
                background: transparent;
            }

            /* ═══ Page Elements ═══ */
            #sectionTitle { 
                font-size: 16px; 
                font-weight: bold; 
                color: #334155; 
                margin-top: 12px; 
                margin-bottom: 8px;
            }

            #searchBox {
                border: 2px solid #e2e8f0; 
                border-radius: 12px; 
                padding: 10px 16px;
                background: white; 
                font-size: 14px;
                color: #1e293b;
                min-height: 20px;
            }

            #searchBox:focus { 
                border: 2px solid #3b82f6; 
                background: #ffffff;
            }

            #searchBox::placeholder {
                color: #94a3b8;
            }

            #primaryBtn {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3b82f6, stop:1 #2563eb);
                color: white; 
                border: none;
                border-radius: 12px; 
                padding: 10px 20px; 
                font-weight: bold;
                font-size: 14px;
                min-height: 20px;
            }

            #primaryBtn:hover { 
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2563eb, stop:1 #1d4ed8);
            }

            #primaryBtn:pressed {
                background: #1e40af;
            }

            #secondaryBtn {
                background-color: #f1f5f9; 
                color: #475569; 
                border: 1.5px solid #cbd5e1;
                border-radius: 12px; 
                padding: 10px 20px;
                font-size: 14px;
                font-weight: 500;
            }

            #secondaryBtn:hover { 
                background-color: #e2e8f0; 
                border-color: #94a3b8;
            }

            #dangerBtn {
                background-color: #fef2f2;
                color: #dc2626;
                border: 1.5px solid #fecaca;
                border-radius: 12px;
                padding: 8px 16px;
                font-size: 13px;
                font-weight: 500;
            }

            #dangerBtn:hover {
                background-color: #dc2626;
                color: white;
                border-color: #dc2626;
            }

            #totalLabel { 
                font-size: 24px; 
                font-weight: bold; 
                color: #1e293b; 
                padding: 16px;
                background: #ffffff;
                border-radius: 16px;
                border: 2px solid #e2e8f0;
                text-align: center;
            }

            #warningLabel { 
                color: #92400e; 
                background: #fef3c7; 
                padding: 12px 16px; 
                border-radius: 12px;
                border: 1px solid #fbbf24;
                font-size: 13px;
                font-weight: 500;
            }

            #successLabel {
                color: #166534;
                background: #dcfce7;
                padding: 12px 16px;
                border-radius: 12px;
                border: 1px solid #86efac;
                font-size: 13px;
                font-weight: 500;
            }

            /* ═══ Tables ═══ */
            QTableWidget {
                background: white; 
                border: 1px solid #e2e8f0; 
                border-radius: 16px;
                gridline-color: #f1f5f9;
                outline: none;
                selection-background-color: #dbeafe;
                selection-color: #1e293b;
            }

            QTableWidget::item {
                padding: 10px 8px;
                border-bottom: 1px solid #f1f5f9;
            }

            QTableWidget::item:selected {
                background-color: #dbeafe;
                color: #1e293b;
            }

            QHeaderView::section {
                background-color: #f8fafc; 
                padding: 12px 10px; 
                border: none; 
                font-weight: bold; 
                color: #475569;
                font-size: 13px;
                border-bottom: 2px solid #e2e8f0;
            }

            QHeaderView::section:first {
                border-top-right-radius: 16px;
            }

            QHeaderView::section:last {
                border-top-left-radius: 16px;
            }

            /* ═══ Lists ═══ */
            QListWidget#productsList {
                background: white; 
                border: 1px solid #e2e8f0; 
                border-radius: 16px; 
                padding: 8px;
                outline: none;
            }

            QListWidget#productsList::item { 
                padding: 14px 12px; 
                border-radius: 10px; 
                margin-bottom: 4px;
                border: 1px solid transparent;
            }

            QListWidget#productsList::item:hover { 
                background-color: #eff6ff; 
                border-color: #bfdbfe;
            }

            QListWidget#productsList::item:selected { 
                background-color: #3b82f6; 
                color: white;
                border-color: #2563eb;
            }

            /* ═══ Cards ═══ */
            #statCard {
                background: white; 
                border: 1px solid #e2e8f0; 
                border-radius: 16px; 
                padding: 20px;
            }

            #statCard:hover {
                border-color: #cbd5e1;
                box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            }

            #statTitle { 
                color: #64748b; 
                font-size: 13px; 
                font-weight: 500;
            }

            #statValue { 
                color: #1e293b; 
                font-size: 28px; 
                font-weight: bold; 
                margin-top: 8px; 
            }

            #statIcon {
                font-size: 28px;
                margin-bottom: 8px;
            }

            /* ═══ Inputs ═══ */
            QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox, QDateEdit {
                border: 2px solid #e2e8f0;
                border-radius: 10px;
                padding: 8px 12px;
                background: white;
                font-size: 13px;
                color: #1e293b;
                min-height: 18px;
            }

            QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus, QDateEdit:focus {
                border: 2px solid #3b82f6;
            }

            QComboBox::drop-down {
                border: none;
                width: 30px;
            }

            QComboBox QAbstractItemView {
                border: 1px solid #e2e8f0;
                border-radius: 10px;
                background: white;
                selection-background-color: #eff6ff;
                padding: 4px;
            }

            QSpinBox::up-button, QDoubleSpinBox::up-button,
            QSpinBox::down-button, QDoubleSpinBox::down-button {
                width: 24px;
                border: none;
                background: #f8fafc;
            }

            QSpinBox::up-button:hover, QDoubleSpinBox::up-button:hover,
            QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover {
                background: #e2e8f0;
            }

            /* ═══ Scrollbars ═══ */
            QScrollBar:vertical {
                background: #f1f5f9;
                width: 10px;
                border-radius: 5px;
            }

            QScrollBar::handle:vertical {
                background: #cbd5e1;
                border-radius: 5px;
                min-height: 30px;
            }

            QScrollBar::handle:vertical:hover {
                background: #94a3b8;
            }

            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }

            QScrollBar:horizontal {
                background: #f1f5f9;
                height: 10px;
                border-radius: 5px;
            }

            QScrollBar::handle:horizontal {
                background: #cbd5e1;
                border-radius: 5px;
                min-width: 30px;
            }

            QScrollBar::handle:horizontal:hover {
                background: #94a3b8;
            }

            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                width: 0px;
            }

            /* ═══ Dialogs ═══ */
            QDialog {
                background: #f8fafc;
            }

            QDialogButtonBox QPushButton {
                padding: 10px 24px;
                border-radius: 10px;
                font-weight: 500;
                min-width: 80px;
            }

            QDialogButtonBox QPushButton[text="Save"] {
                background: #3b82f6;
                color: white;
                border: none;
            }

            QDialogButtonBox QPushButton[text="Cancel"] {
                background: #f1f5f9;
                color: #475569;
                border: 1.5px solid #cbd5e1;
            }

            /* ═══ MessageBox ═══ */
            QMessageBox {
                background: white;
            }

            QMessageBox QPushButton {
                padding: 8px 20px;
                border-radius: 10px;
                font-weight: 500;
                min-width: 80px;
            }
        """)
