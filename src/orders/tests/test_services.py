from unittest import mock

from django.test import TestCase
from rest_framework.request import Request

from src.orders.services import OrderBuyService
from src.portfolio.models import Portfolio
from src.profiles.models import TradingUser
from src.promotions.models import Promotion


class TestService(TestCase):
    def test_valid_order_created(self):
        request = Request()
        request.data = {"pk": 1, "quantity": 2}
        request.user.id = 1
        promotion = Promotion.objects.create(name="promo", price=10, avatar="AWS")
        user = TradingUser.objects.create_user(
            username="user", balance=100, password="zaqxswcdevfr"
        )
        Portfolio.objects.create(user=user)
        OrderBuyService()._user = user
        OrderBuyService()._promotion = promotion
        mock.patch.object(OrderBuyService, "_is_affordable", return_value=True)
        mock.patch.object(OrderBuyService, "_reduce_user_balance")
        mock.patch.object(OrderBuyService, "_update_portfolio")
        result = OrderBuyService().create_order(request)
        self.assertEqual(result["promotion"], promotion.pk)
        self.assertEqual(result["total_sum"], 20)
        self.assertEqual(result["status"], "completed successfully")
        self.assertEqual(result["quantity"], 2)
        self.assertEqual(result["action"], "purchase")
