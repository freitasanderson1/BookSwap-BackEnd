from django.db import models
from django.contrib.auth.models import User

class Comentario(models.Model):
    livro = models.ForeignKey('Livro', on_delete=models.CASCADE, related_name='comentarios')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comentário de {self.usuario.username} em {self.livro.titulo}"
