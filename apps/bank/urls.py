from django.urls import path

from .views import AccountCreateView, AccountDetailView, TransferView

urlpatterns = [
    path("accounts/create/", AccountCreateView.as_view(), name="account-create"),
    path("accounts/<str:account_number>/", AccountDetailView.as_view(), name="account-detail"),
    path("accounts/transfer/", TransferView.as_view(), name="account-transfer"),
]
