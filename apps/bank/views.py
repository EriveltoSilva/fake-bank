"""  bank views"""

from django.http import Http404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Account
from .serializers import AccountSerializer, TransferSerializer


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
    lookup_field = "account_number"

    def get_object(self):
        account_number = self.kwargs.get("account_number", None)
        if not account_number:
            raise Http404("Account number not provided")
        try:
            return Account.objects.get(account_number=account_number)
        except Account.DoesNotExist:
            raise Http404("Account not found")


class TransferView(APIView):
    """Transfer money between accounts"""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """Perform the transfer"""
        serializer = TransferSerializer(data=request.data)
        if serializer.is_valid():
            transfer_data = serializer.save()
            return Response(
                {"message": "Transferência realizada com sucesso!", "transfer_details": transfer_data},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
