from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("csrf/", views.get_csrf, name="csrf"),
    path("login/", views.loginView, name="login"),
    path("register/", views.signupView.as_view(), name="register"),
    path("users_list/", views.UserListView.as_view(), name="users_list"),

]