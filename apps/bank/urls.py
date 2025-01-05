""" bank operation endpoints"""

from django.urls import path

from .views import (
    AccountCreateView,
    AccountDetailByIBANView,
    AccountDetailView,
    ConsultTransactionView,
    TransferByIBANView,
)

urlpatterns = [
    #### Account endpoint###
    path("accounts/create/", AccountCreateView.as_view(), name="account-create"),
    path("accounts/details/", AccountDetailView.as_view(), name="account-detail"),
    path("accounts/details/<str:iban>/", AccountDetailByIBANView.as_view(), name="account-detail-iban"),
    #### Transfer endpoint###
    path("transfer/iban/", TransferByIBANView.as_view(), name="account-transfer"),
    ### Consult balance
    path("transactions/", ConsultTransactionView.as_view(), name="account-detail"),
]
