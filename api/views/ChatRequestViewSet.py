from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from api.models import ChatRequest
from api.serializers import ChatRequestSerializer

class ChatRequestViewSet(viewsets.ModelViewSet):
    queryset = ChatRequest.objects.all()
    serializer_class = ChatRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def aceitar(self, request, pk=None):
        """
        Custom action to accept a chat request.
        """
        chat_request = self.get_object()
        if chat_request.aceito:
            return Response({"detail": "Esta solicitação já foi aceita."}, status=status.HTTP_400_BAD_REQUEST)
        
        chat_request.aceito = True
        chat_request.save()
        return Response({"detail": "Solicitação de chat aceita com sucesso."}, status=status.HTTP_200_OK)
