from django.views.generic import ListView, DetailView
from .models import Catalog, Product

# Create your views here.

class CataloglistView(ListView):
    model = Catalog
    template_name = 'catalog/index.html'
    context_object_name = 'categories'


    def get_queryset(self):
        return Catalog.objects.filter(parent=None)


class ProductByCategoryView(ListView):
    model = Catalog
    template_name = 'catalog/product_by_category.html'
    context_object_name = 'category'

    def get_queryset(self):
        self.category = Catalog.objects.get(slug=self.kwargs['slug'])
        self.categories = Catalog.objects.filter(parent=self.category)
        self.all_categories = self.categories.get_descendants(include_self=True)
        print(self.all_categories)
        queryset = Product.objects.filter(productcategory__category__in=self.all_categories)
        print(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['categories'] = self.categories
        context['category'] = self.category
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product.html'
    context_object_name = 'product'