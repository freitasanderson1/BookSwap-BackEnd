from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from api.models import ChatRequest

class ConcluirTrocaView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, troca_id):
        try:
            troca = ChatRequest.objects.get(chat__id=troca_id)

            if troca.trocaFeita:
                return Response({'erro': 'A troca já foi concluída por ambas as partes'}, status=400)

            if request.user == troca.usuario or request.user == troca.usuarioDestino:
                troca.trocaFeita = True
                troca.usuario.perfil.atualizar_pontuacao()
                troca.usuarioDestino.perfil.atualizar_pontuacao()
                troca.save()
                return Response({'mensagem': 'Troca concluída por ambas as partes'}, status=200)

            else:
                return Response({'erro': 'Você não tem permissão para concluir esta troca'}, status=403)
        except ChatRequest.DoesNotExist:
            return Response({'erro': 'Troca não encontrada'}, status=404)
