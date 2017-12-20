from django.conf import settings
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import render_to_string
from email.mime.image import MIMEImage


def normalize_email_to(email_to):
    email_to = email_to.replace(',', ';')
    if ';' in email_to:
        email_to = email_to.split(';')
    if not isinstance(email_to, list):
        email_to = [email_to]
    return email_to


def send_reminder_email(email_to, subject, message):
    c = Context({'email': email_to, 'message': message, 'subject': subject})

    email_to = normalize_email_to(email_to)

    email_from = settings.DEFAULT_FROM_EMAIL
    email_subject = subject
    email_body = render_to_string('reminder/email_body.txt', c)
    email = EmailMessage(
        email_subject, email_body, email_from,
        email_to, [],
        headers={'Reply-To': email_from}
    )
    return email.send(fail_silently=False)


def send_reminder_email_with_embedded_images(
        email_to, subject, text_message, html_message, images=None):
    images = images or []
    email_to = normalize_email_to(email_to)

    msg = EmailMultiAlternatives(
            subject,
            text_message,
            settings.DEFAULT_FROM_EMAIL,
            email_to)
    msg.attach_alternative(html_message, "text/html")
    msg.mixed_subtype = 'html'

    for f in images:
        fp = open(f.path, 'rb')
        msg_img = MIMEImage(fp.read())
        fp.close()
        msg_img.add_header('Content-ID', '<{}>'.format(f))
        msg.attach(msg_img)

    msg.send()
