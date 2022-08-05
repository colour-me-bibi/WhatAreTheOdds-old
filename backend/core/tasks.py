
from celery import shared_task

from .models import Offer


@shared_task
def trade(instance):
    print(instance.id)
