from rest_framework.exceptions import APIException


class BadRequest(APIException):
    status_code = 400
    default_detail = 'Bad request.'


class NotFound(APIException):
    status_code = 404
    default_detail = 'Not found.'


class PermissionDenied(APIException):
    status_code = 403
    default_detail = 'Permission denied.'
