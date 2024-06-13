from django.urls import path
from . import views as v

app_name = "expedicao"

urlpatterns = [
    path("", v.listaExpedicao, name="listaExpedicao"),
    path("posvendaoriginal", v.listaPosVendaOriginal, name="listaPosVendaOriginal"),
    path(
        "posvendadistribuidora",
        v.listaPosVendaDistribuidora,
        name="listaPosVendaDistribuidora",
    ),
    path("imprimir", v.expedicaoImprimir, name="expedicaoImprimir"),
    path("nfimpressa", v.expedicaoNFImprimir, name="expedicaoNFImprimir"),
]
