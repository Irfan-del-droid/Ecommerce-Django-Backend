from django.db import models
from django.utils.text import slugify
from django.db.models import JSONField
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(max_length=2000, blank=True, null=True)
    short_description = models.TextField(max_length=500, blank=True, null=True)
    
    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    currency = models.CharField(max_length=3, default='INR')
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    subcategory = models.CharField(max_length=100, blank=True, null=True)
    
    emoji = models.CharField(max_length=10, default='👕')
    badge = models.CharField(max_length=50, blank=True, null=True)
    glow = models.CharField(max_length=20, default='#d4af37')
    
    # Using JSONB fields for MongoDB-style flexibility
    images = JSONField(default=list)  # List of {url, alt, isPrimary}
    sizes = JSONField(default=list)   # List of {size, stock}
    colors = JSONField(default=list)  # List of {name, hexCode, stock}
    
    stock = models.IntegerField(default=0)
    sku = models.CharField(max_length=100, unique=True, blank=True, null=True)
    
    material = models.CharField(max_length=100, blank=True, null=True)
    weight = JSONField(default=dict)       # {value, unit}
    dimensions = JSONField(default=dict)   # {length, width, height, unit}
    tags = JSONField(default=list)         # List of strings
    
    brand = models.CharField(max_length=100, default='Loki Stores')
    
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    
    seo = JSONField(default=dict)          # {metaTitle, metaDescription, keywords}
    
    view_count = models.IntegerField(default=0)
    sold_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def discount_percentage(self):
        if self.original_price and self.original_price > self.price:
            return round(((self.original_price - self.price) / self.original_price) * 100)
        return 0

    def __str__(self):
        return self.name

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=5)
    comment = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('product', 'user')
