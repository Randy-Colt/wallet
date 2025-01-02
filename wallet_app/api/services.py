from decimal import Decimal

from django.db.models import F
from django.core.exceptions import ValidationError

from core import constants as const
from core.models import Wallet


def execute_transaction(
    wallet: Wallet,
    operation: str,
    amount: Decimal
) -> None:
    '''
    Проведение операции с балансом кошелька.

    :param wallet: Обязательный; экземпляр кошелька,
                   баланс которого нужно изменить.
    :param operation: Обязательный; тип операции. Если операция неизвестна,
                      поднимается исключение ValidationError.
    :param amount: Обязательный; сумма, с которой будет проведена операция.
                   Если сумма отрицательна, поднимается ValidationError.
    '''
    if operation == const.DEPOSIT:
        wallet.balance = F('balance') + amount
    elif operation == const.WITHDRAW:
        wallet.balance = F('balance') - amount
    else:
        raise ValidationError('Неизвестная операция.')
    wallet.save(update_fields=['balance'])
    wallet.refresh_from_db()
    wallet.clean_fields()
