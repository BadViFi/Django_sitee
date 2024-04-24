
from django.urls import path, include

from .views import ProfileViewSet

app_name = 'api'

urlpatterns = [
    path('profiles/', ProfileViewSet.as_view({'get': 'list'}), name='profiles'),
    path('posts/', include('apps.api.blog.urls'), name='posts'),
    path('catalog/', include('apps.api.catalog.urls'), name='catalog'),
]