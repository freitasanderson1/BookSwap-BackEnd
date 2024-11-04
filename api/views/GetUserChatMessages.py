from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from api.models import Chat, ChatMessages
from api.serializers import ChatSerializer, ChatMessagesSerializer

class GetUserChatMessages(viewsets.ViewSet, APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        # Lista todos os chats em que o usuário está envolvido
        chats = Chat.objects.filter(usuarios=request.user)
        serializer = ChatSerializer(chats, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        # Recupera mensagens de um chat específico
        try:
            chat = Chat.objects.get(id=pk, usuarios=request.user)
            messages = ChatMessages.objects.filter(chat=chat).order_by('dataEnvio')
            serializer = ChatMessagesSerializer(messages, many=True)
            return Response(serializer.data)
        except Chat.DoesNotExist:
            return Response({'error': 'Chat não encontrado ou você não tem permissão.'}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        # Método de criação de mensagens não permitido nesta view
        return Response({'mensagem': 'Não permitido!'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        # Método de destruição não permitido nesta view
        return Response({'mensagem': 'Não permitido!'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
