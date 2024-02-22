from flask import Flask

from config import celery_init_app

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