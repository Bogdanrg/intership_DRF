from src.promotions.models import Promotion


class OrderCreationService:

    #def __init__(self, request_data):
       # self.__

    def create_order(self, request_data: dict, pk: int) -> dict:
        promotion = Promotion.objects.get(pk=pk)
        data = {
            'promotion': promotion.pk,
            'total_sum': int(request_data['quantity']) * promotion.price,
            'status': 'pending',
            'quantity': request_data['quantity']
        }
        return data

   #@staticmethod
   #def is_affordable():


order_service = OrderCreationService()
