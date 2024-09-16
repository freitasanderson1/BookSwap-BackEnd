from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    usuario = models.OneToOneField(User,verbose_name='Dados perfil',on_delete=models.CASCADE)
    image = models.ImageField(blank=True,upload_to='Perfil')
    seguindo = models.ManyToManyField('Perfil',blank=True)
    
    def __str__(self):
        return f"{self.usuario.get_full_name()}"
    
    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'
    
    
    
    
    