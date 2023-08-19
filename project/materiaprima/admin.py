from django.contrib import admin


from .models import UnidadeMedida, MateriaPrima, MateriaPrimaFornecedor


@admin.register(UnidadeMedida)
class UnidadeMedidaAdmin(admin.ModelAdmin):
    list_display = ('nome','descricao')


@admin.register(MateriaPrima)
class MateriaPrimaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'uni_med', 'descricao')
    fieldsets = [
        ('Material',{
            'fields':
                (('nome', 'uni_med'))
        }), 
        ('Descrição',{
            'fields':
                ('descricao',)
        }),
    ]
    list_filter = ['nome', 'uni_med', 'descricao']
    search_fields = ['nome', 'uni_med', 'descricao']
    ordering = ('nome',)


@admin.register(MateriaPrimaFornecedor)
class MateriaPrimaFornecedorAdmin(admin.ModelAdmin):
    list_display = ('materiaprima', 'nome','codigoproduto', 'fornecedor')
