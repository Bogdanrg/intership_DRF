from django.forms import model_to_dict
from django.test import TestCase
from rest_framework.test import APIClient

from src.orders.models import Order
from src.portfolio.models import Portfolio
from src.profiles.models import TradingUser
from src.promotions.models import Promotion

# flake8: noqa


class OrderCRUDViewSetTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = TradingUser.objects.create_user(
            username="bogdan", password="zaqxswcdevfr", balance=3000
        )
        Portfolio.objects.create(user=user)
        user = TradingUser.objects.create_user(
            username="admin", password="zaqxswcdevfr", role="admin", balance=3000
        )
        Portfolio.objects.create(user=user)
        user = TradingUser.objects.create_user(
            username="analyst", password="zaqxswcdevfr", role="analyst", balance=3000
        )
        Portfolio.objects.create(user=user)
        Promotion.objects.create(
            avatar="AWS", name="BTC", price=2900.15, description="Desc"
        )

    def setUp(self) -> None:
        self.client = APIClient()

    def tearDown(self) -> None:
        self.client.logout()

    def test_create_order_purchase(self):
        self.client.login(username="bogdan", password="zaqxswcdevfr")
        resp = self.client.post(
            "/api/v1/orders/", data={"action": "purchase", "pk": 1, "quantity": 1}
        )
        self.assertEqual(resp.status_code, 200)
        user = TradingUser.objects.get(username="bogdan")
        order = Order.objects.get(user=user, action="purchase")
        order_dict = model_to_dict(order)
        self.assertEqual(order_dict["status"], "completed successfully")

    def test_create_order_sale(self):
        self.client.login(username="bogdan", password="zaqxswcdevfr")
        resp = self.client.post(
            "/api/v1/orders/", data={"action": "sale", "pk": 1, "quantity": 1}
        )
        self.assertEqual(resp.status_code, 200)
        user = TradingUser.objects.get(username="bogdan")
        order = Order.objects.get(user=user, action="sale")
        order_dict = model_to_dict(order)
        self.assertEqual(order_dict["status"], "completed successfully")
