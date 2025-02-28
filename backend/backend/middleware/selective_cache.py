from django.conf import settings
from django.core.cache import cache
from django.utils.cache import get_cache_key, learn_cache_key
from django.utils.deprecation import MiddlewareMixin


class SelectiveCacheMiddleware(MiddlewareMixin):
    """
    Middleware для выборочного кэширования.
    Не кэширует запросы к API эндпоинтам, указанным в CACHE_MIDDLEWARE_EXCLUDE_PATHS.
    """

    def __init__(self, get_response=None):
        super().__init__(get_response)
        self.cache_timeout = settings.CACHE_MIDDLEWARE_SECONDS
        self.key_prefix = settings.CACHE_MIDDLEWARE_KEY_PREFIX
        self.cache_alias = settings.CACHE_MIDDLEWARE_ALIAS if hasattr(settings, 'CACHE_MIDDLEWARE_ALIAS') else 'default'
        self.cache = cache
        self.async_mode = False

    def should_cache_path(self, request):
        """Проверяет, нужно ли кэшировать текущий путь"""
        if request.method not in ('GET', 'HEAD'):
            return False

        path = request.path_info.lstrip('/')
        
        # Не кэшируем API эндпоинты из списка исключений
        for excluded_path in getattr(settings, 'CACHE_MIDDLEWARE_EXCLUDE_PATHS', []):
            if path.startswith(excluded_path.lstrip('/')):
                return False
                
        return True

    def process_request(self, request):
        if not self.should_cache_path(request):
            return None

        # Пытаемся получить ответ из кэша
        cache_key = get_cache_key(request, self.key_prefix, 'GET', cache=self.cache)
        if cache_key is None:
            return None

        response = self.cache.get(cache_key)
        if response is None:
            return None

        return response

    def process_response(self, request, response):
        if not self.should_cache_path(request):
            return response

        # Не кэшируем ответы с ошибками
        if not response.status_code == 200:
            return response

        # Не кэшируем, если установлен заголовок Cache-Control: private
        if 'private' in response.get('Cache-Control', ''):
            return response

        cache_key = learn_cache_key(request, response, self.cache_timeout, self.key_prefix, cache=self.cache)
        if hasattr(response, 'render') and callable(response.render):
            response.add_post_render_callback(
                lambda r: self.cache.set(cache_key, r, self.cache_timeout)
            )
        else:
            self.cache.set(cache_key, response, self.cache_timeout)

        return response 