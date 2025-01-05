"""  bank views"""

from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Account, TransferLog
from .serializers import AccountSerializer, ConsultTransferSerializer, TransferByIBANSerializer


class AccountCreateView(generics.CreateAPIView):
    """Create a new account"""

    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [permissions.AllowAny]  # Permite criar contas sem autenticação


class AccountDetailView(generics.RetrieveAPIView):
    """Retrieve a specific account"""

    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user = self.request.user
        try:
            return Account.objects.get(user=user)
        except Account.DoesNotExist:
            raise Http404("Account not found")


class AccountDetailByIBANView(generics.RetrieveAPIView):
    """Retrieve a specific account"""

    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        iban = self.kwargs.get("iban", None)
        if not iban:
            raise Http404("Account iban not provided")
        if iban:
            try:
                return Account.objects.get(iban=iban)
            except Account.DoesNotExist:
                raise Http404("Account not found")
        else:
            raise Http404("Account iban not provided")


class TransferByIBANView(APIView):
    """Transfer money between accounts"""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """Perform the transfer"""
        serializer = TransferByIBANSerializer(data=request.data, context={"user": self.request.user})
        if serializer.is_valid():
            transfer_data = serializer.save()
            return Response(
                {"message": "Transferência realizada com sucesso!", "transfer_details": transfer_data},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConsultTransactionView(generics.ListAPIView):
    """List all transactions for a specific account based on account_number"""

    serializer_class = ConsultTransferSerializer
    permission_classes = [permissions.IsAuthenticated]  # Adjust permissions as needed

    def get_queryset(self):
        account = get_object_or_404(Account, user=self.request.user)
        return TransferLog.objects.filter(sender_account=account) | TransferLog.objects.filter(receiver_account=account)
