from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from api.models import Troca, Perfil, Livro
from api.serializers import TrocaSerializer

class TrocaViewSet(viewsets.ModelViewSet):
    queryset = Troca.objects.all().order_by('-data_troca')
    serializer_class = TrocaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        perfil_id = self.request.query_params.get('perfil_id')
        if perfil_id:
            perfil = get_object_or_404(Perfil, id=perfil_id)
            return Troca.objects.filter(Q(solicitante=perfil) | Q(recebedor=perfil))
        else:
            perfil = self.request.user.perfil
            return Troca.objects.filter(Q(solicitante=perfil) | Q(recebedor=perfil))

    def perform_create(self, serializer):
        solicitante = self.request.user.perfil
        livro_id = self.request.data.get('livro')
        livro = get_object_or_404(Livro, id=livro_id)

        if livro.dono.perfil == solicitante:
            return Response({"detail": "Você não pode trocar um livro que já é seu."}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(solicitante=solicitante, recebedor=livro.dono.perfil, livro=livro)

    @action(detail=True, methods=['post'], url_path='avaliar', permission_classes=[IsAuthenticated])
    def avaliar(self, request, pk=None):
        """
        Endpoint para avaliar uma troca.
        """
        troca = self.get_object()

        if troca.status != 'Concluída':
            return Response({"detail": "A troca deve ser concluída para ser avaliada."}, status=status.HTTP_400_BAD_REQUEST)

        avaliacao_solicitante = request.data.get('avaliacao_solicitante')
        avaliacao_recebedor = request.data.get('avaliacao_recebedor')

        if avaliacao_solicitante is not None:
            troca.avaliacao_solicitante = avaliacao_solicitante
            troca.recebedor.atualizar_pontuacao(avaliacao_solicitante)

        if avaliacao_recebedor is not None:
            troca.avaliacao_recebedor = avaliacao_recebedor
            troca.solicitante.atualizar_pontuacao(avaliacao_recebedor)

        troca.avaliado = True
        troca.save()

        return Response({"detail": "Troca avaliada com sucesso."}, status=status.HTTP_200_OK)