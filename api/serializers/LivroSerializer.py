from rest_framework import serializers
from api.models import Livro

class LivroSerializer(serializers.ModelSerializer):
    dono = serializers.CharField(source='dono.username',read_only=True )
    dataPublicacao = serializers.DateField(format="%d/%m/%Y")
    perfil_id = serializers.IntegerField(source='dono.perfil.id', read_only=True)  # Access the related Perfil's ID
    class Meta:
        model = Livro
        fields = ['url','id','titulo','autor','paginas','descricao','dataPublicacao','editora','capa','dono','perfil_id','condicao','genero','resenha']