from django.contrib import admin


from .models import Transportadora, Rotas


class TransportadoraAdmin(admin.ModelAdmin):
    list_display = (
        "nome",
        "nome_fantasia",
        "tel_principal",
        "tel_contato",
        "email",
        "cidade",
        "atuacao"
    )
    fieldsets = [
        (
            "Contato",
            {
                "fields": (
                    "nome",
                    ("tel_principal", "tel_contato"),
                    "email",
                )
            },
        ),
        (
            "Documentos",
            {
                "fields": (
                    ("cpf", "cnpj"),
                    ("mei", "insc_estadual"),
                )
            },
        ),
        (
            "Localização",
            {
                "fields": (
                    ("logradouro", "numero", "complemento", "bairro"),
                    ("cidade", "estado"),
                     ("atuacao"),
                )
            },
        ),
    ]
    list_filter = ["nome", "cpf", "cnpj", "cidade"]
    search_fields = ["nome", "cpf", "cnpj", "cidade"]
    ordering = ("nome",)
    ...


admin.site.register(Transportadora, TransportadoraAdmin)


class RotasAdmin(admin.ModelAdmin):
    
    list_filter = ["cidade", "estado", "transportadoras"]
    list_display = (
        "cidade",
        "estado",
        "get_transportadoras",
    )
admin.site.register(Rotas, RotasAdmin)
