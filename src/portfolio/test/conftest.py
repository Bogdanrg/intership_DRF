import pytest

from src.profiles.models import TradingUser
from src.promotions.models import Promotion


@pytest.fixture
def default_user() -> TradingUser:
    user = TradingUser.objects.create_user(
        username="Test user",
        email="testuseremail@email.com",
        password="testuserpassword123",
    )
    yield user
    del user


@pytest.fixture
def promotion() -> Promotion:
    promotion = Promotion.objects.create(avatar="AWS", name="BTC", price=2900.01)
    yield promotion
    del promotion


@pytest.fixture
def analyst_user() -> TradingUser:
    user = TradingUser.objects.create_user(
        username="Test user",
        email="testuseremail@email.com",
        password="testuserpassword123",
        role="analyst"
    )
    yield user
    del user


@pytest.fixture
def admin_user() -> TradingUser:
    user = TradingUser.objects.create_user(
        username="Test user",
        email="testuseremail@email.com",
        password="testuserpassword123",
        role="admin"
    )
    yield user
    del user
