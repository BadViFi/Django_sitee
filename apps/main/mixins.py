from django.views import generic



class ListViewBreadcrumbMixin(generic.ListView):
    breadcrumbs = {}
    
    def get_breradcrumb(self):
        return self.breadcrumb
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = self.get_breradcrumb()
        return context
    
class DetailViewBreadcrumbMixin(generic.DetailView):
    breadcrumbs = {}
    
    def get_breradcrumb(self):
        return self.breadcrumbs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = self.get_breradcrumb()
        return context