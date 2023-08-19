from django.contrib import admin

from .models import Categoria, Receita


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
    list_display = ("nome", "descricao")
    ...


@admin.register(Receita)
class ReceitaAdmin(admin.ModelAdmin):
    list_display = ("nome",)
    ...
