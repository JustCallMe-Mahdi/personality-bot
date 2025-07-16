import sqlite3
from datetime import datetime
import pytz
import json

USERS_DB = "users.db"
MBTI_DB = "mbti_results.db"

# ----------- زمان تهران -----------
def get_tehran_timestamp():
    return datetime.now(pytz.timezone('Asia/Tehran')).strftime("%Y-%m-%d %H:%M:%S")

# ----------- ساخت جدول کاربران جدید -----------
def init_user_db():
    with sqlite3.connect(USERS_DB) as conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                name TEXT,
                username TEXT,
                age INTEGER,
                birth_date TEXT,
                gender TEXT,
                join_date TEXT,
                level INTEGER DEFAULT 1,
                xp INTEGER DEFAULT 0,
                coins INTEGER DEFAULT 0,
                rank TEXT,
                badges TEXT,  -- JSON list
                tests_taken TEXT,  -- JSON list of dict
                displayed_test_id TEXT,
                invite_link TEXT
            )
        """)

# ----------- ذخیره یا آپدیت پروفایل کاربر -----------
def save_or_update_user(user_id: int, name: str, age: int, gender: str,
                        username: str = "-", birth_date: str = None, invite_link: str = None):
    with sqlite3.connect(USERS_DB) as conn:
        cur = conn.cursor()

        # آیا کاربر قبلاً ثبت شده؟
        cur.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
        exists = cur.fetchone()

        if exists:
            cur.execute("""
                UPDATE users SET
                    name = ?, username = ?, age = ?, gender = ?,
                    birth_date = ?, invite_link = ?
                WHERE user_id = ?
            """, (name, username, age, gender, birth_date, invite_link, user_id))
        else:
            cur.execute("""
                INSERT INTO users (
                    user_id, name, username, age, gender, birth_date, join_date,
                    level, xp, coins, rank, badges, tests_taken, displayed_test_id, invite_link
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                user_id, name, username, age, gender, birth_date, get_tehran_timestamp(),
                1, 0, 0, None, json.dumps([]), json.dumps([]), None, invite_link
            ))

# ----------- گرفتن پروفایل کامل -----------
def get_user_full_profile(user_id: int):
    with sqlite3.connect(USERS_DB) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        return cur.fetchone()

# ----------- ذخیره تست انجام‌شده در لیست -----------
def add_test_taken(user_id: int, test_name: str, result: str):
    with sqlite3.connect(USERS_DB) as conn:
        cur = conn.cursor()
        cur.execute("SELECT tests_taken FROM users WHERE user_id = ?", (user_id,))
        data = cur.fetchone()
        if data:
            tests = json.loads(data[0] or "[]")
            tests.append({
                "test_name": test_name,
                "result": result,
                "timestamp": get_tehran_timestamp()
            })
            cur.execute("UPDATE users SET tests_taken = ? WHERE user_id = ?", (json.dumps(tests), user_id))

# ----------- افزایش XP و Coin و Level -----------
def add_xp_and_coins(user_id: int, xp_gain: int = 10, coins_gain: int = 5):
    with sqlite3.connect(USERS_DB) as conn:
        cur = conn.cursor()
        cur.execute("SELECT xp, level, coins FROM users WHERE user_id = ?", (user_id,))
        row = cur.fetchone()
        if row:
            xp, level, coins = row
            xp += xp_gain
            coins += coins_gain

            # سیستم ارتقاء سطح
            if xp >= 100:
                level += 1
                xp -= 100

            cur.execute("""
                UPDATE users SET xp = ?, level = ?, coins = ? WHERE user_id = ?
            """, (xp, level, coins, user_id))

# ----------- ذخیره تست MBTI در دیتابیس مجزا -----------
def save_user_result(user_id: int, mbti_type: str, name: str, username: str):
    with sqlite3.connect(MBTI_DB) as conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS results (
                user_id INTEGER,
                mbti_type TEXT,
                name TEXT,
                username TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cur.execute("""
            INSERT INTO results (user_id, mbti_type, name, username)
            VALUES (?, ?, ?, ?)
        """, (user_id, mbti_type, name, username))