from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core import views


router = DefaultRouter()
router.register('todo', views.TodoApiViewSet)

app_name = 'todo'

urlpatterns = [
    path('', include(router.urls)),
]
