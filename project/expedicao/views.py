from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.db.models import Sum
from pytz import timezone
from datetime import date, timedelta, datetime
from django.db.models import Q
from estoque.models import EstoqueMateriaPrima
from venda.models import VendaProduto, Venda
from produto.models import Produto

def expedicaoImprimir(request):
    """
    expedicao Imprimir
    """
    context={}
    template_name = 'expedicao/imprimir.html'
    
    if request.method == "POST":
        lista_imprimir = request.POST.getlist('imprimir')
        vendas = Venda.objects.filter(id__in=lista_imprimir)
        vendas.update(etiqueta_impressa=True)
        context['vendas'] = vendas
        return render(request, template_name, context)            


def listaExpedicao(request):
    """
    lista Expedicao
    """
    context={}
 
    template_name = 'expedicao/listarExpedicao.html'
    if 'EXPEDICAO' in request.user.groups.values_list('name',flat = True) or request.user.is_superuser:
        vendas = Venda.objects.filter(status_venda__in=['expedicao'], etiqueta_impressa=False, status_expedicao__in=['Fazer Cotação', 'Aguardando Transportadora', 'Aguardando Concluir Produtos'])
    else:
        vendas = Venda.objects.filter(status_venda__in=['expedicao'], vendedor=request.user, etiqueta_impressa=False, status_expedicao__in=['Fazer Cotação', 'Conferir Dados', 'Aguardando Transportadora'])
        #vendas = []
    #vendas =  Venda.objects.filter(id=639)#status_venda__in=['expedicao'], vendedor=request.user, etiqueta_impresa=False, status_expedicao__in=['Fazer Cotação', 'Conferir Dados', 'Aguardando Transportadora'])
    relacaoprodutos = []
    for venda in vendas:
        produtos = venda.vendaproduto_set.all()
        for produto in produtos:
            nome = produto.produto.nome
            voltagem = produto.voltagem.nome
            torneira = produto.torneira.nome
            adesivado = produto.adesivado.nome
            qtde = produto.quantidade

            # agora ve a relacao
            if not len(relacaoprodutos):
                # adiciona nova relacao
                nomes = []
                for _venda in vendas:
                    _produtos = _venda.vendaproduto_set.all()
                    for _produto in _produtos:
                        _nome = _produto.produto.nome
                        _voltagem = _produto.voltagem.nome
                        _torneira = _produto.torneira.nome
                        _adesivado = _produto.adesivado.nome
                        _qtde = _produto.quantidade
                        if (_nome == nome and 
                                _voltagem == voltagem and
                                _torneira == torneira and
                                _adesivado == adesivado):
                            for vezes in range(0,_qtde):
                                nomes.append({'nome':_venda.cliente.nome, 'id': _venda.id, 'vendedor': _venda.vendedor})

                relacaoprodutos.append({'nome':nome,
                                        'voltagem':voltagem,
                                        'torneira':torneira,
                                        'adesivado':adesivado,
                                        'qtde':qtde,
                                        'nomes':nomes,
                                        }
                                    )
            else:
                jaexiste = False
                for relacaoproduto in relacaoprodutos:
                    if (nome == relacaoproduto['nome'] and
                        voltagem == relacaoproduto['voltagem'] and
                        torneira == relacaoproduto['torneira'] and
                        adesivado == relacaoproduto['adesivado']
                        ):
                        jaexiste = True
                        
                if jaexiste:
                    #so soma qtde
                    for relacaoproduto in relacaoprodutos:
                        if (nome == relacaoproduto['nome'] and
                            voltagem == relacaoproduto['voltagem'] and
                            torneira == relacaoproduto['torneira'] and
                            adesivado == relacaoproduto['adesivado']
                            ):
                            relacaoproduto['qtde'] += qtde
                else:
                    # adiciona nova relacao
                    nomes = []
                    for _venda in vendas:
                        _produtos = _venda.vendaproduto_set.all()
                        for _produto in _produtos:
                            _nome = _produto.produto.nome
                            _voltagem = _produto.voltagem.nome
                            _torneira = _produto.torneira.nome
                            _adesivado = _produto.adesivado.nome
                            _qtde = _produto.quantidade
                            if (_nome == nome and 
                                    _voltagem == voltagem and
                                    _torneira == torneira and
                                    _adesivado == adesivado):
                                for vezes in range(0,_qtde):
                                    nomes.append({'nome':_venda.cliente.nome, 'id': _venda.id, 'vendedor': _venda.vendedor})
                    
                    relacaoprodutos.append({'nome':nome,
                                            'voltagem':voltagem,
                                            'torneira':torneira,
                                            'adesivado':adesivado,
                                            'qtde':qtde,
                                            "nomes": nomes,
                                            }
                                        )
    if 'EXPEDICAO' in request.user.groups.values_list('name',flat = True) or request.user.is_superuser:
        listagemvendas = Venda.objects.filter(Q(status_venda__in=['expedicao']) | Q(status_venda='enviado', data_status_expedicao__gte=datetime.now().replace(hour=0, minute=0, second=0) , data_status_expedicao__lte=datetime.now().replace(hour=23, minute=59, second=59) )).order_by('-id')
    else:
        listagemvendas = Venda.objects.filter(vendedor=request.user).filter(Q(status_venda__in=['expedicao']) | Q(status_venda='enviado', data_status_expedicao__gte=datetime.now().replace(hour=0, minute=0, second=0) , data_status_expedicao__lte=datetime.now().replace(hour=23, minute=59, second=59) )).order_by('-id')
    # se pesquisou
    if  request.POST.get('pesquisa'):
        context['pesquisa'] =  pesquisa = request.POST.get('pesquisa')
        if 'EXPEDICAO' in request.user.groups.values_list('name',flat = True) or request.user.is_superuser:
            try:
              listagemvendas = Venda.objects.filter(Q(numero_nf=pesquisa) | Q(id=pesquisa) | Q(cliente__nome__icontains=pesquisa)).order_by('-id')
            except:
              listagemvendas = Venda.objects.filter(Q(cliente__nome__icontains=pesquisa)).order_by('-id')    
        else:
            try:
              listagemvendas = Venda.objects.filter(vendedor=request.user).filter(Q(numero_nf=pesquisa) | Q(id=pesquisa) | Q(cliente__nome__icontains=pesquisa)).order_by('-id')
            except:
              listagemvendas = Venda.objects.filter(vendedor=request.user).filter(Q(cliente__nome__icontains=pesquisa)).order_by('-id')   
    context['vendas'] = listagemvendas
    context['bebedouros_na_expedicao'] = relacaoprodutos
    return render(request, template_name, context)
