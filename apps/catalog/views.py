from django.views.generic import ListView, DetailView
from .models import Catalog, Product

# Create your views here.

class CataloglistView(ListView):
    model = Catalog
    template_name = 'catalog/index.html'
    context_object_name = 'categories'


    def get_queryset(self):
        return Catalog.objects.filter(parent=None)
            
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_count'] = Catalog.objects.filter(parent=None).count()
        print(context)
        return context
    

    

class ProductByCategoryView(ListView):
    model = Catalog
    template_name = 'catalog/product_by_category.html'
    context_object_name = 'category'

    def get_queryset(self):
        self.category = Catalog.objects.get(slug=self.kwargs['slug'])
        self.categories = Catalog.objects.filter(parent=self.category)
        self.all_categories = self.categories.get_descendants(include_self=True)
        queryset = Product.objects.filter(productcategory__category__in=self.all_categories)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['categories'] = self.categories
        context['category'] = self.category
        return context
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_queryset = len(list(context['category']))
        context["amount_of_products"] = product_queryset
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product.html'
    context_object_name = 'product'