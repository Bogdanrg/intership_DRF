import datetime

from django.db.models import F
from rest_framework.request import Request

from src.auto_orders.models import AutoOrder
from src.portfolio.models import Portfolio, PortfolioUserPromotion
from src.promotions.models import Promotion


class AutoOrderBuyService:
    @staticmethod
    def create_order(request: Request) -> dict | bool:
        if AutoOrderBuyService._is_affordable(request):
            data = {
                "promotion": request.data["pk"],
                "status": "pending",
                "quantity": request.data["quantity"],
                "action": "purchase",
                "direction": request.data["direction"],
                "total_sum": float(request.data["direction"])
                * int(request.data["quantity"]),
            }
            return data
        return False

    @staticmethod
    def check_auto_orders(auto_order: AutoOrder) -> None:
        if auto_order.direction >= auto_order.promotion.price:
            auto_order.status = "completed successfully"
            auto_order.closed_at = datetime.datetime.now()
            AutoOrderBuyService._reduce_user_balance(auto_order)
            AutoOrderBuyService._update_portfolio(auto_order)
            auto_order.save()

    @staticmethod
    def _is_affordable(request: Request) -> bool:
        if request.user.balance >= (
            float(request.data["direction"]) * int(request.data["quantity"])
        ):
            return True
        return False

    @staticmethod
    def _reduce_user_balance(auto_order: AutoOrder) -> None:
        auto_order.user.balance = F("balance") - auto_order.total_sum
        auto_order.user.save()

    @staticmethod
    def _update_portfolio(auto_order: AutoOrder) -> None:
        portfolio = Portfolio.objects.get(user=auto_order.user)
        try:
            portfolio_user_promotion_obj = PortfolioUserPromotion.objects.get(
                portfolio=portfolio, promotion=auto_order.promotion
            )
            if portfolio_user_promotion_obj:
                portfolio_user_promotion_obj.quantity = (
                    F("quantity") + auto_order.quantity
                )
                portfolio_user_promotion_obj.save()
        except PortfolioUserPromotion.DoesNotExist:
            PortfolioUserPromotion.objects.create(
                portfolio=portfolio,
                promotion=auto_order.promotion,
                quantity=auto_order.quantity,
            )


class DistributiveAutoOrderService:
    @staticmethod
    def distribute(promotion: Promotion) -> None:
        auto_orders = promotion.auto_orders.all()
        for auto_order in auto_orders:
            if auto_order.action == "purchase":
                AutoOrderBuyService.check_auto_orders(auto_order)
            else:
                AutoOrderSaleService.check_auto_orders(auto_order)


class AutoOrderSaleService:
    @staticmethod
    def check_auto_orders(auto_order: AutoOrder) -> None:
        if auto_order.direction <= auto_order.promotion.price:
            auto_order.status = "completed successfully"
            auto_order.closed_at = datetime.datetime.now()
            AutoOrderSaleService._increase_user_balance(auto_order)
            AutoOrderSaleService._update_portfolio(auto_order)
            auto_order.save()

    @staticmethod
    def create_order(request: Request) -> dict | bool:
        if AutoOrderSaleService._in_presence(request):
            data = {
                "promotion": request.data["pk"],
                "status": "pending",
                "quantity": request.data["quantity"],
                "action": "sale",
                "direction": request.data["direction"],
                "total_sum": float(request.data["direction"])
                * int(request.data["quantity"]),
            }
            return data
        return False

    @staticmethod
    def _increase_user_balance(auto_order: AutoOrder) -> None:
        auto_order.user.balance = F("balance") + auto_order.total_sum
        auto_order.user.save()

    @staticmethod
    def _in_presence(request: Request) -> bool:
        portfolio = Portfolio.objects.get(user=request.user)
        try:
            portfolio_user_promotion_object = PortfolioUserPromotion.objects.get(
                portfolio=portfolio, promotion=request.data["pk"]
            )
        except PortfolioUserPromotion.DoesNotExist:
            return False
        if portfolio_user_promotion_object.quanity < request.data["quantity"]:
            return False
        return True

    @staticmethod
    def _update_portfolio(auto_order: AutoOrder) -> None:
        portfolio = Portfolio.objects.get(user=auto_order.user)
        portfolio_user_promotion_obj = PortfolioUserPromotion.objects.get(
            promotion=auto_order.promotion.pk, portfolio=portfolio
        )
        if portfolio_user_promotion_obj.quantity - auto_order.quantity == 0:
            portfolio_user_promotion_obj.delete()
        else:
            portfolio_user_promotion_obj.quantity = F("quantity") - auto_order.quantity
            portfolio_user_promotion_obj.save()
