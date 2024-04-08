from django.urls import path

from .views import AddToCartView, CartView, DeleteFromCartView, ClearCartView, CartOrderingView

app_name = 'order'

urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('add/', AddToCartView.as_view(), name='add_to_cart'),
    
    path('cart/remove/<int:pk>/', DeleteFromCartView.as_view(), name='cart_remove'),
    path('cart/clear/', ClearCartView.as_view(), name='cart_clear'),

    path('cart/ordering', CartOrderingView.as_view(), name='cart_ordering'),
]