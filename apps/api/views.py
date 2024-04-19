from django.shortcuts import render

from rest_framework import viewsets, permissions
from apps.members.models import Profile

from .serializers import ProfileSerializer

# Create your views here.
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = ProfileSerializer