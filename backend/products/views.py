from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.decorators import action
from utils.cache import cache_response, CachedAPIView
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend


class ProductListAPIView(CachedAPIView):
    """
    API endpoint для получения списка всех продуктов.
    """
    permission_classes = [AllowAny]
    cache_key_prefix = 'products_list'
    cache_timeout = 3600  # 1 час

    @swagger_auto_schema(
        operation_description="Получить список всех продуктов",
        responses={200: ProductSerializer(many=True)}
    )
    def get(self, request):
        """
        Возвращает список всех доступных продуктов.
        """
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        response = Response(serializer.data)
        self.cache_response(request, response)
        return response


class ProductDetailAPIView(CachedAPIView):
    """
    API endpoint для получения детальной информации о конкретном продукте.
    """
    permission_classes = [AllowAny]
    cache_key_prefix = 'product_detail'
    cache_timeout = 3600  # 1 час

    @swagger_auto_schema(
        operation_description="Получить детальную информацию о продукте",
        responses={
            200: ProductSerializer,
            404: 'Продукт не найден'
        }
    )
    def get(self, request, pk):
        """
        Возвращает детальную информацию о продукте по его ID.
        
        Args:
            pk (int): Идентификатор продукта
            
        Returns:
            Response: Детальная информация о продукте
        """
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product)
        response = Response(serializer.data)
        self.cache_response(request, response)
        return response


class CategoryViewSet(ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class ProductViewSet(ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    authentication_classes = []  # Отключаем аутентификацию для этого ViewSet
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'category': ['exact'],
        'price': ['gte', 'lte'],
        'is_available': ['exact'],
        'is_vegetarian': ['exact'],
        'is_spicy': ['exact'],
        'calories': ['gte', 'lte'],
        'weight': ['gte', 'lte'],
    }
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'title', 'created_at']
    ordering = ['title']

    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.request.query_params.get('category_slug', None)
        
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
            
        return queryset

    @cache_response(timeout=3600, key_prefix='products_viewset_list')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @cache_response(timeout=3600, key_prefix='products_viewset_detail')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        invalidate_cache_pattern('products')  # Инвалидируем кеш при создании
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        invalidate_cache_pattern('products')  # Инвалидируем кеш при обновлении
        return response

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        invalidate_cache_pattern('products')  # Инвалидируем кеш при удалении
        return response
