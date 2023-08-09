from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"", views.OrderCRUDViewSet, basename="order")
router.register(r"transactions", views.UsersTransactionsViewSet, basename="order")

urlpatterns = router.urls
