from django.contrib import admin

from .models import Empresa, DadosBancarios


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    ...


@admin.register(DadosBancarios)
class DadosBancariosAdmin(admin.ModelAdmin):
    ...
