from django.urls import path

from .views import CataloglistView

app_name = 'catalog'

urlpatterns = [
    path('', CataloglistView.as_view(), name='index'),
    path('<slug:slug>/', CataloglistView.as_view() , name='category'),
]