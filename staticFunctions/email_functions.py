import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(receiver_email, subject, body, body_type="plain"):
    sender_email = "test1.wonderbiz@gmail.com"  # Replace with your email address
    password = "lnmgtmzpuhsubskx"  # Replace with your email password

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email

    # Turn the body into a MIMEText object
    part = MIMEText(body, body_type)

    # Attach the part into message container
    message.attach(part)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
    except Exception as e:
        raise RuntimeError(f"Failed to send email. Error: {str(e)}")