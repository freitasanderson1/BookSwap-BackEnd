from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from api.models import ChatRequest, Livro
from django.contrib.auth.models import User
from api.serializers import ChatRequestSerializer

class ChatRequestViewSet(viewsets.ModelViewSet):
    queryset = ChatRequest.objects.select_related('livro', 'usuario', 'usuarioDestino').all()
    serializer_class = ChatRequestSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['usuario'] = request.user.id

        # Verifica se o usuário já enviou uma solicitação para o mesmo livro
        if ChatRequest.objects.filter(usuario=request.user, livro_id=data['livro']).exists():
            return Response({'error': 'Você já enviou uma solicitação para este livro.'}, status=status.HTTP_400_BAD_REQUEST)

        if 'livro' not in data:
            return Response({'error': 'O campo livro é obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            livro = Livro.objects.get(id=data['livro'])
        except Livro.DoesNotExist:
            return Response({'error': 'O livro especificado não existe.'}, status=status.HTTP_400_BAD_REQUEST)

        if 'usuarioDestino' not in data:
            return Response({'error': 'O campo usuarioDestino é obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            usuario_destino = User.objects.get(id=data['usuarioDestino'])
        except User.DoesNotExist:
            return Response({'error': 'O usuário de destino especificado não existe.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(usuario=request.user, usuarioDestino=usuario_destino, livro=livro)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Verifica se o usuário tem permissão para atualizar a solicitação
        if instance.usuarioDestino != request.user:
            return Response({'error': 'Você não tem permissão para atualizar esta solicitação.'}, status=status.HTTP_403_FORBIDDEN)

        # Atualiza o estado da solicitação
        data = request.data
        aceito = data.get('aceito', instance.aceito)

        if aceito:
            instance.aceito = True
            instance.save()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            # Exclui a solicitação se for rejeitada
            instance.delete()
            return Response({'message': 'Solicitação rejeitada e excluída com sucesso.'}, status=status.HTTP_204_NO_CONTENT)
