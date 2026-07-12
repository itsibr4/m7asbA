# -*- coding: utf-8 -*-
"""
طبقة قاعدة البيانات - SQLite
تحتوي كل الجداول والدوال اللازمة للتعامل مع المنتجات، المبيعات، المخزون، العملاء والمستخدمين.
+ جدول المصاريف الشهرية
+ حقول إضافية للمنتج (نوع، سنة)
+ تحديث بيانات المستخدم
"""

import sqlite3
import hashlib
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sales_data.db")


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


class Database:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.conn.row_factory = sqlite3.Row
        self._create_tables()
        self._ensure_default_owner()
        self._migrate_add_product_fields()
        self._migrate_add_expenses_table()

    # ---------- إنشاء الجداول ----------
    def _create_tables(self):
        cur = self.conn.cursor()
        cur.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('owner','employee')),
                created_at TEXT DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                barcode TEXT UNIQUE,
                category TEXT,
                product_type TEXT,
                year INTEGER,
                purchase_price REAL NOT NULL DEFAULT 0,
                sale_price REAL NOT NULL DEFAULT 0,
                quantity INTEGER NOT NULL DEFAULT 0,
                min_quantity INTEGER NOT NULL DEFAULT 0,
                created_at TEXT DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT,
                debt REAL NOT NULL DEFAULT 0,
                created_at TEXT DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sale_date TEXT DEFAULT (datetime('now')),
                total REAL NOT NULL DEFAULT 0,
                discount REAL NOT NULL DEFAULT 0,
                payment_method TEXT NOT NULL DEFAULT 'cash',
                user_id INTEGER,
                customer_id INTEGER,
                FOREIGN KEY(user_id) REFERENCES users(id),
                FOREIGN KEY(customer_id) REFERENCES customers(id)
            );

            CREATE TABLE IF NOT EXISTS sale_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sale_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                product_name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                unit_price REAL NOT NULL,
                unit_cost REAL NOT NULL,
                FOREIGN KEY(sale_id) REFERENCES sales(id) ON DELETE CASCADE,
                FOREIGN KEY(product_id) REFERENCES products(id)
            );

            CREATE TABLE IF NOT EXISTS stock_movements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                movement_type TEXT NOT NULL CHECK(movement_type IN ('in','out','adjustment')),
                quantity INTEGER NOT NULL,
                note TEXT,
                created_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY(product_id) REFERENCES products(id)
            );
            """
        )
        self.conn.commit()

    def _migrate_add_product_fields(self):
        """إضافة حقول جديدة للمنتج إذا لم تكن موجودة"""
        cur = self.conn.cursor()
        try:
            cur.execute("ALTER TABLE products ADD COLUMN product_type TEXT")
        except:
            pass
        try:
            cur.execute("ALTER TABLE products ADD COLUMN year INTEGER")
        except:
            pass
        self.conn.commit()

    def _migrate_add_expenses_table(self):
        """إضافة جدول المصاريف الشهرية"""
        cur = self.conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                amount REAL NOT NULL DEFAULT 0,
                expense_date TEXT DEFAULT (datetime('now')),
                note TEXT,
                created_at TEXT DEFAULT (datetime('now'))
            )
        """)
        self.conn.commit()

    def _ensure_default_owner(self):
        cur = self.conn.cursor()
        cur.execute("SELECT COUNT(*) as c FROM users")
        if cur.fetchone()["c"] == 0:
            cur.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (?,?,?)",
                ("admin", hash_password("admin123"), "owner"),
            )
            self.conn.commit()

    # ---------- المستخدمين ----------
    def verify_user(self, username: str, password: str):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=?", (username,))
        row = cur.fetchone()
        if row and row["password_hash"] == hash_password(password):
            return dict(row)
        return None

    def add_user(self, username, password, role):
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (?,?,?)",
            (username, hash_password(password), role),
        )
        self.conn.commit()
        return cur.lastrowid

    def list_users(self):
        cur = self.conn.cursor()
        cur.execute("SELECT id, username, role, created_at FROM users ORDER BY id")
        return [dict(r) for r in cur.fetchall()]

    def delete_user(self, user_id):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM users WHERE id=?", (user_id,))
        self.conn.commit()

    def update_user_password(self, user_id, new_password):
        """تحديث كلمة مرور المستخدم"""
        cur = self.conn.cursor()
        cur.execute(
            "UPDATE users SET password_hash = ? WHERE id = ?",
            (hash_password(new_password), user_id)
        )
        self.conn.commit()

    def update_username(self, user_id, new_username):
        """تحديث اسم المستخدم"""
        cur = self.conn.cursor()
        cur.execute(
            "UPDATE users SET username = ? WHERE id = ?",
            (new_username, user_id)
        )
        self.conn.commit()

    # ---------- المنتجات ----------
    def add_product(self, name, barcode, category, product_type, year, purchase_price, sale_price, quantity, min_quantity):
        cur = self.conn.cursor()
        cur.execute(
            """INSERT INTO products (name, barcode, category, product_type, year, purchase_price, sale_price, quantity, min_quantity)
               VALUES (?,?,?,?,?,?,?,?,?)""",
            (name, barcode or None, category, product_type, year, purchase_price, sale_price, quantity, min_quantity),
        )
        self.conn.commit()
        pid = cur.lastrowid
        if quantity:
            cur.execute(
                "INSERT INTO stock_movements (product_id, movement_type, quantity, note) VALUES (?,?,?,?)",
                (pid, "in", quantity, "رصيد افتتاحي"),
            )
            self.conn.commit()
        return pid

    def update_product(self, product_id, **fields):
        if not fields:
            return
        keys = ", ".join(f"{k}=?" for k in fields.keys())
        values = list(fields.values()) + [product_id]
        cur = self.conn.cursor()
        cur.execute(f"UPDATE products SET {keys} WHERE id=?", values)
        self.conn.commit()

    def delete_product(self, product_id):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM products WHERE id=?", (product_id,))
        self.conn.commit()

    def list_products(self, search=None):
        cur = self.conn.cursor()
        if search:
            like = f"%{search}%"
            cur.execute(
                """SELECT * FROM products 
                   WHERE name LIKE ? OR barcode LIKE ? OR product_type LIKE ? OR category LIKE ?
                   ORDER BY name""",
                (like, like, like, like),
            )
        else:
            cur.execute("SELECT * FROM products ORDER BY name")
        return [dict(r) for r in cur.fetchall()]

    def get_product(self, product_id):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM products WHERE id=?", (product_id,))
        row = cur.fetchone()
        return dict(row) if row else None

    def get_product_by_barcode(self, barcode):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM products WHERE barcode=?", (barcode,))
        row = cur.fetchone()
        return dict(row) if row else None

    def low_stock_products(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM products WHERE quantity <= min_quantity ORDER BY quantity")
        return [dict(r) for r in cur.fetchall()]

    # ---------- المخزون ----------
    def add_stock_movement(self, product_id, movement_type, quantity, note=""):
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO stock_movements (product_id, movement_type, quantity, note) VALUES (?,?,?,?)",
            (product_id, movement_type, quantity, note),
        )
        if movement_type == "in":
            cur.execute("UPDATE products SET quantity = quantity + ? WHERE id=?", (quantity, product_id))
        elif movement_type == "out":
            cur.execute("UPDATE products SET quantity = quantity - ? WHERE id=?", (quantity, product_id))
        elif movement_type == "adjustment":
            cur.execute("UPDATE products SET quantity = ? WHERE id=?", (quantity, product_id))
        self.conn.commit()

    def stock_history(self, product_id=None, limit=200):
        cur = self.conn.cursor()
        if product_id:
            cur.execute(
                """SELECT sm.*, p.name as product_name FROM stock_movements sm
                   JOIN products p ON p.id = sm.product_id
                   WHERE sm.product_id=? ORDER BY sm.id DESC LIMIT ?""",
                (product_id, limit),
            )
        else:
            cur.execute(
                """SELECT sm.*, p.name as product_name FROM stock_movements sm
                   JOIN products p ON p.id = sm.product_id
                   ORDER BY sm.id DESC LIMIT ?""",
                (limit,),
            )
        return [dict(r) for r in cur.fetchall()]

    # ---------- العملاء ----------
    def add_customer(self, name, phone="", debt=0.0):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO customers (name, phone, debt) VALUES (?,?,?)", (name, phone, debt))
        self.conn.commit()
        return cur.lastrowid

    def list_customers(self, search=None):
        cur = self.conn.cursor()
        if search:
            like = f"%{search}%"
            cur.execute("SELECT * FROM customers WHERE name LIKE ? OR phone LIKE ? ORDER BY name", (like, like))
        else:
            cur.execute("SELECT * FROM customers ORDER BY name")
        return [dict(r) for r in cur.fetchall()]

    def update_customer_debt(self, customer_id, amount_delta):
        cur = self.conn.cursor()
        cur.execute("UPDATE customers SET debt = debt + ? WHERE id=?", (amount_delta, customer_id))
        self.conn.commit()

    def delete_customer(self, customer_id):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM customers WHERE id=?", (customer_id,))
        self.conn.commit()

    # ---------- المبيعات ----------
    def create_sale(self, items, payment_method, user_id, customer_id=None, discount=0.0):
        """
        items: list of dicts {product_id, name, quantity, unit_price, unit_cost}
        """
        total = sum(i["quantity"] * i["unit_price"] for i in items) - discount
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO sales (total, discount, payment_method, user_id, customer_id) VALUES (?,?,?,?,?)",
            (total, discount, payment_method, user_id, customer_id),
        )
        sale_id = cur.lastrowid
        for it in items:
            cur.execute(
                """INSERT INTO sale_items (sale_id, product_id, product_name, quantity, unit_price, unit_cost)
                   VALUES (?,?,?,?,?,?)""",
                (sale_id, it["product_id"], it["name"], it["quantity"], it["unit_price"], it["unit_cost"]),
            )
            cur.execute(
                "UPDATE products SET quantity = quantity - ? WHERE id=?",
                (it["quantity"], it["product_id"]),
            )
            cur.execute(
                "INSERT INTO stock_movements (product_id, movement_type, quantity, note) VALUES (?,?,?,?)",
                (it["product_id"], "out", it["quantity"], f"بيع #{sale_id}"),
            )
        if payment_method == "credit" and customer_id:
            cur.execute("UPDATE customers SET debt = debt + ? WHERE id=?", (total, customer_id))
        self.conn.commit()
        return sale_id

    def sales_between(self, date_from, date_to):
        cur = self.conn.cursor()
        cur.execute(
            "SELECT * FROM sales WHERE sale_date BETWEEN ? AND ? ORDER BY sale_date DESC",
            (date_from, date_to),
        )
        return [dict(r) for r in cur.fetchall()]

    def profit_report(self, date_from, date_to):
        """يرجع صافي الربح والمبيعات خلال فترة معينة"""
        cur = self.conn.cursor()
        cur.execute(
            """SELECT si.product_name,
                      SUM(si.quantity) as total_qty,
                      SUM(si.quantity * si.unit_price) as total_sales,
                      SUM(si.quantity * si.unit_cost) as total_cost,
                      SUM(si.quantity * (si.unit_price - si.unit_cost)) as total_profit
               FROM sale_items si
               JOIN sales s ON s.id = si.sale_id
               WHERE s.sale_date BETWEEN ? AND ?
               GROUP BY si.product_id
               ORDER BY total_profit DESC""",
            (date_from, date_to),
        )
        rows = [dict(r) for r in cur.fetchall()]
        totals = {
            "total_sales": sum(r["total_sales"] or 0 for r in rows),
            "total_cost": sum(r["total_cost"] or 0 for r in rows),
            "total_profit": sum(r["total_profit"] or 0 for r in rows),
        }
        return rows, totals

    def today_summary(self):
        today = datetime.now().strftime("%Y-%m-%d")
        return self.profit_report(f"{today} 00:00:00", f"{today} 23:59:59")

    # ---------- المصاريف الشهرية ----------
    def add_expense(self, title, amount, expense_date, note=""):
        """إضافة مصروف جديد"""
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO expenses (title, amount, expense_date, note) VALUES (?,?,?,?)",
            (title, amount, expense_date, note)
        )
        self.conn.commit()
        return cur.lastrowid

    def list_expenses(self, date_from=None, date_to=None):
        """قائمة المصاريف مع إمكانية التصفية حسب التاريخ"""
        cur = self.conn.cursor()
        if date_from and date_to:
            cur.execute(
                "SELECT * FROM expenses WHERE expense_date BETWEEN ? AND ? ORDER BY expense_date DESC",
                (date_from, date_to)
            )
        else:
            cur.execute("SELECT * FROM expenses ORDER BY expense_date DESC")
        return [dict(r) for r in cur.fetchall()]

    def delete_expense(self, expense_id):
        """حذف مصروف"""
        cur = self.conn.cursor()
        cur.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
        self.conn.commit()

    def total_expenses(self, date_from=None, date_to=None):
        """إجمالي المصاريف"""
        cur = self.conn.cursor()
        if date_from and date_to:
            cur.execute(
                "SELECT COALESCE(SUM(amount), 0) as total FROM expenses WHERE expense_date BETWEEN ? AND ?",
                (date_from, date_to)
            )
        else:
            cur.execute("SELECT COALESCE(SUM(amount), 0) as total FROM expenses")
        result = cur.fetchone()
        return result["total"] if result else 0

    def profit_after_expenses(self, date_from, date_to):
        """صافي الربح بعد خصم المصاريف"""
        rows, totals = self.profit_report(date_from, date_to)
        expenses = self.total_expenses(date_from, date_to)
        net_profit = (totals["total_profit"] or 0) - expenses
        return {
            "total_sales": totals["total_sales"],
            "total_cost": totals["total_cost"],
            "gross_profit": totals["total_profit"],
            "total_expenses": expenses,
            "net_profit": net_profit,
        }

    def close(self):
        self.conn.close()
