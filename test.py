from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
from rest_framework.authtoken.models import Token
from bookings.models import Booking
from facilities.models import Facility
from django.utils import timezone

class APIFunctionalityTest(APITestCase):
    def setUp(self):
        # Create users for each role
        self.student = User.objects.create_user(username="student", email="student@example.com", password="pass1234", role="Student")
        self.staff = User.objects.create_user(username="staff", email="staff@example.com", password="pass1234", role="Staff")
        self.admin = User.objects.create_user(username="admin", email="admin@example.com", password="pass1234", role="Admin")

        # Tokens for authentication
        self.student_token = Token.objects.create(user=self.student)
        self.staff_token = Token.objects.create(user=self.staff)
        self.admin_token = Token.objects.create(user=self.admin)

        self.facility = Facility.objects.create(
            name="Library",
            description="Main campus library",
            category="Library"  # Again, use a valid value
        )

    def test_student_can_register_and_login(self):
        # Test registration
        url = reverse('user-register')
        data = {
            "email": "newstudent@example.com",
            "username": "newstudent",
            "password": "pass1234"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", response.data)

        # Test login
        url = reverse('user-login')
        response = self.client.post(url, {"email": "newstudent@example.com", "password": "pass1234"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)



    def test_student_can_create_booking(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.student_token.key)
        url = reverse('booking-list')

        data = {
            "user": self.student.id,  # Required
            "facility": self.facility.id,
            "booking_date": timezone.now().date().isoformat(),  # 'YYYY-MM-DD'
            "start_time": "10:00:00",  # Valid time format
            "end_time": "12:00:00",    # Valid time format
        }

        response = self.client.post(url, data)
        print("Booking response data:", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_staff_can_create_facility(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.staff_token.key)
        url = reverse('facility-list')
        data = {
            "name": "Computer Lab",
            "description": "Room with PCs",
            "category": "Lab"  # Add a valid category
        }
        response = self.client.post(url, data)
        print("Facility creation response:", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_student_cannot_create_facility(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.student_token.key)
        url = reverse('facility-list')
        data = {
            "name": "Unauthorized Lab",
            "description": "Students should not create this"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_cannot_create_booking(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.staff_token.key)
        url = reverse('booking-list')
        facility = Facility.objects.create(name="Auditorium", description="Big room")
        data = {
            "facility": facility.id,
            "start_time": "2025-04-06T10:00:00Z",
            "end_time": "2025-04-06T12:00:00Z"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
