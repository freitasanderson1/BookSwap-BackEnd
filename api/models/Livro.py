from django.db import models
from django.contrib.auth.models import User

CONDICAO_CHOICES = [
    ('novo', 'Novo'),
    ('seminovo', 'Seminovo'),
    ('usado', 'Usado'),
]
class Livro(models.Model):
    titulo = models.CharField(max_length=256)
    autor = models.CharField(max_length=256)
    paginas = models.IntegerField()
    descricao = models.TextField()
    dataPublicacao = models.DateField()
    editora = models.CharField(max_length=256)
    genero = models.CharField(max_length=256)
    capa = models.ImageField(upload_to='capas/',blank=True,null=True)
    dono = models.ForeignKey(User,on_delete=models.CASCADE,related_name='livros')
    condicao = models.CharField(
        max_length=10,
        choices=CONDICAO_CHOICES,
        default='usado'
    )
    
    def __str__(self):
        return f"{self.titulo} - {self.descricao}"
    
    class Meta:
        verbose_name = 'Livro'
        verbose_name_plural = 'Livros'