from django.contrib import admin

from .models import FormaPagamento, CondicaoVenda, Venda, MaximoDesconto, Voltagem, Torneira, Adesivado


@admin.register(Voltagem)
class VoltagemAdmin(admin.ModelAdmin):
    ...


@admin.register(Torneira)
class TorneiraAdmin(admin.ModelAdmin):
    ...


@admin.register(Adesivado)
class AdesivadoAdmin(admin.ModelAdmin):
    ...


@admin.register(FormaPagamento)
class FormaPagamentoAdmin(admin.ModelAdmin):
    list_display = ("nome", "descricao")


@admin.register(CondicaoVenda)
class CondicaoVendaAdmin(admin.ModelAdmin):
    list_display = ("nome", "parcelas", "primeira", "demais", "formapgto")
    ...


@admin.register(Venda)
class VendaAdmin(admin.ModelAdmin):
    list_display = (
        "cliente",
        "data_pedido",
        "data_entrega",
        "qtde_produtos",
        "transportadora",
        "vendedor",
        "valor_venda",
        "porcentagem_desconto",
        "subtotal",
        "status_venda",
        "condicaopgto",
    )
    ...


@admin.register(MaximoDesconto)
class MaximoDescontoAdmin(admin.ModelAdmin):
    list_display = ("qtde",)

    def has_add_permission(self, *args, **kwargs):
        return not MaximoDesconto.objects.exists()

    ...
