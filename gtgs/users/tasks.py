from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

from .utils import users_reminder
from .utils import users_remind_birthday
from .utils import users_remind_anniversary


logger = get_task_logger(__name__)


@periodic_task(
    run_every=crontab(hour=[3]),
    name="users_task_reminder"
)
def users_task_reminder():
    logger.info("users_task_reminder")
    users_reminder()


@periodic_task(
    run_every=crontab(hour=[7]),
    name="users_task_remind_birthday"
)
def users_task_remind_birthday():
    logger.info("users_task_remind_birthday")
    users_remind_birthday()


@periodic_task(
    run_every=crontab(hour=[7]),
    name="users_task_remind_anniversary"
)
def users_task_remind_anniversary():
    logger.info("users_task_remind_anniversary")
    users_remind_anniversary()
