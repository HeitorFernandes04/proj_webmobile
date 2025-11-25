# accounts/urls.py
from django.urls import path
from .views import CustomLoginView, logout_view, signup

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
    path("signup/", signup, name="signup"),
]
