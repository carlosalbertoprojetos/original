from django.urls import path

from . import views as v


app_name = "cliente"


urlpatterns = [
    path("", v.clienteList, name="clienteList"),
    path("ajax/", v.getClientesAjax, name="getClientesAjax"),
    path("cadastrar", v.clienteCreate, name="clienteCreate"),
    path("<int:pk>/editar/", v.clienteUpdate, name="clienteUpdate"),
    path("<int:pk>/delete/", v.clienteDelete, name="clienteDelete"),
]
