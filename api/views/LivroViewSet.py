from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from api.models import Livro
from api.serializers import LivroSerializer

class LivroViewSet(viewsets.ModelViewSet):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer

