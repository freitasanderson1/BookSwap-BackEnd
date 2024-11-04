import json
from channels.generic.websocket import AsyncWebsocketConsumer
from urllib.parse import parse_qs
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.username = parse_qs(self.scope['query_string'].decode('utf8')).get('username')[-1]
        print(f"USERNAME: {self.username}")

        self.room_group_name = f'chat_{self.username}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        from api.models import Chat, ChatMessages  # Importação movida para dentro da função
        from django.contrib.auth.models import User
        
        text_data_json = json.loads(text_data)
        chat_id = text_data_json.get('chat')
        message = text_data_json.get('message')

        if not chat_id:
            await self.send(text_data=json.dumps({
                'error': 'ID do chat não fornecido.'
            }))
            return

        try:
            chat = await Chat.objects.aget(id=chat_id)
        except Chat.DoesNotExist:
            await self.send(text_data=json.dumps({
                'error': 'Chat não encontrado.'
            }))
            return

        user = await User.objects.aget(username=self.username)

        novaMensagem = ChatMessages(
            chat=chat,
            quemEnviou=user,
            conteudo=message
        )
        await sync_to_async(novaMensagem.save)()

        for usuario in await sync_to_async(list)(chat.usuarios.all()):
            await self.channel_layer.group_send(
                f'chat_{usuario.username}',
                {
                    'type': 'chat_message',
                    'chatId': str(chat.id),  # Inclui o chatId nas mensagens enviadas
                    'message': message,
                    'time': novaMensagem.dataEnvio.strftime("%Y-%m-%d %H:%M:%S"),
                    'sender_username': self.username,
                }
            )
            if usuario != user:
                await sync_to_async(novaMensagem.quemRecebeu.add)(usuario)

    async def chat_message(self, event):
        chat_id = event['chatId']  # Recebe o chatId
        message = event['message']
        sender_username = event['sender_username']
        time = event['time']

        await self.send(text_data=json.dumps({
            'chatId': chat_id,  # Inclui o chatId na mensagem enviada
            'message': message,
            'sender_username': sender_username,
            'time': time,
        }))
