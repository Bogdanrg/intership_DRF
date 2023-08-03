import pytest
from rest_framework.test import APIClient

from src.auto_orders.models import AutoOrder
from src.auto_orders.services import AutoOrderBuyService, AutoOrderSaleService
from src.portfolio.models import Portfolio, PortfolioUserPromotion


@pytest.mark.django_db
class TestAutoOrder:
    def test_create_purchase_auto_order_with_valid_data(self, default_user, promotion):
        # Arrange
        self.client = APIClient()
        data = {
            "pk": promotion.pk,
            "quantity": 1,
            "action": "purchase",
            "direction": 2900,
        }
        portfolio = Portfolio.objects.create(user=default_user)
        # Act
        self.client.force_login(default_user)
        response = self.client.post("/api/v1/auto-orders/", data)
        # Assert
        assert response.status_code == 200
        assert set(response.data.keys()) == {
            "id",
            "promotion",
            "status",
            "total_sum",
            "action",
            "ordered_at",
            "closed_at",
            "quantity",
            "direction",
        }
        auto_order = AutoOrder.objects.get(id=response.data.get("id"))
        AutoOrderBuyService.check_auto_orders(auto_order)
        default_user.refresh_from_db()
        promotion = PortfolioUserPromotion.objects.filter(
            portfolio=portfolio, promotion=promotion
        )
        assert default_user.balance == 2100.500
        assert len(promotion) == 1

    def test_create_sale_order_with_valid_data(self, default_user, promotion):
        # Arrange
        self.client = APIClient()
        data = {"pk": promotion.pk, "quantity": 1, "action": "sale", "direction": 2900}
        portfolio = Portfolio.objects.create(user=default_user)
        portfolio_user_promotion_obj = PortfolioUserPromotion.objects.create(
            portfolio=portfolio, promotion=promotion, quantity=2
        )
        # Act
        self.client.force_login(default_user)
        response = self.client.post("/api/v1/auto-orders/", data)
        # Assert
        assert response.status_code == 200
        assert set(response.data.keys()) == {
            "id",
            "promotion",
            "status",
            "total_sum",
            "action",
            "ordered_at",
            "closed_at",
            "quantity",
            "direction",
        }
        auto_order = AutoOrder.objects.get(id=response.data.get("id"))
        AutoOrderSaleService.check_auto_orders(auto_order)
        default_user.refresh_from_db()
        portfolio_user_promotion_obj.refresh_from_db()
        assert default_user.balance == 7900.500
        assert portfolio_user_promotion_obj.quantity == 1

    def test_retrieve_auto_order_as_admin(self, admin_user, promotion):
        # Arrange
        self.client = APIClient()
        order = AutoOrder.objects.create(
            action="sale",
            promotion=promotion,
            total_sum=500,
            quantity=2,
            direction=2900,
            user=admin_user,
        )
        # Act
        self.client.force_login(admin_user)
        response = self.client.get(f"/api/v1/auto-orders/{order.pk}/")
        # Assert
        assert response.status_code == 200
        assert set(response.data.keys()) == {
            "id",
            "promotion",
            "user",
            "status",
            "total_sum",
            "action",
            "direction",
            "closed_at",
            "quantity",
        }

    def test_retrieve_auto_order_as_analyst(self, analyst_user, promotion):
        # Arrange
        self.client = APIClient()
        order = AutoOrder.objects.create(
            action="sale",
            promotion=promotion,
            total_sum=500,
            quantity=2,
            user=analyst_user,
            direction=2900,
        )
        # Act
        self.client.force_login(analyst_user)
        response = self.client.get(f"/api/v1/auto-orders/{order.pk}/")
        # Assert
        assert response.status_code == 200
        assert set(response.data.keys()) == {
            "id",
            "promotion",
            "user",
            "status",
            "total_sum",
            "action",
            "closed_at",
            "quantity",
            "direction",
        }

    def test_update_auto_order_as_admin(self, admin_user, promotion):
        # Arrange
        self.client = APIClient()
        data = {
            "pk": promotion.pk,
            "total_sum": 100,
            "status": "pending",
            "quantity": 1,
            "action": "purchase",
            "direction": 2900,
        }
        order = AutoOrder.objects.create(
            action="sale",
            promotion=promotion,
            total_sum=500,
            quantity=2,
            user=admin_user,
            direction=2900,
        )
        # Act
        self.client.force_login(admin_user)
        response = self.client.put(f"/api/v1/auto-orders/{order.pk}/", data)
        # Assert
        assert response.status_code == 200
        assert set(response.data.keys()) == {
            "id",
            "promotion",
            "user",
            "status",
            "total_sum",
            "action",
            "closed_at",
            "direction",
            "quantity",
        }

    def test_update_auto_order_as_analyst(self, analyst_user):
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
        response = self.client.put("/api/v1/auto-orders/1/", data)
        # Assert
        assert response.status_code == 403

    def test_create_purchase_auto_order_with_insufficient_funds(
        self, default_user, promotion
    ):
        # Arrange
        self.client = APIClient()
        data = {
            "pk": promotion.pk,
            "quantity": 10,
            "action": "purchase",
            "direction": 2900,
        }
        # Act
        self.client.force_login(default_user)
        response = self.client.post("/api/v1/auto-orders/", data)
        # Assert
        assert response.status_code == 406

    def test_create_sale_auto_order_with_insufficient_promotions(
        self, default_user, promotion
    ):
        # Arrange
        self.client = APIClient()
        data = {
            "pk": promotion.pk,
            "quantity": 1000000,
            "action": "sale",
            "direction": 2900,
        }
        portfolio = Portfolio.objects.create(user=default_user)
        PortfolioUserPromotion.objects.create(
            portfolio=portfolio, promotion=promotion, quantity=1
        )
        # Act
        self.client.force_login(default_user)
        response = self.client.post("/api/v1/auto-orders/", data)
        # Assert
        assert response.status_code == 406

    def test_delete_as_default(self, default_user):
        # Arrange
        self.client = APIClient()
        # Act
        self.client.force_login(default_user)
        response = self.client.delete("/api/v1/auto-orders/1/")
        # Assert
        assert response.status_code == 403

    def test_delete_as_admin(self, admin_user, promotion):
        # Arrange
        self.client = APIClient()
        order = AutoOrder.objects.create(
            action="sale",
            promotion=promotion,
            total_sum=500,
            quantity=2,
            user=admin_user,
            direction=2900,
        )
        # Act
        self.client.force_login(admin_user)
        response = self.client.delete(f"/api/v1/auto-orders/{order.pk}/")
        # Assert
        assert response.status_code == 204
