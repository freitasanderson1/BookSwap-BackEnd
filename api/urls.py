from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LivroViewSet, UserViewSet, PerfilViewSet, ComentarioViewSet, GetUserChatMessages, ChatRequestViewSet, GetUserUsernameView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Criação do roteador para ViewSets
router = DefaultRouter()
router.register(r'livro', LivroViewSet)
router.register(r'usuario', UserViewSet)
router.register(r'perfil', PerfilViewSet)
router.register(r'comentario', ComentarioViewSet)  
router.register(r'api/UserMessages',GetUserChatMessages, basename='GetUserMessages')
router.register(r'chat-requests', ChatRequestViewSet, basename='chat-request')  # Registre o ChatRequestViewSet
# Definição das URLs
urlpatterns = [
    path('', include(router.urls)),  # Inclui as rotas dos ViewSets
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login com JWT
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh do token JWT
    path('get-username/', GetUserUsernameView.as_view(), name='get-username'),
]
