from uuid import uuid4

from django.core.validators import MinValueValidator
from django.db import models

from core import constants as const


class Wallet(models.Model):
    '''Модель кошелька.'''

    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    balance = models.DecimalField(
        'Баланс',
        default=const.DEFAULT_BALANCE,
        max_digits=const.MAX_DIGITS,
        decimal_places=const.DECIMAL_PLACES,
        validators=[
            MinValueValidator(
                const.DEFAULT_BALANCE,
                f'Баланс не может быть ниже {const.DEFAULT_BALANCE}.'
            )
        ]
    )

    def __str__(self):
        return f'{self.id}, balance = {self.balance}'


class Transaction(models.Model):
    '''Модель отслеживания транзакций.'''

    class OperationChoices(models.TextChoices):
        '''Тип операций с кошельком.'''

        deposit = const.DEPOSIT
        withdraw = const.WITHDRAW

    wallet = models.ForeignKey(
        Wallet,
        verbose_name='Кошелёк',
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    operation = models.CharField(
        'Тип операции',
        choices=OperationChoices.choices,
        max_length=max((len(oper) for oper in OperationChoices.values)),
        editable=False
    )
    amount = models.DecimalField(
        'Сумма',
        max_digits=const.MAX_DIGITS,
        decimal_places=const.DECIMAL_PLACES,
        editable=False,
        validators=[
            MinValueValidator(
                const.MIN_AMOUNT,
                f'Сумма не может быть ниже {const.MIN_AMOUNT}.'
            )
        ]
    )
    date = models.DateTimeField('Дата и время операции', auto_now_add=True)

    def save(self, *args, **kwargs):
        self.clean_fields()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.wallet.id} - {self.operation} - {self.date}'
