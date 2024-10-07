from django.contrib.auth.models import User
from api.models import Perfil
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()  # Adiciona um campo para a imagem de perfil


    class Meta:
        model = User
        fields = ['url', 'id', 'first_name', 'last_name', 'username', 'password', 'email', 'last_login', 'date_joined', 'image']
        extra_kwargs = {
            'password': {'write_only': True}
        }


    def get_image(self, obj):
        # Obtém o perfil do usuário e retorna a URL da imagem, se existir
        try:
            perfil = Perfil.objects.get(usuario=obj)
            if perfil.image:
                request = self.context.get('request')
                return request.build_absolute_uri(perfil.image.url) if request else perfil.image.url
            return None
        except Perfil.DoesNotExist:
            return None


    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()


        # Cria o perfil associado ao usuário
        perfil = Perfil(
            usuario=user,
        )
        perfil.save()
        return user