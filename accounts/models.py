from django.contrib.auth.models import UserManager, AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(UserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "admin")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractUser):

    class RoleChoices(models.TextChoices):
        REGULAR = "regular", _("Regular")
        USER_MANAGER = "user_manager", _("User Manager")
        ADMIN = "admin", _("Admin")

    role = models.CharField(max_length=255, choices=RoleChoices.choices, default=RoleChoices.REGULAR)
    password2 = models.CharField(max_length=255, default='password2')
    objects = CustomUserManager()
