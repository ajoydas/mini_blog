import logging
import time

logger = logging.getLogger(__name__)


class ResponseTimeLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        end_time = time.time()
        response_time = end_time - start_time

        response_code = response.status_code
        logger.info(f'Status: {response_code} | Time taken: {response_time:.2f}s')

        return response
