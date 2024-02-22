from flask import Flask
from celery import shared_task
from config import celery_init_app

from random import randrange

app = Flask(__name__)

# Redis port: 6379 is non-SSL
# Redis port: 6380 is SSL
app.config.from_mapping(
    CELERY=dict(
        broker_url="redis://redis-service:6379",
        result_backend="redis://redis-service:6379",
        task_ignore_result=True,
    ),
)

celery_app = celery_init_app(app)


@shared_task(ignore_result=False)
def add_together(a: int, b: int) -> int:
    return a + b

@app.get("/task/add")
def start_add() -> dict[str, object]:
    a = randrange(10)
    b = randrange(20)
    result = add_together.delay(a, b)
    return {"result_id": result.id}