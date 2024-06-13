from django.contrib import admin

from .models import (
    Produto,
    Peca,
    ProdutoMatPri,
    UnidadeMedida,
)


@admin.register(ProdutoMatPri)
class ProdutosMatPriAdmin(admin.ModelAdmin):
    list_display = ("materiaprima", "peca", "produto")
    ...


@admin.register(Peca)
class PecaAdmin(admin.ModelAdmin):
    list_display = ("nome", "produto")
    ...


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    model = Produto
    list_display = ("empresa", "nome", "ncm", "cfop", "aliq_ipi", "preco")
    fieldsets = [
        (
            "INFORMAÇÕES",
            {
                "fields": (
                    ("empresa"),
                    ("nome", "codigoproduto"),
                    (
                        "unimed",
                        "ncm",
                        "cest",
                        "cst",
                        "cfop",
                        "aliq_ipi",
                        "aliq_icms_interno",
                        "preco",
                        "peso",
                    ), 
                    ("estoque_127"),
                    ("estoque_220"),
                    "status_produto",
                )
            },
        ),
    ]
    readonly_fields = ["criadoem", "atualizadoem"]


@admin.register(UnidadeMedida)
class UnidadeMedidaAdmin(admin.ModelAdmin):
    model = UnidadeMedida
    list_display = ("unidade",)
    fieldsets = [
        (
            "INFORMAÇÕES",
            {"fields": (("unidade", "descricao"),)},
        ),
    ]
