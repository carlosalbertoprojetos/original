from django.urls import path

from . import views as v


app_name = "fornecedor"


urlpatterns = [
    path("", v.fornecedorList, name="fornecedorList"),
    path("cadastrar", v.fornecedorCreate, name="fornecedorCreate"),
    path("<int:pk>/editar/", v.fornecedorUpdate, name="fornecedorUpdate"),
    path("<int:pk>/delete/", v.fornecedorDelete, name="fornecedorDelete"),
]
