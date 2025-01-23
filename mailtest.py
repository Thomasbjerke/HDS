import smtplib
from email.message import EmailMessage

def send_email(subject, body, to_email):
    # Your email credentials
    from_email = "kore.andersen@gmail.com"
    password = "vaqq npaj eoaf yyet"

    # Setting up the email content
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    # Connect to the SMTP server
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:  # Use your provider's SMTP server here
            smtp.starttls()  # Secure the connection
            smtp.login(from_email, password)
            smtp.send_message(msg)
            print("Email sent successfully!")
    except Exception as e:
        print("Error sending email:", e)

# Usage
send_email("Prøver ny måte å sende mail", "Hei Thomas. Jeg prøver å sende mail programmatisk. Funker det?", "thomas.bjerke@hotmail.com")
