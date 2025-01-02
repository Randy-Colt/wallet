from rest_framework import status

from .conftest import BaseTestCase
from core import constants as const
from core.models import Transaction, Wallet


class TestWalletLogic(BaseTestCase):
    '''Класс тестов создания кошелька и операций с ним.'''

    WALLET_CREATED_COUNT = 1
    TRANSACTION_CREATED_COUNT = 1
    AMOUNT = 100

    def test_wallet_create(self):
        '''Тест создания кошелька.'''
        expected_wallets_count = Wallet.objects.count() + self.WALLET_CREATED_COUNT
        response = self.client.post(self.url_wallet_create)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(expected_wallets_count, Wallet.objects.count())

    def test_valid_transactions(self):
        '''Тест проведения валидных транзакций.'''
        operations_amount = (
            (const.DEPOSIT, self.AMOUNT),
            (const.WITHDRAW, -self.AMOUNT)
        )
        for operation, amount in operations_amount:
            with self.subTest(f'Ошибка на операции {operation}'):
                expected_transactions_count = Transaction.objects.count() + self.TRANSACTION_CREATED_COUNT
                data = {'operationType': operation, 'amount': self.AMOUNT}
                expected_balance = self.wallet.balance + amount
                response = self.client.post(self.url_wallet_operation, data)
                self.assertEqual(status.HTTP_201_CREATED, response.status_code)
                self.wallet.refresh_from_db()
                self.assertEqual(expected_balance, self.wallet.balance)
                self.assertEqual(expected_transactions_count, Transaction.objects.count())

    def test_invalid_transactions(self):
        '''Тест проведения невалидных транзакций.'''
        operations_amounts = (
            ('w', self.AMOUNT),
            ('', self.AMOUNT),
            (0, self.AMOUNT),
            (None, self.AMOUNT),
            (const.DEPOSIT, -1),
            (const.DEPOSIT, 'w'),
            (const.DEPOSIT, ''),
            (const.DEPOSIT, None),
            (const.DEPOSIT, 0)
        )
        expected_transactions_count = Transaction.objects.count()
        expected_balance = self.wallet.balance
        for operation, amount in operations_amounts:
            with self.subTest(
                f'Неправильная обработка операции {operation} и суммы {amount}'
            ):
                data = {'operationType': operation, 'amount': amount}
                response = self.client.post(
                    self.url_wallet_operation,
                    data,
                    'json'
                )
                self.assertEqual(
                    status.HTTP_400_BAD_REQUEST,
                    response.status_code
                )
                self.assertEqual(expected_transactions_count, Transaction.objects.count())
                self.wallet.refresh_from_db()
                self.assertEqual(expected_balance, self.wallet.balance)
