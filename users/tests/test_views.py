from .test_setup import TestSetup
from django.test import Client
from rest_framework import status
from django.contrib.auth.models import User

class TestViews(TestSetup):

        def test_register_user_success(self):
            data = {
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "StrongPass123!",
                "password2": "StrongPass123!"
            }
            res = self.client.post(self.register_url, data, format='json')
            
            self.assertEqual(res.status_code,status.HTTP_201_CREATED)
            self.assertTrue(User.objects.filter(username=res.data['username']).exists())
            
        def test_register_with_password_mismatch(self):
            data = {
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "StrongPass123!",
                "password2": "PASF@LJ34L!"
            }
            res = self.client.post(self.register_url, data, format='json')
            
            self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)
            self.assertIn('password',res.data)
            
        def test_register_existing_username(self):
                data = {
                    "username": self.user.username,  # already created in setup
                    "email": "different@example.com",
                    "password": "TestPass123!",
                    "password2": "TestPass123!"
                }
                response = self.client.post(self.register_url, data, format='json')
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertIn("username", response.data)

        def test_register_existing_email(self):

                data = {
                    "username": "uniqueuser",
                    "email": self.user.email,  # duplicate
                    "password": "TestPass123!",
                    "password2": "TestPass123!"
                }
                response = self.client.post(self.register_url, data, format='json')

                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertIn("email", response.data)
                
                
        def test_user_login_without_credentials(self):
                response = self.client.post(self.login_url,format='json')
                self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
                
        def test_user_login_with_credentials(self):
                #wrong credentials
                data ={
                    "username":self.user.username,
                    "password":"jfsldfjsf"
                }
                res_1 = self.client.post(self.login_url,data,format = 'json')
                self.assertEqual(res_1.status_code, status.HTTP_401_UNAUTHORIZED)
                
                #correct credentials
                correct_data = {
                    "username" : self.user.username,
                    "password":'testpassword'
                }
                
                res_2 = self.client.post(self.login_url,correct_data, format ='json')
                # import pdb; pdb.set_trace() # to pause testing and and drops you to python shell were we can interact with responses
                
                self.assertEqual(res_2.status_code, status.HTTP_200_OK)
                
                
        def test_user_not_authenticated(self):
            res = self.client.get(self.auth_check_url)
            self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
            self.assertEqual(res.data['is_authenticated'], False)

        def test_user_is_authenticated(self):
            self.client.force_login(self.user)
            res = self.client.get(self.auth_check_url)
            self.assertEqual(res.status_code, status.HTTP_200_OK)
            self.assertEqual(res.data['is_authenticated'], True)
            self.assertIn('user', res.data)
            self.assertEqual(res.data['user']['username'], self.user.username)
        