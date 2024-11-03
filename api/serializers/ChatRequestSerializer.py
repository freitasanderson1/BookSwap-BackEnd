from rest_framework import serializers
from api.models import ChatRequest

class ChatRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRequest
        fields = '__all__'

    def validate(self, data):
        if not data['livro'].available:
            raise serializers.ValidationError("Este livro não está disponível para troca.")
        return data
