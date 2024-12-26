""" api module form Users views endpoints """

from django.conf import settings
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from . import emails, utils
from .models import Profile
from .permissions import IsAdmin, IsOwnerOrAdmin
from .serializers import MyTokenObtainPairSerializer, ProfileSerializer, UserRegisterSerializer, UserSerializer

User = get_user_model()


class MyTokenObtainPairView(TokenObtainPairView):
    """my customized obtain token class with some user data in token generated"""

    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        tokens = response.data

        response.set_cookie(
            key="access_token",
            value=tokens["access"],
            httponly=True,
            secure=settings.DEBUG,  # Alterar para True em produção
            samesite="Lax",
        )
        response.set_cookie(
            key="refresh_token",
            value=tokens["refresh"],
            httponly=True,
            secure=settings.DEBUG,
            samesite="Lax",
        )
        return response


class PasswordResetEmailVerifyView(generics.RetrieveAPIView):
    """user view to generate a password reset email"""

    permission_classes = [
        AllowAny,
    ]
    serializer_class = UserSerializer

    def get_object(self):
        email = self.kwargs["email"]
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None  # Handling User not found case

        user.otp = utils.generate_otp()
        user.save()
        return user

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        if user is None:
            return Response(
                {"status": "error", "message": "Não existe um usuário com este e-mail"},
                status=status.HTTP_404_NOT_FOUND,
            )

        uidb64 = user.uid
        otp = user.otp
        link = f"http://localhost:3000/create-new-password?otp={otp}&uidb64={uidb64}"
        if not settings.DEBUG:
            try:
                emails.send_password_reset(user, user.email, settings.SYSTEM_NAME, "", link)
            except Exception as e:
                # Show email do user with link in terminal
                print("Error sending email for reset password\n-->", e)
                print("#" * 100, "Clique aqui:", link, "#" * 100, sep="\n")
        else:
            print("#" * 100, "Clique aqui:", link, "#" * 100, sep="\n")

        serializer = self.get_serializer(user)
        return Response(serializer.data)


class PasswordChangeView(generics.CreateAPIView):
    """a password view to change the user password"""

    permission_classes = [
        AllowAny,
    ]
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        otp = request.data["otp"]
        uidb64 = request.data["uidb64"]
        password = request.data["password"]
        confirmation_password = request.data["confirmation_password"]

        if password != confirmation_password:
            return Response(
                {"status": "error", "message": "As senhas são diferentes"}, status=status.HTTP_304_NOT_MODIFIED
            )
        elif len("password") < 8:
            return Response(
                {"status": "error", "message": "As senhas devem ter no mínimo 8 caracteres"},
                status=status.HTTP_304_NOT_MODIFIED,
            )

        user = User.objects.filter(id=uidb64, otp=otp)
        if user:
            user = user.first()
            user.set_password(password)
            user.otp = ""
            user.save()
            return Response(
                {"status": "success", "message": "Palavra-Passe alterada com Sucesso"}, status=status.HTTP_201_CREATED
            )
        return Response(
            {"status": "error", "message": "Ocorreu um erro ao alterar a palavra-passe"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# * -------------------- Users --------------------------------
class UserListView(generics.ListAPIView):
    """User list endpoint."""

    queryset = User.objects.all()
    permission_classes = [IsAdmin]
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "is_staff",
        "is_superuser",
        "date_joined",
    ]


class UserCreateView(generics.CreateAPIView):
    """User view form for creating a new user endpoint."""

    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserRegisterSerializer


class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """user retrieve update destroy view"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsOwnerOrAdmin,)
    lookup_field = "uid"


# * -------------------- Profiles --------------------------------
class ProfileListAPIView(generics.ListAPIView):
    """profile list view"""

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "birthday",
        "gender",
        "created_at",
    ]


class ProfileRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    """profile user detail view to retrieve profile information"""

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrAdmin]
    lookup_field = "pid"

    def retrieve(self, request, *args, **kwargs):
        profile = self.get_object()
        if profile is None:
            return Response({"status": "error", "message": "Perfil não encontrado!"}, status=status.HTTP_404_NOT_FOUND)
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        profile = self.get_object()
        if profile is None:
            return Response({"status": "error", "message": "ID do perfil inválido!"}, status=status.HTTP_404_NOT_FOUND)

        # Include the user in the request data before serializing
        request.data["user"] = profile.user.id
        serializer = self.get_serializer(profile, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
