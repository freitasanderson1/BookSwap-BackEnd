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
        
    def seguir(self,perfil):
        self.seguindo.add(perfil)
        
    def deixar_de_seguir(self,perfil):
        self.seguindo.remove(perfil)
        
    def esta_seguindo(self,perfil):
        return self.seguindo.filter(id=perfil.id).exists()
    
    
    
    
    