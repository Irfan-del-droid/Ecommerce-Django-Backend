from rest_framework import serializers
from .models import Product, Category, Review

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'description')

class ReviewSerializer(serializers.ModelSerializer):
    userName = serializers.CharField(source='user.full_name', read_only=True)
    
    class Meta:
        model = Review
        fields = ('id', 'userName', 'rating', 'comment', 'created_at')

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name')
    discountPercentage = serializers.IntegerField(source='discount_percentage', read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    
    # Map Django field names to match Express API output
    shortDescription = serializers.CharField(source='short_description')
    originalPrice = serializers.DecimalField(source='original_price', max_digits=10, decimal_places=2)
    viewCount = serializers.IntegerField(source='view_count', read_only=True)
    soldCount = serializers.IntegerField(source='sold_count', read_only=True)
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    
    class Meta:
        model = Product
        fields = (
            'id', 'name', 'slug', 'description', 'shortDescription', 
            'price', 'originalPrice', 'discountPercentage', 'currency', 
            'category', 'subcategory', 'emoji', 'badge', 'glow', 
            'images', 'stock', 'sku', 'sizes', 'colors', 'material', 
            'weight', 'dimensions', 'tags', 'brand', 'is_active', 
            'is_featured', 'seo', 'viewCount', 'soldCount', 'reviews', 'createdAt'
        )
