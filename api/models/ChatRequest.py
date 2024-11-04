from django.db import models
import uuid
from api.models import Chat, Livro
from django.contrib.auth.models import User


class ChatRequest(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

  usuario = models.ForeignKey(User, related_name='usuario_solicitante', verbose_name="Usuário que solicitou o Chat", on_delete=models.PROTECT)
  usuarioDestino = models.ForeignKey(User, related_name='usuario_alvo', verbose_name="Usuário alvo do Chat", on_delete=models.PROTECT)
  livro = models.ForeignKey(Livro, on_delete=models.PROTECT, verbose_name="Livro Solicitado")  # Novo campo de livro
  chat = models.ForeignKey(Chat, verbose_name="Chat", on_delete=models.SET_NULL, null=True, blank=True)
  mensagem = models.TextField(u'Conteúdo da Mensagem de solicitação', max_length=300, null=False, blank=False, default=' ')
  
  aceito = models.BooleanField(verbose_name='Aceitou a solicitação?', default=False)
  trocaFeita = models.BooleanField(verbose_name='Troca foi realizada?', default=False)

  dataCriacao = models.DateTimeField('Data de Criação', auto_now_add=True, null=True)

  class Meta:
    verbose_name = 'Solicitação de Chat'
    verbose_name_plural = 'Solicitações de Chats'
    ordering = ['dataCriacao']

  def save(self, *args, **kwargs):
      if self.aceito and not self.chat:
          novoChat = Chat.objects.create()  # Cria e salva a instância de Chat
          novoChat.usuarios.add(self.usuario)
          novoChat.usuarios.add(self.usuarioDestino)

          # Atribui a instância de Chat à solicitação
          self.chat = novoChat

      super(ChatRequest, self).save(*args, **kwargs)
          
  def __str__(self):
    return f'Solicitação de conversa entre {self.usuario.username} e {self.usuarioDestino.username}'