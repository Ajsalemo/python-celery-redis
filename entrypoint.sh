#!/bin/bash

celery -A app.celery_app worker --loglevel INFO & \
    celery -A app.celery_app beat  & \
    gunicorn -b 0.0.0.0:8000 app:app --timeout 600 --access-logfile "-" --error-logfile "-"