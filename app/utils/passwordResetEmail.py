from flask_mail import Message
from app.extensions import mail

def send_reset_email(
    recipient_email,
    reset_url
):

    msg = Message(
        subject="Reset Your Password",
        recipients=[recipient_email]
    )

    msg.body = (
        f"Click the link below "
        f"to reset your password:\n\n"
        f"{reset_url}"
    )

    mail.send(msg)