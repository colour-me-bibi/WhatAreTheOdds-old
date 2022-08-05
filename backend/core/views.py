from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialConnectView, SocialLoginView
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import SAFE_METHODS, BasePermission

from .models import Contract, Market, Offer
from .serializers import ContractSerializer, MarketSerializer, OfferSerializer
from .tasks import trade

# TODO upon each offer, look for buyers take until offer is satisfied
# TODO upon each trade, update contract info
# TODO upon resolution, update and finish price history


GITHUB_CALLBACK_URL = "http://localhost:8000/accounts/github/login/callback"


class GitHubLogin(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter
    callback_url = GITHUB_CALLBACK_URL
    client_class = OAuth2Client


class GithubConnect(SocialConnectView):
    adapter_class = GitHubOAuth2Adapter
    callback_url = GITHUB_CALLBACK_URL
    client_class = OAuth2Client


class IsReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(request.method in SAFE_METHODS)


class MarketViewSet(viewsets.ModelViewSet):
    queryset = Market.objects.all()
    serializer_class = MarketSerializer
    # permission_classes = (IsAdminUser | IsReadOnly,)  # TODO ?


class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    # permission_classes = (IsAdminUser | IsReadOnly,)  # TODO ?


class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    # permission_classes = (IsAdminUser | IsReadOnly,)  # TODO ?


@receiver(post_save, sender=Offer)
def start_trading(sender, instance, **kwargs):
    trade.delay(instance)


# queue for admin"s to resolve contracts
# resolution of contracts


@api_view(["GET"])
@permission_classes
def portfolio(request):
    """
    User must be logged in and not be an admin user
    query for all investment's that match this user
    group investments by contract
    sum the shares
    calulate the average share price for each contract
    calculate the total value of all investments
    calculate the total gain/loss of all investments from all investment"s purchase price
    """
    pass
