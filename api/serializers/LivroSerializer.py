from rest_framework import serializers
from api.models import Livro
from datetime import datetime

class LivroSerializer(serializers.ModelSerializer):
    dono = serializers.CharField(source='dono.username', read_only=True)
    perfil_id = serializers.IntegerField(source='dono.perfil.id', read_only=True)  # Access the related Perfil's ID
    dataPublicacao = serializers.DateField(format="%d/%m/%Y", input_formats=['%d-%m-%Y', '%d/%m/%Y'])
    disponibilidade = serializers.BooleanField(read_only=True)  # Campo para mostrar se o livro está disponível

    class Meta:
        model = Livro
        fields = ['url', 'id', 'titulo', 'autor', 'paginas', 'descricao', 'dataPublicacao', 'editora', 'capa', 'dono', 'perfil_id', 'condicao', 'genero', 'resenha', 'curtidas', 'disponibilidade']
