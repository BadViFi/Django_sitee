from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.home, name='home'),
    path('<str:room>/', views.room, name='room'),
    path('checkview', views.checkview, name='checkview'),
    path('send', views.send, name='send'),
    path('getMessages/<str:room>/', views.getMessages, name='getMessages'),
    path('edit/<int:message_id>/', views.edit_message, name='edit_message'),  
    path('delete/<int:message_id>/', views.delete_message, name='delete_message'),  
]
