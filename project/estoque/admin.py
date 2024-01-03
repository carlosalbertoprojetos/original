from django.contrib import admin

from .models import EnderecoEstoque, EstoqueMateriaPrima, EstoquePecaAcabada


@admin.register(EnderecoEstoque)
class EnderecoEstoqueAdmin(admin.ModelAdmin):
    list_display = ["nome"]


@admin.register(EstoqueMateriaPrima)
class EstoqueMateriaPrimaAdmin(admin.ModelAdmin):
    list_display = ["materiaprima", "enderecoestoque", "qtde"]


@admin.register(EstoquePecaAcabada)
class EstoquePecaAcabadaAdmin(admin.ModelAdmin):
    ...
