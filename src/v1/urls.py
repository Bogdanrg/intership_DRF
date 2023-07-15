from django.urls import path, include


urlpatterns = [
    path('promotions/', include('src.promotions.urls')),
    path('orders/', include('src.orders.urls')),
    path('profiles/', include('src.profiles.urls')),
    path('portfolio/', include('src.portfolio.urls'))
]
