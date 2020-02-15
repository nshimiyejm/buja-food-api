# from django.shortcuts import render
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken 
from rest_framework.settings import api_settings

from user.serializers import UserSericalizer, AuthTokenSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSericalizer

class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = AuthTokenSerializer
    
    # Use the renderer to view the API posts in the browser 
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

