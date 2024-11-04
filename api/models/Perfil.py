from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    usuario = models.OneToOneField(User, verbose_name='Dados perfil', on_delete=models.CASCADE)
    image = models.ImageField(blank=True, upload_to='Perfil')
    seguindo = models.ManyToManyField('Perfil', blank=True, related_name='Seguindo')
    seguidores = models.ManyToManyField('Perfil', blank=True, related_name='Seguidores')
    criado_em = models.DateTimeField(auto_now_add=True)
    pontuacao = models.IntegerField(default=0)  # Campo para armazenar a pontuação do usuário

    def __str__(self):
        return f"{self.usuario.get_full_name()}"

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'

    def seguir(self, perfil):
        if self.id == perfil.id:
            raise ValueError("Você não pode seguir a si mesmo")
        self.seguindo.add(perfil)
        perfil.seguidores.add(self)

    def deixar_de_seguir(self, perfil):
        self.seguindo.remove(perfil)
        perfil.seguidores.remove(self)

    def esta_seguindo(self, perfil):
        return self.seguindo.filter(id=perfil.id).exists()

    def atualizar_pontuacao(self):
        """
        Método para atualizar a pontuação do perfil com base na avaliação recebida.
        """
        self.pontuacao += 1
        self.save()