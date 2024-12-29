"""  bank views"""

from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Account, TransferLog
from .serializers import (
    AccountSerializer,
    ConsultTransferSerializer,
    TransferByAccountNumberSerializer,
    TransferByIBANSerializer,
)


class AccountCreateView(generics.CreateAPIView):
    """Create a new account"""

    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [permissions.AllowAny]  # Permite criar contas sem autenticação


class AccountDetailView(generics.RetrieveAPIView):
    """Retrieve a specific account"""

    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        account_number = self.kwargs.get("account_number", None)
        iban = self.kwargs.get("iban", None)
        if not account_number and not iban:
            raise Http404("Account number or iban not provided")
        if account_number:
            try:
                return Account.objects.get(account_number=account_number)
            except Account.DoesNotExist:
                raise Http404("Account not found")
        else:
            try:
                return Account.objects.get(iban=iban)
            except Account.DoesNotExist:
                raise Http404("Account not found")


class TransferByAccountNumberView(APIView):
    """Transfer money between accounts"""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """Perform the transfer"""
        serializer = TransferByAccountNumberSerializer(data=request.data)
        if serializer.is_valid():
            transfer_data = serializer.save()
            return Response(
                {"message": "Transferência realizada com sucesso!", "transfer_details": transfer_data},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransferByIBANView(APIView):
    """Transfer money between accounts"""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """Perform the transfer"""
        serializer = TransferByIBANSerializer(data=request.data)
        if serializer.is_valid():
            transfer_data = serializer.save()
            return Response(
                {"message": "Transferência realizada com sucesso!", "transfer_details": transfer_data},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConsultTransactionByAccountNumberView(generics.ListAPIView):
    """List all transactions for a specific account based on account_number"""

    serializer_class = ConsultTransferSerializer
    permission_classes = [permissions.AllowAny]  # Adjust permissions as needed

    def get_queryset(self):
        account_number = self.kwargs.get("account_number")
        account = get_object_or_404(Account, account_number=account_number)
        return TransferLog.objects.filter(sender_account=account) | TransferLog.objects.filter(receiver_account=account)
