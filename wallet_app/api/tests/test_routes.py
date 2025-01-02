from rest_framework import status

from .conftest import BaseTestCase


class TestRoutes(BaseTestCase):
    '''Класс тестов ответов API по GET-запросу.'''

    def test_wallet_balance(self):
        '''Тест доступности эндпоинта получения баланса.'''
        response = self.client.get(self.url_wallet_detail)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
