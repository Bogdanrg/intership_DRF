from .models import Promotion
from decimal import Decimal
from src.auto_orders.services import DistributiveAutoOrderService


class PromotionService:

    @staticmethod
    def promotion_pull(promotions: list) -> None:
        for promotion in promotions:
            Promotion.objects.create(avatar="AWS", description="Desc", **promotion)

    @staticmethod
    def promotion_update(promotions: list) -> None:
        promotions_to_update = Promotion.objects.all()
        for promotion_to_update in promotions_to_update:
            for promotion in promotions:
                if promotion_to_update.name == promotion["name"]:
                    promotion_to_update.price = Decimal(promotion["price"])
                    promotion_to_update.save()
                    DistributiveAutoOrderService.distribute(promotion_to_update)
