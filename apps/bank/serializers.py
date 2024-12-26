""" bank serializers"""

from rest_framework import serializers

from apps.accounts.serializers import UserSerializer

from .models import Account, TransferLog


class AccountSerializer(serializers.ModelSerializer):
    """Serializer for Account objects"""

    user = UserSerializer()

    class Meta:
        model = Account
        fields = ["id", "user", "account_number", "balance", "account_type", "created_at"]
        read_only_fields = ["id", "account_number", "created_at", "user"]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user = UserSerializer().create(user_data)
        return Account.objects.create(user=user, **validated_data)


class TransferSerializer(serializers.Serializer):
    """Serializer for Transfer objects"""

    sender_account_number = serializers.CharField(max_length=25)
    receiver_account_number = serializers.CharField(max_length=25)
    amount = serializers.DecimalField(max_digits=20, decimal_places=2)

    def validate(self, data, *args, **kwargs):
        """Validar os dados de transferência"""
        sender_account_number = data["sender_account_number"]
        receiver_account_number = data["receiver_account_number"]
        amount = data["amount"]

        # Garantir que não seja a mesma conta
        if sender_account_number == receiver_account_number:
            raise serializers.ValidationError(
                {"receiver_account_number": "A conta destinatária não pode ser a mesma que a conta remetente."}
            )

        # Verificar se as contas existem
        try:
            sender_account = Account.objects.get(account_number=sender_account_number)
        except Account.DoesNotExist:
            raise serializers.ValidationError({"sender_account_number": "Conta remetente não encontrada."})

        try:
            Account.objects.get(account_number=receiver_account_number)
        except Account.DoesNotExist:
            raise serializers.ValidationError({"receiver_account_number": "Conta destinatária não encontrada."})

        # Verificar se o saldo é suficiente
        if sender_account.balance < amount:
            raise serializers.ValidationError({"amount": "Saldo insuficiente na conta remetente."})

        return data

    def save(self, *args, **kwargs):
        sender_account = Account.objects.get(account_number=self.validated_data["sender_account_number"])
        receiver_account = Account.objects.get(account_number=self.validated_data["receiver_account_number"])
        amount = self.validated_data["amount"]

        # Atualizar saldos
        sender_account.balance -= amount
        receiver_account.balance += amount

        sender_account.save()
        receiver_account.save()

        # Registrar no log
        transfer_log = TransferLog.objects.create(
            sender_account=sender_account, receiver_account=receiver_account, amount=amount
        )

        return {
            "sender_account": sender_account.account_number,
            "receiver_account": receiver_account.account_number,
            "amount": amount,
            "transaction_id": transfer_log.tid,
            "created_at": transfer_log.created_at,
        }
