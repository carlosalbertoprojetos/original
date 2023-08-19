from django.contrib import admin


from .models import CompraMateriaPrima, Compra

"""
@admin.register(UnidadeMedida)
class UnidadeMedidaAdmin(admin.ModelAdmin):
    list_display = ('nome','abreviacao')

"""    
"""

@admin.register(CompraMateriaPrima)
class MateriaPrimaAdmin(admin.ModelAdmin):
    list_display = ('nome','fornecedor', 'uni_med','descrição', 'detalhes')
    fieldsets = [
        ('Fornecedor',{
            'fields':
                ('fornecedor',)
        }),
        ('Material',{
            'fields':
                (('nome', 'uni_med'))
        }), 
        ('Descrição',{
            'fields':
                ('descrição','detalhes',)
        }),
    ]
    list_filter = ['nome', 'fornecedor', 'uni_med', 'descrição']
    search_fields = ['nome', 'fornecedor', 'uni_med', 'descrição']
    ordering = ('nome',)

    from django.contrib import admin


@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ('fornecedor', 'data', 'opcao', 'num_parcelas', 'total')
    fieldsets = [
        ('Fornecedor',{
            'fields':
                ('fornecedor',('data', 'opcao'),)
        }), 
        ('Custos',{
            'fields':
                (('num_parcelas','total'),)
        }),
    ]
    readonly_fields = ('num_parcelas', 'total',)
    inlines = [
        MateriaPrimaAdmin,
    ]
    ordering = ('data',) 
    search_fields = ['fornecedor', 'data', 'opcao', 'criadoem']
    list_filter = ['fornecedor', 'data', 'opcao', 'criadoem']
    ...
 """