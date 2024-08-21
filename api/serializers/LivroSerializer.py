from rest_framework import serializers
from api.models import Livro

class LivroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Livro
        fields = ['id', 'titulo', 'autor', 'paginas', 'descricao', 'dataPublicacao', 'editora', 'capa', 'dono']