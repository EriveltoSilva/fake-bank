"""accounts users models"""

import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify

from .enums import UserGenderEnum


class User(AbstractUser):
    """User model with additional fields"""

    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField(unique=True)
    email = models.EmailField(unique=True, null=False, blank=False)
    phone = models.CharField(max_length=30, blank=True, null=True)
    otp = models.CharField(max_length=100, null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self) -> str:
        if self.full_name:
            return str(self.full_name)
        return f"{self.first_name} {self.last_name}"

    def get_full_name(self) -> str:
        return str(self.full_name)

    def save(self, *args, **kwargs) -> None:
        email_username = self.email.split("@")
        if not self.full_name:
            self.full_name = email_username[0]

        if not self.first_name and self.full_name:
            names = str(self.full_name).split(" ")
            self.first_name = names[0]
            self.last_name = names[-1]

        if not self.slug:
            self.slug = slugify(email_username[0])
        if not self.username:
            self.username = email_username[0]

        return super().save(*args, **kwargs)


class Profile(models.Model):
    """Profile model with additional fields"""

    GENDER = (
        (UserGenderEnum.MALE.value, "Male"),
        (UserGenderEnum.FEMALE.value, "Female"),
        (UserGenderEnum.OTHER.value, "Other"),
    )

    pid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name="profile")

    full_name = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER, default=GENDER[0])
    image = models.ImageField(upload_to="profile", blank=True)
    # phone = models.CharField(max_length=13, null=True, blank=True)

    country = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfis"
        ordering = ["user"]

    def __str__(self) -> str:
        return self.get_full_name()

    def get_full_name(self) -> str:
        """Return the full name of the user"""
        if self.full_name:
            return self.full_name
        return self.user.get_full_name()

    def image_url(self) -> str:
        """Return the image URL"""

        try:
            url = self.image.url  # pylint: disable= no-member
        except ValueError:
            url = "/static/assets/images/user.png"
        return url

    def save(self, *args, **kwargs) -> None:
        if not self.full_name:
            self.full_name = self.user.get_full_name()
        return super().save(*args, **kwargs)
