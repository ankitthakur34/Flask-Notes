from flask_mail import Message

from app.extensions import mail

from app.backgroundJobs.celery_app import celery


@celery.task
def send_email_task(
    recipient_email,
    subject,
    body
):

    msg = Message(
        subject=subject,
        recipients=[recipient_email]
    )

    msg.body = body

    mail.send(msg)

    return "Email Sent"