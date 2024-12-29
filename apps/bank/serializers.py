""" bank serializers"""

from rest_framework import serializers

from apps.accounts.serializers import UserSerializer

from .models import Account, TransferLog


class AccountSerializer(serializers.ModelSerializer):
    """Serializer for Account objects"""

    user = UserSerializer()

    class Meta:
        model = Account
        fields = [
            "id",
            "account_type",
            "account_number",
            "iban",
            "balance",
            "created_at",
            "user",
        ]
        read_only_fields = [
            "id",
            "account_number",
            "iban",
            "created_at",
            "user",
        ]

    def create(self, validated_data):
        # Extraindo dados do usuário
        user_data = validated_data.pop("user")
        # profile_data = validated_data.pop("profile")

        # Criando o usuário
        user = UserSerializer().create(user_data)
        # profile = user.profile
        # profile.birthday = profile_data.get("birthday")
        # profile.gender = profile_data.get("gender")
        # profile.country = profile_data.get("country")
        # profile.state = profile_data.get("state")
        # profile.city = profile_data.get("city")
        # profile.address = profile_data.get("address")
        # profile.save()
        return Account.objects.create(user=user, **validated_data)


class TransferByAccountNumberSerializer(serializers.Serializer):
    """Serializer for Transfer objects"""

    transfer_type = serializers.CharField(max_length=25)
    sender_account_number = serializers.CharField(max_length=25)
    receiver_account_number = serializers.CharField(max_length=25)
    amount = serializers.DecimalField(max_digits=20, decimal_places=2)

    def validate(self, attrs):
        """Validar os dados de transferência"""
        sender_account_number = attrs["sender_account_number"]
        receiver_account_number = attrs["receiver_account_number"]
        amount = attrs["amount"]

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

        return attrs

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
            sender_account=sender_account,
            receiver_account=receiver_account,
            amount=amount,
            transfer_type=self.validated_data.get("transfer_type", "debit"),
        )

        return {
            "sender_name": sender_account.user.get_full_name(),
            "sender_account": sender_account.account_number,
            "receiver_account": receiver_account.account_number,
            "receiver_name": receiver_account.user.get_full_name(),
            "amount": amount,
            "transaction_id": transfer_log.tid,
            "transfer_type": transfer_log.transfer_type,
            "created_at": transfer_log.created_at,
        }


class TransferByIBANSerializer(serializers.Serializer):
    """Serializer for Transfer objects"""

    transfer_type = serializers.CharField(max_length=25)
    sender_iban = serializers.CharField(max_length=25)
    receiver_iban = serializers.CharField(max_length=25)
    amount = serializers.DecimalField(max_digits=20, decimal_places=2)

    def validate(self, attrs):
        """Validar os dados de transferência"""
        sender_iban = attrs["sender_iban"]
        receiver_iban = attrs["receiver_iban"]
        amount = attrs["amount"]

        # Garantir que não seja a mesma conta
        if sender_iban == receiver_iban:
            raise serializers.ValidationError(
                {"receiver_iban": "A conta destinatária não pode ser a mesma que a conta remetente."}
            )

        # Verificar se as contas existem
        try:
            sender_account = Account.objects.get(iban=sender_iban)
        except Account.DoesNotExist:
            raise serializers.ValidationError({"sender_iban": "Conta remetente não encontrada."})

        try:
            Account.objects.get(iban=receiver_iban)
        except Account.DoesNotExist:
            raise serializers.ValidationError({"receiver_iban": "Conta destinatária não encontrada."})

        # Verificar se o saldo é suficiente
        if sender_account.balance < amount:
            raise serializers.ValidationError({"amount": "Saldo insuficiente na conta remetente."})

        return attrs

    def save(self, *args, **kwargs):
        sender_account = Account.objects.get(iban=self.validated_data["sender_iban"])
        receiver_account = Account.objects.get(iban=self.validated_data["receiver_iban"])
        amount = self.validated_data["amount"]

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
            transfer_type=self.validated_data.get("transfer_type", "debit"),
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


class ConsultTransferSerializer(serializers.ModelSerializer):
    """Serializer for Transfer objects"""

    sender_account = serializers.CharField(source="sender_account.iban")
    receiver_account = serializers.CharField(source="receiver_account.iban")

    class Meta:
        model = TransferLog
        fields = ["tid", "sender_account", "receiver_account", "amount", "created_at"]
