from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.create_user(email, password, **kwargs)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.email


class Market(models.Model):
    prompt = models.CharField(max_length=255)

    def __str__(self):
        return self.prompt


class Tag(models.Model):
    name = models.CharField(max_length=16)

    def __str__(self):
        return self.name


class MarketTagMap(models.Model):
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__(self):
        return self.market.prompt + " <---> " + self.tag.name


class Contract(models.Model):
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    description = models.TextField()
    projected_end = models.DateTimeField()

    # updated every trade
    latest_yes_price = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(99)])
    latest_price_movement = models.IntegerField(validators=[MinValueValidator(-98), MaxValueValidator(98)])

    @property
    def best_buy_yes(self):
        offer = Offer.objects.filter(
            contract=self, contract_type=Offer.YES, offer_type=Offer.BUY,
        ).order_by('price')[0]

        return offer.price

    @property
    def best_sell_offer(self):
        offer = Offer.objects.filter(
            contract=self, contract_type=Offer.YES, offer_type=Offer.SELL,
        ).order_by('-price')[0]

        return offer.price

    def __str__(self):
        return self.name


class Offer(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    price = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(99)])

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


class PriceHistory(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    price = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(99)])
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.contract.name} @ {self.price} | {self.timestamp}"

    class Meta:
        ordering = ['-timestamp']
