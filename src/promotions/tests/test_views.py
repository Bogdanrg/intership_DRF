import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestPromotion:
    def test_retrieve_promotion_works(self, default_user, promotion):
        # Arrange
        self.client = APIClient()
        # Act
        self.client.force_login(default_user)
        response = self.client.get(f"/api/v1/promotions/{promotion.id}/")
        # Assert
        assert response.status_code == 200
        assert set(response.data.keys()) == {"avatar", "name", "price", "description"}

    def test_retrieve_promotion_unauthorized(self):
        # Arrange
        self.client = APIClient()
        # Act
        response = self.client.get("/api/v1/promotions/1/")
        # Assert
        assert response.status_code == 401

    def test_create_promotion_as_default(self, default_user):
        # Arrange
        self.client = APIClient()

        # Act
        self.client.force_login(default_user)
        response = self.client.post(
            "/api/v1/promotions/", {"avatar": "AWS", "name": "BTC", "price": 2900.01}
        )
        # Assert
        assert response.status_code == 403

    def test_create_promotion_as_admin(self, admin_user):
        # Arrange
        self.client = APIClient()

        # Act
        self.client.force_login(admin_user)
        response = self.client.post(
            "/api/v1/promotions/", {"avatar": "AWS", "name": "BTC", "price": 2900.01}
        )
        # Assert
        assert response.status_code == 201
        assert set(response.data.keys()) == {"avatar", "name", "price", "description"}

    def test_update_promotion_as_default(self, default_user):
        # Arrange
        self.client = APIClient()

        # Act
        self.client.force_login(default_user)
        response = self.client.put(
            "/api/v1/promotions/1/", {"avatar": "AWS", "name": "BTC", "price": 2900.01}
        )
        # Assert
        assert response.status_code == 403

    def test_update_promotion_as_admin(self, admin_user, promotion):
        # Arrange
        self.client = APIClient()

        # Act
        self.client.force_login(admin_user)
        response = self.client.put(
            f"/api/v1/promotions/{promotion.id}/",
            {"avatar": "AWS", "name": "BTC", "price": 2900.01},
        )
        # Assert
        assert response.status_code == 200
        assert set(response.data.keys()) == {"avatar", "name", "price", "description"}

    def test_delete_promotion_as_default(self, default_user, promotion):
        # Arrange
        self.client = APIClient()

        # Act
        self.client.force_login(default_user)
        response = self.client.delete("/api/v1/promotions/4/")
        # Assert
        assert response.status_code == 403

    def test_delete_promotion_as_admin(self, admin_user, promotion):
        # Arrange
        self.client = APIClient()

        # Act
        self.client.force_login(admin_user)
        response = self.client.delete(f"/api/v1/promotions/{promotion.id}/")
        deleted_response = self.client.get("/api/v1/promotions/5/")
        # Assert
        assert response.status_code == 204
        assert deleted_response.status_code == 404

    def test_list_promotion_as_default(self, default_user, promotion):
        # Arrange
        self.client = APIClient()

        # Act
        self.client.force_login(default_user)
        response = self.client.get("/api/v1/promotions/")
        # Assert
        assert response.status_code == 200
        assert set(response.data[0].keys()) == {"avatar", "name", "price", "id"}
