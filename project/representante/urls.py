from django.urls import path

from . import views as v


app_name = "representante"


urlpatterns = [
    path("", v.representantesList, name="representantesList"),
    path("cadastrar/", v.representanteCreate, name="representanteCreate"),
    path("<int:pk>/editar/", v.representanteUpdate, name="representanteUpdate"),
    path("<int:pk>/deletar/", v.representanteDelete, name="representanteDelete"),
    # path("regiao/", v.regiaoList, name="regiaoList"),
    # path("regiao/cadastrar/", v.regiaoCreate, name="regiaoCreate"),
    # path("regiao/<int:pk>/editar", v.regiaoUpdate, name="regiaoUpdate"),
    # path("regiao/<int:pk>/deletar/", v.regiaoDelete, name="regiaoDelete"),
    # path("conta/pesquisa/", v.contaBancaria, name="contaBancaria"),
    path(
        "<int:pk>/conta/cadastrar/",
        v.representanteContaCreate,
        name="representanteContaCreate",
    ),
    path(
        "conta/<int:pk>/editar/",
        v.representanteContaUpdate,
        name="representanteContaUpdate",
    ),
    path(
        "conta/<int:pk>/deletar/",
        v.representanteContaDelete,
        name="representanteContaDelete",
    ),
    path("<int:pk>/servicos/", v.servicosList, name="servicosList"),
    path("<int:pk>/servico/cadastrar/", v.servicoCreate, name="servicoCreate"),
    path(
        "servico/<int:pk>/editar/",
        v.servicoUpdate,
        name="servicoUpdate",
    ),
    path("servico/<int:pk>/deletar/", v.servicoDelete, name="servicoDelete"),
]
