from django.conf import settings
from django.template import Context
from django.template.loader import render_to_string
from .models import User
from .models import user_ordered_by_month_day
from reminder.emails import send_reminder_email
from reminder.emails import send_reminder_email_with_embedded_images


template_text = 'users/msg_card.txt'
template_html = 'users/msg_card.html'


def users_reminder():
    for user in User.objects.all():
        send_reminder_email('roberta.takenaka@scielo.org', 'user item', '?')
        subject = 'Greetings, {}!'.format(user.username)
        message = user.date_joined
        send_reminder_email(user.email, subject, message)


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
    text_message = render_to_string(template_html, context)
    send_reminder_email_with_embedded_images(
        settings.EMAIL_DESTINATARY,
        subject,
        text_message,
        html_message,
        images)


def users_remind_birthday():
    for user in user_ordered_by_month_day('birthday', '01-01'):
        subject = 'Feliz aniversário, {}!'.format(user.username)
        greetings = 'Feliz aniversário!'
        send_greetings(subject, greetings, user)


def users_remind_anniversary():
    for user in user_ordered_by_month_day('birthday', '01-01'):
        subject = '{}, parabéns por {}!'.format(user.username, user.display_years)
        greetings = 'Parabéns por {}!'.format(user.display_years)
        send_greetings(subject, greetings, user)

