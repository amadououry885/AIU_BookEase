from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserRegisterView, UserLoginView, UserProfileView

# Create a router and register your viewset for User
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')


urlpatterns = [
    path('', include(router.urls)),  # Automatically generates CRUD endpoints for users
    path('register/', UserRegisterView.as_view(), name='user-register'),  # Registration endpoint
    path('login/', UserLoginView.as_view(), name='user-login'),  # Login endpoint
    path('profile/', UserProfileView.as_view(), name='user-profile'),  # Profile endpoint
]
