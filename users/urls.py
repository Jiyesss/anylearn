from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path("", views.Users.as_view()),
    path("me", views.Me.as_view()),
    path("change-password", views.ChangePassword.as_view()),
    path("sign_in", views.LogIn.as_view()),
    path("sign_out", views.LogOut.as_view()),
    path("@<str:email>", views.PublicUser.as_view()),
    path("sign_up", views.UserRegistrationView.as_view()),
]
