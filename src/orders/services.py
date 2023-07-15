from django.db.models import F
from src.portfolio.models import Portfolio, PortfolioUserPromotion
from src.promotions.models import Promotion


class OrderCreationService:
    def __init__(self):
        self.__user = None
        self.__promotion = None

    def create_order(self, request) -> dict:
        data = {
            "promotion": self.__promotion.pk,
            "total_sum": int(request.data["quantity"]) * self.__promotion.price,
            "status": "pending",
            "quantity": request.data["quantity"],
            "action": "purchase"
        }
        return data

    def is_affordable(self, request) -> bool:
        self.__user = request.user
        self.__promotion = Promotion.objects.get(pk=request.data["pk"])
        if request.data["quantity"] <= 0:
            return False
        if self.__user.balance >= (
                self.__promotion.price * int(request.data["quantity"])
        ):
            return True
        return False

    def reduce_user_balance(self, data: dict) -> None:
        self.__user.balance = F('balance') - data['total_sum']
        self.__user.save()

    def update_portfolio(self, data: dict) -> None:
        portfolio = Portfolio.objects.get(user=self.__user)
        try:
            portfolio_user_promotion_obj = PortfolioUserPromotion.objects. \
                get(portfolio=portfolio, promotion=self.__promotion)
            if portfolio_user_promotion_obj:
                portfolio_user_promotion_obj.quantity = F('quantity') + data['quantity']
                portfolio_user_promotion_obj.save()
        except PortfolioUserPromotion.DoesNotExist:
            PortfolioUserPromotion.objects.create(portfolio=portfolio,
                                                  promotion=self.__promotion,
                                                  quantity=data['quantity'])
