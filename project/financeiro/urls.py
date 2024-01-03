from django.urls import path


from . import views as v
import sys

sys.path.append("..")
from integracoes.banco.Itau.boleto import boleto

app_name = "financeiro"

urlpatterns = [
    path("", v.FluxodeCaixa, name="fluxodecaixa"),
    path("contasapagar/", v.ContasaPagar, name="contasapagar"),
    path("<int:pk>/despesa/deletar/", v.parcelaDelete, name="parcelaDelete"),
    path("contasareceber/", v.ContasaReceber, name="contasareceber"),
    # path("boleto/", boleto.formboleto, name="formboleto"),
    path("comissao/", v.comissaoVendedorList, name="comissaoVendedorList"),
    # path(
    #     "<parcela>/comissao/",
    #     v.updateDataComissao,
    #     name="updateDataComissao",
    # ),
    path("<int:pk>/comissao/", v.updateDataComissao, name="updateDataComissao"),
]
