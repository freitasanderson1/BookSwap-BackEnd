from rest_framework import serializers
from api.models import Chat
from api.serializers import ChatMessagesSerializer

class ChatSerializer(serializers.ModelSerializer):
  mensagens = ChatMessagesSerializer(source='chatmessages_set', many=True)

  class Meta:
    model = Chat
    fields = '__all__'