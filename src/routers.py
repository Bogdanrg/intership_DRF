from django.urls import path, include


urlpatterns = [
    path('v1/', include("src.v1.urls")),
]
