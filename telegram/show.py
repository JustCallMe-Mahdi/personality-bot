import sqlite3
from tabulate import tabulate

DB_PATH = "mbti_results.db"  # یا مسیر MBTI_DB خودت


def show_all_results():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # اطمینان از وجود جدول با فیلدهای name و username
    cur.execute("""
        CREATE TABLE IF NOT EXISTS results (
            user_id INTEGER,
            name TEXT,
            username TEXT,
            mbti_type TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cur.execute("""
        SELECT rowid, user_id, name, username, mbti_type, created_at
        FROM results
        ORDER BY created_at DESC
    """)
    rows = cur.fetchall()

    headers = ["Row ID", "User ID", "Name", "Username", "MBTI Type", "Saved At"]
    print(tabulate(rows, headers=headers, tablefmt="fancy_grid"))

    conn.close()

def delete_result_by_rowid(rowid):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM results WHERE rowid = ?", (rowid,))
    conn.commit()
    conn.close()
    print(f"✅ Result with Row ID {rowid} deleted.")

# اجرای برنامه
if __name__ == "__main__":
    show_all_results()
    try:
        rowid = int(input("🗑️ Enter the Row ID of the result you want to delete (or 0 to cancel): "))
        if rowid != 0:
            delete_result_by_rowid(rowid)
    except ValueError:
        print("❌ Invalid input. Please enter a number.")
