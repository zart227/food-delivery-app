import logging

logger = logging.getLogger(__name__)


class LogRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Логируем заголовки
        print(f"Headers: {dict(request.headers)}")
        logger.info(f"Headers: {dict(request.headers)}")

        # Логируем тело запроса (только для методов POST, PUT, PATCH)
        if request.method in ["POST", "PUT", "PATCH"]:
            try:
                logger.info(f"Body: {request.body.decode('utf-8')}")
                print(f"Body: {request.body.decode('utf-8')}")
            except Exception as e:
                logger.error(f"Error decoding body: {e}")

        response = self.get_response(request)
        return response
