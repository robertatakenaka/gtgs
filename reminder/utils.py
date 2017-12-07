from datetime import datetime
from django.template import Context
from django.template.loader import render_to_string
from celery.utils.log import get_task_logger
from gtgs.users.models import user_ordered_by_month_day
from gtgs.users.models import get_sysadmin_email
from .emails import send_reminder_email
from .emails import send_reminder_email_with_embedded_images


template_text = 'users/msg_card.txt'
template_html = 'users/msg_card.html'

logger = get_task_logger(__name__)


def birthdate_greetings(user):
    subject = 'Feliz aniversário, {}!'.format(user.fullname())
    greetings = 'Feliz aniversário!'
    return subject, greetings


def anniversary_greetings(user):
    years = user.display_years()
    subject = '{}, parabéns por {}!'.format(user.fullname(), years)
    greetings = 'Parabéns por {}!'.format(years)
    return subject, greetings


GREETINGS = {
    'birthdate': birthdate_greetings,
    'anniversary': anniversary_greetings,
}


def send_absence_of_message(date, reminder):
    email_to = reminder.email_to_alt
    if '@' not in email_to:
        email_to = get_sysadmin_email()
    send_reminder_email(
        email_to,
        date + ' ' + reminder.name,
        date + ' ' + reminder.name)


def send_greetings(email_to, greetings_function, user):
    subject, greetings = ('', '') if greetings_function is None else greetings_function(user)
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


def remind_date(reminder):
    logger.info("remind_date(): inicio: name={}".format(reminder.name))

    month_day = datetime.now().isoformat()[5:10]
    logger.info("remind_date(): today={}".format(month_day))

    if '-' in reminder.default_date:
        month_day = reminder.default_date
        logger.info("remind_date(): month_day={}".format(month_day))
    users = user_ordered_by_month_day(reminder.name, month_day)
    if len(users) == 0:
        logger.info("remind_date(): mensagem ninguem nesta data {}".format(month_day))
        send_absence_of_message(month_day, reminder)
    else:
        for user in users:
            logger.info("remind_date(): mensagem para {} sobre {}".format(reminder.email_to, user.fullname))
            send_greetings(reminder.email_to, GREETINGS.get(reminder.name), user)
