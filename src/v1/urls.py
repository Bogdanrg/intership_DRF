from django.urls import include, path

urlpatterns = [
    path("promotions/", include("src.promotions.urls")),
    path("orders/", include("src.orders.urls")),
    path("profiles/", include("src.profiles.urls")),
    path("portfolio/", include("src.portfolio.urls")),
    path("auto-orders/", include("src.auto_orders.urls")),
]
