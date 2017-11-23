from django.conf import settings
from django.core.mail import EmailMessage
from django.template import Context
from django.template.loader import render_to_string


def send_reminder_email(email_to, subject, message):
    c = Context({'email': email_to, 'message': message, 'subject': subject})

    if not isinstance(email_to, list):
        email_to = [email_to]

    email_from = settings.DEFAULT_FROM_EMAIL
    email_subject = subject
    email_body = render_to_string('reminder/email_body.txt', c)
    email = EmailMessage(
        email_subject, email_body, email_from,
        email_to, [],
        headers={'Reply-To': email_from}
    )
    return email.send(fail_silently=False)
