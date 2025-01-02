from decimal import Decimal

# Константы для Decimal-значений
MAX_DIGITS = 21
DECIMAL_PLACES = 2

# Константа баланса кошелька
DEFAULT_BALANCE = Decimal('0.0')

# Минимальная сумма для пополнения/снятия
MIN_AMOUNT = Decimal('1.0')

# Названия типов операций
DEPOSIT = 'DEPOSIT'
WITHDRAW = 'WITHDRAW'

# Версия API
ACTUAL_API_VERSION = 'v1'
