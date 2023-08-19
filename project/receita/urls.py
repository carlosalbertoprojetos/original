from django.urls import path

from . import views as v


app_name = 'receita'


urlpatterns = [
    path('', v.receitaList, name='receitaList'),
    path('cadastrar/', v.receitaCreate, name='receitaCreate'),
    path('<int:pk>/detalhes/', v.receitaDetails, name='receitaDetails'),
    path('<int:pk>/editar/', v.receitaUpdate, name='receitaUpdate'),
    path('<int:pk>/deletar/', v.receitaDelete, name='receitaDelete')
]