from django.urls import path

from .views import AddToCartView

app_name = 'order'

urlpatterns = [
    path('add/', AddToCartView.as_view(), name='add_to_cart'),
]