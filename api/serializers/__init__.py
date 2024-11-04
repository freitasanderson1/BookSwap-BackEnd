# Importa todos os serializers relevantes para o sistema, incluindo os necessários para perfis
from .LivroSerializer import LivroSerializer
from .UserSerializer import UserSerializer
from .ComentarioSerializer import ComentarioSerializer # Adiciona o serializer para Troca
from .PerfilSerializer import PerfilSerializer, PerfilCreateUpdateSerializer, PerfilSearchSerializer  # Adiciona o PerfilSearchSerializer para busca de perfis
from .ComentarioSerializer import ComentarioSerializer
from .ChatMessagesSerializer import ChatMessagesSerializer
from .ChatSerializer import ChatSerializer
from .ChatRequestSerializer import ChatRequestSerializer