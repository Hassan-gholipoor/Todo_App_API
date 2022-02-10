from rest_framework import serializers
from core.models import Todo
from user.serializers import UserSerializer


class TodoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Todo
        fields = ('id', 'title', 'description', 'start_time', 'end_time', 'owner')
        read_only_fields = ('id',)


class TodoDetailSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    
    class Meta:
        model = Todo
        fields = ('id', 'title', 'description', 'start_time', 'end_time', 'owner')
        read_only_fields = ('id',)