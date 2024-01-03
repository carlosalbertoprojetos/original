from django.urls import path

from . import views as v

app_name = "producao"


urlpatterns = [
    path("estoque/previsao", v.previsaoEstoque, name="previsaoEstoque"),
    path("estoque/real", v.estoqueReal, name="estoqueReal"),
    path("iniciarproducao", v.iniciarProducao, name="iniciarProducao"),
    path("chaodefabrica", v.chaodeFabrica, name="chaodeFabrica"),
    path("relatorio/produto", v.relatorioProducao, name="relatorioProducao"),
    path("relatorio/venda", v.relatorioVenda, name="relatorioVenda"),
    path("enviarexpedicao", v.enviarExpedicao, name="enviarExpedicao"),
    path("edit_status_ajax", v.edit_status_ajax, name="edit_status_ajax"),
    path("criar_produto_ajax", v.criar_produto_ajax, name="criar_produto_ajax"),
    path("peca/estoque/previsao/", v.previsaoEstoquePecas, name="previsaoEstoquePecas"),
    path("peca/estoque/real/", v.estoqueRealPecas, name="estoqueRealPecas"),
]
