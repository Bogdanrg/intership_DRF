from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register(r'', views.UserPortfolioViewSet, basename='portfoliouserpromotion')
router.register(r'', views.AnyUserPortfolioViewSet, basename='portfoliouserpromotion')

urlpatterns = router.urls
