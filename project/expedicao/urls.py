from django.urls import path
from . import views as v

app_name="expedicao"

urlpatterns = [
   path("" ,v.listaExpedicao, name="listaExpedicao")
]
