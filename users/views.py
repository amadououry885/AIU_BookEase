from rest_framework import viewsets, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status, permissions
from django.contrib.auth import authenticate
from .models import User
from .serializers import UserSerializer
from .permissions import IsStudent, IsAdmin, IsStaff


# ViewSet to handle CRUD operations for Users (excluding registration and login)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user  # Ensures only the logged-in user's data is accessed


# User Registration View
class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        username = request.data.get('username')
        password = request.data.get('password')

        # Check if user already exists
        if User.objects.filter(email=email).exists():
            return Response({"detail": "Email already registered"}, status=status.HTTP_400_BAD_REQUEST)

        # Create new user
        user = User.objects.create_user(email=email, username=username, password=password)
        user.save()

        # Generate token for the newly created user
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "token": token.key,
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username
            }
        }, status=status.HTTP_201_CREATED)

# User Login
class UserLoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email=email, password=password)
        if user:
            # Generate token for authenticated user
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "token": token.key,
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "username": user.username,
                    "role": user.role
                }
            }, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


# User Profile (updated to allow updates and retrieval of the user’s profile)
class UserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]  # Ensure user is authenticated to access their profile
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user  # Return only the logged-in user's data

# Admin Profile View (only admin can access their profile)
class AdminProfileView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, IsAdmin]  # Only admin can access this
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user  # Return the logged-in user's data

# Staff Profile View (only staff can access their profile)
class StaffProfileView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, IsStaff]  # Only staff can access this
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user  # Return the logged-in user's data

# Student Profile View (only student can access their profile)
class StudentProfileView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, IsStudent]  # Only student can access this
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user  # Return the logged-in user's data
