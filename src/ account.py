import random
from src.database import connect_db


def generate_account_number():
    return "AC" + str(random.randint(10000000, 99999999))


def create_account(user_email):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM accounts WHERE user_email=?",
        (user_email,)
    )

    if cursor.fetchone():
        print("\nYou already have a bank account.")
        conn.close()
        return

    print("\n========== CREATE BANK ACCOUNT ==========")

    print("1. Savings")
    print("2. Current")

    choice = input("Choose Account Type: ").strip()

    if choice == "1":
        account_type = "Savings"
    elif choice == "2":
        account_type = "Current"
    else:
        print("\nInvalid choice.")
        conn.close()
        return

    account_no = generate_account_number()

    cursor.execute("""
        INSERT INTO accounts(
            account_no,
            user_email,
            account_type,
            balance
        )
        VALUES(?,?,?,?)
    """, (
        account_no,
        user_email,
        account_type,
        0
    ))

    conn.commit()
    conn.close()

    print("\n===================================")
    print("Bank Account Created Successfully")
    print("===================================")
    print(f"Account Number : {account_no}")
    print(f"Account Type   : {account_type}")
    print("Balance        : ₹0.00")


def view_account(user_email):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            account_no,
            account_type,
            balance
        FROM accounts
        WHERE user_email=?
    """, (user_email,))

    account = cursor.fetchone()

    conn.close()

    if account is None:
        print("\nNo bank account found.")
        return

    print("\n========== ACCOUNT DETAILS ==========")
    print(f"Account Number : {account[0]}")
    print(f"Account Type   : {account[1]}")
    print(f"Balance        : ₹{account[2]:.2f}")


def check_balance(user_email):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT balance
        FROM accounts
        WHERE user_email=?
    """, (user_email,))

    account = cursor.fetchone()

    conn.close()

    if account is None:
        print("\nNo bank account found.")
        return

    print(f"\nCurrent Balance : ₹{account[0]:.2f}")