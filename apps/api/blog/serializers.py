from rest_framework import serializers


from django.contrib.auth.models import User
from apps.blog.models import Post, Comment
from apps.members.models import Profile


class AuthorSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = Profile
        fields = (
            'id',
            'user',
            'get_avatar',
            'bio',
            'get_absolute_url'
        )
    


class PostReadSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(source='author.profile', read_only=True)
    
    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'content',
            'image',
            # 'thumbnail',
            'likes',
            'views',
            'created_at',
            'is_published',
            'author',
            'get_thumbnail'
        )
        
    
        