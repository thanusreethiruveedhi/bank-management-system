from src.database import create_tables
from src.auth import register_user, login_user
from src.account import (
    create_account,
    view_account,
    check_balance
)
from src.transaction import (
    deposit_money,
    withdraw_money,
    transaction_history
)
from src.statement import generate_statement

logged_user = None


def login_required():
    global logged_user

    if logged_user is None:
        print("\nPlease login first.")
        return False

    return True


def menu():

    print("\n" + "=" * 60)
    print("           BANK MANAGEMENT SYSTEM")
    print("=" * 60)

    print("1. Register")
    print("2. Login")
    print("3. Create Bank Account")
    print("4. View Account")
    print("5. Check Balance")
    print("6. Deposit Money")
    print("7. Withdraw Money")
    print("8. Transaction History")
    print("9. Generate PDF Statement")
    print("10. Logout")
    print("11. Exit")

    print("=" * 60)


def main():

    global logged_user

    create_tables()

    while True:

        menu()

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            register_user()

        elif choice == "2":
            logged_user = login_user()

        elif choice == "3":
            if login_required():
                create_account(logged_user["email"])

        elif choice == "4":
            if login_required():
                view_account(logged_user["email"])

        elif choice == "5":
            if login_required():
                check_balance(logged_user["email"])

        elif choice == "6":
            if login_required():
                deposit_money(logged_user["email"])

        elif choice == "7":
            if login_required():
                withdraw_money(logged_user["email"])

        elif choice == "8":
            if login_required():
                transaction_history(logged_user["email"])

        elif choice == "9":
            if login_required():
                generate_statement(logged_user["email"])

        elif choice == "10":

            if logged_user:
                print(f"\n{logged_user['name']} logged out successfully.")
                logged_user = None
            else:
                print("\nNo user is logged in.")

        elif choice == "11":
            print("\nThank you for using Bank Management System.")
            break

        else:
            print("\nInvalid choice.")


if __name__ == "__main__":
    main()