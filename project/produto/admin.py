from django.contrib import admin

from .models import Produto, MateriaPrimaProduto, ProdutosMatPri


class ProdutosMatPriAdmin(admin.TabularInline):
    model = ProdutosMatPri
    extra = 3


class MateriaPrimaProdutoAdmin(admin.ModelAdmin):
    model = MateriaPrimaProduto
    fieldsets = [
        ("INFORMAÇÕES", {"fields": (("materiaprima", "valor"))}),
    ]
    inlines = (ProdutosMatPriAdmin,)


admin.site.register(MateriaPrimaProduto, MateriaPrimaProdutoAdmin)


class ProdutoAdmin(admin.ModelAdmin):
    model = Produto
    list_display = ("nome", "preco")
    fieldsets = [
        (
            "INFORMAÇÕES",
            {
                "fields": (
                    ("nome", "codigoproduto"),
                    ("preco", "unimed", "ncm", "cst", "cfop", "estoque_ini"),
                    "status_produto",
                )
            },
        ),
    ]
    readonly_fields = ["criadoem", "atualizadoem"]


admin.site.register(Produto, ProdutoAdmin)
