from django.test import TestCase
from rest_framework.test import APIClient

from src.portfolio.models import Portfolio, PortfolioUserPromotion
from src.portfolio.serializers import PortfolioSerializer
from src.profiles.models import TradingUser
from src.promotions.models import Promotion

# flake8: noqa


class UserPortfolioViewSetTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        promotion = Promotion.objects.create(
            avatar="AWS", name="BTC", price=2900.15, description="Desc"
        )
        user = TradingUser.objects.create_user(
            username="bogdan", password="zaqxswcdevfr"
        )
        portfolio = Portfolio.objects.create(user=user)
        PortfolioUserPromotion.objects.create(
            portfolio=portfolio, promotion=promotion, quantity=2
        )
        self.promotion = promotion
        self.user = user
        self.client.login(username="bogdan", password="zaqxswcdevfr")

    def test_users_portfolio(self):
        resp = self.client.get("/api/v1/portfolio/")
        portfolio = Portfolio.objects.get(user_id=self.user.id)
        promotion = Promotion.objects.get(id=self.promotion.id)
        portfolio_user_promotion_obj = PortfolioUserPromotion.objects.get(
            portfolio=portfolio, promotion=promotion
        )
        serializer = PortfolioSerializer(portfolio_user_promotion_obj)
        self.assertEqual(serializer.data["promotion"], resp.data[0]["promotion"])
        self.assertEqual(serializer.data["quantity"], resp.data[0]["quantity"])
        self.client.logout()


class AnyUserPortfolioViewSetTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        TradingUser.objects.create_user(
            username="admin", password="zaqxswcdevfr", role="admin"
        )
        TradingUser.objects.create_user(
            username="analyst", password="zaqxswcdevfr", role="analyst"
        )

    def setUp(self) -> None:
        self.user = TradingUser.objects.create_user(
            username="bogdan", password="zaqxswcdevfr"
        )
        promotion = Promotion.objects.create(
            avatar="AWS", name="ETH", price=1800.15, description="Desc"
        )
        portfolio = Portfolio.objects.create(user=self.user)
        PortfolioUserPromotion.objects.create(
            portfolio=portfolio, promotion=promotion, quantity=2
        )
        self.client = APIClient()

    def test_any_user_portfolio_as_admin(self):
        self.client.login(username="admin", password="zaqxswcdevfr")
        resp = self.client.get(f"/api/v1/portfolio/{self.user.id}/")
        self.assertEqual(resp.status_code, 200)
        self.client.logout()

    def test_any_user_portfolio_as_analyst(self):
        self.client.login(username="analyst", password="zaqxswcdevfr")
        resp = self.client.get(f"/api/v1/portfolio/{self.user.id}/")
        self.assertEqual(resp.status_code, 200)
        self.client.logout()

    def test_any_user_portfolio_as_default(self):
        self.client.login(username="bogdan", password="zaqxswcdevfr")
        resp = self.client.get(f"/api/v1/portfolio/{self.user.id}/")
        self.assertEqual(resp.status_code, 403)
        self.client.logout()
