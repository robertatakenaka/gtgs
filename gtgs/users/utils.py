from datetime import datetime
from django.conf import settings
from django.template import Context
from django.template.loader import render_to_string
from .models import user_ordered_by_month_day
from reminder.emails import send_reminder_email
from reminder.emails import send_reminder_email_with_embedded_images


template_text = 'users/msg_card.txt'
template_html = 'users/msg_card.html'


def send_absence_of_message(date, greetings):
    send_reminder_email(
        settings.DJANGO_DEFAULT_FROM_EMAIL,
        date + ' ' + greetings,
        date + ' ' + greetings)


def send_greetings(subject, greetings, user):
    context = Context(
                {
                    'fullname': user.fullname,
                    'greetings': greetings,
                    'photo': user.photo
                }
            )
    images = [user.photo]

    html_message = render_to_string(template_html, context)
    text_message = render_to_string(template_text, context)

    send_reminder_email_with_embedded_images(
        settings.EMAIL_DESTINATION,
        subject,
        text_message,
        html_message,
        images)


def users_remind_birthday():
    month_day = '06-07'
    month_day = datetime.now().isoformat()[5:10]
    date_type = 'birthdate'
    users = user_ordered_by_month_day('birthdate', month_day)
    if len(users) == 0:
        send_absence_of_message(month_day, date_type)
    else:
        for user in users:
            subject = 'Feliz aniversário, {}!'.format(user.fullname())
            greetings = 'Feliz aniversário!'
            send_greetings(subject, greetings, user)


def users_remind_anniversary():
    month_day = '06-01'
    month_day = datetime.now().isoformat()[5:10]
    date_type = 'anniversary'
    users = user_ordered_by_month_day('anniversary', month_day)
    if len(users) == 0:
        send_absence_of_message(month_day, date_type)
    else:
        for user in users:
            subject = '{}, parabéns por {}!'.format(user.fullname(), user.display_years())
            greetings = 'Parabéns por {}!'.format(user.display_years())
            send_greetings(subject, greetings, user)
