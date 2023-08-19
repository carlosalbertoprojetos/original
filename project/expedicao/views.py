from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.db.models import Sum
from pytz import timezone
from datetime import date, timedelta, datetime

from estoque.models import EstoqueMateriaPrima
from venda.models import VendaProduto, Venda
from produto.models import Produto

def listaExpedicao(request):
    """
    lista Expedicao
    """
    context={}
    if request.method == "POST":
        pass
 
    template_name = 'expedicao/listarExpedicao.html'
    
    vendas = Venda.objects.filter(status_venda__in=['expedicao'])
    context['vendas'] = vendas
    return render(request, template_name, context)
