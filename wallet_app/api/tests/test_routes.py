from django.urls import reverse
from rest_framework import status

from .conftest import BaseTestCase


class TestRoutes(BaseTestCase):
    '''Класс тестов ответов API по GET-запросу.'''

    def test_wallet_get_balance(self):
        '''Тест доступности эндпоинта получения баланса.'''
        urls_statuses = (
            (self.url_wallet_detail, status.HTTP_200_OK),
            (reverse('wallet-detail', args=['non-existent']), status.HTTP_404_NOT_FOUND)
        )
        for url, expected_status in urls_statuses:
            with self.subTest(
                f'Неверный код статуса по адресу: {url} '
                f'ожидается {expected_status}'
            ):
                response = self.client.get(url)
                self.assertEqual(expected_status, response.status_code)
