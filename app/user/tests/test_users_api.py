from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    ''' Test the users api (public) '''

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_sucess(self):
        '''test creating using user with valid payload is sucessfull'''
        payload = {
            'email': 'test@londonappdev.com',
            'password': 'testpass',
            'name': 'Test Name'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        '''test creating user that already exists fails'''
        payload = {
            'email': 'test@londonappdev.com',
            'password': 'testpass',
            'name': 'Test',
            }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        '''test that the password must be more than 5 charecters'''
        payload = {
            'email': 'test@londonapp.com',
            'password': 'pw',
            'name': 'Test',
            }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        User_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(User_exists)

    def test_create_token_for_user(self):
        '''Test that a token is created for the user'''
        payload = {
            'email': 'test@londonapp.com',
            'password': 'testpass',
            'name': 'Test',
            }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        '''Test that token is not created if invalid credentials are given'''
        create_user(email='test@londonapp.com', password='testpass')
        payload = {'email': 'test@londonappdev.com', 'password': 'wrongpass'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        '''test that token is not created if user doesn't exist'''
        payload = {'email': 'test@londonappdev.com', 'password': 'wrongpass'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        '''Test that email and password are required'''
        res = self.client.post(
            TOKEN_URL,
            {'email': 'test@londonappdev.com', 'password': ''}
            )
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
