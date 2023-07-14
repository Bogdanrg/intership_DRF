from django.urls import path

from . import views

urlpatterns = [
    path("", views.CreateTokePairAPIView.as_view()),
    path("refresh/", views.RefreshAccessToken.as_view()),
]
