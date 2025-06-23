from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User

class TestSetup(APITestCase):
    def setUp(self):
        self.user_data = {
            "username": "testuser",
            "password": "testpassword"
        }
        self.user2_data ={
            "username":"testuser2",
            "password":"testpassword"
        }
        self.user = User.objects.create_user(**self.user_data)
        self.user2 = User.objects.create_user(**self.user2_data)
        self.admin = User.objects.create_superuser(username='admin', password='adminpass')
        
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.csrf_url = reverse('csrfset')
        self.auth_check_url = reverse('authcheck')

        super().setUp()  # optional, but fine to include

    def tearDown(self):
        super().tearDown()
