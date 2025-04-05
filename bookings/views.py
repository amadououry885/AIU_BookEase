from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Booking
from .serializers import BookingSerializer
from facilities.models import Facility
from users.permissions import IsStudent, IsStaff, IsAdmin

class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]  # All authenticated users can view bookings
        elif self.action == 'create':
            return [permissions.IsAuthenticated(), IsStudent()]  # Students can book
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsStaff()]  # Staff can modify or delete
        return [permissions.IsAuthenticated(), IsAdmin()]  # Admins get full access

    def get_queryset(self):
        user = self.request.user
        
        # Students can only see their own bookings
        if user.role == 'Student':
            return Booking.objects.filter(user=user)
        # Staff and Admin can see all bookings
        return Booking.objects.all()

    def perform_create(self, serializer):
        """
        Override create to assign the logged-in student to the booking.
        """
        serializer.save(user=self.request.user)  # Ensure the booking is tied to the requesting student