from django.urls import path

from . import views as v
from django.contrib.auth.decorators import permission_required


app_name = "cliente"


urlpatterns = [
    path("", v.clienteList, name="clienteList"),
    path("ajax/", v.getClientesAjax, name="getClientesAjax"),
    path(
        "cadastrar",
        v.clienteCreate,
        name="clienteCreate",
    ),
    path(
        "<int:pk>/editar/",
        v.clienteUpdate,
        name="clienteUpdate",
    ),
    path(
        "<int:pk>/delete/",
        v.clienteDelete,
        name="clienteDelete",
    ),
    path(
        "<cliente>/createuser/",
        v.clienteUser,
        name="clienteUser",
    ),
    path(
        "mensagem/",
        v.mensagem,
        name="mensagem",
    ),
    path("<cliente>/dashboard/", v.dashboard, name="dashboard"),
    path("<cliente>/dashboard/logout/", v.clienteLogout, name="clienteLogout"),
    path("<cliente>/pedido/", v.compraCreate, name="compraCreate"),
    path("<cliente>/pedido/realizado/", v.mensagem_compra, name="mensagem_compra"),
    path("<cliente>/lista/compras/", v.comprasList, name="comprasList"),
    path("<cliente>/lista/boletos/", v.boletoClienteList, name="boletoClienteList"),
    # SUPORTE
    path(
        "<cliente>/lista/assistencias/", v.suportClienteList, name="suportClienteList"
    ),
    path(
        "<venda>/assistencia/produto/",
        v.clienteSuporteProduto,
        name="clienteSuporteProduto",
    ),
    path(
        "<venda>/pedido/assistencia/", v.suporteClientCreate, name="suporteClientCreate"
    ),
]
