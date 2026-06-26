from app import create_app
from app.backgroundJobs.celery_app import (
    make_celery,
    celery
)

app = create_app()

make_celery(app)