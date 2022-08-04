from .models import Contract, PriceHistory


def track_price_history():
    contracts = Contract.objects.all()
    for contract in contracts:
        PriceHistory.objects.create(contract=contract, price=contract.latest_yes_price)
