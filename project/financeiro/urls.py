from django.urls import path


from . import views as v


app_name = "financeiro"


urlpatterns = [
    path("", v.FluxodeCaixa, name="fluxodecaixa"),
    path("contasapagar/", v.ContasaPagar, name="contasapagar"),
    path("contasareceber/", v.ContasaReceber, name="contasareceber"),
    path("comissao/", v.comissaoVendedorList, name="comissaoVendedorList"),
    # path(
    #     "<parcela>/comissao/",
    #     v.updateDataComissao,
    #     name="updateDataComissao",
    # ),
    path("<int:pk>/comissao/", v.updateDataComissao, name="updateDataComissao"),
]
