from django.conf import settings
from django.urls import path, include

from api import views
from core import constants as const


router_v1 = settings.API_ROUTER()
router_v1.register('wallets', views.WalletViewSet)

urlpatterns = [
    path(f'{const.ACTUAL_API_VERSION}/', include(router_v1.urls))
]
