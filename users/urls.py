from django.urls import path
from . import views

urlpatterns = [
    path("", views.Users.as_view()),
    path("me", views.Me.as_view()),
    path("change-password", views.ChangePassword.as_view()),
    path("sign_in", views.LogIn.as_view()),
    path("sign_out", views.LogOut.as_view()),
    path("@<str:email>", views.PublicUser.as_view()),
    path("sign_up_one", views.UserRegistrationView.as_view()),
    path("sign_up_two", views.UserRegistrationView_two.as_view()),
]
