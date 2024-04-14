from django.urls import path

from .views import (AddToCartView, CartView, DeleteFromCartView, 
                    ClearCartView, CartOrderingView, OrderComplete, CartUpdateView)
app_name = 'order'

urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('add/', AddToCartView.as_view(), name='add_to_cart'),
    
    path('cart/remove/<int:pk>/', DeleteFromCartView.as_view(), name='cart_remove'),
    path('cart/clear/', ClearCartView.as_view(), name='cart_clear'),

    path('cart/ordering', CartOrderingView.as_view(), name='cart_ordering'),
    
    path('cart/update/<int:cart_id>/<str:action>/', CartUpdateView.as_view(), name='cart_item_update'),
    
    path("complete/<int:order_id>/", OrderComplete.as_view(), name='complete'),
]