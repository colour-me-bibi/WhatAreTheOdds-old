from rest_framework import serializers

from .models import Contract, Investment, Market, Offer, PriceHistory, Tag


# class UserCreateSerializer(UserCreateSerializer):  # TODO ???
#     class Meta(UserCreateSerializer.Meta):
#         model = get_user_model()
#         fields = ("id", "email", "name", "password")


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class MarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = '__all__'


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = '__all__'


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = '__all__'


class PriceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceHistory
        fields = '__all__'


class InvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investment
        fields = '__all__'
