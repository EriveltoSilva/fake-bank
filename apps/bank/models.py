""" fake bank models"""

import random
import uuid

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Account(models.Model):
    """Account model"""

    ACCOUNT_TYPES = [
        ("checking", "Conta Corrente"),
        ("savings", "Conta Poupança"),
    ]

    aid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="accounts")
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPES)
    account_number = models.PositiveBigIntegerField(unique=True)
    iban = models.CharField(max_length=25, unique=True)
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.account_type} - {self.account_number}"

    def save(self, *args, **kwargs):
        if not self.account_number and not self.iban:
            account_number = self.generate_account_number()
            self.account_number = account_number
            self.iban = self.generate_iban(account_number)
        super().save(*args, **kwargs)

    @staticmethod
    def generate_iban(account_number: int) -> str:
        """Generates the iban"""
        # Formato: AO0600400000XXXXXXXXXXXXX
        prefix = "AO06"
        bank_code = "0040"
        branch_code = "0000"
        return f"{prefix}{bank_code}{branch_code}{account_number}"

    @staticmethod
    def generate_account_number() -> int:
        """Generates the account number"""
        # Formato: XXXXXXXXXXXXX
        account_number = "".join(random.choices("0123456789", k=13))
        return int(account_number)


class TransferLog(models.Model):
    """Model para registrar transferências de conta"""

    TRANSFER_TYPE = (
        ("debit", "debito"),
        ("credit", "credito"),
    )

    tid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    sender_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="sent_transfers")
    receiver_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="received_transfers")
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    transfer_type = models.CharField(max_length=10, choices=TRANSFER_TYPE, default=TRANSFER_TYPE[0])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Transferência"
        verbose_name_plural = "Transferências"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Transferência {self.tid} - {self.sender_account.iban} -> {self.receiver_account.iban}"
