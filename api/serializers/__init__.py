# Importa todos os serializers relevantes para o sistema, incluindo os necessários para perfis
from .LivroSerializer import LivroSerializer
from .UserSerializer import UserSerializer
from .PerfilSerializer import PerfilSerializer, PerfilCreateUpdateSerializer, PerfilSearchSerializer
from .TrocaSerializer import TrocaSerializer
from .ComentarioSerializer import ComentarioSerializer # Adiciona o serializer para Troca