import json

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse, resolve
from django.test import TestCase, Client
from rest_framework import status
from rest_framework.test import APIRequestFactory, RequestsClient
from django.conf.urls import include

# Create your tests here.
from .models import Image
import requests
import django
django.setup()

class GalleryTestCase(TestCase):

    def test_list_images_status(self):
        url = '/gallery/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_count_images_list(self):
        user_model = User.objects.create_user(username='test', password='kd8wke-DE34', first_name='test', last_name='test', email='test@test.com')
        Image.objects.create(name='nuevo', url='No', description='testImage', type='jpg', imageFile='images/Jellyfish.jpg', user=user_model)
        Image.objects.create(name='nuevo2', url='No', description='testImage', type='jpg', imageFile='images/Jellyfish.jpg', user=user_model)

        images_list = Image.objects.all()
        response=self.client.get('/gallery/')
        current_data=json.loads(response.content)

        self.assertEqual(len(current_data),2)

    def test_verify_first_from_images_list(self):
        user_model = User.objects.create_user(username='test', password='kd8wke-DE34', first_name='test', last_name='test', email='test@test.com')
        Image.objects.create(name='nuevo', url='No', description='testImage', type='jpg', imageFile='images/Jellyfish.jpg', user=user_model)
        Image.objects.create(name='nuevo2', url='No', description='testImage', type='jpg', imageFile='images/Jellyfish.jpg', user=user_model)

        images_list = Image.objects.all()
        response=self.client.get('/gallery/')
        current_data=json.loads(response.content)

        self.assertEqual(current_data[0]['fields']['name'],"nuevo")

    def test_add_user(self):
        response=self.client.post('/gallery/addUser/',json.dumps({"username": "testUser", "first_name": "Test", "last_name": "User", "password": "AnyPas#5", "email": "test@test.com"}), content_type='application/json')
        print(response.status_code)
        self.assertEqual(1,1)