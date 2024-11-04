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
    capa = models.ImageField(upload_to='capas/', blank=True, null=True)
    dono = models.ForeignKey(User, on_delete=models.CASCADE, related_name='livros')
    condicao = models.CharField(
        max_length=10,
        choices=CONDICAO_CHOICES,
        default='usado'
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    resenha = models.TextField(null=True, blank=True)
    curtidas = models.ManyToManyField('Perfil', related_name='livros_curtidos', blank=True)  # Campo de curtidas
    disponibilidade = models.BooleanField(default=True)
    media_avaliacoes = models.FloatField(default=0.0)  # Campo para armazenar a média das avaliações do livro
    total_avaliacoes = models.PositiveIntegerField(default=0)  # Campo para armazenar o número total de avaliações
    
    def __str__(self):
        return f"{self.titulo} - {self.descricao}"

    class Meta:
        verbose_name = 'Livro'
        verbose_name_plural = 'Livros'

    def avaliar_livro(self, avaliacao):
        """
        Método para avaliar o livro.
        """
        total = self.total_avaliacoes + 1
        nova_media = ((self.media_avaliacoes * self.total_avaliacoes) + avaliacao) / total
        self.media_avaliacoes = nova_media
        self.total_avaliacoes = total
        self.save()

    def marcar_como_indisponivel(self):
        """
        Método para marcar o livro como indisponível para troca.
        """
        self.disponibilidade = False
        self.save()

    def marcar_como_disponivel(self):
        """
        Método para marcar o livro como disponível para troca.
        """
        self.disponibilidade = True
        self.save()