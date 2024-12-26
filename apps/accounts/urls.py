""" accounts app urls and api endpoints """

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

app_name = "accounts"

urlpatterns = [
    # Authentication
    path("token", views.MyTokenObtainPairView.as_view(), name="token"),
    path("token/refresh", TokenRefreshView.as_view(), name="token-refresh"),
    path("password/reset/<str:email>", views.PasswordResetEmailVerifyView.as_view()),
    path("password/change", views.PasswordChangeView.as_view(), name="password-change"),
    # Users endpoints
    path("users", views.UserListView.as_view(), name="user-list"),
    path("users/create", views.UserCreateView.as_view(), name="user-create"),
    path("users/<uuid:uid>", views.UserRetrieveUpdateDestroyAPIView.as_view(), name="user-retrieve-update-delete"),
    # ! Create, Read, Update, Delete
    # Profile endpoints
    path("profiles", views.ProfileListAPIView.as_view(), name="profile-list"),
    path("profiles/<uuid:pid>", views.ProfileRetrieveUpdateView.as_view(), name="profile-retrieve-update"),
]
