from flask import Flask
from celery import shared_task
from celery.result import AsyncResult
from config import celery_init_app

from random import randrange
from datetime import datetime


app = Flask(__name__)

# Redis port: 6379 is non-SSL
# Redis port: 6380 is SSL
app.config.from_mapping(
    CELERY=dict(
        broker_url="redis://redis-service:6379",
        result_backend="redis://redis-service:6379",
        task_ignore_result=True,
        # https://docs.celeryq.dev/en/stable/userguide/configuration.html#broker-connection-retry-on-startup
        broker_connection_retry_on_startup=True,
    ),
)

celery_app = celery_init_app(app)

# Set up get_current_datetime() to run every 30 seconds
@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(30.0, get_current_datetime.s(), name='get-date-and-time-ever-30-seconds')


@shared_task(ignore_result=False)
def add_together(a: int, b: int) -> int:
    return a + b


@shared_task(ignore_result=False)
def get_current_datetime() -> str:
    print(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
    return datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')


@app.get("/task/add")
def start_add() -> dict[str, object]:
    a = randrange(10)
    b = randrange(20)
    result = add_together.delay(a, b)
    return {"result_id": result.id}


@app.get("/task/result/<id>")
def task_result(id: str) -> dict[str, object]:
    result = AsyncResult(id)
    return {
        "ready": result.ready(),
        "successful": result.successful(),
        "value": result.result if result.ready() else None,
    }
