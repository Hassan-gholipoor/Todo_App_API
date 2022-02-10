from rest_framework import viewsets, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status

from core.serializers import TodoSerializer, TodoDetailSerializer
from core.models import Todo

class TodoApiViewSet(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Todo.objects.all()
    
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user).order_by('-title')

    def get_serializer_class(self, *args, **kwargs):
        if self.action == 'retrieve':
            return TodoDetailSerializer
        
        return self.serializer_class

    def create(self, request):
        data = request.POST.copy()
        data['owner'] = self.request.user.pk
        serializer = TodoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
