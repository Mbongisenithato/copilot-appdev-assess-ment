import time
import schedule
import argparse
import smtplib
from email.message import EmailMessage

def send_reminder(message: str, method: str = "print", email: str = None):
    """
    Sends a reminder message to the user.

    Args:
        message (str): The reminder content.
        method (str): 'print' or 'email'
        email (str): Recipient email address (if method is 'email')
    """
    if method == "print":
        print(f"🔔 Reminder: {message}")
    elif method == "email" and email:
        try:
            msg = EmailMessage()
            msg.set_content(message)
            msg["Subject"] = "Reminder"
            msg["From"] = "reminder@app.com"
            msg["To"] = email

            # For local testing with aiosmtpd on port 1025
            with smtplib.SMTP("localhost", 1025) as server:
                server.send_message(msg)

            print(f"🔔 Reminder sent to {email}")
        except Exception as e:
            print(f"❌ Failed to send email: {e}")
    else:
        print("⚠️ Invalid method or missing email address.")

def main():
    parser = argparse.ArgumentParser(description="Simple Reminder App")
    parser.add_argument(
        "--message", type=str, default="Take a short break!",
        help="Reminder message"
    )
    parser.add_argument(
        "--interval", type=int, default=10,
        help="Interval in seconds"
    )
    parser.add_argument(
        "--method", choices=["print", "email"], default="print",
        help="Reminder method"
    )
    parser.add_argument(
        "--email", type=str,
        help="Recipient email address (required if method is 'email')"
    )
    args = parser.parse_args()

    if args.method == "email" and not args.email:
        parser.error("--email is required when method is 'email'")

    schedule.every(args.interval).seconds.do(
        send_reminder,
        message=args.message,
        method=args.method,
        email=args.email
    )

    print("✅ Reminder app started. Press Ctrl+C to stop.")
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()