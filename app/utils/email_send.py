from flask_mail import Message
from app.extensions import mail

def send_verification_email(
    recipient_email,
    verification_url
):

    msg = Message(
        subject="Verify Your Email",
        recipients=[recipient_email]
    )

    msg.body = (
        f"Click the link below "
        f"to verify your account:\n\n"
        f"{verification_url}"
    )

    mail.send(msg)