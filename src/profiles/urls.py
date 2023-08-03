from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"profile", views.UserProfileViewSet, basename="tradinguser")
router.register(
    r"subscriptions", views.SubscribeOnPromotionListViewSet, basename="promotion"
),

urlpatterns = router.urls
