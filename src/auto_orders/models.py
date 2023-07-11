from django.db import models

from src.base.classes import AbstractOrder


class AutoOrder(AbstractOrder):
    begun_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="auto_order_total_sum_greater_or_equals_to_zero",
                check=models.Q(total_sum__gte=0),
            ),
        ]
