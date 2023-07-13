from django.urls import path, include


urlpatterns = [
    path('promotions/', include('src.promotions.urls')),
    path('orders/', include('src.orders.urls'))
]
