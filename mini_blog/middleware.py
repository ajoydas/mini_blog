import logging
import time

logger = logging.getLogger(__name__)


class ResponseTimeLoggerMiddleware:
    """
    This class logs the response time of each API call.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        end_time = time.time()
        response_time = end_time - start_time

        response_code = response.status_code
        path = request.path
        logger.info(f'{path} | Status: {response_code} | Time taken: {response_time:.2f}s')

        return response
