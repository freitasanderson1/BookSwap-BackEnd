from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets, status
from api.models import Comentario, Livro
from rest_framework.response import Response
from api.serializers import ComentarioSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import NotFound

class ComentarioViewSet(viewsets.ModelViewSet):
    queryset = Comentario.objects.all().order_by('-criado_em')
    serializer_class = ComentarioSerializer
    filter_backends = [DjangoFilterBackend]

    def get_permissions(self):
        """Customiza as permissões por método"""
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        # Filtro para retornar apenas comentários de um livro específico
        livro_id = self.request.query_params.get('livro', None)
        if livro_id:
            return Comentario.objects.filter(livro__id=livro_id).order_by('-criado_em')
        return super().get_queryset()

    def perform_create(self, serializer):
        # Pega o ID do livro a partir do campo 'livro' enviado pelo frontend
        livro_id = self.request.data.get('livro')  # Use 'livro' para alinhar com o frontend
        try:
            livro = Livro.objects.get(id=livro_id)
        except Livro.DoesNotExist:
            raise NotFound("Livro não encontrado.")
        
        # Associa o comentário ao usuário logado e ao livro
        serializer.save(usuario=self.request.user, livro=livro)
