from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

from .utils import remind_date
from .models import Reminder


logger = get_task_logger(__name__)

"""
def task_info(name):
    try:
        Reminder.objects.get(name=name)
    except Reminder.DoesNotExist:
        return Reminder.create()


REMINDERS = {
        'birthdate': task_info('birthdate'),
        'anniversary': task_info('anniversary'),
    }

BIRTHDATE_HOUR = 6 if REMINDERS['birthdate'] is None else REMINDERS['birthdate'].hour
ANNIVERSARY_HOUR = 6 if REMINDERS['anniversary'] is None else REMINDERS['anniversary'].hour


def task_remind(name):
    logger.info("task_remind_{}".format(name))
    if REMINDERS[name] is not None:
        if REMINDERS[name].is_active is True:
            remind_date(REMINDERS[name])
        else:
            logger.info("task_remind_birthday: NOT_ACTIVE")


@periodic_task(
    run_every=crontab(hour=BIRTHDATE_HOUR),
    name="task_remind_birthday"
)
def task_remind_birthday():
    task_remind('birthdate')


@periodic_task(
    run_every=crontab(hour=ANNIVERSARY_HOUR),
    name="task_remind_anniversary"
)
def task_remind_anniversary():
    task_remind('anniversary')
"""