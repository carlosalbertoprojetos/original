from django.urls import path

from . import views as v

app_name = "produto"


urlpatterns = [
    path("", v.produtoList, name="produtoList"),
    path("cadastrar/", v.produtoCreate, name="produtoCreate"),
    path("<int:pk>/editar/", v.produtoUpdate, name="produtoUpdate"),
    path("<int:pk>/deletar/", v.produtoDelete, name="produtoDelete"),
    path("peca/", v.pecaList, name="pecaList"),
    path("cadastrar/peca/", v.pecaCreate, name="pecaCreate"),
    path("<int:pk>/editar/peca/", v.pecaUpdate, name="pecaUpdate"),
    path("<int:pk>/deletar/peca/", v.pecaDelete, name="pecaDelete"),
    path("custo/", v.produtoCustoList, name="produtoCustoList"),
    path(
        "custo/<produto>/detalhes/", v.produtoCustoDetails, name="produtoCustoDetails"
    ),
]
