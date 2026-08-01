from datetime import datetime
from src.database import connect_db


def save_transaction(account_no, transaction_type, amount, balance):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO transactions(
            account_no,
            transaction_type,
            amount,
            balance_after,
            transaction_time
        )
        VALUES(?,?,?,?,?)
    """, (
        account_no,
        transaction_type,
        amount,
        balance,
        datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def deposit_money(user_email):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT account_no, balance
        FROM accounts
        WHERE user_email=?
    """, (user_email,))

    account = cursor.fetchone()

    if account is None:
        print("\nNo account found.")
        conn.close()
        return

    account_no, balance = account

    try:
        amount = float(input("Enter Deposit Amount: ₹"))
    except ValueError:
        print("\nInvalid amount.")
        conn.close()
        return

    if amount <= 0:
        print("\nAmount must be greater than zero.")
        conn.close()
        return

    balance += amount

    cursor.execute("""
        UPDATE accounts
        SET balance=?
        WHERE account_no=?
    """, (balance, account_no))

    conn.commit()
    conn.close()

    save_transaction(account_no, "Deposit", amount, balance)

    print(f"\n₹{amount:.2f} deposited successfully.")
    print(f"Current Balance: ₹{balance:.2f}")


def withdraw_money(user_email):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT account_no, balance
        FROM accounts
        WHERE user_email=?
    """, (user_email,))

    account = cursor.fetchone()

    if account is None:
        print("\nNo account found.")
        conn.close()
        return

    account_no, balance = account

    try:
        amount = float(input("Enter Withdrawal Amount: ₹"))
    except ValueError:
        print("\nInvalid amount.")
        conn.close()
        return

    if amount <= 0:
        print("\nAmount must be greater than zero.")
        conn.close()
        return

    if amount > balance:
        print("\nInsufficient balance.")
        conn.close()
        return

    balance -= amount

    cursor.execute("""
        UPDATE accounts
        SET balance=?
        WHERE account_no=?
    """, (balance, account_no))

    conn.commit()
    conn.close()

    save_transaction(account_no, "Withdrawal", amount, balance)

    print(f"\n₹{amount:.2f} withdrawn successfully.")
    print(f"Current Balance: ₹{balance:.2f}")


def transaction_history(user_email):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT account_no
        FROM accounts
        WHERE user_email=?
    """, (user_email,))

    account = cursor.fetchone()

    if account is None:
        print("\nNo account found.")
        conn.close()
        return

    account_no = account[0]

    cursor.execute("""
        SELECT
            transaction_type,
            amount,
            balance_after,
            transaction_time
        FROM transactions
        WHERE account_no=?
        ORDER BY id DESC
    """, (account_no,))

    transactions = cursor.fetchall()

    conn.close()

    if not transactions:
        print("\nNo transactions found.")
        return

    print("\n========== TRANSACTION HISTORY ==========\n")

    for transaction in transactions:

        print(f"""
Type        : {transaction[0]}
Amount      : ₹{transaction[1]:.2f}
Balance     : ₹{transaction[2]:.2f}
Date & Time : {transaction[3]}
----------------------------------------
""")