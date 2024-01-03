from django.urls import path

from . import views as v


app_name = "venda"


urlpatterns = [
    path("", v.vendaList, name="vendaList"),
    path("ajax/", v.getVendasAjax, name="getVendasAjax"),
    path("relatorios/", v.relatorios, name="relatorios"),
    path("ano/", v.total_vendido_ano, name="total_vendido_ano"),
    path("mes/", v.total_vendido_mes, name="total_vendido_mes"),
    path("select/", v.meses_ajax, name="meses_ajax"),
    path("cadastrar/", v.vendaCreate, name="vendaCreate"),
    path("cadastrar/preco/", v.produtoPrecoAjax, name="produtoPrecoAjax"),
    path("cadastrar/cliente/", v.clienteAjax, name="clienteAjax"),
    path("cadastrar/condicoes/parcelas/", v.condicaoAjax, name="condicaoAjax"),
    path("boletos/", v.boletoList, name="boletoList"),
    path("<hash>/orcamento/", v.orcamento, name="orcamento"),
    path("<int:pk>/editar/", v.vendaUpdate, name="vendaUpdate"),
    path("<int:pk>/clonevenda/", v.vendaClone, name="vendaClone"),
    path("<int:pk>/deletar/", v.vendaDelete, name="vendaDelete"),
    path("<int:pk>/nf/", v.vendaNF, name="vendaNF"),
    path("<int:pk>/expedicao/", v.expedicaoNF, name="expedicaoNF"),
]
