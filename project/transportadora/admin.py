from django.contrib import admin


from .models import Transportadora


class TransportadoraAdmin(admin.ModelAdmin):
    list_display = (
        "nome",
        "nome_fantasia",
        "tel_principal",
        "tel_contato",
        "email",
        "cidade",
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
                )
            },
        ),
    ]
    list_filter = ["nome", "cpf", "cnpj", "cidade"]
    search_fields = ["nome", "cpf", "cnpj", "cidade"]
    ordering = ("nome",)
    ...


admin.site.register(Transportadora, TransportadoraAdmin)
