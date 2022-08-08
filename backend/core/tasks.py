
from celery import shared_task

from .models import Contract, Offer, PriceHistory


@shared_task
def trade(instance):
    print(instance.id)


@shared_task
def record_price_history():
    contracts = Contract.objects.all()
    for contract in contracts:
        PriceHistory.objects.create(contract=contract, price=contract.latest_yes_price)
