import pytest
from rest_framework.test import APIClient

from src.orders.models import Order
from src.portfolio.models import Portfolio, PortfolioUserPromotion
from src.profiles.models import TradingUser


@pytest.mark.django_db
class TestOrder:
    def test_create_purchase_order_with_valid_data(self, default_user, promotion):
        # Arrange
        self.client = APIClient()
        data = {
            "pk": promotion.pk,
            "quantity": 1,
            "action": "purchase",
        }
        portfolio = Portfolio.objects.create(user=default_user)
        # Act
        self.client.force_login(default_user)
        response = self.client.post("/api/v1/orders/", data)
        # Assert
        assert response.status_code == 200
        assert set(response.data.keys()) == {
            "id",
            "promotion",
            "status",
            "total_sum",
            "action",
            "ordered_at",
            "quantity",
        }
        default_user.refresh_from_db()
        promotion = PortfolioUserPromotion.objects.filter(
            portfolio=portfolio, promotion=promotion
        )
        assert default_user.balance == 2100.500
        assert len(promotion) == 1

    def test_create_sale_order_with_valid_data(self, default_user, promotion):
        # Arrange
        self.client = APIClient()
        data = {
            "pk": promotion.pk,
            "quantity": 1,
            "action": "sale",
        }
        portfolio = Portfolio.objects.create(user=default_user)
        portfolio_user_promotion_obj = PortfolioUserPromotion.objects.create(
            portfolio=portfolio, promotion=promotion, quantity=2
        )
        # Act
        self.client.force_login(default_user)
        response = self.client.post("/api/v1/orders/", data)
        # Assert
        assert response.status_code == 200
        assert set(response.data.keys()) == {
            "id",
            "promotion",
            "status",
            "total_sum",
            "action",
            "ordered_at",
            "quantity",
        }
        default_user.refresh_from_db()
        portfolio_user_promotion_obj.refresh_from_db()
        assert default_user.balance == 7900.500
        assert portfolio_user_promotion_obj.quantity == 1

    def test_retrieve_order_as_admin(self, admin_user, promotion):
        # Arrange
        self.client = APIClient()
        order = Order.objects.create(
            action="sale",
            promotion=promotion,
            total_sum=500,
            quantity=2,
            user=admin_user,
        )
        # Act
        self.client.force_login(admin_user)
        print(promotion.pk)
        response = self.client.get(f"/api/v1/orders/{order.pk}/")
        # Assert
        assert response.status_code == 200
        assert set(response.data.keys()) == {
            "id",
            "promotion",
            "user",
            "status",
            "total_sum",
            "action",
        }

    def test_retrieve_order_as_analyst(self, analyst_user, promotion):
        # Arrange
        self.client = APIClient()
        order = Order.objects.create(
            action="sale",
            promotion=promotion,
            total_sum=500,
            quantity=2,
            user=analyst_user,
        )
        # Act
        self.client.force_login(analyst_user)
        response = self.client.get(f"/api/v1/orders/{order.pk}/")
        # Assert
        assert response.status_code == 200
        assert set(response.data.keys()) == {
            "id",
            "promotion",
            "user",
            "status",
            "total_sum",
            "action",
        }

    def test_update_order_as_admin(self, admin_user, promotion):
        # Arrange
        self.client = APIClient()
        data = {
            "pk": promotion.pk,
            "total_sum": 100,
            "status": "pending",
            "quantity": 1,
            "action": "purchase",
        }
        order = Order.objects.create(
            action="sale",
            promotion=promotion,
            total_sum=500,
            quantity=2,
            user=admin_user,
        )
        # Act
        self.client.force_login(admin_user)
        response = self.client.put(f"/api/v1/orders/{order.pk}/", data)
        # Assert
        assert response.status_code == 200
        assert set(response.data.keys()) == {
            "id",
            "promotion",
            "user",
            "status",
            "total_sum",
            "action",
        }

    def test_update_order_as_analyst(self, analyst_user):
        # Arrange
        self.client = APIClient()
        data = {
            "pk": 1,
            "total_sum": 100,
            "status": "pending",
            "quantity": 1,
            "action": "purchase",
        }
        # Act
        self.client.force_login(analyst_user)
        response = self.client.put("/api/v1/orders/1/", data)
        # Assert
        assert response.status_code == 403

    def test_create_purchase_order_with_insufficient_funds(
        self, default_user, promotion
    ):
        # Arrange
        self.client = APIClient()
        data = {
            "pk": promotion.pk,
            "quantity": 10,
            "action": "purchase",
        }
        # Act
        self.client.force_login(default_user)
        response = self.client.post("/api/v1/orders/", data)
        # Assert
        assert response.status_code == 406

    def test_create_sale_order_with_insufficient_promotions(
        self, default_user, promotion
    ):
        # Arrange
        self.client = APIClient()
        data = {
            "pk": promotion.pk,
            "quantity": 1000000,
            "action": "sale",
        }
        portfolio = Portfolio.objects.create(user=default_user)
        PortfolioUserPromotion.objects.create(
            portfolio=portfolio, promotion=promotion, quantity=1
        )
        # Act
        self.client.force_login(default_user)
        response = self.client.post("/api/v1/orders/", data)
        # Assert
        assert response.status_code == 406

    def test_delete_as_default(self, default_user):
        # Arrange
        self.client = APIClient()
        # Act
        self.client.force_login(default_user)
        response = self.client.delete("/api/v1/orders/1/")
        # Assert
        assert response.status_code == 403

    def test_delete_as_admin(self, admin_user, promotion):
        # Arrange
        self.client = APIClient()
        order = Order.objects.create(
            action="sale",
            promotion=promotion,
            total_sum=500,
            quantity=2,
            user=admin_user,
        )
        # Act
        self.client.force_login(admin_user)
        response = self.client.delete(f"/api/v1/orders/{order.pk}/")
        # Assert
        assert response.status_code == 204


@pytest.mark.django_db
class TestTransactions:
    def test_transactions_as_admin(self, order, auto_order):
        # Arrange
        user = TradingUser.objects.create_user(
            username="Bogdan", password="zaqxswcdevfr", role="admin"
        )
        self.client = APIClient()
        # Act
        self.client.force_login(user)
        response = self.client.get(f"/api/v1/orders/transactions/{order.user.pk}/")
        # Assert
        assert response.status_code == 200
        assert set(response.data[0].keys()) == {
            "id",
            "promotion",
            "status",
            "total_sum",
            "action",
            "quantity",
            "ordered_at",
        }
        assert set(response.data[1].keys()) == {
            "id",
            "promotion",
            "status",
            "total_sum",
            "action",
            "quantity",
            "ordered_at",
            "closed_at",
            "direction",
        }

    def test_transactions_as_analyst(self, order, auto_order):
        # Arrange
        user = TradingUser.objects.create_user(
            username="Bogdan", password="zaqxswcdevfr", role="analyst"
        )
        self.client = APIClient()
        # Act
        self.client.force_login(user)
        response = self.client.get(f"/api/v1/orders/transactions/{order.user.pk}/")
        # Assert
        assert response.status_code == 200
        assert set(response.data[0].keys()) == {
            "id",
            "promotion",
            "status",
            "total_sum",
            "action",
            "quantity",
            "ordered_at",
        }
        assert set(response.data[1].keys()) == {
            "id",
            "promotion",
            "status",
            "total_sum",
            "action",
            "quantity",
            "ordered_at",
            "closed_at",
            "direction",
        }

    def test_transactions_as_default(self):
        # Arrange
        user = TradingUser.objects.create_user(
            username="Bogdan", password="zaqxswcdevfr"
        )
        self.client = APIClient()
        # Act
        self.client.force_login(user)
        response = self.client.get("/api/v1/orders/transactions/1/")
        # Assert
        assert response.status_code == 403
