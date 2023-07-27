from django.conf import settings
from django.db import models

from src.base.classes import AbstractOrder


class AutoOrder(AbstractOrder):
    closed_at = models.DateTimeField(blank=True, null=True)
    direction = models.DecimalField(decimal_places=10, max_digits=20)
    total_sum = models.DecimalField(
        decimal_places=10, max_digits=20, blank=True, null=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="auto_orders"
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="auto_order_total_sum_greater_or_equals_to_zero",
                check=models.Q(total_sum__gte=0),
            ),
        ]
