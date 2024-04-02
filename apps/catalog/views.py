from django.urls import reverse
from django.views.generic import ListView, DetailView
from .models import Catalog, Product
#import Q
from django.db.models import Q

from apps.main.mixins import ListViewBreadcrumbMixin, DetailViewBreadcrumbMixin


# Create your views here.

class CataloglistView(ListViewBreadcrumbMixin):
    model = Catalog
    template_name = 'catalog/index.html'
    context_object_name = 'categories' 
    
    def get_queryset(self):
        return Catalog.objects.filter(parent=None)
    
    
    def get_breradcrumb(self):
        self.breadcrumbs = {
            'current': 'Каталог',
        }
        return self.breadcrumbs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_count'] = Catalog.objects.filter(parent=None).count()
        print(context)
        return context
    

class ProductByCategoryView(ListViewBreadcrumbMixin):
    model = Catalog
    template_name = 'catalog/product_by_category.html'
    context_object_name = 'category'
    
    def get_queryset(self):
        self.category = Catalog.objects.get(slug=self.kwargs['slug'])
        self.categories = Catalog.objects.filter(parent=self.category)
        self.all_categories = self.categories.get_descendants(include_self=True)
        print(self.all_categories)
        queryset = Product.objects.filter( Q(productcategory__category__in=self.all_categories) | Q(productcategory__category=self.category))
        print(queryset)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['categories'] = self.categories
        context['category'] = self.category
        return context
    
    def get_breradcrumb(self):
        breadcrumbs = { reverse('catalog:index'): 'Каталог' }
        if self.category.parent:
            linkss = []
            parent = self.category.parent
            while parent is not None:
                linkss.append(
                    (
                        reverse('catalog:category', kwargs={'slug': parent.slug}),
                        parent.name
                    )
                )
                parent = parent.parent
            for url, name in reversed(linkss):
                breadcrumbs[url] = name
                breadcrumbs.update({url: name})
        breadcrumbs.update({'current': self.category.name})
        return breadcrumbs
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_queryset = len(list(context['category']))
        context["amount_of_products"] = product_queryset
        return context
    
class ProductDetailView(DetailViewBreadcrumbMixin):
    model = Product
    template_name = 'catalog/product.html'
    context_object_name = 'product'
    
    def get_breradcrumb(self):
        breadcrumbs = { reverse('catalog:index'): 'Каталог' }
        category = self.object.main_category()
        if category:
            if category.parent:
                linkss = []
                parent = category.parent
                while parent is not None:
                    linkss.append(
                        (
                            reverse('catalog:category', kwargs={'slug': parent.slug}),
                            parent.name
                        )
                    )
                    parent = parent.parent
                for url, name in reversed(linkss):
                    breadcrumbs[url] = name
                    breadcrumbs.update({url: name})
            breadcrumbs.update({reverse('catalog:category', kwargs={'slug': category.slug}): category.name})
        breadcrumbs.update({'current': self.object.name})
        return breadcrumbs