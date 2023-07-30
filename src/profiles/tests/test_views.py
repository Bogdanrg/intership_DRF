from django.test import TestCase
from rest_framework.test import APIClient

from src.profiles.models import PromotionUserSubscriptions, TradingUser
from src.promotions.models import Promotion
from src.promotions.serializers import PromotionListSerializer


# flake8: noqa

class UserProfileViewSetTestAuthenticatedTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        TradingUser.objects.create_user(
            username="bogdan", password="zaqxswcdevfr", email="Bogdan20160902@gmail.com"
        )

        TradingUser.objects.create_user(
            username="admin",
            password="zaqxswcdevfr",
            email="Bogdan20160902@gmail.com",
            role="admin",
        )

    def setUp(self) -> None:
        self.client = APIClient()

    def test_retrieve_profile_as_default(self):
        self.client.login(username="bogdan", password="zaqxswcdevfr")
        resp = self.client.get("/api/v1/profiles/profile/1")
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get("/api/v1/profiles/profile/2")
        self.assertEqual(resp.status_code, 403)

    def test_retrieve_profile_as_admin(self):
        self.client.login(username="admin", password="zaqxswcdevfr")
        resp = self.client.get("/api/v1/profiles/profile/1")
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get("/api/v1/profiles/profile/2")
        self.assertEqual(resp.status_code, 200)

    def test_update_profile_as_admin(self):
        self.client.login(username="admin", password="zaqxswcdevfr")
        resp = self.client.put("/api/v1/profiles/profile/1/")
        self.assertEqual(resp.status_code, 200)
        resp = self.client.put("/api/v1/profiles/profile/2/")
        self.assertEqual(resp.status_code, 200)

    def test_update_profile_as_default(self):
        self.client.login(username="bogdan", password="zaqxswcdevfr")
        resp = self.client.put("/api/v1/profiles/profile/1/")
        self.assertEqual(resp.status_code, 403)
        resp = self.client.put("/api/v1/profiles/profile/2/")
        self.assertEqual(resp.status_code, 403)


class SubscribeOnPromotionListViewSetAuthenticatedTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        promotion = Promotion.objects.create(
            avatar=f"AWS/BTC", name=f"BTC", price=2900.01, description=f"Desc"
        )

        user = TradingUser.objects.create_user(
            username="artem", password="zaqxswcdevfr", email="Bogdan20160902@gmail.com"
        )

        PromotionUserSubscriptions.objects.create(user=user, promotion=promotion)

    def setUp(self) -> None:
        self.client = APIClient()
        self.client.login(username="artem", password="zaqxswcdevfr")

    def test_response_subscriptions(self):
        resp = self.client.get("/api/v1/profiles/subscriptions/")
        self.assertEqual(resp.status_code, 200)
        promotion = Promotion.objects.get(id=1)
        serializer = PromotionListSerializer(promotion)
        self.assertEquals(serializer.data, resp.data[0])

    def test_create_subscriptions(self):
        Promotion.objects.create(
            avatar=f"AWS/ETH", name=f"ETH", price=1800.01, description=f"Desc"
        )
        user = TradingUser.objects.get(username="artem")
        self.client.post("/api/v1/profiles/subscriptions/", data={"pk": 2})
        resp = self.client.get("/api/v1/profiles/subscriptions/")
        self.assertEquals(len(resp.data), 2)
