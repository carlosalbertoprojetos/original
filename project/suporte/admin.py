from django.contrib import admin
from .forms import AcoesForm

from .models import (
    Suporte,
    Status,
    Timeline,
    Acoes,
    WorkFlow,
    Problema,
    Subproblema,
    ProblemaSuporte,
    ArquivosSuporte,
)


@admin.register(Suporte)
class SuporteAdmin(admin.ModelAdmin):
    list_display = ["venda", "statusAtual", "responsavel"]
    ...


admin.site.register(ArquivosSuporte)


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin): ...


@admin.register(Timeline)
class TimelineAdmin(admin.ModelAdmin): ...


@admin.register(Acoes)
class Acoes(admin.ModelAdmin):
    form = AcoesForm
    list_display = ["nome", "tempo", "workflow", "cor"]


@admin.register(WorkFlow)
class WorkFlow(admin.ModelAdmin): ...


@admin.register(Problema)
class Problema(admin.ModelAdmin):
    list_display = ["nome", "descricao"]
    ...


@admin.register(Subproblema)
class Subproblema(admin.ModelAdmin):
    list_display = ["problema", "nome"]
    ...


@admin.register(ProblemaSuporte)
class ProblemaSuporte(admin.ModelAdmin):
    list_display = ["suporte", "problema"]
    ...
