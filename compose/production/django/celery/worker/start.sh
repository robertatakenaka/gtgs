#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset


celery -A gtgs.taskapp worker -l INFO
