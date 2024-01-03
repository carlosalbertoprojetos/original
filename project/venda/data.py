from datetime import date, timedelta, datetime
from django.db.models import Sum

from .models import VendaProduto, MaximoDesconto
from producao.models import LimiteProducaoDiaria


def dataAgendaProducao():
    agenda = VendaProduto.objects.all()

    # lista as datas com agendamento
    # limiteproducaodiaria = LimiteProducaoDiaria.objects.first()
    # if limiteproducaodiaria:
    #    limiteproducaodiaria = limiteproducaodiaria.qtde
    # else:
    #    limiteproducaodiaria = 0

    data_count = []
    for a in agenda:
        if a.venda.data_entrega:
            data_count.append(a.venda.data_entrega.strftime("%Y-%m-%d"))

    lista_data = set(data_count)

    # soma a quantidade de produtos agendados para fabricação diária
    quant_data = []
    # prox_dia = 0
    for l in lista_data:
        qtde = VendaProduto.objects.filter(venda__data_entrega=l).aggregate(
            Sum("quantidade")
        )["quantidade__sum"]
        # qtde = qtde# + prox_dia
        # if qtde > limiteproducaodiaria:
        #    prox_dia = qtde - limiteproducaodiaria
        #    num = limiteproducaodiaria
        # else:
        num = qtde
        # prox_dia = 0
        quant_data.append({l: num})

    today = date.today()
    lista_dias = []

    # gera lista com datas do dia atual + 44 dias seguintes
    for i in range(45):
        di = today + timedelta(i)
        dat = di.strftime("%Y-%m-%d")
        lista_dias.append((dat, di.strftime("%d/%m/%Y")))

    # insere a quantidade de produção agendada para cada data
    for d in quant_data:
        for k, v in d.items():
            conv = datetime.strptime(k, "%Y-%m-%d")
            va = 0
            if not v == 10:
                va = f"0{v}"
            else:
                va = v

            for i in lista_dias:
                if i[0] == k:
                    lista_dias.remove(i)
                    lista_dias.append((str(k), conv.strftime(f"%d/%m/%Y ({va})")))

    # ordena os dias da lista de dias em data de Produção
    lista = sorted(lista_dias)
    try:
        lista
    except:
        lista = []
    return lista


def ChoiceMaximoDesconto():
    maximodesconto = MaximoDesconto.objects.first()
    if not maximodesconto:
        return [(0, "0%")]
    else:
        maximodesconto = maximodesconto.qtde
        retorno = []
        for o in range(0, maximodesconto):
            retorno.append((o, "%s %%" % o))
        return retorno
