from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("csrf/", views.get_csrf, name="csrf"),
    path("login/", views.loginView, name="login"),
    # path("register/", views.RegisterView.as_view(), name="register"),
]