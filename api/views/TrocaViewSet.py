from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from api.models import Troca, Perfil, Livro
from api.serializers import TrocaSerializer

class TrocaViewSet(viewsets.ModelViewSet):
    queryset = Troca.objects.all().order_by('-data')
    serializer_class = TrocaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        perfil_id = self.request.query_params.get('perfil_id')
        if perfil_id:
            # Consulta o histórico de trocas de um perfil específico
            perfil = get_object_or_404(Perfil, id=perfil_id)
            return Troca.objects.filter(solicitante=perfil) | Troca.objects.filter(destinatario=perfil)
        else:
            # Retorna apenas o histórico do usuário logado
            perfil = self.request.user.perfil
            return Troca.objects.filter(solicitante=perfil) | Troca.objects.filter(destinatario=perfil)

    def perform_create(self, serializer):
        solicitante = self.request.user.perfil
        livro_id = self.request.data.get('livro')
        livro = get_object_or_404(Livro, id=livro_id)

        if livro.dono.perfil == solicitante:
            return Response({"detail": "Você não pode trocar um livro que já é seu."}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(solicitante=solicitante, destinatario=livro.dono.perfil, livro=livro)

    @action(detail=True, methods=['post'], url_path='avaliar', url_name='avaliar')
    def avaliar(self, request, pk=None):
        troca = self.get_object()
        if troca.status != 'aceita':
            return Response({"detail": "A troca precisa estar no status 'aceita' para ser avaliada."}, status=status.HTTP_400_BAD_REQUEST)

        avaliacao = request.data.get('avaliacao')
        if avaliacao is None or not (1 <= int(avaliacao) <= 5):
            return Response({"detail": "Avaliação deve estar entre 1 e 5."}, status=status.HTTP_400_BAD_REQUEST)

        troca.avaliacao = avaliacao
        troca.calcular_pontuacao()
        troca.save()
        return Response({"detail": "Troca avaliada com sucesso."}, status=status.HTTP_200_OK)