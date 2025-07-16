import sqlite3
from tabulate import tabulate
import json

DB_PATH = "users.db"  # مسیر دیتابیس

def show_all_users():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # برای دسترسی دیکشنری‌وار به ستون‌ها
    cur = conn.cursor()

    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()

    if not rows:
        print("❌ هیچ کاربری در دیتابیس وجود ندارد.")
        return

    # استخراج نام ستون‌ها
    column_names = rows[0].keys()

    # آماده‌سازی ردیف‌ها
    formatted_rows = []
    for row in rows:
        row_dict = dict(row)
        # مقادیر JSON مثل badges و tests_taken را خواناتر می‌کنیم
        for key in ["badges", "tests_taken"]:
            if key in row_dict and row_dict[key]:
                try:
                    row_dict[key] = json.dumps(json.loads(row_dict[key]), ensure_ascii=False, indent=1)
                except Exception:
                    pass  # اگر نتوانستیم پارس کنیم، همان مقدار خام را بگذاریم
        formatted_rows.append(list(row_dict.values()))

    # نمایش جدول
    print(tabulate(formatted_rows, headers=column_names, tablefmt="fancy_grid"))

    conn.close()

show_all_users()


def delete_user_by_id(user_id: int):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()
    print(f"\n🗑️ کاربر با شناسه {user_id} حذف شد.")

try:
    user_id = int(input("\n🔎 شماره ID کاربری که می‌خوای حذف کنی رو وارد کن (یا Enter برای صرف‌نظر): ").strip())
    delete_user_by_id(user_id)
except ValueError:
    print("⏭️ حذف انجام نشد. ورودی معتبری دریافت نشد.")