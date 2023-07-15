from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"", views.UsersOrderListViewSet, basename="order")
router.register(r"", views.OrderViewSet, basename='order')

urlpatterns = router.urls
