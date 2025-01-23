import smtplib
from email.message import EmailMessage

def send_email(subject, body, to_email):
    # Microsoft 365 email credentials
    from_email = "thomas.bjerke@hotmail.com"  # Replace with your Microsoft 365 email
    password = "Heisann123"  # Replace with your Microsoft 365 account password

    # Create the email
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    # Connect to the Microsoft 365 SMTP server
    try:
        with smtplib.SMTP("smtp.office365.com", 587) as smtp:
            smtp.starttls()  # Upgrade the connection to secure
            smtp.login(from_email, password)  # Log in to your account
            smtp.send_message(msg)  # Send the email
            print("Email sent successfully!")
    except Exception as e:
        print("Error sending email:", e)

# Usage
send_email(
    subject="Test Email from Python",
    body="This is a test email sent using Microsoft 365 SMTP server.",
    to_email="kore.andersen@gmail.com"
)