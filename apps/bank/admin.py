""" bank account"""

from django.contrib import admin

from .models import Account, TransferLog


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    """Bank account admin configuration"""

    list_display = ("account_number", "iban", "user", "account_type", "balance", "created_at")
    list_filter = ("account_type", "created_at")
    search_fields = ("account_number", "user__username", "user__email")
    ordering = ("-created_at",)
    readonly_fields = ("aid", "account_number", "created_at")

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "aid",
                    "user",
                    "account_number",
                    "balance",
                    "account_type",
                    "created_at",
                ),
            },
        ),
    )


@admin.register(TransferLog)
class TransferLogAdmin(admin.ModelAdmin):
    """Bank transfer log admin configuration"""

    list_display = ("tid", "sender_account", "receiver_account", "amount", "created_at")
    list_filter = ("created_at",)
    search_fields = ("sender_account__account_number", "receiver_account__account_number", "tid")
    ordering = ("-created_at",)
