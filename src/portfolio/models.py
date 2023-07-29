from django.conf import settings
from django.db import models

from src.promotions.models import Promotion


class Portfolio(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    promotions = models.ManyToManyField(Promotion,
                                        through="PortfolioUserPromotion",
                                        blank=True)


class PortfolioUserPromotion(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
