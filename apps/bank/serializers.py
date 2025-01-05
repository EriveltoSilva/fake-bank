""" bank serializers"""

from django.db import transaction
from rest_framework import serializers

from apps.accounts.serializers import UserSerializer

from .models import Account, TransferLog


class AccountSerializer(serializers.ModelSerializer):
    """Serializer for Account objects"""

    user = UserSerializer()

    class Meta:
        model = Account
        fields = ["id", "account_type", "account_number", "iban", "balance", "created_at", "user"]
        read_only_fields = ["id", "account_number", "iban", "created_at", "user"]

    def create(self, validated_data):
        # Extraindo dados do usuário
        user_data = validated_data.pop("user")

        # Criando o usuário
        user = UserSerializer().create(user_data)
        return Account.objects.create(user=user, **validated_data)


class ConsultTransferSerializer(serializers.ModelSerializer):
    """Serializer for Transfer objects"""

    sender_account = serializers.CharField(source="sender_account.iban")
    receiver_account = serializers.CharField(source="receiver_account.iban")

    class Meta:
        model = TransferLog
        fields = ["tid", "sender_account", "receiver_account", "amount", "created_at"]


class TransferByIBANSerializer(serializers.Serializer):
    """Serializer for Transfer objects"""

    transfer_type = serializers.CharField(max_length=25)
    receiver_iban = serializers.CharField(max_length=25)
    amount = serializers.DecimalField(max_digits=20, decimal_places=2)

    def validate(self, attrs):
        """Validate transfer data."""
        receiver_iban = attrs["receiver_iban"]
        amount = attrs["amount"]

        # Accessing user from context
        user = self.context.get("user", None)

        # Validate user authentication
        if not user or not user.is_authenticated:
            raise serializers.ValidationError({"message": "Usuário não autenticado."})

        try:
            sender_account = Account.objects.get(user=user)
        except Account.DoesNotExist:
            raise serializers.ValidationError({"message": "Conta remetente não encontrada para o usuário autenticado."})

        try:
            receiver_account = Account.objects.get(iban=receiver_iban)
        except Account.DoesNotExist:
            raise serializers.ValidationError({"message": "Conta destinatária não encontrada"})

        # Garantir que não seja a mesma conta
        if sender_account == receiver_account:
            raise serializers.ValidationError(
                {"message": "A conta destinatária não pode ser a mesma que a conta remetente."}
            )

        # Verificar se o saldo é suficiente
        if sender_account.balance < amount:
            raise serializers.ValidationError({"message": "Saldo insuficiente na conta remetente."})

        # Adicionar as contas para uso no save
        attrs["sender_account"] = sender_account
        attrs["receiver_account"] = receiver_account

        return attrs

    @transaction.atomic
    def save(self, *args, **kwargs):
        sender_account = self.validated_data["sender_account"]
        receiver_account = self.validated_data["receiver_account"]
        amount = self.validated_data["amount"]
        transfer_type = self.validated_data.get("transfer_type", "debit")

        # Atualizar saldos
        sender_account.balance -= amount
        receiver_account.balance += amount

        sender_account.save()
        receiver_account.save()

        # Registrar no log
        transfer_log = TransferLog.objects.create(
            sender_account=sender_account,
            receiver_account=receiver_account,
            amount=amount,
            transfer_type=transfer_type,
        )

        return {
            "sender_name": sender_account.user.get_full_name(),
            "sender_account": sender_account.iban,
            "receiver_account": receiver_account.iban,
            "receiver_name": receiver_account.user.get_full_name(),
            "amount": amount,
            "transaction_id": transfer_log.tid,
            "transfer_type": transfer_log.transfer_type,
            "created_at": transfer_log.created_at,
        }
