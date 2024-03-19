from django.urls import path
from .views import *

app_name = 'members'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', signup_view, name='signup'),
    
    path('profile/update/', profile_update_view, name='profile_update'),
    
    path('profile/<str:username>', profile_view, name='profile'),
    path('profile/<str:username>/follow/', follow_view, name='follow'),
    
    path('search/', search_view, name='search_profile'),
    
    ] 