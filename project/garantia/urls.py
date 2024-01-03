from django.urls import path

from . import views as v


app_name = "garantia"


urlpatterns = [
    path("", v.produtosEmGarantia, name="produtosEmGarantia"),
    path("vendas/", v.vendasGarantiaList, name="vendasGarantiaList"),
    path("<venda>/", v.produtosVenda, name="produtosVenda"),
    path("<produto>/create/", v.produtoCreateGarantia, name="produtoCreateGarantia"),
    path(
        "<garantia>/list/timeline/", v.garantiaTimeLineList, name="garantiaTimeLineList"
    ),
    path(
        "<timeline>/update/timeline/",
        v.garantiaTimeLineUpdate,
        name="garantiaTimeLineUpdate",
    ),
]
