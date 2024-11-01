from rest_framework import serializers
from api.models import Perfil
from django.contrib.auth.models import User
from api.serializers import UserSerializer  # Importa o UserSerializer centralizado que funcionou anteriormente

# Serializer principal para o Perfil

class PerfilSerializer(serializers.ModelSerializer):
    usuario = UserSerializer(read_only=True)
    seguindo = serializers.PrimaryKeyRelatedField(many=True, queryset=Perfil.objects.all())
    pontuacao_total = serializers.IntegerField(read_only=True)
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = Perfil
        fields = ['id', 'usuario', 'image', 'seguindo', 'seguidores', 'criado_em', 'pontuacao_total', 'is_following']

    def get_is_following(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            perfil_autenticado = getattr(request.user, 'perfil', None)
            if perfil_autenticado:
                return perfil_autenticado.esta_seguindo(obj)
        return False

# Serializer para criação/atualização de perfil
class PerfilCreateUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)  
    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)
    email = serializers.EmailField(write_only=True, required=False)
    username = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Perfil
        fields = ['id', 'image', 'password', 'first_name', 'last_name', 'email', 'username']

    def update(self, instance, validated_data):
        # Atualizando a imagem se presente
        image = validated_data.get('image', None)
        if image:
            instance.image = image

        # Atualizando os campos do usuário
        user = instance.usuario

        # Atualizando o nome, sobrenome, e-mail e nome de usuário
        user.first_name = validated_data.get('first_name', user.first_name)
        user.last_name = validated_data.get('last_name', user.last_name)
        user.email = validated_data.get('email', user.email)
        user.username = validated_data.get('username', user.username)

        # Atualizando a senha, se fornecida
        password = validated_data.get('password', None)
        if password:
            user.set_password(password)

        # Salvando o usuário e o perfil
        user.save()
        instance.save()

        return instance


# Serializer para busca de perfis
class PerfilSearchSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='usuario.first_name', read_only=True)
    last_name = serializers.CharField(source='usuario.last_name', read_only=True)
    username = serializers.CharField(source='usuario.username', read_only=True)
    pontuacao_total = serializers.IntegerField(read_only=True)  # Inclui a pontuação total para visualização na busca

    class Meta:
        model = Perfil
        fields = ['id', 'first_name', 'last_name', 'username', 'image', 'pontuacao_total']
