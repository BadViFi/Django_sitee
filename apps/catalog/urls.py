from django.urls import path

from .views import CataloglistView, ProductByCategoryView, ProductDetailView

app_name = 'catalog'

urlpatterns = [
    path('', CataloglistView.as_view(), name='index'),
    path('<slug:slug>/', ProductByCategoryView.as_view() , name='category'),
    path('<slug:category_slug>/<slug:slug>/', ProductDetailView.as_view(), name='product'),
]