import pytest
from django.contrib.auth.hashers import check_password
from rest_framework.test import APIClient

from src.portfolio.models import Portfolio


@pytest.mark.django_db
class TestJWTPair:
    def test_valid_credentials_pair(self, default_user):
        # Arrange
        self.client = APIClient()
        data = {"username": default_user.username, "password": "testuserpassword123"}
        # Act
        response = self.client.post("/api/auth-custom/", data)
        # Assert
        assert response.status_code == 200
        assert set(response.data.keys()) == {"access_token", "refresh_token"}

    def test_invalid_credentials(self, default_user):
        # Arrange
        self.client = APIClient()
        data = {"username": default_user.username, "password": "testuserpassword1235"}
        # Act
        response = self.client.post("/api/auth-custom/", data)
        # Assert
        assert response.status_code == 400

    def test_unknown_user(self):
        # Arrange
        self.client = APIClient()
        data = {"username": "some username", "password": "testuserpassword1235"}
        # Act
        response = self.client.post("/api/auth-custom/", data)
        # Assert
        assert response.status_code == 400


@pytest.mark.django_db
class TestRefreshAccessToken:
    def test_valid_refresh_token(self, default_user):
        # Arrange
        self.client = APIClient()
        data = {"username": default_user.username, "password": "testuserpassword123"}
        # Act
        response = self.client.post("/api/auth-custom/", data)
        response_refresh = self.client.post(
            "/api/auth-custom/refresh/",
            {"refresh_token": response.data.get("refresh_token")},
        )
        # Assert
        assert response_refresh.status_code == 200
        assert set(response_refresh.data.keys()) == {"access_token", "refresh_token"}

    def test_invalid_refresh_token(self, default_user):
        # Arrange
        self.client = APIClient()
        data = {"username": default_user.username, "password": "testuserpassword123"}
        # Act
        self.client.post("/api/auth-custom/", data)
        response_refresh = self.client.post(
            "/api/auth-custom/refresh/", {"refresh_token": "some refresh token"}
        )
        # Assert
        assert response_refresh.status_code == 400


@pytest.mark.django_db
class TestRegistration:
    def test_valid_credentials(self):
        # Arrange
        self.client = APIClient()
        data = {
            "username": "Bogdan",
            "password": "zaqxswcdevfr",
            "repeat_password": "zaqxswcdevfr",
            "email": "bogdan20160902@gmail.com",
        }
        # Act
        response = self.client.post("/api/auth-custom/registration/", data)
        # Assert
        assert response.status_code == 200
        assert response.data == "Verify your email"

    def test_password_missmatch(self):
        # Arrange
        self.client = APIClient()
        data = {
            "username": "Bogdan",
            "password": "zaqxswcdevfr",
            "repeat_password": "123",
            "email": "bogdan20160902@gmail.com",
        }
        # Act
        response = self.client.post("/api/auth-custom/registration/", data)
        # Assert
        assert response.status_code == 400

    def test_missing_email(self):
        # Arrange
        self.client = APIClient()
        data = {
            "username": "Bogdan",
            "password": "zaqxswcdevfr",
            "repeat_password": "123",
        }
        # Act
        response = self.client.post("/api/auth-custom/registration/", data)
        # Assert
        assert response.status_code == 400


@pytest.mark.django_db
class TestVerification:
    def test_valid_username(self, default_user):
        # Arrange
        self.client = APIClient()
        default_user.is_active = False
        default_user.save()
        # Act
        response = self.client.get(
            f"/api/auth-custom/verification/{default_user.username}"
        )
        # Assert
        assert response.status_code == 200
        default_user.refresh_from_db()
        assert default_user.is_active is True
        portfolio = Portfolio.objects.filter(user=default_user)
        assert len(portfolio) == 1

    def test_invalid_username(self, default_user):
        # Arrange
        self.client = APIClient()
        default_user.is_active = False
        default_user.save()
        # Act
        response = self.client.get("/api/auth-custom/verification/asdf")
        # Assert
        assert response.status_code == 403


@pytest.mark.django_db
class TestPasswordChange:
    def test_valid_old_password(self, default_user):
        # Arrange
        self.client = APIClient()
        data = {
            "old_password": "testuserpassword123",
            "new_password": "test_new_password",
        }
        # Act
        self.client.force_login(default_user)
        response = self.client.put("/api/auth-custom/change_password/", data)
        # Assert
        assert response.status_code == 200
        default_user.refresh_from_db()
        assert check_password("test_new_password", default_user.password) is True
        assert response.data == "Password has been changed"

    def test_invalid_old_password(self, default_user):
        # Arrange
        self.client = APIClient()
        data = {
            "old_password": "testuserpassword1234",
            "new_password": "test_new_password",
        }
        # Act
        self.client.force_login(default_user)
        response = self.client.put("/api/auth-custom/change_password/", data)
        # Assert
        assert response.status_code == 400
        assert response.data == "Wrong old password"


@pytest.mark.django_db
class TestPasswordReset:
    def test_valid_username_reset_password(self, default_user):
        # Arrange
        self.client = APIClient()
        data = {"username": default_user.username, "email": "someemail@gmail.com"}
        # Act
        response = self.client.post("/api/auth-custom/password_reset/", data)
        # Assert
        assert response.status_code == 200
        assert response.data == "Check our email"

    def test_invalid_username_reset_password(self, default_user):
        # Arrange
        self.client = APIClient()
        data = {"username": "some name", "email": "someemail@gmail.com"}
        # Act
        response = self.client.post("/api/auth-custom/password_reset/", data)
        # Assert
        assert response.status_code == 400

    def test_missing_email_reset_password(self):
        # Arrange
        self.client = APIClient()
        data = {"username": "some name"}
        # Act
        response = self.client.post("/api/auth-custom/password_reset/", data)
        # Assert
        assert response.status_code == 400
