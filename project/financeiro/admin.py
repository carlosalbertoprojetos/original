from django.contrib import admin

from .models import ContaPagar, ContaReceber, ControleExtratosBancarios, ExtratoBancario


@admin.register(ContaPagar)
class ContaPagarAdmin(admin.ModelAdmin):
    class Meta:
        ordering = ["-datavencimento"]

    list_display = [
        "__str__",
        "datavencimento",
        "valor",
        "datapagamento",
        "valor_pago",
        "conciliado",
    ]
    search_fields = [
        "datavencimento",
        "valor",
        "datapagamento",
        "valor_pago",
    ]
    list_filter = [
        "datavencimento",
        "valor",
        "datapagamento",
        "valor_pago",
    ]
    ...


@admin.register(ContaReceber)
class ContaReceberAdmin(admin.ModelAdmin):
    class Meta:
        ordering = ["-datavencimento"]

    list_display = [
        "__str__",
        "datavencimento",
        "valor",
        "datapagamento",
        "valor_pago",
        "conciliado",
    ]
    search_fields = [
        "datavencimento",
        "valor",
        "datapagamento",
        "valor_pago",
    ]
    list_filter = [
        "datavencimento",
        "valor",
        "datapagamento",
        "valor_pago",
    ]

    # def vencimento(self, obj):
    #     if obj.datavencimento:
    #         return obj.datavencimento.strftime("%d/%m/%y")

    # def pagamento(self, obj):
    #     if obj.datapagamento:
    #         return obj.datapagamento.strftime("%d/%m/%y")

    ...


@admin.register(ControleExtratosBancarios)
class ControleExtratosBancariosAdmin(admin.ModelAdmin):
    list_display = ["data_extrato", "__str__", "data_upload", "saldo"]
    search_fields = [
        "data_extrato",
        "upload",
    ]
    list_filter = [
        "datahora",
        "upload",
    ]

    # admin.display(description="Data")

    def data_extrato(self, obj):
        if obj.datahora:
            return obj.datahora.strftime("%d/%m/%y")

    def data_upload(self, obj):
        if obj.upload:
            return obj.upload.strftime("%d/%m/%y")

    ...


@admin.register(ExtratoBancario)
class ExtratoBancarioAdmin(admin.ModelAdmin):
    list_display = (
        "get_data",
        "lancamento",
        "origem",
        "valor",
        "saldo",
        "get_conciliado",
    )
    fieldsets = [
        ("Controle", {"fields": ("controle",)}),
        (
            "Lançamentos",
            {
                "fields": (
                    ("data", "lancamento", "origem", "valor", "saldo", "conciliado")
                )
            },
        ),
    ]
    list_filter = ["data"]
    search_fields = ["data", "lancamento", "valor", "saldo", "conciliado"]
    ordering = ("data",)

    @admin.display(description="Data")
    def get_data(self, obj):
        if obj.data:
            return obj.data.strftime("%d/%m/%y")

    @admin.display(description="Conciliado")
    def get_conciliado(self, obj):
        if obj.conciliado:
            return obj.conciliado.strftime("%d/%m/%y")

    ...
