from django.conf import settings
from django.db import models
from django_enum import EnumField

from src.promotions.models import Promotion


class AbstractDate(models.Model):
    ordered_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AbstractOrder(AbstractDate):
    class OrderStatus(models.TextChoices):
        PENDING = "pending", "pending"
        SUCCESS = "completed successfully", "completed successfully"
        FAILURE = "completed with an error", "completed with an error"

    promotion = models.ForeignKey(Promotion, on_delete=models.PROTECT)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    status = EnumField(OrderStatus, null=True, blank=True)
    total_sum = models.DecimalField(decimal_places=10, max_digits=20)

    class Meta:
        abstract = True
