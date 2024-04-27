
from rest_framework import serializers


from django.contrib.auth.models import User
from apps.blog.models import Post, Comment
from apps.members.models import Profile
from apps.catalog.models import Catalog, Product, ProductCategory, Image


class CatalogSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Catalog
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Image
        fields = '__all__'     

class ProductSerializer(serializers.ModelSerializer):    
    category = CatalogSerializer(many=True)
    images = ImageSerializer(many=True)
    class Meta:
        model = Product
        fields = '__all__'






