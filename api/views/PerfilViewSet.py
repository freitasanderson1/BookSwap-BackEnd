from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from api.models import Perfil
from api.serializers import PerfilSerializer, PerfilCreateUpdateSerializer

class PerfilViewSet(viewsets.ModelViewSet):
    queryset = Perfil.objects.all()  # Define um queryset genérico
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Retorna apenas o perfil do usuário autenticado
        return Perfil.objects.filter(usuario=self.request.user)

    def get_serializer_class(self):
        # Usa um serializer diferente para create, update, partial_update
        if self.action in ['update', 'partial_update']:
            return PerfilCreateUpdateSerializer
        return PerfilSerializer

    def get_object(self):
        # Usa get_object_or_404 para retornar o perfil do usuário autenticado
        queryset = self.get_queryset()
        # Garante que existe apenas um perfil por usuário
        return get_object_or_404(queryset)

    def perform_update(self, serializer):
        # Lida com a atualização, incluindo a possibilidade de alterar a senha
        serializer.save()
