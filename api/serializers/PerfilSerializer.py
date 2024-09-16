from rest_framework import serializers
from api.models import Perfil
from django.contrib.auth.models import User
from api.serializers import UserSerializer

# Serializer para o Perfil
class PerfilSerializer(serializers.ModelSerializer):
    usuario = UserSerializer(read_only=True)  # Inclui o serializer do usuário
    seguindo = serializers.StringRelatedField(many=True, read_only=True)  # Exibe o nome do perfil que está sendo seguido

    class Meta:
        model = Perfil
        fields = ['id', 'usuario', 'image', 'seguindo']

# Serializer para criar/atualizar perfil
class PerfilCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfil
        fields = ['id', 'image', 'seguindo']  # Campos editáveis
