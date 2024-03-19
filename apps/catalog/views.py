from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView
from .models import Catalog
# Create your views here.

class CataloglistView(ListView):
    model = Catalog
    template_name = 'catalog/index.html'
    context_object_name = 'categories'
    # paginate_by = 3