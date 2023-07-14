import smtplib
import email_config
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(sender=email_config.SENDER, receiver=email_config.RECEIVER, subject=email_config.SUBJECT, message = email_config.MESSAGE):
    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Cc'] = ",".join(email_config.CC)
    msg['Subject'] = subject


    message = email_config.MESSAGE + '\n' + message + '\n' + email_config.FOOTER
    # Attach the message to the email
    html_content = f"""<html><body><style> 
    table, th, td {{ border: 1px solid black; border-collapse: collapse; }}
    th, td {{ padding: 5px; }}
    </style>{message}</body></html>"""
    msg.attach(MIMEText(html_content, 'html'))
    try:
        with smtplib.SMTP(email_config.SMPT_SERVER, email_config.SMTP_PORT) as server:
            server.starttls()
            server.login(email_config.EMAIL_USERNAME, email_config.EMAIL_PASSWORD)
            server.send_message(msg)
        print('Email sent successfully!')
    except Exception as e:
        print('An error occurred while sending the email:', str(e))