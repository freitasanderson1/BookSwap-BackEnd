from rest_framework import serializers
from api.models import Perfil
from django.contrib.auth.models import User
from api.serializers import UserSerializer

# Serializer para o Perfil
class PerfilSerializer(serializers.ModelSerializer):
    usuario = UserSerializer(read_only=True)  # Inclui o serializer do usuário
    seguindo = serializers.PrimaryKeyRelatedField(many=True, queryset=Perfil.objects.all())

    class Meta:
        model = Perfil
        fields = ['id', 'usuario', 'image', 'seguindo']


# Serializer para criar/atualizar perfil
class PerfilCreateUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)  # Campo para escrita da senha, opcional
    first_name = serializers.CharField(write_only=True, required=False)  # Campos para o nome
    last_name = serializers.CharField(write_only=True, required=False)
    email = serializers.EmailField(write_only=True, required=False)
    username = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Perfil
        fields = ['id', 'image', 'password', 'first_name', 'last_name', 'email', 'username']  # Inclui os campos do usuário

    def update(self, instance, validated_data):
        # Atualizando a imagem se presente
        image = validated_data.get('image', None)
        if image:
            instance.image = image

        # Atualizando os campos do usuário
        user = instance.usuario  # Pega a instância do usuário associada ao perfil

        # Atualizando o nome, sobrenome, e-mail e nome de usuário
        user.first_name = validated_data.get('first_name', user.first_name)
        user.last_name = validated_data.get('last_name', user.last_name)
        user.email = validated_data.get('email', user.email)
        user.username = validated_data.get('username', user.username)

        # Atualizando a senha, se fornecida
        password = validated_data.get('password', None)
        if password:
            user.set_password(password)  # Gera o hash da nova senha

        # Salvando o usuário e o perfil
        user.save()
        instance.save()

        return instance


# Serializer para busca de perfis
class PerfilSearchSerializer(serializers.ModelSerializer):
    # Inclui os campos de usuário associados ao perfil
    first_name = serializers.CharField(source='usuario.first_name', read_only=True)
    last_name = serializers.CharField(source='usuario.last_name', read_only=True)
    username = serializers.CharField(source='usuario.username', read_only=True)

    class Meta:
        model = Perfil
        fields = ['id', 'first_name', 'last_name', 'username', 'image']  # Inclui os campos necessários para a busca
