from rest_framework import viewsets
from api.models import Perfil
from api.serializers import PerfilSerializer, PerfilCreateUpdateSerializer
from rest_framework.permissions import IsAuthenticated

class PerfilViewSet(viewsets.ModelViewSet):
    queryset = Perfil.objects.all()  # Define um queryset genérico
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Retorna apenas o perfil do usuário autenticado
        return Perfil.objects.filter(usuario=self.request.user)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return PerfilCreateUpdateSerializer
        return PerfilSerializer

    def get_object(self):
        # Retorna o perfil do usuário autenticado
        queryset = self.get_queryset()
        return queryset.get()

    def perform_create(self, serializer):
        # Associa o perfil ao usuário logado ao criar um novo perfil
        serializer.save(usuario=self.request.user)

