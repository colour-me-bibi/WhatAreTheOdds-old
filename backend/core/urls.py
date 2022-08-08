from dj_rest_auth.registration.views import (SocialAccountDisconnectView,
                                             SocialAccountListView)
from django.contrib import admin
from django.urls import include, path
from rest_framework_nested import routers

from .views import (ContractViewSet, GithubConnect, GitHubLogin, MarketViewSet,
                    OfferViewSet)

# from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

router = routers.DefaultRouter()
router.register(r"markets", MarketViewSet)

markets_router = routers.NestedSimpleRouter(router, r"markets", lookup="market")
markets_router.register(r"contracts", ContractViewSet)

contracts_router = routers.NestedSimpleRouter(markets_router, r"contracts", lookup="contract")
contracts_router.register(r"offers", OfferViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),

    # path('schema/', SpectacularAPIView.as_view(), name='schema'),
    # path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path("auth/", include("dj_rest_auth.urls")),
    path("auth/registration/", include("dj_rest_auth.registration.urls")),
    path("auth/github/", GitHubLogin.as_view()),
    path("auth/github/connect/", GithubConnect.as_view()),
    path("auth/socialaccounts/", SocialAccountListView.as_view()),
    path("auth/socialaccounts/<int:pk>/disconnect/", SocialAccountDisconnectView.as_view()),

    path("", include(router.urls)),
    path("", include(markets_router.urls)),
    path("", include(contracts_router.urls)),
]
