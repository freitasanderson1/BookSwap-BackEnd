from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from api.models import Livro, Perfil
from api.serializers import LivroSerializer
from api.filters.LivroFilter import LivroFilter

class LivroViewSet(viewsets.ModelViewSet):
    queryset = Livro.objects.all().order_by('-criado_em')
    serializer_class = LivroSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = LivroFilter
    search_fields = ['titulo', 'condicao']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        meus_livros = self.request.query_params.get('meus_livros', None)
        usuario = self.request.query_params.get('usuario', None)
        perfil = self.request.query_params.get('perfil', None)
        disponivel = self.request.query_params.get('disponivel', None)

        # Filtra os livros do próprio usuário autenticado
        if meus_livros and self.request.user.is_authenticated:
            return Livro.objects.filter(dono=self.request.user).order_by('-criado_em')

        # Filtra os livros de um usuário específico (pelo `User`), se o parâmetro 'usuario' for fornecido
        if usuario:
            return Livro.objects.filter(dono__id=usuario).order_by('-criado_em')

        # Filtra os livros de um perfil específico, se o parâmetro 'perfil' for fornecido
        if perfil:
            return Livro.objects.filter(dono__perfil__id=perfil).order_by('-criado_em')

        # Filtra os livros disponíveis, se solicitado
        if disponivel:
            return Livro.objects.filter(disponibilidade=True).order_by('-criado_em')

        # Retorna todos os livros (padrão)
        return super().get_queryset()

    def perform_create(self, serializer):
        # Define o dono do livro como o usuário autenticado
        serializer.save(dono=self.request.user)

    def get_object(self):
        # Garante que apenas o dono pode editar ou deletar o livro
        obj = super().get_object()
        if self.action in ['update', 'partial_update', 'destroy'] and obj.dono != self.request.user:
            raise PermissionDenied("Você não tem permissão para editar este livro.")
        return obj

    @action(detail=True, methods=['post'], url_path='curtir', url_name='curtir')
    def curtir_livro(self, request, pk=None):
        livro = self.get_object()
        perfil = Perfil.objects.get(usuario=request.user)

        if perfil in livro.curtidas.all():
            livro.curtidas.remove(perfil)
            return Response({'status': 'Você descurtiu este livro.'}, status=status.HTTP_200_OK)
        else:
            livro.curtidas.add(perfil)
            return Response({'status': 'Você curtiu este livro.'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'], url_path='alterar-disponibilidade', url_name='alterar_disponibilidade')
    def alterar_disponibilidade(self, request, pk=None):
        # Ação personalizada para alterar a disponibilidade do livro
        livro = self.get_object()
        if livro.dono != request.user:
            raise PermissionDenied("Você não tem permissão para alterar a disponibilidade deste livro.")

        livro.disponibilidade = not livro.disponibilidade
        livro.save()
        return Response({'status': f'Disponibilidade alterada para {"disponível" if livro.disponibilidade else "indisponível"}.'}, status=status.HTTP_200_OK)
