from rest_framework import serializers
from api.models import ChatRequest, Livro
from django.contrib.auth.models import User
from api.serializers import UserSerializer, LivroSerializer

class ChatRequestSerializer(serializers.ModelSerializer):
    usuario = UserSerializer(read_only=True)
    usuarioDestino = UserSerializer(read_only=True)
    livro = LivroSerializer(read_only=True)

    class Meta:
        model = ChatRequest
        fields = '__all__'

    def validate(self, data):
        livro_id = self.initial_data.get('livro')
        if livro_id:
            try:
                livro = Livro.objects.get(id=livro_id)
                if not livro.disponibilidade:
                    raise serializers.ValidationError("Este livro não está disponível para troca.")
            except Livro.DoesNotExist:
                raise serializers.ValidationError("O livro especificado não existe.")
        else:
            raise serializers.ValidationError("O campo 'livro' é obrigatório.")
        
        return data
