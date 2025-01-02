from decimal import Decimal

from rest_framework.exceptions import ValidationError

from .conftest import BaseTestCase
from api.serializers import TransactionSerializer, WalletSerializer
from core import constants as const
from core.models import Transaction


class TestSerializers(BaseTestCase):
    '''Класс тестов сериализаторов.'''

    AMOUNT = Decimal('100.00')
    TRANSACTION_CREATED_COUNT = 1

    def test_wallet(self):
        '''Тест сериализатора кошелька.'''
        expected_data = {
            'id': self.wallet.id.__str__(),
            'balance': Decimal(f'{self.wallet.balance:.2f}')
        }
        serializer_data = WalletSerializer(self.wallet).data
        self.assertEqual(expected_data, serializer_data)

    def test_transaction_with_valid_data(self):
        '''Тест сериализатора транзакции с валидным запросом.'''
        expected_data = {
            'operationType': const.DEPOSIT,
            'amount': self.AMOUNT,
            'balance': Decimal(f'{self.wallet.balance:.2f}') + self.AMOUNT
        }
        request_data = {
            'operationType': const.DEPOSIT,
            'amount': self.AMOUNT
        }
        expected_balance = self.wallet.balance + self.AMOUNT
        expected_transactions_count = Transaction.objects.count() + self.TRANSACTION_CREATED_COUNT
        serializer = TransactionSerializer(
            data=request_data,
            context={'wallet': self.wallet}
        )
        serializer.is_valid(True)
        serializer.save()
        self.wallet.refresh_from_db()
        self.assertEqual(expected_data, serializer.data)
        self.assertEqual(expected_balance, self.wallet.balance)
        self.assertEqual(expected_transactions_count, Transaction.objects.count())

    def test_transaction_with_invalid_data(self):
        '''Тест сериализатора транзакции с невалидными запросами.'''
        operations_amounts = (
            {'operationType': 'dr', 'amount': self.AMOUNT},
            {'operationType': '', 'amount': self.AMOUNT},
            {'operationType': 1, 'amount': self.AMOUNT},
            {'operationType': None, 'amount': self.AMOUNT},
            {'amount': self.AMOUNT},
            {'operationType': const.DEPOSIT, 'amount': 0},
            {'operationType': const.DEPOSIT, 'amount': -20},
            {'operationType': const.DEPOSIT, 'amount': None},
            {'operationType': const.DEPOSIT, 'amount': ''},
            {'operationType': const.DEPOSIT},
        )
        for request_data in operations_amounts:
            with self.subTest(
                'Ошибка при передаче в сериализатор невалидного запроса '
                f'{request_data}'
            ):
                serializer = TransactionSerializer(
                    data=request_data,
                    context={'wallet': self.wallet}
                )
                self.assertRaises(ValidationError, serializer.is_valid, True)
