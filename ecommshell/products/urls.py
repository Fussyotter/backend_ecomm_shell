from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views


app_name = "products"

urlpatterns = [
    path("", views.ProductListView.as_view(), name="store_home"),
    path("category/", views.CategoryListView.as_view(), name="categories"),
    path("products/<slug:slug>/", views.ProductDetail.as_view(), name="product"),
    path("category/<slug:slug>/",
         views.CategoryItemView.as_view(), name="category_item"),

    ]
