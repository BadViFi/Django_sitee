from django.shortcuts import render

from rest_framework import viewsets, permissions

from apps.catalog.models import Catalog, Product, ProductCategory


from .serializers import CatalogSerializer, ProductSerializer

# Create your views here.

#10 random products
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('?').prefetch_related('category').prefetch_related('images')
    serializer_class = ProductSerializer
    permission_classes = []