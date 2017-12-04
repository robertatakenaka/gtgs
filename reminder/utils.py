from datetime import datetime
from django.conf import settings
from django.template import Context
from django.template.loader import render_to_string
#from app.users.models import user_ordered_by_month_day
from gtgs.users.models import user_ordered_by_month_day
from .emails import send_reminder_email
from .emails import send_reminder_email_with_embedded_images


template_text = 'users/msg_card.txt'
template_html = 'users/msg_card.html'


def send_absence_of_message(date, greetings):
    send_reminder_email(
        settings.EMAIL_ADMIN,
        date + ' ' + greetings,
        date + ' ' + greetings)


def send_greetings(email_to, greetings_function, user):
    subject, greetings = greetings_function(user)
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
        email_to,
        subject,
        text_message,
        html_message,
        images)


def birthdate_greetings(user):
    subject = 'Feliz aniversário, {}!'.format(user.fullname())
    greetings = 'Feliz aniversário!'
    return subject, greetings


def anniversary_greetings(user):
    years = user.display_years()
    subject = '{}, parabéns por {}!'.format(user.fullname(), years)
    greetings = 'Parabéns por {}!'.format(years)
    return subject, greetings


def remind_date(reminder):
    month_day = datetime.now().isoformat()[5:10]
    if '-' in reminder.default_date:
        month_day = reminder.default_date
    greeting_function = birthdate_greetings if reminder.name == 'birthdate' else anniversary_greetings
    users = user_ordered_by_month_day(reminder.name, month_day)
    if len(users) == 0:
        send_absence_of_message(month_day, reminder.name)
    else:
        for user in users:
            send_greetings(email_to, greeting_function, user)
