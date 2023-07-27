from rest_framework.request import Request

from src.promotions.models import Promotion


class AutoOrderBuyService:
    def __init__(self) -> None:
        self._promotion = None

    def create_order(self, request: Request) -> dict | bool:
        self._promotion = Promotion.objects.get(pk=request.data.get("pk"))
        data = {
            "promotion": self._promotion.pk,
            "status": "pending",
            "quantity": request.data["quantity"],
            "action": "purchase",
            "direction": request.data["direction"],
        }
        return data
