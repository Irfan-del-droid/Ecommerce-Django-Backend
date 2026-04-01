from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, Category, Review
from .serializers import ProductSerializer, CategorySerializer, ReviewSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

    def get_authenticators(self):
        # Public catalog: skip JWT so a stale Bearer cannot cause 401 before AllowAny.
        return []

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny] # Default list/retrieve is public
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category__name', 'badge', 'is_featured']
    search_fields = ['name', 'description', 'tags']
    ordering_fields = ['price', 'created_at', 'sold_count']

    def get_permissions(self):
        if hasattr(self, 'action') and self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return super().get_permissions()

    def get_authenticators(self):
        if hasattr(self, 'action') and self.action in ('list', 'retrieve', 'featured'):
            return []
        return super().get_authenticators()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.view_count += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response({
            'status': 'success',
            'product': serializer.data
        })

    @action(detail=False, methods=['get'])
    def featured(self, request):
        featured_products = self.queryset.filter(is_featured=True)[:10]
        serializer = self.get_serializer(featured_products, many=True)
        return Response({
            'status': 'success',
            'results': serializer.data
        })
