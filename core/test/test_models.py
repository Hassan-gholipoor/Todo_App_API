from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models

class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        payload = {
            'email': 'test@email.com',
            'password': 'pasworddtest'
        }
        user = get_user_model().objects.create_user(**payload)

        self.assertEqual(user.email, payload['email'])
        self.assertTrue(user.check_password(payload['password']))

    def test_normalized_email(self):
        payload = {
            'email': 'test@GMAIL.com',
            'password': 'pasworddtest'
        }
        user = get_user_model().objects.create_user(**payload)
        
        self.assertEqual(user.email, payload['email'].lower())
    
    def test_new_user_invalid_email(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'testpsssss')

    def test_create_superuser(self):
        payload = {
            'email': 'test@email.com',
            'password': 'pasworddtest',
        }
        user = get_user_model().objects.create_superuser(**payload)

        self.assertEqual(user.email, payload['email'])
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
    
    def test_todo_str_representaion(self):
        payload = {
            'email': 'test@email.com',
            'password': 'pasworddtest',
        }
        user = get_user_model().objects.create_superuser(**payload)
        todo = models.Todo.objects.create(title='gym', owner=user)

        self.assertEqual(todo.title, 'gym')

        

