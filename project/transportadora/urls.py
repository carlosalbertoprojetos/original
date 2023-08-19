from django.urls import path

from . import views as v


app_name = "transportadora"


urlpatterns = [
    path("", v.transporteList, name="transporteList"),
    path("cadastrar", v.transporteCreate, name="transporteCreate"),
    path("<int:pk>/editar/", v.transporteUpdate, name="transporteUpdate"),
    path("<int:pk>/delete/", v.transporteDelete, name="transporteDelete"),
]
