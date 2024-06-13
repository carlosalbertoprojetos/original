from django.urls import path

from . import views as v


app_name = "despesa"


urlpatterns = [
    path(
        "fluxodecaixa_eventos_ajax/",
        v.fluxodecaixa_eventos_ajax,
        name="fluxodecaixa_eventos_ajax",
    ),
    path(
        "fluxodecaixa_edit_day_ajax/",
        v.fluxodecaixa_edit_day_ajax,
        name="fluxodecaixa_edit_day_ajax",
    ),
    path("fluxo/calendario/", v.fluxodecaixa, name="fluxodecaixa"),
    path("lista", v.despesaList, name="despesaList"),
    path("cadastrar/", v.despesaCreate, name="despesaCreate"),
    path("<int:pk>/detalhes/", v.despesaDetails, name="despesaDetails"),
    path("<int:pk>/editar/", v.despesaUpdate, name="despesaUpdate"),
    path("<int:pk>/deletar/", v.despesaDelete, name="despesaDelete"),
]
