from django.contrib import admin

# Register your models here.


from .models import EnderecoEstoque, EstoqueMateriaPrima


@admin.register(EnderecoEstoque)
class EnderecoEstoqueAdmin(admin.ModelAdmin):
    list_display = ["nome"]


@admin.register(EstoqueMateriaPrima)
class EstoqueMateriaPrimaAdmin(admin.ModelAdmin):
    list_display = ["materiaprima", "enderecoestoque", "qtde"]
