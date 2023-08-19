from django.contrib import admin

from .models import ContaReceber


@admin.register(ContaReceber)
class ContaRecebermAdmin(admin.ModelAdmin):
    ...
