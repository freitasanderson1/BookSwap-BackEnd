from django.db import models
from django.contrib.auth.models import User

from django.db import models

class Troca(models.Model):
    solicitante = models.ForeignKey('Perfil', related_name='trocas_solicitadas', on_delete=models.CASCADE)
    destinatario = models.ForeignKey('Perfil', related_name='trocas_recebidas', on_delete=models.CASCADE)
    livro = models.ForeignKey('Livro', on_delete=models.SET_NULL, null=True)
    data = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('pendente', 'Pendente'), ('aceita', 'Aceita'), ('recusada', 'Recusada')])
    avaliacao = models.PositiveIntegerField(null=True, blank=True)
    pontuacao = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Troca de {self.solicitante} para {self.destinatario}"
    
    def calcular_pontuacao(self):
        """
        Calcula a pontuação com base na avaliação e adiciona ao perfil do destinatário.
        A pontuação é calculada da seguinte forma:
        - 1 ou 2 estrelas: 0 pontos
        - 3 estrelas: 5 pontos
        - 4 estrelas: 20 pontos
        - 5 estrelas: 50 pontos
        """
        if self.avaliacao and 1 <= self.avaliacao <= 5 and self.status == 'aceita':
            if self.avaliacao in [1, 2]:
                pontos = 0
            elif self.avaliacao == 3:
                pontos = 5
            elif self.avaliacao == 4:
                pontos = 20
            elif self.avaliacao == 5:
                pontos = 50

            self.pontuacao = pontos
            self.save()
            self.destinatario.adicionar_pontuacao(pontos)

    def save(self, *args, **kwargs):
        """
        Sobrescreve o método save para alterar a disponibilidade do livro.
        """
        if self.status == 'pendente' and self.livro.disponibilidade:
            # Torna o livro indisponível se a troca está pendente
            self.livro.disponibilidade = False
            self.livro.save()
        elif self.status in ['aceita', 'recusada'] and not self.livro.disponibilidade:
            # Torna o livro disponível novamente se a troca foi concluída (aceita ou recusada)
            self.livro.disponibilidade = True
            self.livro.save()
        super().save(*args, **kwargs)
