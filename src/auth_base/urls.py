from django.urls import path

from . import views

urlpatterns = [
    path("", views.CreateTokenPairAPIView.as_view()),
    path("refresh/", views.RefreshAccessToken.as_view()),
    path("registration/", views.RegistrationUserAPIView.as_view()),
    path("verification/<username>", views.ActivateUserAPIView.as_view()),
    path("change_password/", views.ChangePasswordViewSet.as_view({"put": "update"})),
    path("password_reset/", views.ResetPasswordAPIView.as_view()),
    path("password_reset/confirm/", views.ConfirmResetPasswordAPIView.as_view()),
]
