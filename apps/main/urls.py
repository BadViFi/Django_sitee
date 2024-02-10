from django.urls import path
app_name = 'main'
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('about/',views.about,name='ja sigma'),
    path('lol/',views.home,name='ja sigmach'),
]