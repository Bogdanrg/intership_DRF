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
        response = self.client.get("/api/v1/profiles/profile/1/")
        response_another_profile = self.client.get("/api/v1/profiles/profile/2/")
        # Assert
        assert response.status_code == 200
        assert response_another_profile.status_code == 403

    def test_retrieve_profile_as_admin(self, admin_user, another_default_user):
        # Arrange
        self.client = APIClient()
        # Act
        self.client.force_login(admin_user)
        response = self.client.get("/api/v1/profiles/profile/3/")
        response_another_profile = self.client.get("/api/v1/profiles/profile/4/")
        # Assert
        assert response.status_code == 200
        assert response_another_profile.status_code == 200

    def test_update_profile_as_admin(self, admin_user, another_default_user):
        # Arrange
        self.client = APIClient()
        # Act
        self.client.force_login(admin_user)
        response = self.client.put("/api/v1/profiles/profile/6/", {"balance": 2000})
        # Assert
        assert Decimal(response.data.get("balance")) == 2000
        assert response.status_code == 200

    def test_update_profile_as_default(self, default_user):
        # Arrange
        self.client = APIClient()
        # Act
        self.client.force_login(default_user)
        response = self.client.put("/api/v1/profiles/profile/7/", {"balance": 2000})
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
        response = self.client.delete("/api/v1/profiles/subscriptions/", {"pk": 2})
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
        response = self.client.post("/api/v1/profiles/subscriptions/", {"pk": 4})
        # Assert
        assert response.status_code == 406

    def test_create_subscription(self, default_user, promotion):
        # Arrange
        self.client = APIClient()
        # Act
        self.client.force_login(default_user)
        response = self.client.post("/api/v1/profiles/subscriptions/", {"pk": 5})
        list_response = self.client.get("/api/v1/profiles/subscriptions/")
        # Assert
        assert response.status_code == 200
        assert len(list_response.data) == 1
