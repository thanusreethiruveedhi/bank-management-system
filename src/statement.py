import os
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

from src.database import connect_db

REPORTS_DIR = "reports"
os.makedirs(REPORTS_DIR, exist_ok=True)


def generate_statement(user_email):

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

    if account is None:
        print("\nNo account found.")
        conn.close()
        return

    account_no, account_type, balance = account

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

    file_path = os.path.join(REPORTS_DIR, f"{account_no}_statement.pdf")

    styles = getSampleStyleSheet()

    document = SimpleDocTemplate(file_path)

    story = []

    story.append(
        Paragraph(
            "<b><font size='18'>Bank Account Statement</font></b>",
            styles["Title"]
        )
    )

    story.append(Paragraph("<br/>", styles["BodyText"]))

    story.append(
        Paragraph(f"<b>Account Number:</b> {account_no}", styles["BodyText"])
    )

    story.append(
        Paragraph(f"<b>Account Type:</b> {account_type}", styles["BodyText"])
    )

    story.append(
        Paragraph(f"<b>Current Balance:</b> ₹{balance:.2f}", styles["BodyText"])
    )

    story.append(Paragraph("<br/>", styles["BodyText"]))

    story.append(
        Paragraph("<b>Transaction History</b>", styles["Heading2"])
    )

    story.append(Paragraph("<br/>", styles["BodyText"]))

    if not transactions:
        story.append(
            Paragraph("No transactions available.", styles["BodyText"])
        )
    else:
        for transaction in transactions:
            story.append(
                Paragraph(
                    f"""
                    <b>{transaction[0]}</b><br/>
                    Amount: ₹{transaction[1]:.2f}<br/>
                    Balance: ₹{transaction[2]:.2f}<br/>
                    Date: {transaction[3]}
                    <br/><br/>
                    """,
                    styles["BodyText"]
                )
            )

    document.build(story)

    print("\nStatement generated successfully.")
    print(f"Saved to: {file_path}")