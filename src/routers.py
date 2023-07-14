from django.urls import include, path

urlpatterns = [
    path("v1/", include("src.v1.urls")),
    path("auth-custom/", include("src.custom_jwt.urls")),
]
