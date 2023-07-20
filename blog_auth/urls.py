from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from blog_auth.views import UserLoginView, UserRegistrationView, ProfileView

urlpatterns = [
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('register', UserRegistrationView.as_view(), name='register'),
    path('login', UserLoginView.as_view(), name='login'),
    path('profile/<str:username>', ProfileView.as_view(), name='profile'),
]
