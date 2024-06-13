from django.shortcuts import render
from datetime import datetime
from django.db.models import Q

from suporte.models import Suporte
from venda.models import Venda, VendaProduto
from produto.models import Produto
from django.contrib.auth.decorators import login_required


def expedicaoImprimir(request):
    """
    expedicao Imprimir
    """
    context = {}
    template_name = "expedicao/imprimir.html"

    if request.method == "POST":
        _lista_imprimir = request.POST.getlist("imprimir")
        lista_imprimir = []
        for o in _lista_imprimir:
            lista_imprimir.append(o.replace(".", ""))
        vendas = Venda.objects.filter(id__in=lista_imprimir)
        vendas.update(
            etiqueta_impressa=True,
            data_impressao=datetime.now(),
            status_expedicao="Aguardando Concluir Produtos",
        )
        context["vendas"] = vendas
        return render(request, template_name, context)


def expedicaoNFImprimir(request):
    """ """
    if request.method == "GET":
        nota = request.POST.getlist("nota")
        nota = nota.replace(",", "")
        vendas = Venda.objects.filter(id=nota)
        vendas.update(nfjaimpressa=True)
        vendas.save()


@login_required
def listaPosVendaOriginal(request):
    """
    lista Pos Venda
    """
    context = {}
    template_name = "expedicao/listarPosVenda.html"
    vendas = (
        Venda.objects.filter(codigo_mercadolivre__isnull=True)
        .filter(
            ~Q(status_posvenda__in=["Concluido"]),
            status_venda__in=["enviado"],
            status_expedicao__in=[
                "Enviado",
            ],
        )
        .order_by("-id")
    )
    context["vendas"] = vendas

    return render(request, template_name, context)


@login_required
def listaPosVendaDistribuidora(request):
    """
    lista Pos Venda
    """
    context = {}
    template_name = "expedicao/listarPosVenda.html"
    vendas = (
        Venda.objects.filter(codigo_mercadolivre__isnull=False)
        .filter(
            ~Q(status_posvenda__in=["Concluido"]),
            status_venda__in=["enviado"],
            status_expedicao__in=[
                "Enviado",
            ],
        )
        .order_by("-id")
    )
    context["vendas"] = vendas

    return render(request, template_name, context)


def atendimento(request, id):

    return


@login_required
def listaExpedicao(request):
    """
    lista Expedicao
    """
    context = {}
    template_name = "expedicao/listarExpedicao.html"

    if (
        "EXPEDICAO" in request.user.groups.values_list("name", flat=True)
        or request.user.is_superuser
    ):
        vendas = Venda.objects.filter(
            status_venda__in=["expedicao"],
            etiqueta_impressa=False,
            status_expedicao__in=[
                "Imprimir Etiqueta",
            ],
        )
    else:
        vendas = Venda.objects.filter(
            status_venda__in=["expedicao"],
            vendedor=request.user,
            etiqueta_impressa=False,
            status_expedicao__in=[
                "Imprimir Etiqueta",
            ],
        )
        # vendas = []
    # vendas =  Venda.objects.filter(id=639)#status_venda__in=['expedicao'], vendedor=request.user, etiqueta_impresa=False, status_expedicao__in=['Fazer Cotação', 'Conferir Dados', 'Aguardando Transportadora'])
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
                        if (
                            _nome == nome
                            and _voltagem == voltagem
                            and _torneira == torneira
                            and _adesivado == adesivado
                        ):
                            for vezes in range(0, _qtde):
                                nomes.append(
                                    {
                                        "nome": _venda.cliente.nome,
                                        "id": _venda.id,
                                        "vendedor": _venda.vendedor,
                                    }
                                )

                relacaoprodutos.append(
                    {
                        "nome": nome,
                        "voltagem": voltagem,
                        "torneira": torneira,
                        "adesivado": adesivado,
                        "qtde": qtde,
                        "nomes": nomes,
                    }
                )
            else:
                jaexiste = False
                for relacaoproduto in relacaoprodutos:
                    if (
                        nome == relacaoproduto["nome"]
                        and voltagem == relacaoproduto["voltagem"]
                        and torneira == relacaoproduto["torneira"]
                        and adesivado == relacaoproduto["adesivado"]
                    ):
                        jaexiste = True

                if jaexiste:
                    # so soma qtde
                    for relacaoproduto in relacaoprodutos:
                        if (
                            nome == relacaoproduto["nome"]
                            and voltagem == relacaoproduto["voltagem"]
                            and torneira == relacaoproduto["torneira"]
                            and adesivado == relacaoproduto["adesivado"]
                        ):
                            relacaoproduto["qtde"] += qtde
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
                            if (
                                _nome == nome
                                and _voltagem == voltagem
                                and _torneira == torneira
                                and _adesivado == adesivado
                            ):
                                for vezes in range(0, _qtde):
                                    nomes.append(
                                        {
                                            "nome": _venda.cliente.nome,
                                            "id": _venda.id,
                                            "vendedor": _venda.vendedor,
                                        }
                                    )

                    relacaoprodutos.append(
                        {
                            "nome": nome,
                            "voltagem": voltagem,
                            "torneira": torneira,
                            "adesivado": adesivado,
                            "qtde": qtde,
                            "nomes": nomes,
                        }
                    )
    if (
        "EXPEDICAO" in request.user.groups.values_list("name", flat=True)
        or request.user.is_superuser
    ):
        listagemvendas = Venda.objects.filter(
            Q(status_venda__in=["expedicao"])
            | Q(
                status_venda="enviado",
                data_status_expedicao__gte=datetime.now().replace(
                    hour=0, minute=0, second=0
                ),
                data_status_expedicao__lte=datetime.now().replace(
                    hour=23, minute=59, second=59
                ),
            )
        ).order_by("-urgente", "-id")
    else:
        listagemvendas = (
            Venda.objects.filter(vendedor=request.user)
            .filter(
                Q(status_venda__in=["expedicao"])
                | Q(
                    status_venda="enviado",
                    data_status_expedicao__gte=datetime.now().replace(
                        hour=0, minute=0, second=0
                    ),
                    data_status_expedicao__lte=datetime.now().replace(
                        hour=23, minute=59, second=59
                    ),
                )
            )
            .order_by("-urgente", "-id")
        )
    filtro = ""
    if request.GET.get("filtro") == "mercadolivre":
        filtro = "mercadolivre"
        listagemvendas = listagemvendas.filter(nickname_mercadolivre__isnull=False)
    elif request.GET.get("filtro") == "original":
        filtro = "original"
        listagemvendas = listagemvendas.filter(nickname_mercadolivre__isnull=True)
    # se pesquisou
    if request.POST.get("pesquisa"):
        context["pesquisa"] = pesquisa = request.POST.get("pesquisa")
        if (
            "EXPEDICAO" in request.user.groups.values_list("name", flat=True)
            or request.user.is_superuser
        ):

            # ve se e inteiro ou str
            try:
                pesquisa = int(pesquisa)
                listagemvendas = Venda.objects.filter(
                    Q(numero_nf=pesquisa)
                    | Q(id=pesquisa)
                    | Q(cliente__cnpj__icontains=pesquisa)
                    | Q(cliente__cpf__icontains=pesquisa)
                ).order_by("-urgente", "-id")
            except:

                listagemvendas = Venda.objects.filter(
                    Q(cliente__nome__icontains=pesquisa)
                    | Q(cliente__cidade__icontains=pesquisa)
                ).order_by("-urgente", "-id")

        else:
            try:
                pesquisa = int(pesquisa)
                listagemvendas = (
                    Venda.objects.filter(vendedor=request.user)
                    .filter(
                        Q(numero_nf=pesquisa)
                        | Q(id=pesquisa)
                        | Q(cliente__cnpj__icontains=pesquisa)
                        | Q(cliente__cpf__icontains=pesquisa)
                    )
                    .order_by("-urgente, " "-id")
                )
            except:
                listagemvendas = Venda.objects.filter(
                    Q(cliente__nome__icontains=pesquisa)
                    | Q(cliente__cidade__icontains=pesquisa)
                ).order_by("-urgente", "-id")

    estoquefiscal = []
    for produto in Produto.objects.filter(empresa__id=2):
        estoquefiscal.append(
            {"nome": produto.nome, "voltagem": "127", "qtde": produto.estoque_127}
        )
        estoquefiscal.append(
            {"nome": produto.nome, "voltagem": "220", "qtde": produto.estoque_220}
        )

    # agora remove tudo que vendeu pela distribuidora
    vendas = Venda.objects.filter(
        status_venda="enviado", vendedor__extenduser__empresa__id=2
    )
    for venda in vendas:
        for vendaproduto in venda.vendaproduto_set.all():
            for pos, estoque in enumerate(estoquefiscal):
                if (
                    estoque["nome"] == vendaproduto.produto.nome
                    and estoque["voltagem"] == vendaproduto.voltagem.nome
                ):
                    estoquefiscal[pos]["qtde"] -= vendaproduto.quantidade

    produtos = VendaProduto.objects.filter(venda__status_expedicao="Fazer Cotação")
    context["estoquefiscal"] = estoquefiscal
    context["vendas"] = listagemvendas
    context["cotacao"] = Venda.objects.filter(status_expedicao="Fazer Cotação")
    context["produtos"] = produtos

    # lista os ids das vendas
    ids_vendas = list(
        produtos.values_list("venda_id", flat=True).distinct().order_by("venda_id")
    )
    # lista a soma dos pesos dos produtos e a quantidade de produtos por venda
    volume_peso = []
    for id in ids_vendas:
        volume = 0
        peso = 0
        for p in produtos:
            if p.venda.id == id:
                volume += p.quantidade
                try:
                    peso += p.produto.peso * p.quantidade
                except:
                    peso += 50
                if p.produto.peso:
                    peso += p.produto.peso * p.quantidade
        volume_peso.append({"venda": id, "Volumes": volume, "Peso": peso})

    context["volume_peso"] = volume_peso
    context["bebedouros_na_expedicao"] = relacaoprodutos
    suporte = Suporte.objects.values_list("venda_id", flat=True)
    context["atendimento"] = list(suporte)
    context["data"] = Suporte.objects.filter(venda__id__in=list(suporte))
    return render(request, template_name, context)
