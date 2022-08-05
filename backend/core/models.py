from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class CentsField(models.IntegerField):  # TODO maybe change the name?
    def __init__(self, *args, **kwargs):
        kwargs["validators"] = [MinValueValidator(1), MaxValueValidator(99)]
        super().__init__(*args, **kwargs)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # TODO

    def __str__(self):
        return f"{self.user.username}'s profile"


class Tag(models.Model):
    name = models.CharField(max_length=16, primary_key=True)

    def __str__(self):
        return self.name


class Market(models.Model):
    prompt = models.CharField(max_length=255)
    # slug = models.SlugField(max_length=255, unique=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.prompt


class Contract(models.Model):
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    name = models.CharField(max_length=32, default="Latest Price")
    # slug = models.SlugField(max_length=32, unique=True)
    description = models.TextField()
    projected_end = models.DateTimeField(blank=True, null=True)

    # updated every trade
    latest_yes_price = CentsField(blank=True, null=True)
    latest_price_movement = models.IntegerField(
        validators=[MinValueValidator(-98), MaxValueValidator(98)],
        blank=True, null=True,
    )

    @property
    def best_buy_yes(self):
        offer = Offer.objects.filter(
            contract=self, contract_type=Offer.YES, offer_type=Offer.BUY,
        ).order_by("price").first()

        return offer.price if offer else None

    @property
    def best_sell_offer(self):
        offer = Offer.objects.filter(
            contract=self, contract_type=Offer.YES, offer_type=Offer.SELL,
        ).order_by("-price").first()

        return offer.price if offer else None

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["market", "name"], name="unique_contract_name"),
        ]


class Offer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    price = CentsField()

    YES = "Y"
    NO = "N"
    CONTRACT_TYPE_CHOICES = (
        (YES, "Yes"),
        (NO, "No"),
    )
    contract_type = models.CharField(max_length=1, choices=CONTRACT_TYPE_CHOICES)

    BUY = "B"
    SELL = "S"
    OFFER_TYPE_CHOICES = (
        (BUY, "Buy"),
        (SELL, "Sell"),
    )
    offer_type = models.CharField(max_length=1, choices=OFFER_TYPE_CHOICES)

    def __str__(self):
        return f"{self.offer_type} {self.contract_type} @ {self.price} | {self.contract.name}"


class PriceHistory(models.Model):  # TODO probably change to a linked list kind of thing
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    price = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.contract.name} @ {self.price} | {self.timestamp}"

    class Meta:
        ordering = ["-timestamp"]


class Investment(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    purchase_price = CentsField()
    purchase_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.portfolio.user.name}'s investment into {self.contract.name} @ {self.purchase_price}"
