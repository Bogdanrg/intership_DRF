from django.contrib.auth.models import AbstractUser
from django.db import models
from django_enum import EnumField

from src.promotions.models import Promotion


class TradingUser(AbstractUser):
    """inheritance from abstract user"""

    class RoleEnum(models.TextChoices):
        ADMIN = "admin", "admin"
        ANALYST = "analyst", "analyst"
        DEFAULT_USER = "default", "default"

    avatar = models.ImageField(upload_to="users/avatar/", blank=True, null=True)
    login = models.CharField(max_length=30)
    balance = models.DecimalField(decimal_places=10, max_digits=20)
    date_joined = models.DateTimeField(auto_now_add=True)
    role = EnumField(RoleEnum, null=True, blank=True)
    subscription = models.ForeignKey(Promotion, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="balance_greater_or_equals_to_zero",
                check=models.Q(balance__gte=0),
            ),
        ]
