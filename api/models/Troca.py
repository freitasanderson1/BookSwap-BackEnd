from django.db import models
from django.contrib.auth.models import User
from .Perfil import Perfil  # Certifique-se de que o caminho para o arquivo Perfil.py esteja correto
from .Livro import Livro  # Importando o modelo Livro, se necessário

class Troca(models.Model):
    solicitante = models.ForeignKey(Perfil, related_name='trocas_solicitadas', on_delete=models.CASCADE)
    recebedor = models.ForeignKey(Perfil, related_name='trocas_recebidas', on_delete=models.CASCADE)
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    data_troca = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('Pendente', 'Pendente'), ('Concluída', 'Concluída'), ('Cancelada', 'Cancelada')], default='Pendente')
    avaliado = models.BooleanField(default=False)
    avaliacao_solicitante = models.PositiveIntegerField(null=True, blank=True)  # Avaliação do recebedor ao solicitante
    avaliacao_recebedor = models.PositiveIntegerField(null=True, blank=True)  # Avaliação do solicitante ao recebedor

    class Meta:
        verbose_name = 'Troca'
        verbose_name_plural = 'Trocas'
    
    def __str__(self):
        return f"{self.solicitante} trocou {self.livro} com {self.recebedor}"

    def concluir_troca(self):
        """
        Método para concluir a troca, atualizar status e marcar o livro como indisponível.
        """
        self.status = 'Concluída'
        self.livro.marcar_como_indisponivel()  # Atualiza a disponibilidade do livro
        self.save()

    def cancelar_troca(self):
        """
        Método para cancelar a troca, atualizar status e deixar o livro disponível.
        """
        self.status = 'Cancelada'
        self.livro.marcar_como_disponivel()  # Atualiza a disponibilidade do livro
        self.save()

    def avaliar_troca(self, solicitante_avaliacao=None, recebedor_avaliacao=None):
        """
        Método para avaliar a troca, tanto pelo solicitante quanto pelo recebedor.
        """
        if solicitante_avaliacao:
            self.avaliacao_solicitante = solicitante_avaliacao
        if recebedor_avaliacao:
            self.avaliacao_recebedor = recebedor_avaliacao
        self.avaliado = True
        self.save()

        # Atualizar pontuação dos perfis envolvidos
        if solicitante_avaliacao:
            self.recebedor.atualizar_pontuacao(solicitante_avaliacao)
        if recebedor_avaliacao:
            self.solicitante.atualizar_pontuacao(recebedor_avaliacao)
        
        # Atualizar a avaliação do livro
        if solicitante_avaliacao:
            self.livro.avaliar_livro(solicitante_avaliacao)