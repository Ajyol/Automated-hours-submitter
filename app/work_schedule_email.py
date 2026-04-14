import schedule
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

def job():
    sender_email = os.getenv("SENDER_EMAIL")
    receiver_email = os.getenv("RECEIVER_EMAIL")
    password = os.getenv("EMAIL_PASSWORD")

    # Compute start of week (Monday)
    start_date = datetime.now() - timedelta(days=datetime.now().weekday())
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    dates = [(start_date + timedelta(days=i)).strftime("%B %d") for i in range(5)]

    subject = "Weekly Work Hours Report (Monday–Friday)"
    body = f"""Greetings ma'am,

    I hope you're doing well. I am writing to report the hours I have worked this week, totaling 20 hours. Below is the breakdown of my work schedule:

    {days[0]} ({dates[0]}): 8:00 AM – 11:30 AM, 4:00 PM – 6:00 PM (5.5 hours)
    {days[1]} ({dates[1]}): 8:00 AM – 11:30 AM, 3:30 PM - 5:30 PM (5.5 hours)
    {days[2]} ({dates[2]}): 8:00 AM – 11:30 AM, 3:30 PM – 5:00 PM (5 hours)
    {days[3]} ({dates[3]}): 1:00 PM – 5:00 PM (4 hours)

    Total: 20 hours

    Yours sincerely,  
    Ajyol Dhamala
    """

    msg = MIMEMultipart()
    msg["From"] = f"Ajyol Dhamala <{sender_email}>"
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.send_message(msg)
        print("✅ Weekly hours email sent.")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")


schedule.every().thursday.at("17:00").do(job)

print("⏳ Scheduler running... will send email every Thursday at 5:00 PM.")

while True:
    schedule.run_pending()
    time.sleep(60)
