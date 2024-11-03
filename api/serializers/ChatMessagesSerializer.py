from rest_framework import serializers
from api.models import ChatMessages

class ChatMessagesSerializer(serializers.ModelSerializer):

  class Meta:
    model = ChatMessages
    fields = ['id', 'conteudo', 'quemEnviou', 'quemRecebeu', 'quemLeu', 'dataEnvio']