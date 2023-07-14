from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register(r'', views.CreateListPromotionViewSet, basename='promotion')
router.register(r'', views.RetrieveUpdateDestroyViewSet, basename='promotion')

urlpatterns = router.urls
