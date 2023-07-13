from rest_framework import routers

from . import views

urlpatterns = []

router_list = routers.SimpleRouter()
router_list.register(r'', views.ListPromotionViewSet, basename='promotion')


class CustomCRUDRouter(routers.SimpleRouter):
    routes = [
        routers.Route(
            url=r'^/add$',
            mapping={'post': 'create'},
            name='{basename}-create',
            detail=False,
            initkwargs={}
        ),
        routers.Route(
            url=r'^/{lookup}$',
            mapping={'get': 'retrieve', 'put': 'update', 'delete': 'destroy'},
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Detail'}
        ),
    ]


router_detail = CustomCRUDRouter()
router_detail.register('', views.CreateRetrieveUpdateDestroyViewSet, basename='promotion')

urlpatterns += router_list.urls + router_detail.urls
