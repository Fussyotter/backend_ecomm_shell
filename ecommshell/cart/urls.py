from django.urls import path
from . import views
app_name = "cart"
urlpatterns = [
    # ...
    path('add/<int:product_id>/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('', views.CartView.as_view(), name='cart'),
    path('checkout/', views.CreateCheckoutSessionView.as_view(), name='create_checkout_session'),
    path('webhook/stripe/', views.WebHook.as_view()),
    
    # ...
]
