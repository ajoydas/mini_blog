from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from blog_auth.models import Profile
from blog_auth.permissions import IsOwnerOrSuperuser
from blog_auth.serializers import UserSerializer, ProfileSerializer, TokenSerializer, LoginSerializer
from mini_blog.errors import NotAuthenticated, BadRequest, ErrorSerializer


@swagger_auto_schema(request_body=UserSerializer)
class UserRegistrationView(generics.CreateAPIView):
    """
    User registration API.

    This API handles user registration.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    throttle_classes = [AnonRateThrottle, UserRateThrottle]


class UserLoginView(APIView):
    permission_classes = (AllowAny,)
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={
            200: openapi.Response('Successful login', TokenSerializer),
            401: openapi.Response('Invalid Credentials', ErrorSerializer),
        },
    )
    def post(self, request):
        """
        User login API.

        This API is used to authenticate a user and generate JWT tokens for the user.
        Parameters:
            request (Request): Request object containing username and password.
        Returns:
            Response: Response containing access and refresh JWT tokens on successful login.
        """
        input_request = LoginSerializer(data=request.data)
        if input_request.is_valid():
            user = User.objects.filter(username=input_request.validated_data['username']).get()
            if user is None or not user.check_password(input_request.validated_data['password']):
                raise NotAuthenticated('Invalid Credentials')

            # Authentication is successful, generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            response = TokenSerializer(data={'refresh': refresh_token, 'access': access_token})
            return Response(response.initial_data)
        raise BadRequest(input_request.errors)


class ProfileView(APIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        if self.request.method == 'PUT':
            return [IsAuthenticated(), IsOwnerOrSuperuser()]
        return []

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(name='username', in_=openapi.IN_PATH, type='string'),
        ],
        responses={
            200: openapi.Response('Successful profile retrieval', ProfileSerializer),
            401: openapi.Response('Not authenticated', ErrorSerializer),
        },
    )
    def get(self, request, username):
        """
        Profile retrieval API.

        This API is used to retrieve the profile of a user.
        Parameters:
            request (Request): Request object containing user id.
            username (str): Username of the user whose profile is to be retrieved.
        Returns:
            Response: Response containing the profile of the user.
        """
        profile = get_object_or_404(Profile, user__username=username)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(name='username', in_=openapi.IN_PATH, type='string'),
        ],
        request_body=ProfileSerializer,
        responses={
            200: openapi.Response('Successful profile update', ProfileSerializer),
            401: openapi.Response('Not authenticated', ErrorSerializer),
            403: openapi.Response('Unauthorized', ErrorSerializer),
        },
    )
    def put(self, request, username):
        """
        Profile update API.

        This API is used to update the profile of a user.
        Parameters:
            request (Request): Request object containing user id and profile data.
            username (str): Username id of the user whose profile is to be updated.
        Returns:
            Response: Response containing the updated profile of the user.
        """
        profile = get_object_or_404(Profile, user__username=username)
        if not request.user.is_superuser and 'role' in request.data:
            # For non-superusers, throw error for unauthorized modification.
            raise BadRequest('You are not authorized to perform this action. You cannot modify role.')

        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            self.check_object_permissions(request, profile)
            serializer.save()
            return Response(serializer.data)
        raise BadRequest(serializer.errors)
