from rest_framework import serializers

from api.services import execute_transaction
from core.models import Transaction, Wallet
from core import constants as const


class WalletSerializer(serializers.ModelSerializer):
    '''Сериализатор кошелька.'''

    class Meta:
        model = Wallet
        fields = ('id', 'balance')
        extra_kwargs = {'balance': {'coerce_to_string': False}}


class TransactionSerializer(serializers.ModelSerializer):
    '''Сериализатор транзакций.'''

    operationType = serializers.ChoiceField(
        Transaction.OperationChoices.choices,
        source='operation'
    )
    balance = serializers.DecimalField(
        source='wallet.balance',
        read_only=True,
        max_digits=const.MAX_DIGITS,
        decimal_places=const.DECIMAL_PLACES,
        coerce_to_string=False
    )
    amount = serializers.DecimalField(
        max_digits=const.MAX_DIGITS,
        decimal_places=const.DECIMAL_PLACES,
        min_value=const.MIN_AMOUNT,
        coerce_to_string=False
    )

    class Meta:
        model = Transaction
        fields = ('operationType', 'amount', 'balance')

    def validate(self, attrs):
        amount = attrs.get('amount')
        balance = self.context['wallet'].balance
        operation = attrs.get('operation')
        if balance < amount and operation == const.WITHDRAW:
            raise serializers.ValidationError(
                'Недостаточно средств.'
            )
        return attrs

    def create(self, validated_data):
        wallet = self.context['wallet']
        execute_transaction(
            wallet,
            validated_data.get('operation'),
            validated_data.get('amount')
        )
        return Transaction.objects.create(wallet=wallet, **validated_data)
