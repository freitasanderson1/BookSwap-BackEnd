from rest_framework import serializers
from api.models import Livro

class LivroSerializer(serializers.ModelSerializer):
    dono = serializers.CharField(source='dono.username',read_only=True )
    dataPublicacao = serializers.DateField(format="%d/%m/%Y")
    class Meta:
        model = Livro
        fields = ['url','id','titulo','autor','paginas','descricao','dataPublicacao','editora','capa','dono','condicao','genero']