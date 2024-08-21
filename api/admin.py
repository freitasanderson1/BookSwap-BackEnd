from django.contrib import admin
from api.models import Livro

@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    ...
