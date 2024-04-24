from django.urls import path, include

from .views import PostViewSet


urlpatterns = [
    path('', PostViewSet.as_view({'get': 'list'})),
]