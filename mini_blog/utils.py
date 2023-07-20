from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    if isinstance(exc, APIException):
        data = {'error': exc.default_detail}
        return Response(data, status=exc.status_code)

    # Fallback to default exception handler for other exceptions
    return exception_handler(exc, context)
