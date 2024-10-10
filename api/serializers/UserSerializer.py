from django.contrib.auth.models import User
from api.models import Perfil
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'id', 'first_name', 'last_name', 'username', 'password', 'email', 'last_login', 'date_joined')
        extra_kwargs = {
            'password': {'write_only':True}
        }
        
    def create(self, validated_data):
        user = User(
            username = validated_data['username'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            email = validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        perfil = Perfil(
            usuario = user,
        )
        perfil.save()
        return user