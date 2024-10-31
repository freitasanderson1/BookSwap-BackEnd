from rest_framework import serializers
from api.models import Troca, Perfil

class PerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfil
        fields = ['id', 'usuario', 'nome', 'sobrenome']  # Campos relevantes do perfil

class TrocaSerializer(serializers.ModelSerializer):
    solicitante = PerfilSerializer(read_only=True)
    destinatario = PerfilSerializer(read_only=True)
    livro = serializers.CharField(source='livro.titulo', read_only=True)

    class Meta:
        model = Troca
        fields = ['id', 'solicitante', 'destinatario', 'livro', 'data', 'status', 'avaliacao', 'pontuacao']
        read_only_fields = ['id', 'data', 'pontuacao']