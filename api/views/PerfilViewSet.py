from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from django.db.models import Q  # Para consultas complexas (OR)
from api.models import Perfil, Troca  # Certifique-se de importar 'Troca' junto com 'Perfil'
from api.serializers.PerfilSerializer import PerfilSerializer, PerfilCreateUpdateSerializer, PerfilSearchSerializer
from api.serializers import TrocaSerializer  # Certifique-se de importar o TrocaSerializer

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from django.db.models import Q
from api.models import Perfil, Troca
from api.serializers.PerfilSerializer import PerfilSerializer, PerfilCreateUpdateSerializer, PerfilSearchSerializer
from api.serializers import TrocaSerializer

class PerfilViewSet(viewsets.ModelViewSet):
    queryset = Perfil.objects.all()  # Define o queryset padrão

    def get_permissions(self):
        # Permitir busca sem autenticação, exigir autenticação para o restante
        if self.action == 'list':
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def get_serializer_class(self):
        # Use um serializer diferente para 'update', 'partial_update' e para busca
        if self.action == 'list' and self.request.query_params.get('search'):
            return PerfilSearchSerializer
        if self.action in ['update', 'partial_update']:
            return PerfilCreateUpdateSerializer
        return PerfilSerializer

    def get_queryset(self):
        queryset = Perfil.objects.all()
        search_query = self.request.query_params.get('search', None)

        # Se houver uma query de busca, filtra pelo nome, sobrenome ou username
        if search_query:
            queryset = queryset.filter(
                Q(usuario__first_name__icontains=search_query) |
                Q(usuario__last_name__icontains=search_query) |
                Q(usuario__username__icontains=search_query)
            )
        return queryset

    def get_object(self):
        # Retorna o perfil com base no ID fornecido na URL, se disponível
        if self.kwargs.get('pk'):
            return get_object_or_404(Perfil, pk=self.kwargs['pk'])
        # Se nenhum 'pk' for fornecido, retorna o perfil do usuário autenticado
        queryset = self.get_queryset().filter(usuario=self.request.user)
        return get_object_or_404(queryset)

    def perform_update(self, serializer):
        # Log para verificar o que está sendo enviado
        print("Request FILES: ", self.request.FILES)
        print("Request DATA: ", self.request.data)

        # Salvar o perfil e a imagem
        serializer.save()

    # Seguir perfil
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated], url_path='seguir')
    def seguir(self, request, pk=None):
        perfil_a_seguir = get_object_or_404(Perfil, pk=pk)
        perfil_autenticado = request.user.perfil

        if perfil_autenticado.esta_seguindo(perfil_a_seguir):
            return Response({'detail': 'Você já está seguindo este perfil.'}, status=status.HTTP_400_BAD_REQUEST)

        perfil_autenticado.seguir(perfil_a_seguir)
        return Response({'detail': 'Agora você está seguindo este perfil.'}, status=status.HTTP_200_OK)

    # Deixar de seguir perfil
    @action(detail=True, methods=['delete'], permission_classes=[IsAuthenticated], url_path='deixar_de_seguir')
    def deixar_de_seguir(self, request, pk=None):
        perfil_para_deixar = get_object_or_404(Perfil, pk=pk)
        perfil_autenticado = request.user.perfil

        if not perfil_autenticado.esta_seguindo(perfil_para_deixar):
            return Response({'detail': 'Você não está seguindo este perfil.'}, status=status.HTTP_400_BAD_REQUEST)

        perfil_autenticado.deixar_de_seguir(perfil_para_deixar)
        return Response({'detail': 'Você deixou de seguir este perfil.'}, status=status.HTTP_200_OK)

    # Histórico de trocas
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated], url_path='historico-trocas')
    def historico_trocas(self, request, pk=None):
        perfil = self.get_object()
        trocas = Troca.objects.filter(Q(solicitante=perfil) | Q(destinatario=perfil))
        serializer = TrocaSerializer(trocas, many=True)
        return Response(serializer.data)
