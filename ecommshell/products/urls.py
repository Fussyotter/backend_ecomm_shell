from django.urls import path

from . import views
from .views import get_random_products
# from .views import WebHook
from django.views.decorators.csrf import csrf_exempt


app_name = "products"

urlpatterns = [
    path("", views.ProductListView.as_view(), name="store_home"),
    path('random/<int:count>/', get_random_products, name='random_products'),
    path("category/", views.CategoryListView.as_view(), name="categories"),
    path("products/<slug:slug>/", views.ProductDetail.as_view(), name="product"),
    path("category/<slug:slug>/",
         views.CategoryItemView.as_view(), name="category_item"),
#     path("checkout/<slug:slug>/", views.CreateCheckoutSessionView.as_view(), name="create_checkout_session"),
#     path("webhook/stripe/", views.WebHook.as_view()),
    ]
