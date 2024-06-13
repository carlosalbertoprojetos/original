from django.urls import path

from . import views as v


app_name = "suporte"


urlpatterns = [
    path("", v.suporteList, name="suporteList"),
    path("<int:venda>/", v.suporteCreate, name="suporteCreate"),
    path(
        "<venda>/timeline/create/",
        v.suporteTimeLineCreate,
        name="suporteTimeLineCreate",
    ),
    path("fluxo/acoes/", v.acoesFluxoAjax, name="acoesFluxoAjax"),
    path("problema/subprob/", v.subproblemasAjax, name="subproblemasAjax"),
    path(
        "<suporte>/reabrir/atendimento/",
        v.reabrirAtendimento,
        name="reabrirAtendimento",
    ),
]
