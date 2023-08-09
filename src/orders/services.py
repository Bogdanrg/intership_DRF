from django.db.models import F

from src.portfolio.models import Portfolio, PortfolioUserPromotion
from src.profiles.models import TradingUser
from src.promotions.models import Promotion


class OrderBuyService:
    def __init__(self) -> None:
        self._user = None
        self._promotion = None

    def create_order(self, data: dict, user: TradingUser) -> dict | bool:
        self._promotion = Promotion.objects.get(pk=data.get("pk"))
        if not self._promotion:
            return False
        self._user = TradingUser.objects.get(pk=user.id)
        data = {
            "promotion": self._promotion.pk,
            "total_sum": int(data["quantity"]) * self._promotion.price,
            "status": "pending",
            "quantity": data["quantity"],
            "action": "purchase",
        }
        if self._is_affordable(data):
            self._reduce_user_balance(data)
            self._update_portfolio(data)
            data["status"] = "completed successfully"
            return data
        return False

    def _is_affordable(self, data: dict) -> bool:
        if int(data["quantity"]) <= 0:
            return False
        if self._user.balance >= (self._promotion.price * int(data["quantity"])):
            return True
        return False

    def _reduce_user_balance(self, data: dict) -> None:
        self._user.balance = F("balance") - data["total_sum"]
        self._user.save()

    def _update_portfolio(self, data: dict) -> None:
        portfolio = Portfolio.objects.get(user=self._user)
        try:
            portfolio_user_promotion_obj = PortfolioUserPromotion.objects.get(
                portfolio=portfolio, promotion=self._promotion.pk
            )
            if portfolio_user_promotion_obj:
                portfolio_user_promotion_obj.quantity = F("quantity") + data["quantity"]
                portfolio_user_promotion_obj.save()
        except PortfolioUserPromotion.DoesNotExist:
            PortfolioUserPromotion.objects.create(
                portfolio=portfolio,
                promotion=self._promotion,
                quantity=data["quantity"],
            )


class OrderSellService:
    def __init__(self) -> None:
        self._user = None
        self._promotion = None

    def _in_presence(self, data: dict) -> bool:
        portfolio = Portfolio.objects.get(user=self._user)
        try:
            portfolio_user_promotion_obj = PortfolioUserPromotion.objects.get(
                promotion=data["promotion"], portfolio=portfolio
            )
            if portfolio_user_promotion_obj.quantity < int(data["quantity"]):
                return False
            return True
        except PortfolioUserPromotion.DoesNotExist:
            return False

    def create_order(self, data: dict, user: TradingUser) -> dict | bool:
        self._promotion = Promotion.objects.get(pk=data.get("pk"))
        if not self._promotion:
            return False
        self._user = TradingUser.objects.get(pk=user.id)
        data = {
            "promotion": self._promotion.pk,
            "total_sum": int(data["quantity"]) * self._promotion.price,
            "status": "pending",
            "quantity": data["quantity"],
            "action": "sale",
        }
        if self._in_presence(data):
            self._increase_user_balance(data)
            self._update_portfolio(data)
            data["status"] = "completed successfully"
            return data
        return False

    def _increase_user_balance(self, data: dict) -> None:
        self._user.balance = F("balance") + data["total_sum"]
        self._user.save()

    def _update_portfolio(self, data: dict) -> None:
        portfolio = Portfolio.objects.get(user=self._user)
        portfolio_user_promotion_obj = PortfolioUserPromotion.objects.get(
            promotion=self._promotion.pk, portfolio=portfolio
        )
        if portfolio_user_promotion_obj.quantity - int(data["quantity"]) == 0:
            portfolio_user_promotion_obj.delete()
        else:
            portfolio_user_promotion_obj.quantity = F("quantity") - int(
                data["quantity"]
            )
            portfolio_user_promotion_obj.save()
