import pytest

from src.auto_orders.models import AutoOrder
from src.orders.models import Order
from src.profiles.models import TradingUser
from src.promotions.models import Promotion


@pytest.fixture
def promotion() -> Promotion:
    promotion = Promotion.objects.create(avatar="AWS", name="BTC", price=2900.00)
    yield promotion
    del promotion


@pytest.fixture
def default_user() -> TradingUser:
    user = TradingUser.objects.create_user(
        username="Test user",
        email="testuseremail@email.com",
        password="testuserpassword123",
        balance=5000.500,
    )
    yield user
    del user


@pytest.fixture
def analyst_user() -> TradingUser:
    user = TradingUser.objects.create_user(
        username="Test user",
        email="testuseremail@email.com",
        password="testuserpassword123",
        role="analyst",
    )
    yield user
    del user


@pytest.fixture
def admin_user() -> TradingUser:
    user = TradingUser.objects.create_user(
        username="Test user",
        email="testuseremail@email.com",
        password="testuserpassword123",
        role="admin",
    )
    yield user
    del user


@pytest.fixture
def another_default_user() -> TradingUser:
    user = TradingUser.objects.create_user(
        username="Test User 2", password="testpassword2", email="testemail@gmail.com"
    )
    yield user
    del user


@pytest.fixture
def another_promotion() -> Promotion:
    promotion = Promotion.objects.create(avatar="AWS", name="ETH", price=2900.01)
    yield promotion
    del promotion


@pytest.fixture
def order(promotion, default_user) -> Order:
    order = Order.objects.create(
        promotion=promotion,
        quantity=1,
        user=default_user,
        total_sum=500,
        action="purchase",
    )
    yield order
    del order


@pytest.fixture
def auto_order(promotion, default_user) -> AutoOrder:
    order = AutoOrder.objects.create(
        promotion=promotion,
        quantity=5,
        user=default_user,
        total_sum=6000,
        action="purchase",
        direction=2900,
    )
    yield order
