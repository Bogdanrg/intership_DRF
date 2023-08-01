import pytest
from rest_framework.test import APIClient

from src.portfolio.models import Portfolio, PortfolioUserPromotion


@pytest.mark.django_db
class TestPortfolio:
    def test_user_portfolio_list(self, default_user, promotion):
        # Arrange
        portfolio = Portfolio.objects.create(user=default_user)
        self.client = APIClient()
        PortfolioUserPromotion.objects.create(
            portfolio=portfolio, promotion=promotion, quantity=2
        )
        # Act

        self.client.force_authenticate(default_user)
        response = self.client.get("/api/v1/portfolio/")
        # Assert
        assert response.status_code == 200
        assert response.data[0]["quantity"] == 2

    def test_user_portfolio_list_unauthorized(self):
        # Arrange
        self.client = APIClient()
        # Act
        response = self.client.get("/api/v1/portfolio/")
        # Assert
        assert response.status_code == 401


@pytest.mark.django_db
class TestAnyUserPortfolio:
    def test_retrieve_default_user(self, default_user, promotion):
        # Arrange
        portfolio = Portfolio.objects.create(user=default_user)
        PortfolioUserPromotion.objects.create(
            portfolio=portfolio, promotion=promotion, quantity=2
        )
        self.client = APIClient()
        # Act
        self.client.force_authenticate(default_user)
        response = self.client.get("/api/v1/portfolio/1/")
        # Assert
        assert response.status_code == 403

    def test_retrieve_analyst_user(self, analyst_user, promotion):
        # Arrange
        portfolio = Portfolio.objects.create(user=analyst_user)
        PortfolioUserPromotion.objects.create(
            portfolio=portfolio, promotion=promotion, quantity=2
        )
        self.client = APIClient()
        # Act
        self.client.force_authenticate(analyst_user)
        response = self.client.get("/api/v1/portfolio/2/")
        # Assert
        assert response.status_code == 200
        assert response.data[0]["quantity"] == 2

    def test_retrieve_admin_user(self, admin_user, promotion):
        # Arrange
        portfolio = Portfolio.objects.create(user=admin_user)
        PortfolioUserPromotion.objects.create(
            portfolio=portfolio, promotion=promotion, quantity=2
        )
        self.client = APIClient()
        # Act
        self.client.force_authenticate(admin_user)
        response = self.client.get("/api/v1/portfolio/3/")
        # Assert
        assert response.status_code == 200
        assert response.data[0]["quantity"] == 2

    def test_retrieve_user_unauthorized(self):
        # Arrange
        self.client = APIClient()
        # Act
        response = self.client.get("/api/v1/portfolio/1/")
        # Assert
        assert response.status_code == 401
