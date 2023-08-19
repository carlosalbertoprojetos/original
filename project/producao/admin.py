from django.contrib import admin

from .models import ProdutoAcabado, LimiteProducaoDiaria, TempoDesejadoProducao


# @admin.register(ProdutoAcabado)
# class ProdutoAcabadoAdmin(admin.ModelAdmin):
#     # list_display = ('nome', 'descricao')
#     ...


# @admin.register(MateriaPrimaProduto)
# class MateriaPrimaProdutoAdmin(admin.ModelAdmin):
#     list_display = ("materiaprimausada", "produto", "quant", "valor")
#     ...


@admin.register(LimiteProducaoDiaria)
class LimiteProducaoDiariaAdmin(admin.ModelAdmin):
    list_display = (
        "produto",
        "quantidade",
    )

    def has_add_permission(self, *args, **kwargs):
        return not LimiteProducaoDiaria.objects.exists()

    ...


@admin.register(TempoDesejadoProducao)
class TempoDesejadoProducaoAdmin(admin.ModelAdmin):
    list_display = ("status", "tempo_verde", "tempo_amarelo")
    ...
