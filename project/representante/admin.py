from django.contrib import admin

from .models import (
    Regiao,
    Cidade,
    Representante,
    DadosBancarios,
    ServicoRepresentante,
)


# class CidadeInline(admin.StackedInline):
#     model = Regiao.cidade.through
#     extra = 1
#     verbose_name_plural = "Cidades da Região"
# classes = ["collapse"]


@admin.register(Cidade)
class CidadeAdmin(admin.ModelAdmin):
    pass


@admin.register(Regiao)
class RegiaoAdmin(admin.ModelAdmin):
    list_display = ["__str__"]
    search_fields = ("nome", "cidade")
    # ...
    # inlines = [
    #     CidadeInline,
    # ]
    # exclude = [
    #     "cidade",
    # ]
    ...


@admin.register(Representante)
class RepresentanteAdmin(admin.ModelAdmin):
    ...


@admin.register(DadosBancarios)
class DadosBancariosAdmin(admin.ModelAdmin):
    ...


@admin.register(ServicoRepresentante)
class ServicoRepresentanteAdmin(admin.ModelAdmin):
    ...
