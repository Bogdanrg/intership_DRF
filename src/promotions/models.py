from django.db import models


class Promotion(models.Model):
    avatar = models.ImageField(upload_to="promotions/avatar/", blank=True, null=True)
    name = models.CharField(max_length=30)
    price = models.DecimalField(decimal_places=10, max_digits=20)
    description = models.TextField(default="The most beneficial asset")
