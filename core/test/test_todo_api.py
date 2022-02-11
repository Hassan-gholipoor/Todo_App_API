from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Todo
from core import serializers

TODO_URL = reverse('todo:todo-list')

def todo_update_url(idx):
    return reverse('todo:todo-detail', args=[idx])


class PublicTodoAPITests(TestCase):
    
    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        res = self.client.get(TODO_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTodoAPITests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='admin@gmail.com', 
            password='teestadmin'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_todos(self):
        Todo.objects.create(title='gym', owner=self.user)
        Todo.objects.create(title='study', owner=self.user)
        res = self.client.get(TODO_URL)

        todos = Todo.objects.all().order_by('-title')
        seriailzer = serializers.TodoSerializer(todos, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, seriailzer.data)

    def test_retrieve_todos_limited_to_authenticated_user(self):
        user2 = get_user_model().objects.create_user(
            email='second@gmail.com',
            password='tstpassword'
        )
        t1 = Todo.objects.create(title='gym', owner=self.user)
        t2 = Todo.objects.create(title='study', owner=user2)
        res = self.client.get(TODO_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['title'], t1.title)

    def test_create_todo_success(self):
        payload = {
            'title': 'Shopping'
        }
        self.client.post(TODO_URL, payload)

        exists = Todo.objects.filter(
            owner=self.user,
            title=payload['title']
        ).exists()
        self.assertTrue(exists)

    def test_create_todo_invalid(self):
        payload = {'title': ''}
        res = self.client.post(TODO_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_partial_update_todo(self):
        todo = Todo.objects.create(title='game', owner=self.user)
        payload = {
            'title': 'new title'
        }
        url = todo_update_url(todo.id)
        self.client.patch(url, payload)
        todo.refresh_from_db()
        self.assertEqual(todo.title, payload['title'])

    def test_filter_todos_by_title(self):
        t1 = Todo.objects.create(title='game', owner=self.user)
        t2 = Todo.objects.create(title='gym', owner=self.user)
        t3 = Todo.objects.create(title='work', owner=self.user)

        res = self.client.get(TODO_URL,{'titles': f'{t1.title},{t2.title}'})
        serializer1 = serializers.TodoSerializer(t1)
        serializer2 = serializers.TodoSerializer(t2)
        serializer3 = serializers.TodoSerializer(t3)

        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)





