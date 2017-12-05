#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset


#celery -A gtgs.taskapp beat -l INFO
celery -A gtgs.taskapp beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler