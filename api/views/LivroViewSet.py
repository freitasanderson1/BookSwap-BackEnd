from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets, filters, status
from api.models import Livro, Perfil
from rest_framework.decorators import action
from rest_framework.response import Response
from api.serializers import LivroSerializer
from api.filters.LivroFilter import LivroFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

class LivroViewSet(viewsets.ModelViewSet):
    queryset = Livro.objects.all().order_by('-criado_em')
    serializer_class = LivroSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = LivroFilter
    search_fields = ['titulo', 'condicao']

    def get_permissions(self):
        """Customiza as permissões por método"""
        if self.action in ['list', 'retrieve']:  # Se for um GET (listar ou ver um livro), é público
            permission_classes = [AllowAny]
        else:  # Para qualquer outra ação (POST, PUT, DELETE, etc.), exige autenticação
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        # Se um parâmetro "meus_livros" for passado, filtramos para livros do usuário
        meus_livros = self.request.query_params.get('meus_livros', None)
        if meus_livros and self.request.user.is_authenticated:
            return Livro.objects.filter(dono=self.request.user).order_by('-criado_em')
        return super().get_queryset()

    def perform_create(self, serializer):
        # Associa o livro criado ao usuário autenticado
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

    @action(detail=True, methods=['put'], permission_classes=[IsAuthenticated])
    def editar(self, request, pk=None):
        """
        Endpoint para editar um livro.
        """
        livro = get_object_or_404(Livro, pk=pk)
        if livro.dono != request.user:
            return Response({'detail': 'Você não tem permissão para editar este livro.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(livro, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)