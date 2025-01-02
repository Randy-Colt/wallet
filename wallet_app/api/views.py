from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.serializers import WalletSerializer, TransactionSerializer
from core.models import Wallet


class WalletViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    '''
    Вьюсет для работы с кошельком.

    POST /: создать кошелёк
    GET /{WALLET_UUID}: получить кошелёк по uuid
    POST /{WALLET_UUID}/operation: произвести операции с балансом.
    '''
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

    @action(detail=True, methods=['POST'], url_path='operation')
    def execude_operation(self, request, pk):
        wallet = self.get_object()
        try:
            with transaction.atomic():
                serializer = TransactionSerializer(
                    data=request.data,
                    context={'wallet': wallet}
                )
                serializer.is_valid(True)
                serializer.save()
        except (IntegrityError, ValidationError) as error:
            return Response(
                {'detail': f'Транзакция отменена по причине: {error.messages}'},
                status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.data, status.HTTP_201_CREATED)
