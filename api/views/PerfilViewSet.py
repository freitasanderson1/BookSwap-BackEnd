from rest_framework import viewsets
from api.models import Perfil
from api.serializers import PerfilSerializer, PerfilCreateUpdateSerializer
from rest_framework.permissions import IsAuthenticated

class PerfilViewSet(viewsets.ModelViewSet):
    queryset = Perfil.objects.all()  # Adiciona o queryset diretamente aqui
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Retorna apenas o perfil do usuário autenticado
        return Perfil.objects.filter(usuario=self.request.user)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return PerfilCreateUpdateSerializer
        return PerfilSerializer

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)  # Associa o perfil ao usuário logado
