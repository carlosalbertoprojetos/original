from django.urls import path

from . import views as v

app_name = "mercadolivre"


urlpatterns = [
    path("contas", v.ContasList, name="contas"),
    path("", v.mercadolivre, name="mercadolivre"),
    path("redirect/", v.mercadolivreredirect, name="reredirect"),
    path("mercadolivrevendas/", v.mercadolivrevendas, name="mercadolivrevendas"),
]
