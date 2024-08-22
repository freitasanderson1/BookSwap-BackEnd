from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LivroViewSet, UserViewSet

router = DefaultRouter()
router.register(r'Livros', LivroViewSet)
router.register(r'User', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
