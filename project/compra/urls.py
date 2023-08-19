from django.urls import path


from . import views as v


app_name = 'compra'


urlpatterns = [
    path('', v.compraList, name='compraList'),
    path('cadastrar/', v.compraCreate, name='compraCreate'),
    path('<int:pk>/detalhes/', v.compraDetails, name='compraDetails'),
    path('<int:pk>/editar/', v.compraUpdate, name='compraUpdate'),
    path('<int:pk>/deletar/', v.compraDelete, name='compraDelete'),
]