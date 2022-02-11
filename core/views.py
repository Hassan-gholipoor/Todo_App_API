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

    def _params_to_str(self, qs):
        return [str(title) for title in qs.split(',')]
    
    def get_queryset(self):
        titles = self.request.query_params.get('titles')
        queryset = self.queryset
        if titles:
            title_to_str = self._params_to_str(titles)
            queryset = queryset.filter(title__in=title_to_str).order_by('-title')

        return queryset.filter(owner=self.request.user).order_by('-title')

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
