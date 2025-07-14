import sqlite3
from datetime import datetime
import pytz

# ----------- مسیر پایگاه‌داده‌ها -----------
USERS_DB = "users.db"
MBTI_DB = "mbti_results.db"

# ----------- زمان تهران -----------
def get_tehran_timestamp():
    return datetime.now(pytz.timezone('Asia/Tehran')).strftime("%Y-%m-%d %H:%M:%S")

# ----------- راه‌اندازی دیتابیس کاربران -----------
def init_user_db():
    with sqlite3.connect(USERS_DB) as conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                name TEXT,
                age INTEGER,
                gender TEXT,
                test_result TEXT,
                test_type TEXT,
                test_datetime TEXT
            )
        """)

# ----------- ذخیره یا به‌روزرسانی پروفایل کاربر -----------
def save_user_profile(user_id: int, name: str, age: str, gender: str, test_result: str = None, test_type: str = None):
    with sqlite3.connect(USERS_DB) as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT OR REPLACE INTO users (user_id, name, age, gender, test_result, test_type)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, name, age, gender, test_result, test_type))

# ----------- دریافت پروفایل کاربر -----------
def get_user_profile(user_id: int):
    with sqlite3.connect(USERS_DB) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT name, age, gender, test_result, test_type
            FROM users
            WHERE user_id = ?
        """, (user_id,))
        return cur.fetchone()  # None if not found

# ----------- ذخیره آخرین تست کاربر -----------
def save_latest_test(user_id: int, test_result: str, test_type: str):
    timestamp = get_tehran_timestamp()
    with sqlite3.connect(USERS_DB) as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO users (user_id, test_result, test_type, test_datetime)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                test_result=excluded.test_result,
                test_type=excluded.test_type,
                test_datetime=excluded.test_datetime
        """, (user_id, test_result, test_type, timestamp))

# ----------- ذخیره تست MBTI در تاریخچه مجزا -----------
def save_user_result(user_id: int, mbti_type: str):
    with sqlite3.connect(MBTI_DB) as conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS results (
                user_id INTEGER,
                mbti_type TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cur.execute("""
            INSERT INTO results (user_id, mbti_type)
            VALUES (?, ?)
        """, (user_id, mbti_type))

# ----------- ذخیره تست در تاریخچه نتایج (همه تست‌ها) -----------
def save_test_history(user_id: int, test_result: str, test_type: str):
    timestamp = get_tehran_timestamp()
    with sqlite3.connect(USERS_DB) as conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS test_results (
                user_id INTEGER,
                test_result TEXT,
                test_type TEXT,
                timestamp TEXT
            )
        """)
        cur.execute("""
            INSERT INTO test_results (user_id, test_result, test_type, timestamp)
            VALUES (?, ?, ?, ?)
        """, (user_id, test_result, test_type, timestamp))

# ----------- ارتقاء جدول کاربران (اضافه کردن ستون جدید اگر وجود ندارد) -----------
def upgrade_users_table():
    with sqlite3.connect(USERS_DB) as conn:
        cur = conn.cursor()
        for column in ["test_result", "test_datetime"]:
            try:
                cur.execute(f"ALTER TABLE users ADD COLUMN {column} TEXT")
            except sqlite3.OperationalError:
                pass  # ستون وجود دارد
