from django.conf import settings
from django.db import models

from src.base.classes import AbstractOrder


class Order(AbstractOrder):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="orders"
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="order_total_sum_greater_or_equals_to_zero",
                check=models.Q(total_sum__gte=0),
            ),
        ]
