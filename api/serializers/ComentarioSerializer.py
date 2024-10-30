from rest_framework import serializers
from api.models import Comentario

class ComentarioSerializer(serializers.ModelSerializer):
    usuario = serializers.CharField(source='usuario.username', read_only=True)

    class Meta:
        model = Comentario
        fields = ['id', 'livro', 'usuario', 'texto', 'criado_em']
        read_only_fields = ['id', 'usuario', 'criado_em']
