from django.contrib.auth.models import User
from rest_framework import permissions, viewsets, filters
from api.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]  # Permite que qualquer um veja a lista de usuários
   
    # Adiciona o filtro de pesquisa
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'first_name', 'last_name']  # Campos que podem ser pesquisados