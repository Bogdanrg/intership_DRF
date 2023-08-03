from django.db import models


class Promotion(models.Model):
    avatar = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=30)
    price = models.DecimalField(decimal_places=10, max_digits=20)
    description = models.TextField(default="The most beneficial asset")

    def __str__(self) -> str:
        return f"Promotion: [{self.name}, {self.price}]"
