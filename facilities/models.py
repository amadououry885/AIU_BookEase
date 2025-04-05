from django.db import models
from django.conf import settings

class Facility(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    availability = models.BooleanField(default=True)
    category = models.CharField(max_length=20)

    def __str__(self):
        return self.name


# The relationship for users' access control
class UserFacilityAccess(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)
    can_view = models.BooleanField(default=False)
    can_edit = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} access to {self.facility.name}"
