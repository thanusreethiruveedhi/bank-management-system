import hashlib
from src.database import connect_db


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register_user():

    conn = connect_db()
    cursor = conn.cursor()

    print("\n========== USER REGISTRATION ==========")

    full_name = input("Full Name : ").strip()
    email = input("Email      : ").strip().lower()
    phone = input("Phone      : ").strip()
    password = input("Password   : ").strip()

    if not full_name or not email or not phone or not password:
        print("\nAll fields are required.")
        conn.close()
        return

    cursor.execute(
        "SELECT * FROM users WHERE email=?",
        (email,)
    )

    if cursor.fetchone():
        print("\nUser already exists.")
        conn.close()
        return

    role = "admin" if email == "admin@bank.com" else "user"

    cursor.execute("""
        INSERT INTO users(
            full_name,
            email,
            phone,
            password,
            role
        )
        VALUES(?,?,?,?,?)
    """, (
        full_name,
        email,
        phone,
        hash_password(password),
        role
    ))

    conn.commit()
    conn.close()

    print("\nRegistration Successful!")


def login_user():

    conn = connect_db()
    cursor = conn.cursor()

    print("\n========== LOGIN ==========")

    email = input("Email    : ").strip().lower()
    password = input("Password : ").strip()

    cursor.execute("""
        SELECT full_name, role
        FROM users
        WHERE email=? AND password=?
    """, (
        email,
        hash_password(password)
    ))

    user = cursor.fetchone()

    conn.close()

    if user:
        print(f"\nWelcome {user[0]}!")

        return {
            "name": user[0],
            "email": email,
            "role": user[1]
        }

    print("\nInvalid email or password.")
    return None


def list_users():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT full_name, email, phone, role
        FROM users
        ORDER BY full_name
    """)

    users = cursor.fetchall()

    conn.close()

    if not users:
        print("\nNo users found.")
        return

    print("\n========== USERS ==========\n")

    for user in users:
        print(f"""
Name  : {user[0]}
Email : {user[1]}
Phone : {user[2]}
Role  : {user[3]}
------------------------------
""")