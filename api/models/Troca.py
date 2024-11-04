from django.db import models
from django.contrib.auth.models import User
from .Perfil import Perfil
from .Livro import Livro

class Troca(models.Model):
    solicitante = models.ForeignKey(Perfil, related_name='trocas_solicitadas', on_delete=models.CASCADE)
    recebedor = models.ForeignKey(Perfil, related_name='trocas_recebidas', on_delete=models.CASCADE)
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    data_troca = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('Pendente', 'Pendente'), ('Aceita', 'Aceita'), ('Concluída', 'Concluída'), ('Cancelada', 'Cancelada')], default='Pendente')
    solicitante_aceitou = models.BooleanField(default=False)
    recebedor_aceitou = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Troca'
        verbose_name_plural = 'Trocas'

    def __str__(self):
        return f"{self.solicitante} trocando {self.livro} com {self.recebedor}"

    def concluir_troca(self):
        if self.solicitante_aceitou and self.recebedor_aceitou:
            self.status = 'Concluída'
            self.livro.disponivel = False  # Supondo que o modelo `Livro` tenha um campo de disponibilidade
            self.livro.save()
            self.solicitante.atualizar_pontuacao(5)  # Exemplo de pontuação
            self.recebedor.atualizar_pontuacao(5)
            self.save()
