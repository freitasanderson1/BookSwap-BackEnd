from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets,filters
from api.models import Livro
from api.serializers import LivroSerializer

class LivroViewSet(viewsets.ModelViewSet):
    queryset = Livro.objects.all().order_by('-criado_em')
    serializer_class = LivroSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['titulo']

    def get_permissions(self):
        """Customiza as permissões por método"""
        if self.action in ['list', 'retrieve']:  # Se for um GET (listar ou ver um livro), é público
            permission_classes = [AllowAny]
        else:  # Para qualquer outra ação (POST, PUT, DELETE, etc.), exige autenticação
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(dono=self.request.user)