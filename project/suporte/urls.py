from django.urls import path

from . import views as v


app_name = "suporte"


urlpatterns = [
    path("", v.suporteGeralList, name="suporteGeralList"),
    path("<venda>/", v.suporteCreate, name="suporteCreate"),
    path(
        "<venda>/timeline/create/",
        v.suporteTimeLineCreate,
        name="suporteTimeLineCreate",
    ),
    path(
        "<timeline>/timeline/update/",
        v.suporteTimeLineUpdate,
        name="suporteTimeLineUpdate",
    ),
]
