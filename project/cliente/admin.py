from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Cliente


class ClienteResource(resources.ModelResource):
    class Meta:
        model = Cliente


@admin.register(Cliente)
class ClienteAdmin(ImportExportModelAdmin):
    resource_class = ClienteResource
    list_display = ("nome",)

    fieldsets = (
        (
            "Cadastro",
            {
                "classes": ["grp-collapse grp-closed"],
                "fields": (
                    ("nome", "nome_fantasia"),
                    ("tel_principal", "tel_contato"),
                    ("email", "cpf"),
                    ("cnpj", "insc_estadual"),
                    ("descricao"),
                ),
            },
        ),
        (
            "Endereço",
            {
                "classes": ["grp-collapse grp-closed"],
                "fields": (
                    ("logradouro", "numero"),
                    ("complemento", "cep"),
                    ("cidade", "estado"),
                ),
            },
        ),
    )

    search_fields = ["nome", "cpf", "cnpj"]


# admin.site.register(Cliente, ClienteAdmin)
