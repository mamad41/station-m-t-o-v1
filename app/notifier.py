import smtplib
from email.mime.text import MIMEText
import os

def send_alert_email(subject: str, message: str):
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    recipient = os.getenv("ALERT_RECIPIENT")

    if not smtp_user or not smtp_password:
        print("[SMTP] Identifiants manquants, alerte non envoyée.")
        return

    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = smtp_user
    msg["To"] = recipient

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
            print(f"[SMTP] Alerte transmise à {recipient}")
    except Exception as e:
        print(f"[SMTP] Erreur d'envoi : {e}")