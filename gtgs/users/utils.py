from reminder.emails import send_reminder_email
from .models import User


def send_email_all_users():
    for result in User.objects.all():
        send_reminder_email('roberta.takenaka@scielo.org', 'user item', '?')
        subject = 'Greetings, {}!'.format(result.username)
        message = result.date_joined
        send_reminder_email(result.email, subject, message)
