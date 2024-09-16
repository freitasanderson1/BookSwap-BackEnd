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
    password = serializers.CharField(write_only=True, required=False)  # Campo para escrita da senha, opcional

    class Meta:
        model = Perfil
        fields = ['id', 'image', 'password']  # Inclui imagem e senha

    def update(self, instance, validated_data):
        # Atualizando a imagem se presente
        image = validated_data.get('image', None)
        if image:
            instance.image = image

        # Atualizando a senha, se fornecida
        password = validated_data.get('password', None)
        print(password)
        if password:
            user = instance.usuario  # Pega a instância do usuário associada ao perfil
            user.set_password(password)  # Gera o hash da nova senha
            user.save()  # Salva o usuário com a nova senha hasheada

        # Salvando a instância do perfil
        instance.save()

        return instance
