from django.urls import path

from . import views as v

app_name = "estoque"


urlpatterns = [
    path("", v.estoqueList, name="estoqueList"),
    path("<int:pk>/lista/conferencia/", v.confereEstoque, name="confereEstoque"),
]
