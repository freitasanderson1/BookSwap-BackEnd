import django_filters
from ..models import Livro

class LivroFilter(django_filters.FilterSet):
    titulo = django_filters.CharFilter(field_name='titulo', lookup_expr='icontains')
    condicao = django_filters.CharFilter(field_name='condicao', lookup_expr='exact')
    genero = django_filters.CharFilter(field_name='genero', lookup_expr='exact')
    

    class Meta:
        model = Livro
        fields = ['titulo', 'condicao', 'genero']

    def filter_queryset(self, queryset):
        # Recebe os parâmetros de pesquisa
        search = self.data.get('search', '')

        # Se o campo titulo estiver vazio, não aplica filtro no título
        if search:
            # Filtra pelo título (icontains) ou pela condição (exata)
            queryset = queryset.filter(titulo__icontains=search) | queryset.filter(condicao=search) | queryset.filter(genero=search)
            
        return queryset
