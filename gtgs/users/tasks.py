from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

from .utils import send_email_all_users


logger = get_task_logger(__name__)


@periodic_task(
    run_every=crontab(hour=[1]),
    name="users_remind"
)
def users_remind():
    logger.info("users_remind")
    send_email_all_users()
