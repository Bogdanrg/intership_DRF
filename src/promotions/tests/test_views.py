from django.test import TestCase
from rest_framework.test import APIClient

from src.profiles.models import TradingUser
from src.promotions.models import Promotion
from src.promotions.serializers import PromotionListSerializer, PromotionSerializer

# flake8: noqa


class PromotionListCRUDViewSetTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        promotion_count = 5
        for promotion in range(promotion_count + 1):
            Promotion.objects.create(
                avatar=f"AWS/{promotion}",
                name=f"{promotion}",
                price=promotion * 200.01,
                description=f"Desc of {promotion}",
            )

        TradingUser.objects.create_user(
            username="bogdan", password="zaqxswcdevfr", email="Bogdan20160902@gmail.com"
        )

        TradingUser.objects.create_user(
            username="admin",
            password="zaqxswcdevfr",
            email="Bogdan20160902@gmail.com",
            role="admin",
        )

        TradingUser.objects.create_user(
            username="analyst",
            password="zaqxswcdevfr",
            email="Bogdan20160902@gmail.com",
            role="analyst",
        )

    def setUp(self) -> None:
        self.promotion_count = 5
        self.client = APIClient()

    def test_promotion_list_as_default(self):
        self.client.login(username="bogdan", password="zaqxswcdevfr")
        promotions_expected = Promotion.objects.all()
        resp = self.client.get("/api/v1/promotions/")
        self.assertEqual(len(promotions_expected), len(resp.data))
        serializer = PromotionListSerializer(promotions_expected, many=True)
        for i in range(len(serializer.data)):
            promotion_expected = serializer.data[i]
            promotion_result = resp.data[i]
            self.assertEqual(promotion_expected["name"], promotion_result["name"])
            self.assertEqual(promotion_expected["price"], promotion_result["price"])
            self.assertEqual(promotion_expected["avatar"], promotion_result["avatar"])
            self.assertEqual(promotion_expected["id"], promotion_result["id"])

    def test_promotion_list_as_admin(self):
        self.client.login(username="admin", password="zaqxswcdevfr")
        promotions_expected = Promotion.objects.all()
        resp = self.client.get("/api/v1/promotions/")
        self.assertEqual(len(promotions_expected), len(resp.data))
        serializer = PromotionListSerializer(promotions_expected, many=True)
        for i in range(len(serializer.data)):
            promotion_expected = serializer.data[i]
            promotion_result = resp.data[i]
            self.assertEqual(promotion_expected["name"], promotion_result["name"])
            self.assertEqual(promotion_expected["price"], promotion_result["price"])
            self.assertEqual(promotion_expected["avatar"], promotion_result["avatar"])
            self.assertEqual(promotion_expected["id"], promotion_result["id"])

    def test_promotion_list_as_analyst(self):
        self.client.login(username="analyst", password="zaqxswcdevfr")
        promotions_expected = Promotion.objects.all()
        resp = self.client.get("/api/v1/promotions/")
        self.assertEqual(len(promotions_expected), len(resp.data))
        serializer = PromotionListSerializer(promotions_expected, many=True)
        for i in range(len(serializer.data)):
            promotion_expected = serializer.data[i]
            promotion_result = resp.data[i]
            self.assertEqual(promotion_expected["name"], promotion_result["name"])
            self.assertEqual(promotion_expected["price"], promotion_result["price"])
            self.assertEqual(promotion_expected["avatar"], promotion_result["avatar"])
            self.assertEqual(promotion_expected["id"], promotion_result["id"])

    def test_promotion_retrieve_as_admin(self):
        self.client.login(username="admin", password="zaqxswcdevfr")
        promotion_expected = Promotion.objects.get(id=1)
        resp = self.client.get("/api/v1/promotions/1/")
        serializer = PromotionSerializer(promotion_expected)
        self.assertEqual(serializer.data, resp.data)

    def test_promotion_retrieve_as_default(self):
        self.client.login(username="bogdan", password="zaqxswcdevfr")
        promotion_expected = Promotion.objects.get(id=1)
        resp = self.client.get("/api/v1/promotions/1/")
        serializer = PromotionSerializer(promotion_expected)
        self.assertEqual(serializer.data, resp.data)

    def test_promotion_retrieve_as_analyst(self):
        self.client.login(username="analyst", password="zaqxswcdevfr")
        promotion_expected = Promotion.objects.get(id=1)
        resp = self.client.get("/api/v1/promotions/1/")
        serializer = PromotionSerializer(promotion_expected)
        self.assertEqual(serializer.data, resp.data)

    def test_promotion_destroy_as_admin(self):
        self.client.login(username="admin", password="zaqxswcdevfr")
        resp = self.client.delete("/api/v1/promotions/1/")
        self.assertEqual(resp.status_code, 204)

    def test_promotion_destroy_as_analyst(self):
        self.client.login(username="analyst", password="zaqxswcdevfr")
        resp = self.client.delete("/api/v1/promotions/1/")
        self.assertEqual(resp.status_code, 403)

    def test_promotion_destroy_as_default(self):
        self.client.login(username="bogdan", password="zaqxswcdevfr")
        resp = self.client.delete("/api/v1/promotions/1/")
        self.assertEqual(resp.status_code, 403)

    def test_promotion_update_as_admin(self):
        self.client.login(username="admin", password="zaqxswcdevfr")
        resp = self.client.put(
            "/api/v1/promotions/1/", {"name": "variable", "price": 100.011}
        )
        self.assertEqual(resp.status_code, 200)

    def test_promotion_update_as_analyst(self):
        self.client.login(username="analyst", password="zaqxswcdevfr")
        resp = self.client.put("/api/v1/promotions/1/", {"some": "variable"})
        self.assertEqual(resp.status_code, 403)

    def test_promotion_update_as_default(self):
        self.client.login(username="bogdan", password="zaqxswcdevfr")
        resp = self.client.put("/api/v1/promotions/1/", {"some": "variable"})
        self.assertEqual(resp.status_code, 403)

    def test_promotion_create_as_admin(self):
        self.client.login(username="admin", password="zaqxswcdevfr")
        resp = self.client.post(
            "/api/v1/promotions/", {"name": "variable", "price": 100}
        )
        self.assertEqual(resp.status_code, 201)

    def test_promotion_create_as_analyst(self):
        self.client.login(username="analyst", password="zaqxswcdevfr")
        resp = self.client.post("/api/v1/promotions/", {"some": "variable"})
        self.assertEqual(resp.status_code, 403)

    def test_promotion_create_as_default(self):
        self.client.login(username="bogdan", password="zaqxswcdevfr")
        resp = self.client.post("/api/v1/promotions/", {"some": "variable"})
        self.assertEqual(resp.status_code, 403)
