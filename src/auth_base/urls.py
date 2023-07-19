from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.CreateTokenPairAPIView.as_view()),
    path("refresh/", views.RefreshAccessToken.as_view()),
    path("registration/", views.RegistrationUserAPIView.as_view()),
    path("verification/<username>", views.ActivateUserAPIView.as_view()),
    path("change_password/", views.ChangePasswordViewSet.as_view({"put": "update"})),
    path(
        "password_reset/",
        include("django_rest_passwordreset.urls", namespace="password_reset"),
    ),
]
