from functools import wraps
from django.core.cache import cache
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView


def cache_response(timeout=None, key_prefix=''):
    """
    Декоратор для кеширования ответов DRF views.
    
    Args:
        timeout (int): Время жизни кеша в секундах
        key_prefix (str): Префикс для ключа кеша
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(view_instance, request, *args, **kwargs):
            # Формируем ключ кеша
            cache_key = (
                f"{key_prefix}:{request.path}:"
                f"{request.query_params}:{request.user.id if request.user.is_authenticated else 'anonymous'}"
            )

            # Пытаемся получить данные из кеша
            response_data = cache.get(cache_key)
            
            if response_data is None:
                # Если данных нет в кеше, выполняем view
                response = view_func(view_instance, request, *args, **kwargs)
                
                if isinstance(response, Response):
                    response_data = {
                        'data': response.data,
                        'status': response.status_code,
                    }
                    # Сохраняем в кеш
                    cache.set(cache_key, response_data, timeout or settings.CACHE_MIDDLEWARE_SECONDS)
                    return response
                return response
            
            # Возвращаем данные из кеша
            return Response(
                data=response_data['data'],
                status=response_data['status']
            )
        
        return _wrapped_view
    return decorator


def invalidate_cache_pattern(pattern):
    """
    Инвалидация кеша по паттерну.
    
    Args:
        pattern (str): Паттерн для поиска ключей кеша
    """
    keys = cache.keys(f"*{pattern}*")
    if keys:
        cache.delete_many(keys)


class CachedAPIView(APIView):
    """
    Базовый класс для API views с кешированием.
    """
    cache_timeout = settings.CACHE_MIDDLEWARE_SECONDS
    cache_key_prefix = ''

    def get_cache_key(self, request):
        """
        Формирует ключ кеша для запроса.
        """
        return (
            f"{self.cache_key_prefix}:{request.path}:"
            f"{request.query_params}:{request.user.id if request.user.is_authenticated else 'anonymous'}"
        )

    def get_cached_data(self, request):
        """
        Получает данные из кеша.
        """
        cache_key = self.get_cache_key(request)
        return cache.get(cache_key)

    def cache_response(self, request, response):
        """
        Кеширует ответ.
        """
        if isinstance(response, Response):
            cache_key = self.get_cache_key(request)
            response_data = {
                'data': response.data,
                'status': response.status_code,
            }
            cache.set(cache_key, response_data, self.cache_timeout)

    def invalidate_cache(self, request):
        """
        Инвалидирует кеш для текущего запроса.
        """
        cache_key = self.get_cache_key(request)
        cache.delete(cache_key) 