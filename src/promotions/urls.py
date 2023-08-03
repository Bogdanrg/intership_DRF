from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"", views.PromotionListCRUDViewSet, basename="promotion")

urlpatterns = router.urls
