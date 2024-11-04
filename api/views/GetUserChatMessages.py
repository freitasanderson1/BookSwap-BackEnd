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
        data = Chat.objects.filter(usuarios=request.user)
        messages = ChatSerializer(data, many=True).data[0] if data else None
        return Response(messages)
    
    def retrieve(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        data = Chat.objects.filter(id=id)
        messages = ChatSerializer(data, many=True).data[0] if data else None
        return Response(messages)
    def create(self, request, *args, **kwargs):
        # Método de criação de mensagens não permitido nesta view
        return Response({'mensagem': 'Não permitido!'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        # Método de destruição não permitido nesta view
        return Response({'mensagem': 'Não permitido!'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
