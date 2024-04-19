from django.shortcuts import render

from rest_framework import viewsets, permissions
from apps.blog.models import Post

from .serializers import PostReadSerializer

# Create your views here.
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(is_published=True).prefetch_related('author__profile').prefetch_related('comments').prefetch_related('likes').prefetch_related('author')
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = PostReadSerializer


    