from decimal import Decimal

import pytest
from rest_framework.test import APIClient

from src.profiles.models import PromotionUserSubscriptions


@pytest.mark.django_db
class TestUserProfile:
    def test_retrieve_profile_as_default(self, default_user, another_default_user):
        # Arrange
        self.client = APIClient()
        # Act
        self.client.force_login(default_user)
        response = self.client.get(f"/api/v1/profiles/profile/{default_user.id}/")
        response_another_profile = self.client.get(
            f"/api/v1/profiles/profile/{another_default_user.id}/"
        )
        # Assert
        assert response.status_code == 200
        assert response_another_profile.status_code == 403

    def test_retrieve_profile_as_admin(self, admin_user, another_default_user):
        # Arrange
        self.client = APIClient()
        # Act
        self.client.force_login(admin_user)
        response = self.client.get(f"/api/v1/profiles/profile/{admin_user.id}/")
        response_another_profile = self.client.get(
            f"/api/v1/profiles/profile/{another_default_user.id}/"
        )
        # Assert
        assert response.status_code == 200
        assert response_another_profile.status_code == 200

    def test_update_profile_as_admin(self, admin_user, another_default_user):
        # Arrange
        self.client = APIClient()
        # Act
        self.client.force_login(admin_user)
        response = self.client.put(
            f"/api/v1/profiles/profile/{another_default_user.id}/", {"balance": 2000}
        )
        # Assert
        assert Decimal(response.data.get("balance")) == 2000
        assert response.status_code == 200

    def test_update_profile_as_default(self, default_user):
        # Arrange
        self.client = APIClient()
        # Act
        self.client.force_login(default_user)
        response = self.client.put(
            f"/api/v1/profiles/profile/{default_user.id}/", {"balance": 2000}
        )
        # Assert
        assert response.status_code == 403


@pytest.mark.django_db
class TestSubscriptions:
    def test_user_subscriptions(self, default_user, promotion):
        # Arrange
        self.client = APIClient()
        PromotionUserSubscriptions.objects.create(
            user=default_user, promotion=promotion
        )
        # Act
        self.client.force_login(default_user)
        response = self.client.get("/api/v1/profiles/subscriptions/")
        # Assert
        assert set(response.data[0].keys()) == {"avatar", "name", "price", "id"}
        assert response.status_code == 200

    def test_delete_subscription(self, default_user, promotion, another_promotion):
        # Arrange
        self.client = APIClient()
        PromotionUserSubscriptions.objects.create(
            user=default_user, promotion=promotion
        )
        PromotionUserSubscriptions.objects.create(
            user=default_user, promotion=another_promotion
        )
        # Act
        self.client.force_login(default_user)
        response = self.client.delete(
            "/api/v1/profiles/subscriptions/", {"pk": promotion.id}
        )
        list_response = self.client.get("/api/v1/profiles/subscriptions/")
        # Assert
        assert response.status_code == 200
        assert len(list_response.data) == 1

    def test_delete_null_subscription(self, default_user):
        # Arrange
        self.client = APIClient()
        # Act
        self.client.force_login(default_user)
        response = self.client.delete("/api/v1/profiles/subscriptions/", {"pk": 2})
        # Assert
        assert response.status_code == 406

    def test_create_existed_subscription(self, default_user, promotion):
        # Arrange
        PromotionUserSubscriptions.objects.create(
            user=default_user, promotion=promotion
        )
        self.client = APIClient()
        # Act
        self.client.force_login(default_user)
        response = self.client.post(
            "/api/v1/profiles/subscriptions/", {"pk": promotion.id}
        )
        # Assert
        assert response.status_code == 406

    def test_create_subscription(self, default_user, promotion):
        # Arrange
        self.client = APIClient()
        # Act
        self.client.force_login(default_user)
        response = self.client.post(
            "/api/v1/profiles/subscriptions/", {"pk": promotion.id}
        )
        list_response = self.client.get("/api/v1/profiles/subscriptions/")
        # Assert
        assert response.status_code == 200
        assert len(list_response.data) == 1
