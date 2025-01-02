from django.urls import reverse
from rest_framework.test import APITestCase

from core.models import Wallet


class BaseTestCase(APITestCase):
    '''Базовый класс тестов с подготовленными данными.'''

    @classmethod
    def setUpTestData(cls):
        cls.wallet = Wallet.objects.create()
        cls.url_wallet_detail = reverse('wallet-detail', args=[cls.wallet.id])
        cls.url_wallet_create = reverse('wallet-list')
        cls.url_wallet_operation = reverse(
            'wallet-execude-operation',
            args=[cls.wallet.id]
        )
