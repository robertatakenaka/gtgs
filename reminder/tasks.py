from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

from .utils import remind_date
from .models import Reminder


logger = get_task_logger(__name__)


def task_remind(name):
    logger.info("task_remind({}): inicio".format(name))
    reminder = Reminder.objects.get(name=name)
    if reminder is not None:
        if reminder.is_active is True:
            remind_date(reminder)
        else:
            logger.info("task_remind({}): reminder.is_active is False".format(name))
    else:
        logger.info("task_remind({}): {}".format(name, 'reminder is None'))
    logger.info("task_remind({}): fim".format(name))


@periodic_task(
    run_every=crontab(hour=7, minute=30),
    name="task_remind_birthday"
)
def task_remind_birthday():
    task_remind('birthdate')


@periodic_task(
    run_every=crontab(hour=7, minute=40),
    name="task_remind_anniversary"
)
def task_remind_anniversary():
    task_remind('anniversary')
