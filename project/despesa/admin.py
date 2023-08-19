from django.contrib import admin

from .models import Categoria, Categoria2, Despesa, Saldo


# class DespesaAdmin(admin.ModelAdmin):
#     list_display = ('nome',)
    
#     fieldsets = (
#         ('Despesa', {
#             'classes': ('grp-collapse grp-closed',),
#             'fields': ('nome',)
#         })
#     )
    
#     search_fields = ('nome',)

# admin.site.register(Despesa, DespesaAdmin)


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria2', 'descricao')
    #...

@admin.register(Categoria2)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao')
    #...

@admin.register(Despesa)
class DespesaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    #...

@admin.register(Saldo)
class SaldoAdmin(admin.ModelAdmin):
    list_display = ('saldo','limite')
    def has_add_permission(self, *args, **kwargs):
        return not Saldo.objects.exists()
    #...
