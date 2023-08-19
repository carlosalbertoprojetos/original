import collections, functools, operator
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.db.models import Sum
from pytz import timezone
from datetime import date, timedelta, datetime
from django.forms import modelformset_factory

from .models import (
    LimiteProducaoDiaria,
    ProdutoAcabado,
    HistoricoMontagem,
)
from estoque.models import EstoqueMateriaPrima
from compra.models import Compra, CompraMateriaPrima
from produto.models import Produto, ProdutosMatPri
from materiaprima.models import MateriaPrima
from venda.models import VendaProduto, Venda
from producao.forms import QuantidadeProducaoForm


def criar_produto_ajax(request):
    """
    cria produto
    """
    pk = request.GET.get("id_produto")
    status = "montagem"
    if pk:
        produto = ProdutoAcabado.objects.create(
            produto_id=pk,
            status=status,
            hora_inicio=datetime.now(),
            hora_momento=datetime.now(),
        )
    data = {}
    return JsonResponse(data, safe=False)


def edit_status_ajax(request):
    """
    altera o status do ProdutoAcabado
    """
    pk = request.GET.get("id")
    status = request.GET.get("status")
    produto = ProdutoAcabado.objects.get(id=pk)
    agora = datetime.now().astimezone(timezone("America/Sao_Paulo"))
    if produto:
        if status == "excluir":
            produto.delete()

        elif status == "estoque":
            hora_inicio = produto.hora_inicio
            hora_momento = produto.hora_momento

            duracao = agora - hora_momento.astimezone(timezone("America/Sao_Paulo"))
            duracao = duracao.total_seconds() / 60 / 60

            HistoricoMontagem.objects.get_or_create(
                produtoacabado=produto,
                hora_inicio=hora_momento,
                hora_fim=agora,
                duracao=duracao,
                status=produto.status,
            )

            duracao = agora - hora_inicio.astimezone(timezone("America/Sao_Paulo"))
            duracao = duracao.total_seconds() / 60 / 60
            produto.status = status
            produto.hora_momento = agora
            produto.hora_fim = agora
            produto.duracao = duracao
            produto.save()

        else:
            hora_momento = produto.hora_momento
            duracao = agora - hora_momento.astimezone(timezone("America/Sao_Paulo"))
            duracao = duracao.total_seconds() / 60 / 60

            HistoricoMontagem.objects.get_or_create(
                produtoacabado=produto,
                hora_inicio=hora_momento,
                hora_fim=agora,
                duracao=duracao,
                status=produto.status,
            )

            produto.status = status
            produto.hora_momento = agora
            produto.save()

    data = {}
    return JsonResponse(data, safe=False)


def chaodeFabrica(request):
    """
    chaodeFabrica
    """
    template_name = "producao/chaodeFabrica.html"
    context = {}
    context["faltandomateriaprima"] = ProdutoAcabado.objects.filter(
        status="faltandomateriaprima"
    )
    context["montagem"] = ProdutoAcabado.objects.filter(status="montagem")
    context["eletrica"] = ProdutoAcabado.objects.filter(status="eletrica")
    context["refrigeracao"] = ProdutoAcabado.objects.filter(status="refrigeracao")
    context["acabamento"] = ProdutoAcabado.objects.filter(status="acabamento")
    context["embalagem"] = ProdutoAcabado.objects.filter(status="embalagem")
    context["estoque"] = ProdutoAcabado.objects.filter(status="estoque")
    context["excluir"] = ProdutoAcabado.objects.filter(status="excluir")

    context["lista_produtos"] = Produto.objects.all()
    context["media_faltandomateriaprima"] = "-"
    context["media_montagem"] = "-"
    context["media_eletrica"] = "-"
    context["media_refrigeracao"] = "-"
    context["media_acabamento"] = "-"
    context["media_embalagem"] = "-"
    context["media_estoque"] = "-"
    if HistoricoMontagem.objects.filter(status="montagem"):
        lista = [
            "faltandomateriaprima",
            "montagem",
            "eletrica",
            "refrigeracao",
            "acabamento",
            "embalagem",
            "estoque",
        ]
        for _l in lista:
            if HistoricoMontagem.objects.filter(status=_l).aggregate(Sum("duracao"))[
                "duracao__sum"
            ]:
                media = (
                    HistoricoMontagem.objects.filter(status=_l).aggregate(
                        Sum("duracao")
                    )["duracao__sum"]
                    / HistoricoMontagem.objects.filter(status=_l).count()
                )
                media = str(round(media)).replace(".", ":")
                context["media_" + _l] = media
    return render(request, template_name, context)


def iniciarProducao(request):
    """
    iniciar producao
    """
    if request.method == "POST":
        # return HttpResponseRedirect(reverse('producao:chaodeFabrica'))
        vendas = request.POST.get("venda")
        # muda status para em producao e cria os produtos sendo produzidos e envia pro chao de fabrica
        for id_venda in vendas:
            venda = Venda.objects.get(id=id_venda)
            if venda:
                # gera os produtos
                for produto in venda.vendaproduto_set.all():
                    qtde = produto.quantidade
                    for o in range(0, qtde):
                        produto = ProdutoAcabado.objects.create(
                            produto=produto.produto,
                            status="montagem",
                            hora_inicio=datetime.now(),
                            hora_momento=datetime.now(),
                        )
            venda.status_venda = "emproducao"
            venda.save()
            return HttpResponseRedirect(reverse("producao:chaodeFabrica"))

    template_name = "producao/iniciarProducao.html"
    context = {}
    vendas = Venda.objects.filter(status_venda="autorizado")
    context["vendas"] = vendas
    lista_produtos = []
    for produto in Produto.objects.all():
        produtosacabados = ProdutoAcabado.objects.filter(
            produto=produto, status="estoque"
        )  # produto em fabricação - chão de fábrica
        if len(produtosacabados):
            lista_produtos.append(
                {"nome": produto.nome, "qtde": produtosacabados.count()}
            )
    context["estoque"] = lista_produtos
    vendas = Venda.objects.filter(status_venda__in=["autorizado", "emproducao"])
    context["vendas"] = vendas
    context["lista_produtos"] = Produto.objects.all()

    return render(request, template_name, context)


def enviarExpedicao(request):
    """
    enviar Expedicao
    """
    context = {}
    if request.method == "POST":
        template_name = "producao/enviarExpedicao.html"
        # return HttpResponseRedirect(reverse('producao:chaodeFabrica'))
        vendas = request.POST.get("venda")
        # muda status para em producao e cria os produtos sendo produzidos e envia pro chao de fabrica

        lista_produtos = []
        for produto in Produto.objects.all():
            _produto = {"nome": produto.nome, "qtde_estoque": 0, "qtde_vendidos": 0}
            produtosacabados = ProdutoAcabado.objects.filter(
                produto=produto, status="estoque"
            )
            if len(produtosacabados):
                _produto["qtde_estoque"] = produtosacabados.count()
            lista_produtos.append(_produto)

        temestoque = False
        for id_venda in vendas:
            venda = Venda.objects.get(id=id_venda)
            if venda:
                for produto in venda.vendaproduto_set.all():
                    for _produto in lista_produtos:
                        if _produto["nome"] == produto.produto.nome:
                            _produto["qtde_vendidos"] += produto.quantidade

        # verifica se tem estoque para tudo
        temestoque = True
        for _produto in lista_produtos:
            if _produto["qtde_vendidos"] > _produto["qtde_estoque"]:
                temestoque = False

        if temestoque:
            for id_venda in vendas:
                venda = Venda.objects.get(id=id_venda)
                if venda:
                    # verifica se tem estoque suficiente
                    for produto in venda.vendaproduto_set.all():
                        quantidade = produto.quantidade
                        for o in range(0, quantidade):
                            _produto = ProdutoAcabado.objects.get(
                                produto=produto.produto, status="estoque"
                            )
                            _produto.delete()

                    venda.status_venda = "expedicao"
                    venda.save()
                    # remove do estoque o produto
            # if temestoque:
            return HttpResponseRedirect(reverse("producao:chaodeFabrica"))
        else:
            context["erro"] = "True"

    template_name = "producao/enviarExpedicao.html"

    lista_produtos = []
    for produto in Produto.objects.all():
        produtosacabados = ProdutoAcabado.objects.filter(
            produto=produto, status="estoque"
        )
        if len(produtosacabados):
            lista_produtos.append(
                {"nome": produto.nome, "qtde": produtosacabados.count()}
            )
    context["estoque"] = lista_produtos
    vendas = Venda.objects.filter(status_venda__in=["autorizado", "emproducao"])
    context["vendas"] = vendas
    context["lista_produtos"] = Produto.objects.all()
    return render(request, template_name, context)


def estoqueReal(request):
    template_name = "producao/estoqueReal.html"
    bd_produto = Produto.objects.all()

    # dias de produção a serem estimados
    previsao_dias = 35
    today = date.today()
    meses_extenso = (
        "Janeiro",
        "Fevereiro",
        "Março",
        "Abril",
        "Maio",
        "Junho",
        "Julho",
        "Agosto",
        "Setembro",
        "Outubro",
        "Novembro",
        "Dezembro",
    )

    # lista os meses referentes ao período 'previsao_dias'
    datas = []
    dias_ = []
    dia = []
    mp = []
    for i in range(previsao_dias):
        dia = today + timedelta(i)
        datas.append(dia.strftime("%Y-%m-%d"))
        dias_.append(dia.day)
        var = {dia.year: dia.month}
        if not var in mp:
            mp.append({dia.year: dia.month})

    # lista data, produtos e quantidade a serem fabricados
    vendas = VendaProduto.objects.filter(venda__data_entrega__range=(today, dia))
    dict_prod_diaria = {}
    tot_mp_prod_diaria = {}
    lista_datas = []
    tot_prod_vendas = []

    # dict matérias primas e quantidade a ser consumida no dia
    consumo_mp_periodo = {}
    mp_usadas = {}
    for v in vendas:
        dict_prod_diaria.update({str(v.venda.data_entrega): v.quantidade})
        total_producao_diaria = VendaProduto.objects.filter(
            venda__data_entrega=v.venda.data_entrega
        ).aggregate(Sum("quantidade"))["quantidade__sum"]
        tot_mp_prod_diaria.update({str(v.venda.data_entrega): total_producao_diaria})
        lista_datas.append(str(v.venda.data_entrega))
        tot_prod_vendas.append(v.quantidade)

        pmp = ProdutosMatPri.objects.filter(prod__nome=v.produto)
        mp_usada = {}
        for p in pmp:
            if p.prod.nome == v.produto.nome:
                sum_mp = p.quant * v.quantidade
                mp_usada.update({p.mp: int(sum_mp)})
        mp_usadas.update({p.prod: mp_usada})
        sum_mp = {}
        consumo_mp_periodo.update({v.venda.data_entrega: mp_usadas})

    # lista datas individualizadas e ordenadas
    lista_datas = set(lista_datas)
    lista_datas = sorted(lista_datas)

    prods_fabricados_mesmo_dia = {}
    for ld in lista_datas:
        lista = {}
        for ven in vendas:
            if str(ven.venda.data_entrega) == ld:
                produto_mp = ProdutosMatPri.objects.filter(prod__nome=ven.produto)
                mps_produto = {}
                for promp in produto_mp:
                    quant = promp.quant * ven.quantidade
                    mps_produto.update({promp.mp.materiaprima.nome: int(quant)})
                lista.update({ven.produto: {ven.quantidade: mps_produto}})
        prods_fabricados_mesmo_dia.update({ld: lista})

    # total matérias primas utilizadas por data
    tmpud = {}
    custo_mp_posicao = []
    cont = 0
    for ld in lista_datas:
        tmpud2 = {}
        mps_somadas = []
        for k, v in prods_fabricados_mesmo_dia[ld].items():
            for ka, va in v.items():
                mps_somadas.append(va)
            soma_mps = dict(
                functools.reduce(operator.add, map(collections.Counter, mps_somadas))
            )
        tmpud2.update({cont: soma_mps})
        cont += 1
        tmpud.update({ld: soma_mps})
        custo_mp_posicao.append(tmpud2)

    # total diário a ser subtraído por mp
    tdsmp = []
    for ld in lista_datas:
        quants = []
        for k, v in tmpud[ld].items():
            quants.append(int(v))
        tdsmp.append(quants)

    dict_prod_diaria2 = []
    for k in bd_produto:
        dpd = {}
        for v in vendas:
            if k == v.produto:
                date_ = v.venda.data_entrega
                dpd.update({date_.strftime("%Y-%m-%d"): v.quantidade})
        dict_prod_diaria2.append(dpd)

    # cria lista dos dias no período por produto id
    prod_diaria = 0

    # for le in range(len(dict_prod_diaria2)):
    lista_prod_diaria = {}
    cont = 0
    for dpd2 in dict_prod_diaria2:
        lpd21 = []
        for l in range(previsao_dias):
            lpd21.append(prod_diaria)
        for d in datas:
            for dpkey, dpvalue in dpd2.items():
                index = datas.index(d)
                if str(d) == dpkey:
                    lpd21[index] = dpd2[dpkey]
        lista_prod_diaria.update({str(bd_produto[cont]): lpd21})
        cont += 1

    # matérias primas catalogadas
    materias_primas_catalogadas = MateriaPrima.objects.all()

    # dict contento todas as matérias primas e suas quantidades zeradas
    materias_primas_geral = {}
    for mpc in materias_primas_catalogadas:
        materias_primas_geral.update({mpc.nome: 0})

    # estoque atual de matérias primas
    estoque_atual = EstoqueMateriaPrima.objects.all()

    # insere a quantidade de cada matéria prima no materias_primas_geral
    for ea in estoque_atual:
        for egkey, egvalue in materias_primas_geral.items():
            if ea.materiaprima.nome == egkey:
                materias_primas_geral.update({ea.materiaprima.nome: int(ea.qtde)})

    # posição, produto, quantidade comprada, na posição da data correspondente
    mpCompras = CompraMateriaPrima.objects.filter(compra__previsaoentrega__gte=today)

    # lista matéria prima e quantidade na posição correspondente a previsão de entrega
    posicoes = []
    posicoes2 = {}

    quantMpCompras = {}
    for d in range((len(dias_) - 1)):
        dia = today + timedelta(d)
        for da in lista_datas:
            if str(dia) == da:
                posicoes.append(d)

        for mpc in mpCompras:
            poprodquant = {}
            quantMpCompras.update(
                {mpc.compra.previsaoentrega: {mpc.produto.nome: mpc.quantidade}}
            )
            if dia == mpc.compra.previsaoentrega:
                poprodquant.update({mpc.produto.nome: mpc.quantidade})
                posicoes2.update({d: poprodquant})

    # estoque por dia
    estoque = materias_primas_geral
    lista_mps = []
    for d in range(len(dias_)):  # 1-35
        vls = {}
        for p1k, p1v in posicoes2.items():
            for p1vk, p1vv in p1v.items():
                if d == p1k:
                    saldoCompras = estoque[p1vk] + p1vv
                    estoque.update({p1vk: saldoCompras})

        for p2 in range(len(posicoes)):
            if d == posicoes[p2]:
                for k, v in custo_mp_posicao[p2].items():
                    for ka, va in v.items():
                        saldoPosicao = estoque[ka] - va
                        estoque.update({ka: saldoPosicao})
            vls.update(estoque)
        lista_mps.append(vls)

    # relacionar saldo mp aos produtos
    produtos_mps_totais = {}
    for e in estoque:
        quantidades = []
        for lm in lista_mps:
            for vk, vv in lm.items():
                if e == vk:
                    quantidades.append(vv)
        produtos_mps_totais.update({e: quantidades})

    # cria um dicionário (dict_produtos_mp) com todos os produtos cadastrados
    tot_prods = Produto.objects.all()
    tot_produtos = []
    dict_produtos_mp = {}
    for i in tot_prods:
        tot_produtos.append(i.nome)
        dict_produtos_mp.update({i.nome: materias_primas_geral})

    # lista o que cada produto utiliza de matérias primas e a quantidade necessária para produção
    listaprodutos = ProdutosMatPri.objects.all()

    # cria um dicionário por produto, matéria prima e sua quantidade
    list_prod = {}
    for bdp in tot_produtos:
        mp_produtos = {}
        for l in listaprodutos:
            if bdp == l.prod.nome:
                mp_produtos.update({l.mp.materiaprima.nome: l.quant})
        list_prod.update({bdp: mp_produtos})

    lista_mp_final_por_produto = {}
    for k, v in list_prod.items():
        mps_por_prod = {}
        for ka, va in v.items():
            mps_por_prod.update({ka: int(va)})
        lista_mp_final_por_produto.update({k: mps_por_prod})

    tot_dict_prod_diaria = {}
    tot_datas_vendas = []
    tot_prod_vendas = []
    for v in vendas:
        date_ = v.venda.data_entrega
        total_producao_diaria = VendaProduto.objects.filter(
            venda__data_entrega=date_
        ).aggregate(Sum("quantidade"))["quantidade__sum"]
        tot_dict_prod_diaria.update({date_.strftime("%Y-%m-%d"): total_producao_diaria})
        tot_datas_vendas.append(date_.strftime("%Y-%m-%d"))
        tot_prod_vendas.append(v.quantidade)

    # cria lista dos dias no período por produto id
    tot_geral_prod_diaria = 0
    tot_prod_diaria_geral = []
    for l in range(previsao_dias):
        tot_prod_diaria_geral.append(tot_geral_prod_diaria)

    # lista o total de todos os produtos a serem fabricado por dia
    datas_fabricacao = []
    for d in datas:
        for lkey, lvalue in tot_dict_prod_diaria.items():
            index = datas.index(d)
            if str(d) == lkey:
                datas_fabricacao.append(lkey)
                tot_prod_diaria_geral[index] = tot_dict_prod_diaria[lkey]

    # período base de cálculo para a programação da previsão de estoque vs produção
    meses_ = []
    for i in mp:
        for d, e in i.items():
            meses_.append(e)

    meses_periodo_extenso = []
    for i in meses_:
        meses_periodo_extenso.append(meses_extenso[i - 1])

    # lista por produto, matéria prima e quantidade comprados por data
    vlrs_amarelos = []
    for bdp in bd_produto:
        for pok, pov in posicoes2.items():
            for povk, povv in pov.items():
                # print(bdp, pok, povk, povv)
                vlrs_amarelos.append(
                    f"{bdp}/{povk}/{pok+1}/{produtos_mps_totais[povk][pok]}"
                )

    context = {
        "dias": dias_,
        "meses": meses_periodo_extenso,
        "prod_diaria": lista_prod_diaria,
        "tot_diaria": tot_prod_diaria_geral,
        "produto": bd_produto,
        "nome_materia_prima": lista_mp_final_por_produto,
        "materia_prima": produtos_mps_totais,
        "vlrs_amarelos": vlrs_amarelos,
    }
    return render(request, template_name, context)


def previsaoEstoque(request):
    template_name = "producao/previsaoEstoque.html"
    bd_produto = Produto.objects.all()

    # dias de produção a serem estimados
    previsao_dias = 35
    today = date.today()
    meses_extenso = (
        "Janeiro",
        "Fevereiro",
        "Março",
        "Abril",
        "Maio",
        "Junho",
        "Julho",
        "Agosto",
        "Setembro",
        "Outubro",
        "Novembro",
        "Dezembro",
    )

    # lista os meses referentes ao período 'previsao_dias'
    datas = []
    dias_ = []
    dia = []
    mp = []
    for i in range(previsao_dias):
        dia = today + timedelta(i)
        datas.append(dia.strftime("%Y-%m-%d"))
        dias_.append(dia.day)
        var = {dia.year: dia.month}
        if not var in mp:
            mp.append({dia.year: dia.month})

    # lista dos produtos e suas matérias primas e quantidades para sua fabricação
    producao_diaria = LimiteProducaoDiaria.objects.all()
    # lista da quantidade de cada produto a se produzido
    lista_prod_diaria = {}
    # mp_usadas = {}
    mp_usadas = []
    for pd in producao_diaria:
        pmp = ProdutosMatPri.objects.filter(prod__nome=pd.produto)
        mp_usada = {}

        for p in pmp:
            if p.prod.nome == pd.produto.nome:
                sum_mp = p.quant * pd.quantidade
                mp_usada.update({p.mp.materiaprima.nome: int(sum_mp)})
                quantidade = []
                for l in range(previsao_dias):
                    quantidade.append(pd.quantidade)
                lista_prod_diaria.update({p.prod.nome: quantidade})
        mp_usadas.append(mp_usada)

    # lista com a soma das matérias primas utilizadas para a produção da quantidade de produtos informados
    consumo_mp = dict(
        functools.reduce(operator.add, map(collections.Counter, mp_usadas))
    )

    # estoque atual de matérias primas
    estoque_atual = EstoqueMateriaPrima.objects.all()

    materias_primas_geral = {}
    # insere a quantidade de cada matéria prima no materias_primas_geral
    for ea in estoque_atual:
        materias_primas_geral.update({ea.materiaprima.nome: int(ea.qtde)})

    # cria lista dos dias no período por produto id
    tot_diaria_prods = LimiteProducaoDiaria.objects.all().aggregate(Sum("quantidade"))[
        "quantidade__sum"
    ]

    # posição, produto, quantidade comprada, na posição da data correspondente
    mpCompras = CompraMateriaPrima.objects.filter(compra__previsaoentrega__gte=today)
    quantMpCompras = {}
    for mpc in mpCompras:
        quantMpCompras.update(
            {mpc.compra.previsaoentrega: {mpc.produto.nome: mpc.quantidade}}
        )

    estoque = materias_primas_geral
    produtos_mps_totais = {}

    posicoes = {}
    # organiza as posições das quantidades de matérias primas correspondente as datas
    for key, value in estoque.items():
        vls = []
        tot_prod_diaria_geral = []
        for d in range(len(dias_)):  # 1-35
            tot_prod_diaria_geral.append(tot_diaria_prods)
            dia = today + timedelta(d)

            # lista matéria prima e quantidade na posição correspondente a previsão de entrega
            poprodquant = {}
            for mpcom in mpCompras:
                if dia == mpcom.compra.previsaoentrega:
                    poprodquant.update({d: mpcom.quantidade})
                    posicoes.update({mpcom.produto.nome: poprodquant})

            # se produto e posição iguais, soma ao valor correspondente no estoque
            quantEstoque = 0
            for qmpck, qmpcv in quantMpCompras.items():
                for qmpcvk, qmpcvv in qmpcv.items():
                    if dia == qmpck and qmpcvk == key:
                        quantEstoque = qmpcvv

            estoqueComCompras = quantEstoque + estoque[key]
            if key in consumo_mp:
                calc = estoqueComCompras - consumo_mp[key]
            else:
                calc = estoqueComCompras
            vls.append(calc)
            estoque.update({key: calc})
        produtos_mps_totais.update({key: vls})

    # cria um dicionário (dict_produtos_mp) com todos os produtos cadastrados
    tot_prods = Produto.objects.all()
    tot_produtos = []
    dict_produtos_mp = {}
    for i in tot_prods:
        tot_produtos.append(i.nome)
        dict_produtos_mp.update({i.nome: materias_primas_geral})

    # lista o que cada produto utiliza de matérias primas e a quantidade necessária para produção
    listaprodutos = ProdutosMatPri.objects.all()

    # cria um dicionário por produto, matéria prima e sua quantidade
    list_prod = {}
    for bdp in tot_produtos:
        mp_produtos = {}
        for l in listaprodutos:
            if bdp == l.prod.nome:
                mp_produtos.update({l.mp.materiaprima.nome: l.quant})
        list_prod.update({bdp: mp_produtos})

    lista_mp_final_por_produto = {}
    for k, v in list_prod.items():
        mps_por_prod = {}
        for ka, va in v.items():
            mps_por_prod.update({ka: int(va)})
        lista_mp_final_por_produto.update({k: mps_por_prod})

    # período base de cálculo para a programação da previsão de estoque vs produção
    meses_ = []
    for i in mp:
        for d, e in i.items():
            meses_.append(e)

    meses_periodo_extenso = []
    for i in meses_:
        meses_periodo_extenso.append(meses_extenso[i - 1])

    # lista por produto, matéria prima e quantidade comprados por data
    vlrs_amarelos = []
    for bdp in bd_produto:
        for pok, pov in posicoes.items():
            for povk, povv in pov.items():
                vlrs_amarelos.append(
                    f"{bdp}/{pok}/{povk+1}/{produtos_mps_totais[pok][povk]}"
                )

    formsetFactory = modelformset_factory(
        LimiteProducaoDiaria, form=QuantidadeProducaoForm, extra=0
    )
    if request.method == "POST":
        formset = formsetFactory(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect("producao:previsaoEstoque")
        else:
            context = {
                "formset": formset,
                "dias": dias_,
                "meses": meses_periodo_extenso,
                "prod_diaria": lista_prod_diaria,
                "tot_diaria": tot_prod_diaria_geral,
                "produto": bd_produto,
                "nome_materia_prima": lista_mp_final_por_produto,
                "materia_prima": produtos_mps_totais,
                "vlrs_amarelos": vlrs_amarelos,
            }
            return render(request, template_name, context)
    else:
        formset = formsetFactory()
        context = {
            "formset": formset,
            "dias": dias_,
            "meses": meses_periodo_extenso,
            "prod_diaria": lista_prod_diaria,
            "tot_diaria": tot_prod_diaria_geral,
            "produto": bd_produto,
            "nome_materia_prima": lista_mp_final_por_produto,
            "materia_prima": produtos_mps_totais,
            "vlrs_amarelos": vlrs_amarelos,
        }
        return render(request, template_name, context)


# lista dos produtos a serem fabricados agrupados por produto
def relatorioProducao(request):
    producao_base = ProdutoAcabado.objects.all()
    produto = []

    for prod in producao_base:
        if not prod.produto in produto:
            produto.append(prod.produto)

    context = {"producao": producao_base, "produto": produto}
    template_name = "producao/imprimirProducao.html"

    return render(request, template_name, context)


# lista dos produtos a serem fabricados agrupados por venda
def relatorioVenda(request):
    producao_base = ProdutoAcabado.objects.all()
    venda = []

    for prod in producao_base:
        if not prod.produto in venda:
            venda.append(prod.produto)

    context = {"producao": producao_base, "venda": venda}
    template_name = "producao/imprimirVenda.html"

    return render(request, template_name, context)
