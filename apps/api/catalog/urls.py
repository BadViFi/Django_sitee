from django.urls import path, include

from .views import *


urlpatterns = [
    path('', ProductViewSet.as_view({'get': 'list'}), name='product'),
]