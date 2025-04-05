from rest_framework import viewsets, permissions
from .models import Facility, UserFacilityAccess
from .serializers import FacilitySerializer
from users.permissions import IsStaff, IsAdmin



class FacilityViewSet(viewsets.ModelViewSet):
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]  # Everyone logged in can view
        elif self.action in ['create', 'update', 'destroy']:
            return [permissions.IsAuthenticated(), IsStaff()]  # Only staff can modify
        return [permissions.IsAuthenticated(), IsAdmin()]

    def get_queryset(self):
        # Return all facilities, regardless of the user role
        return Facility.objects.all()

    def perform_create(self, serializer):
        """
        Override to handle creating UserFacilityAccess for the logged-in user.
        """
        facility = serializer.save()
        UserFacilityAccess.objects.create(user=self.request.user, facility=facility, can_view=True, can_edit=True, can_delete=True)
