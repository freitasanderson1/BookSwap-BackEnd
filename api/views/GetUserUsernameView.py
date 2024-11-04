from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from api.models import ChatRequest

from django.db.models import Q
class GetUserUsernameView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        chatReceiver = ChatRequest.objects.filter(Q(usuario=request.user)|Q(usuarioDestino=request.user), aceito=True, trocaFeita=False).last().usuarioDestino.username
        content = {'username': request.user.username, 'receiver': chatReceiver}
        return Response(content)
