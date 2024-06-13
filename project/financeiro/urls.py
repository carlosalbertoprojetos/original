from django.urls import path


from . import views as v
import sys

sys.path.append("..")


app_name = "financeiro"

urlpatterns = [
    path("", v.fluxodeCaixa, name="fluxodecaixa"),
    path("contasapagar/", v.ContasaPagar, name="contasapagar"),
    path("<int:pk>/despesa/deletar/", v.parcelaDelete, name="parcelaDelete"),
    path("contasareceber/", v.contasaReceber, name="contasareceber"),
    path("upload/extrato/", v.extratoUpload, name="extratoUpload"),
    path("conciliar/conta/", v.extratoConciliar, name="extratoConciliar"),
    path(
        "conciliar/pagamento/<int:id>/",
        v.conciliarContaPagar,
        name="conciliarContaPagar",
    ),
    path(
        "conciliar/recebimento/<int:id>/",
        v.conciliarContaReceber,
        name="conciliarContaReceber",
    ),
    path(
        "conciliar/salvar/",
        v.conciliarSalvarAjax,
        name="conciliarSalvarAjax",
    ),
    path("comissao/", v.comissaoVendedorList, name="comissaoVendedorList"),
    path("<int:pk>/comissao/", v.updateDataComissao, name="updateDataComissao"),
    path(
        "fluxo/extratobancario/",
        v.fluxoCaixaExtratoBancario,
        name="fluxoCaixaExtratoBancario",
    ),
]
