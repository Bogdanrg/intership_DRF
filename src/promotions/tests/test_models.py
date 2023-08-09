from django.test import TestCase

from src.promotions.models import Promotion


class PromotionModelTest(TestCase):
    def setUp(self):
        self.promotion = Promotion.objects.create(
            avatar="AWS", name="BTC", price=2900.29, description="Desc"
        )

    def test_object_is_first_name_price_last(self):
        promotion = Promotion.objects.get(id=self.promotion.pk)
        expected_object_name = f"Promotion: [{promotion.name}, {promotion.price}]"
        self.assertEquals(expected_object_name, str(promotion))
