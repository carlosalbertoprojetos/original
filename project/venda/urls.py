from django.urls import path

from . import views as v

app_name = "venda"


urlpatterns = [
    path("", v.vendaList, name="vendaList"),
    path("relatorios/", v.relatorios, name="relatorios"),
    path("ano/", v.total_vendido_ano, name="total_vendido_ano"),
    path("mes/", v.total_vendido_mes, name="total_vendido_mes"),
    path("select/", v.meses_ajax, name="meses_ajax"),
    # path("filter/", v.relatorio_meses_ajax, name="relatorio_meses_ajax"),
    # path("faturamento/", v.relatorio_faturamento, name="relatorio_faturamento"),
    # path("mensal/", v.relatorio_vendas_mensal, name="relatorio_vendas_mensal"),
    # path("produtos/", v.relatorio_produtos, name="relatorio_produtos"),
    # path("vendedor/", v.relatorio_vendedores, name="relatorio_vendedores"),
    path("cadastrar/", v.vendaCreate, name="vendaCreate"),
    path("cadastrar/preco/", v.produtoPrecoAjax, name="produtoPrecoAjax"),
    path("cadastrar/condicoes/parcedlas/", v.condicaoAjax, name="condicaoAjax"),
    path("<int:pk>/orcamento/", v.orcamento, name="orcamento"),
    path("<int:pk>/detalhes/", v.vendaDetails, name="vendaDetails"),
    path("<int:pk>/editar/", v.vendaUpdate, name="vendaUpdate"),
    path("<int:pk>/clonevenda/", v.vendaClone, name="vendaClone"),
    path("<int:pk>/deletar/", v.vendaDelete, name="vendaDelete"),
]
