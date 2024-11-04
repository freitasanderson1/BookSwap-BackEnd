from rest_framework import serializers
from api.models import Troca, Perfil, Livro

class PerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfil
        fields = ['id', 'usuario', 'nome', 'sobrenome']  # Campos relevantes do perfil

class TrocaSerializer(serializers.ModelSerializer):
    solicitante = PerfilSerializer(read_only=True)
    recebedor = PerfilSerializer(read_only=True)
    livro = serializers.CharField(source='livro.titulo', read_only=True)
    avaliacao_solicitante = serializers.IntegerField(required=False)
    avaliacao_recebedor = serializers.IntegerField(required=False)

    class Meta:
        model = Troca
        fields = [
            'id', 'solicitante', 'recebedor', 'livro', 'data_troca', 'status', 
            'avaliacao_solicitante', 'avaliacao_recebedor', 'avaliado'
        ]
        read_only_fields = ['id', 'data_troca', 'status']  # Remova 'avaliado' de read_only_fields

    def update(self, instance, validated_data):
        """
        Atualiza o status da troca, avaliações e as pontuações dos perfis envolvidos.
        """
        instance.avaliacao_solicitante = validated_data.get('avaliacao_solicitante', instance.avaliacao_solicitante)
        instance.avaliacao_recebedor = validated_data.get('avaliacao_recebedor', instance.avaliacao_recebedor)

        # Atualizar a pontuação dos perfis envolvidos com base nas avaliações
        if instance.avaliacao_solicitante:
            instance.recebedor.atualizar_pontuacao(instance.avaliacao_solicitante)
        if instance.avaliacao_recebedor:
            instance.solicitante.atualizar_pontuacao(instance.avaliacao_recebedor)

        # Marcar troca como avaliada
        instance.avaliado = True
        instance.save()
        return instance