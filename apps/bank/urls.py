""" bank operation endpoints"""

from django.urls import path

from .views import (
    AccountCreateView,
    AccountDetailView,
    ConsultTransactionByAccountNumberView,
    TransferByAccountNumberView,
    TransferByIBANView,
)

urlpatterns = [
    #### Account endpoint###
    path("accounts/create/", AccountCreateView.as_view(), name="account-create"),
    path("accounts/details/<int:account_number>/", AccountDetailView.as_view(), name="account-detail"),
    path("accounts/details/iban/<str:iban>/", AccountDetailView.as_view(), name="account-detail-iban"),
    #### Transfer endpoint###
    path("transfer/account-number/", TransferByAccountNumberView.as_view(), name="account-transfer"),
    path("transfer/iban/", TransferByIBANView.as_view(), name="account-transfer"),
    ### Consult balance
    path("transactions/<int:account_number>/", ConsultTransactionByAccountNumberView.as_view(), name="account-detail"),
    path("transactions/iban/<str:iban>/", AccountDetailView.as_view(), name="account-detail-iban"),
]
