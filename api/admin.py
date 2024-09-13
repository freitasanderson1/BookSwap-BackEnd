from django.contrib import admin
from api.models import Livro, Perfil


@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    icon_name = 'book'

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    icon_name = 'person_pin'
    search_fields = ['usuario']
    autocomplete_fields = ['seguindo']