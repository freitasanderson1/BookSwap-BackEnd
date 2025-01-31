# views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from django.db.models import Q
from api.models import Perfil
from api.serializers import PerfilSerializer, PerfilCreateUpdateSerializer, PerfilSearchSerializer

class PerfilViewSet(viewsets.ModelViewSet):
    queryset = Perfil.objects.all()

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'list' and self.request.query_params.get('search'):
            return PerfilSearchSerializer
        if self.action in ['update', 'partial_update']:
            return PerfilCreateUpdateSerializer
        return PerfilSerializer

    def get_queryset(self):
        queryset = Perfil.objects.all()
        search_query = self.request.query_params.get('search', None)

        if search_query:
            queryset = queryset.filter(
                Q(usuario__first_name__icontains=search_query) |
                Q(usuario__last_name__icontains=search_query) |
                Q(usuario__username__icontains=search_query)
            )
        return queryset

    def get_object(self):
        if self.kwargs.get('pk'):
            return get_object_or_404(Perfil, pk=self.kwargs['pk'])
        queryset = self.get_queryset().filter(usuario=self.request.user)
        return get_object_or_404(queryset)

    def perform_update(self, serializer):
        print("Request FILES: ", self.request.FILES)
        print("Request DATA: ", self.request.data)
        serializer.save()

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated], url_path='seguir')
    def seguir(self, request, pk=None):
        perfil_a_seguir = get_object_or_404(Perfil, pk=pk)
        perfil_autenticado = request.user.perfil

        if perfil_autenticado.esta_seguindo(perfil_a_seguir):
            return Response({'detail': 'Você já está seguindo este perfil.'}, status=status.HTTP_400_BAD_REQUEST)

        perfil_autenticado.seguir(perfil_a_seguir)
        return Response({'detail': 'Agora você está seguindo este perfil.'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['delete'], permission_classes=[IsAuthenticated], url_path='deixar_de_seguir')
    def deixar_de_seguir(self, request, pk=None):
        perfil_para_deixar = get_object_or_404(Perfil, pk=pk)
        perfil_autenticado = request.user.perfil

        if not perfil_autenticado.esta_seguindo(perfil_para_deixar):
            return Response({'detail': 'Você não está seguindo este perfil.'}, status=status.HTTP_400_BAD_REQUEST)

        perfil_autenticado.deixar_de_seguir(perfil_para_deixar)
        return Response({'detail': 'Você deixou de seguir este perfil.'}, status=status.HTTP_200_OK)

    # Histórico de trocas com gamificação (avaliação e pontuação)
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated], url_path='historico-trocas')
    def historico_trocas(self, request, pk=None):
        perfil = get_object_or_404(Perfil, pk=pk)
        trocas = Troca.objects.filter(Q(solicitante=perfil) | Q(recebedor=perfil))
        serializer = TrocaSerializer(trocas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Nova ação para buscar perfil pelo user_id
    @action(detail=False, methods=['get'], url_path='by-user/(?P<user_id>[^/.]+)', permission_classes=[AllowAny])
    def get_profile_by_user_id(self, request, user_id=None):
        perfil = get_object_or_404(Perfil, usuario_id=user_id)
        serializer = self.get_serializer(perfil)
        return Response(serializer.data, status=status.HTTP_200_OK)