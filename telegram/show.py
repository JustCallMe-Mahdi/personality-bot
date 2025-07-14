import sqlite3

from tabulate import tabulate

def show_all_users():
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("""
        SELECT user_id, name, age, gender, test_result, test_datetime,test_type
        FROM users
    """)
    users = cur.fetchall()

    headers = ["User ID", "Name", "Age", "Gender", "Test result", "Test datetime", "Test type"]
    print(tabulate(users, headers=headers, tablefmt="grid"))

    conn.close()


def delete_user_by_id(user_id):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()
    print(f"User with ID {user_id} has been deleted.")

show_all_users()
user_id = int(input("Enter the ID of the user you want to delete: "))
delete_user_by_id(user_id)
