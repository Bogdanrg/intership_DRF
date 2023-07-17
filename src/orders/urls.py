from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"buy", views.UsersOrderListViewSet, basename="order")
router.register(r"order", views.OrderViewSet, basename='order')
router.register(r"sell", views.OrderSellListViewSet, basename='order')

urlpatterns = router.urls
