from rest_framework import serializers
from rest_framework.exceptions import APIException

"""
This file contains custom exceptions used within this project
"""


class BadRequest(APIException):
    status_code = 400
    default_detail = 'Bad request.'


class NotAuthenticated(APIException):
    status_code = 401
    default_detail = 'You are not authenticated.'


class NotFound(APIException):
    status_code = 404
    default_detail = 'Not found.'


class PermissionDenied(APIException):
    status_code = 403
    default_detail = 'You are not authorized to perform this action.'


class ErrorSerializer(serializers.Serializer):
    """
    This class is written to aid API documentation generation for error responses.
    """
    error = serializers.CharField(read_only=True)
