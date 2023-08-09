from decimal import Decimal

from django.db.models import F
from django.utils import timezone

from src.auto_orders.models import AutoOrder
from src.portfolio.models import Portfolio, PortfolioUserPromotion
from src.profiles.models import TradingUser
from src.promotions.models import Promotion


class AutoOrderBuyService:
    @staticmethod
    def create_order(data: dict, user: TradingUser) -> dict | bool:
        if AutoOrderBuyService.is_affordable(data, user):
            data = {
                "promotion": data["pk"],
                "status": "pending",
                "quantity": data["quantity"],
                "action": "purchase",
                "direction": data["direction"],
            }
            return data
        return False

    @staticmethod
    def check_auto_orders(auto_order: AutoOrder) -> None:
        if auto_order.direction >= auto_order.promotion.price:
            auto_order.status = "completed successfully"
            auto_order.closed_at = timezone.now()
            AutoOrderBuyService.reduce_user_balance(auto_order)
            AutoOrderBuyService.update_portfolio(auto_order)
            auto_order.save()

    @staticmethod
    def is_affordable(data: dict, user: TradingUser) -> bool:
        if user.balance >= (Decimal(data["direction"]) * int(data["quantity"])):
            return True
        return False

    @staticmethod
    def reduce_user_balance(auto_order: AutoOrder) -> None:
        total_sum = auto_order.quantity * auto_order.promotion.price
        auto_order.user.balance = F("balance") - total_sum
        auto_order.total_sum = total_sum
        auto_order.save()
        auto_order.user.save()

    @staticmethod
    def update_portfolio(auto_order: AutoOrder) -> None:
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
        auto_orders = promotion.auto_orders.filter(status="pending")
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
            auto_order.closed_at = timezone.now()
            AutoOrderSaleService.increase_user_balance(auto_order)
            AutoOrderSaleService.update_portfolio(auto_order)
            auto_order.save()

    @staticmethod
    def create_order(data: dict, user: TradingUser) -> dict | bool:
        if AutoOrderSaleService.in_presence(data, user):
            data = {
                "promotion": data["pk"],
                "status": "pending",
                "quantity": data["quantity"],
                "action": "sale",
                "direction": data["direction"],
            }
            return data
        return False

    @staticmethod
    def increase_user_balance(auto_order: AutoOrder) -> None:
        total_sum = auto_order.quantity * auto_order.promotion.price
        auto_order.user.balance = F("balance") + total_sum
        auto_order.total_sum = total_sum
        auto_order.save()
        auto_order.user.save()

    @staticmethod
    def in_presence(data: dict, user: TradingUser) -> bool:
        portfolio = Portfolio.objects.get(user=user)
        try:
            portfolio_user_promotion_object = PortfolioUserPromotion.objects.get(
                portfolio=portfolio, promotion=data["pk"]
            )
        except PortfolioUserPromotion.DoesNotExist:
            return False
        if portfolio_user_promotion_object.quantity < int(data["quantity"]):
            return False
        return True

    @staticmethod
    def update_portfolio(auto_order: AutoOrder) -> None:
        portfolio = Portfolio.objects.get(user=auto_order.user)
        portfolio_user_promotion_obj = PortfolioUserPromotion.objects.get(
            promotion=auto_order.promotion.pk, portfolio=portfolio
        )
        if portfolio_user_promotion_obj.quantity - auto_order.quantity == 0:
            portfolio_user_promotion_obj.delete()
        else:
            portfolio_user_promotion_obj.quantity = F("quantity") - auto_order.quantity
            portfolio_user_promotion_obj.save()
