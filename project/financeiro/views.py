import csv
from datetime import date, datetime, timedelta
from django.utils import timezone
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.urls import reverse_lazy as _
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import (
    OuterRef,
    Subquery,
    Sum,
)


from .models import (
    ContaReceber,
    ContaPagar,
    Comissao,
    ControleExtratosBancarios,
    ExtratoBancario,
)
from .forms import ComissaoForm
from financeiro.models import DadosBancarios


data_atual = date.today()


# Lista a comissão de todos os vendedores
def comissaoVendedorList(request):
    template_name = "financeiro/comisAdminVendedorList.html"
    # comissao = Comissao.objects.all()[: 100 + 500]
    comissao = Comissao.objects.all()

    vendedores = []
    for c in comissao:
        if not c.parcela.venda.vendedor in vendedores:
            vendedores.append(c.parcela.venda.vendedor)

    select_vendedor = request.GET.get("vendedores")

    if request.user.is_superuser:
        if select_vendedor:
            comissao = Comissao.objects.filter(
                parcela__venda__vendedor__username=select_vendedor
            )
            # comissao = Comissao.objects.filter(
            #     parcela__venda__vendedor__username=select_vendedor
            # )[: 100 + 500]
        mensagem = "Aguardar pagamento"
    else:
        comissao = Comissao.objects.filter(parcela__venda__vendedor=request.user)
        #     comissao = Comissao.objects.filter(parcela__venda__vendedor=request.user)[
        #         : 100 + 500
        #     ]
        mensagem = "À receber"

    # parcelas aguardando pagamento
    pagamento = 0
    # comissões pendentes de pagamento
    pendentes = 0
    # comissões recebidas
    recebidas = 0

    for mod in comissao:
        if mod.parcela.datapagamento == None:
            pagamento += mod.comissao
        else:
            if mod.data_comissao != None and mod.data_comissao <= data_atual:
                recebidas += mod.comissao
            else:
                pendentes += mod.comissao

    context = {
        "vendedores": vendedores,
        "object_list": comissao,
        "mensagem": mensagem,
        "pagamentos": pagamento,
        "pendentes": pendentes,
        "recebidos": recebidas,
    }

    return render(request, template_name, context)


class UpdateComissaoData(LoginRequiredMixin, UpdateView):
    model = Comissao
    form_class = ComissaoForm
    template_name = "financeiro/comisVendedorList.html"
    success_url = _("financeiro:comissaoVendedorList")

    def get_context_data(self, **kwargs):
        context = super(UpdateComissaoData, self).get_context_data(**kwargs)
        context["data"] = Comissao.objects.filter(pk=self.kwargs.get("pk"))
        return context


updateDataComissao = UpdateComissaoData.as_view()


class FluxodeCaixa(LoginRequiredMixin, ListView):
    model = ContaReceber


fluxodeCaixa = FluxodeCaixa.as_view()


@login_required
def ContasaPagar(request):
    template_name = "financeiro/contasPagarList.html"
    object_list = ContaPagar.objects.filter(
        datavencimento__month__in=[
            data_atual.month - 1,
            data_atual.month,
            data_atual.month + 1,
        ],
        conciliado__isnull=True,
    )

    data_ini = request.GET.get("data_ini")
    data_fim = request.GET.get("data_fim")
    if data_ini and data_fim:
        object_list = ContaPagar.objects.filter(
            datavencimento__range=[data_ini, data_fim]
        )

    vencidos = 0.00
    vencem_hoje = 0.00
    avencer = 0.00
    for valor in object_list:
        if valor.datavencimento < data_atual and valor.datapagamento == None:
            vencidos += int(valor.valor)

        if valor.datavencimento == data_atual:
            vencem_hoje += int(valor.valor)

        if valor.datavencimento > data_atual:
            avencer += int(valor.valor)

    pagas = 0.00
    for valor in object_list:
        if valor.datapagamento:
            pagas += int(valor.valor)

    context = {
        "vencidos": vencidos,
        "vencem_hoje": vencem_hoje,
        "avencer": avencer,
        "pagas": pagas,
        "data_ini": data_ini,
        "data_fim": data_fim,
        "object_list": object_list,
    }
    return render(request, template_name, context)


class ParcelaDelete(LoginRequiredMixin, DeleteView, PermissionRequiredMixin):
    model = ContaPagar
    template_name = "despesa/despesaDelete.html"
    success_url = _("despesa:despesaList")
    permission_required = "despesa.delete_despesa"


parcelaDelete = ParcelaDelete.as_view()


@login_required
def contasaReceber(request):
    template_name = "financeiro/contasReceberList.html"
    object_list = ContaReceber.objects.filter(
        datavencimento__month__in=[
            data_atual.month - 1,
            data_atual.month,
            data_atual.month + 1,
        ],
        conciliado__isnull=True,
    )

    data_ini = request.GET.get("data_ini")
    data_fim = request.GET.get("data_fim")
    if data_ini and data_fim:
        object_list = ContaReceber.objects.filter(
            datavencimento__range=[data_ini, data_fim]
        )

    vencidos = 0.00
    vencem_hoje = 0.00
    avencer = 0.00
    for valor in object_list:
        if valor.datavencimento < data_atual and valor.datapagamento == None:
            vencidos += int(valor.valor)

        if valor.datavencimento == data_atual:
            vencem_hoje += int(valor.valor)

        if valor.datavencimento > data_atual:
            avencer += int(valor.valor)

    recebidos = 0.00
    for valor in object_list:
        if valor.datapagamento:
            recebidos += int(valor.valor)

    context = {
        "recebidos": recebidos,
        "avencer": avencer,
        "vencidos": vencidos,
        "vencem_hoje": vencem_hoje,
        "data_ini": data_ini,
        "data_fim": data_fim,
        "object_list": object_list,
    }
    return render(request, template_name, context)


@login_required
def extratoUpload(request):
    template_name = "financeiro/extratoUpload.html"
    extrato = ""
    context = {}

    # dados do controle
    csv_file = []
    csv_data = []
    numConta = 0
    # se última data do extrato for menor que hoje
    extrato_defasado = []
    if request.method == "POST":
        csv_file = "arquivo" in request.FILES and request.FILES["arquivo"]

        # Verifica se é um arquivo CSV
        if not csv_file.name.endswith(".csv"):
            messages.error(
                request,
                "O arquivo enviado não é um CSV. Por favor, envie um arquivo com a extensão .csv.",
            )
            return redirect(request.path_info)  # Recarrega a página

        # Processamento do arquivo CSV
        decoded_file = csv_file.read().decode("ISO-8859-1")
        csv_reader = csv.reader(decoded_file.splitlines())
        for row in csv_reader:
            csv_data.append(row)

        periodo = []
        dataExtrato = []
        atualizacao = []
        saldo_dia = 0

        # Lista as movimentações diárias extrato Itaú
        for x in csv_data:
            # salva o último saldo do extrato
            if x[:11][1] == "SALDO DO DIA":
                base = x[:11][4]
                saldo_dia = base.replace(",", ".")

            c = "Conta:"
            # retorna o número da conta
            if c in x:
                numConta = x[1]

            a = "Atualiza??o:"
            # retorna data/hora da atualizacao
            if a in x:
                atualizacao.append(x[1])

                di = x[1][:2]
                me = x[1][3:5]
                an = x[1][6:10]
                date = f"{int(an)}-{int(me)}-{int(di)}"
                d = datetime.strptime(date, "%Y-%m-%d")
                data_ = d.date()

                dataExtrato.append(f"{x[1][:10]} {x[1][-9:-1]}")

                # se última data do extrato for menor que hoje
                if data_atual > data_:
                    dias = (data_atual - data_).days
                    extrato_defasado.append(f"Extrato defasado há {dias} dias")
                    # print(f"Extrato defasado há {dias} dias")

            p = "Periodo:"
            # retorna data início fim do extrato
            if p in x:
                periodo.append(x[1])

        datahora = datetime.strptime(dataExtrato[0], "%d/%m/%Y %H:%M:%S")
        datahora = timezone.make_aware(datahora, timezone.get_default_timezone())

        try:
            # verifica se a conta está cadastrada
            conta = DadosBancarios.objects.get(conta=numConta)
            controle = ControleExtratosBancarios.objects.get(
                datahora=datahora, conta=conta
            )
            messages.error(
                request,
                "O upload desse extrato já foi realizado",
            )
        except ControleExtratosBancarios.DoesNotExist:
            controle = ControleExtratosBancarios.objects.create(
                responsavel=request.user,
                arquivo=csv_file,
                datahora=datahora,
                conta=conta,
                saldo=saldo_dia,
            )

            for x in csv_data:
                # dados do extrato
                if len(x[0]) == 10:

                    # a = x[0]
                    # dia = a[:2]
                    # mes = a[3:5]
                    # ano = a[6:10]
                    # data = datetime(int(ano), int(mes), int(dia))
                    # d = datetime.strptime(x[0], "%d/%m/%Y")
                    # data = d.date()

                    a = x[0]
                    dia = a[:2]
                    mes = a[3:5]
                    ano = a[6:10]
                    date = f"{int(ano)}-{int(mes)}-{int(dia)}"
                    d = datetime.strptime(date, "%Y-%m-%d")
                    data = d.date()

                    lancamento = x[1]
                    origem = x[2]
                    if x[3]:
                        valor = float(x[3].replace(",", "."))
                    else:
                        valor = None
                    # if x[4]:
                    #     saldo_extrato = float(x[4].replace(",", "."))
                    # else:
                    #     saldo_extrato = None
                    # Verifica se já existe um extrato com os mesmos valores
                    if not ExtratoBancario.objects.filter(
                        data=data, lancamento=lancamento, origem=origem, valor=valor
                    ).exists():
                        if lancamento != "SALDO DO DIA":
                            ExtratoBancario.objects.create(
                                controle=controle,
                                data=data,
                                lancamento=lancamento,
                                origem=origem,
                                valor=valor,
                            )
                        extrato = ExtratoBancario.objects.all()[:50]
        except DadosBancarios.DoesNotExist:
            messages.error(
                request,
                f"Conta {numConta} não cadastrada",
            )
    conta = ControleExtratosBancarios.objects.all()

    try:
        conta = ControleExtratosBancarios.objects.latest("id")
    except:
        pass

    if extrato_defasado:
        extrato_defasado = extrato_defasado[0]

    context = {
        "csv_data": csv_data,
        "conta": conta,
        "extrato": extrato,
        "extrato_defasado": extrato_defasado,
    }
    return render(request, template_name, context)


@login_required
def extratoConciliar(request):
    template_name = "financeiro/extratoconciliar.html"
    # extrato = ExtratoBancario.objects.all().order_by("id")
    extrato = ExtratoBancario.objects.filter(
        valor__isnull=False, conciliado__isnull=True
    )
    context = {"extrato": extrato}
    return render(request, template_name, context)


def conciliarSalvarAjax(request):
    if request.method == "POST":
        id_url_page = request.POST.get("id_url_page")
        id_linha = request.POST.get("id_linha")
        id = id_linha.replace(".", "")

        try:
            # Realize as operações necessárias aqui
            lancamento = ExtratoBancario.objects.get(id=id)
            lancamento.conciliado = datetime.now()
            lancamento.save()

            if lancamento.valor < 0:
                conta = ContaPagar.objects.get(id=id_url_page)
                conta.conciliado = lancamento
                conta.valor_pago = -(lancamento.valor)
                conta.datapagamento = lancamento.data
                conta.save()
            else:
                conta = ContaReceber.objects.get(id=id_url_page)
                conta.conciliado = lancamento
                conta.valor_pago = lancamento.valor
                conta.datapagamento = lancamento.data
                conta.save()

            # Retorna uma resposta de sucesso
            return JsonResponse({"success": True})

        except Exception as e:
            # Se houver algum erro, retorne uma resposta de erro com uma mensagem apropriada
            return JsonResponse({"success": False, "error_message": str(e)}, status=500)


@login_required
def conciliarContaPagar(request, id):
    template_name = "financeiro/conciliarLancamento.html"
    conta_a_pagar = ContaPagar.objects.filter(id=id)
    mensagem = ""
    extrato = ""
    conta = ""
    for cp in conta_a_pagar:
        data_inicio = cp.datavencimento - timedelta(days=10)
        data_fim = cp.datavencimento + timedelta(days=10)
        menor_valor = -(cp.valor - 100)
        maior_valor = -(cp.valor + 100)
        extrato = ExtratoBancario.objects.filter(
            data__range=(data_inicio, data_fim),
            valor__gte=maior_valor,
            valor__lte=menor_valor,
        )

        inicio = data_inicio.strftime("%d/%m/%y")
        fim = data_fim.strftime("%d/%m/%y")
        if not extrato:
            mensagem = f"Não há lançamentos entre as datas {inicio} a {fim} cujos valores estejam entre R$ {menor_valor} e R$ {maior_valor}"

    conta = conta_a_pagar
    pagar = True
    context = {"extrato": extrato, "mensagem": mensagem, "conta": conta, "pagar": pagar}

    return render(request, template_name, context)


@login_required
def conciliarContaReceber(request, id):
    template_name = "financeiro/conciliarLancamento.html"
    conta_a_receber = ContaReceber.objects.filter(id=id)
    mensagem = ""
    extrato = ""
    conta = ""
    for cp in conta_a_receber:
        data_inicio = cp.datavencimento - timedelta(days=10)
        data_fim = cp.datavencimento + timedelta(days=10)
        menor_valor = cp.valor - 100
        maior_valor = cp.valor + 100
        extrato = ExtratoBancario.objects.filter(
            data__range=(data_inicio, data_fim),
            valor__gte=menor_valor,
            valor__lte=maior_valor,
        )

        inicio = data_inicio.strftime("%d/%m/%y")
        fim = data_fim.strftime("%d/%m/%y")
        if not extrato:
            mensagem = f"Não há lançamentos entre as datas {inicio} a {fim} cujos valores estejam entre R$ {menor_valor} e R$ {maior_valor}"

    conta = conta_a_receber
    receber = True
    context = {
        "extrato": extrato,
        "mensagem": mensagem,
        "conta": conta,
        "receber": receber,
    }

    return render(request, template_name, context)


@login_required
def fluxoCaixaExtratoBancario(request):
    # datas da pesquisa
    data_ini = request.GET.get("data_ini")
    data_fim = request.GET.get("data_fim")
    object_list = []

    if data_ini and data_fim:
        data_ini_ = datetime.strptime(data_ini, "%Y-%m-%d")
        data_fim_ = datetime.strptime(data_fim, "%Y-%m-%d")

        # Subquery para pegar o último registro de cada conta
        bd_saldo = (
            ControleExtratosBancarios.objects.filter(
                conta=OuterRef("conta"), datahora__lte=(data_fim_ + timedelta(days=1))
            )
            .order_by("-datahora")
            .values("id")[:1]
        )

        # Query principal que anota com a última datahora até `data_fim` e filtra
        ultimos_extratos_por_conta = ControleExtratosBancarios.objects.filter(
            id__in=Subquery(bd_saldo)
        )

        # Soma do saldo atual de todas as contas
        saldo_hoje = ultimos_extratos_por_conta.aggregate(Sum("saldo"))

        # Consulta para somar o campo 'valor' com as condições especificadas
        bd_a_receber = ContaReceber.objects.filter(
            datapagamento__isnull=True,
            valor_pago=0,
            datavencimento__gte=data_ini,
            datavencimento__lte=data_fim,
        ).aggregate(Sum("valor"))

        # arecebervencidos => soma os valores que não possuem data de pagamento e nem valor pago, filtrados entre data_ini e data_fim
        # exemplo: há dois valores um dia 10(data_ini) outro dia 11(data_fim) sendo ambos abaixo da data_atual e não houver registro do pagamento
        bd_areceber_vencidas = ContaReceber.objects.filter(
            datapagamento__isnull=True,
            valor_pago=0,
            datavencimento__gte=data_ini,
            datavencimento__lt=data_fim,
        ).aggregate(Sum("valor"))

        # A Pagar => soma dos valores ContaPagar ainda não conciliados
        bd_a_pagar = ContaPagar.objects.filter(
            datapagamento__isnull=True,
            valor_pago=0,
            datavencimento__gte=data_ini,
            datavencimento__lte=data_fim,
        ).aggregate(Sum("valor"))

        # apagarvencidos => soma os valores que não possuem data de pagamento e nem valor pago, filtrados entre data_ini e data_fim
        bd_apagar_vencidas = ContaPagar.objects.filter(
            datapagamento__isnull=True,
            valor_pago=0,
            datavencimento__gte=data_ini,
            datavencimento__lt=data_fim,
        ).aggregate(Sum("valor"))

        """     
        dia => datas vencimento ContaPagar e ContaReceber
        saldo => soma dos últimos saldos de cada conta até a data_fim
        a receber => soma dos valores de ContaReceber no dia
        a pagar => soma dos valores de ContaPagar no dia
        balanco => (saldo + a receber) - a pagar
        """

        dias = (data_fim_ - data_ini_).days + 1
        for i in range(dias):
            dia = data_ini_ + timedelta(days=i)
            dia = dia.date()

        # Obtenha todas as datas de vencimento de ContaReceber e ContaPagar
        datas_vencimento = list(
            ContaReceber.objects.values_list("datavencimento", flat=True).distinct()
        ) + list(ContaPagar.objects.values_list("datavencimento", flat=True).distinct())

        # Converta para datetime, se necessário, e filtre as datas no intervalo
        datas_vencimento = [
            datetime.strptime(data, "%d/%m/%y") if isinstance(data, str) else data
            for data in datas_vencimento
        ]

        # Filtrar datas entre data_ini e data_fim
        datas_filtradas = [
            data
            for data in datas_vencimento
            if data_ini_.date() <= data <= data_fim_.date()
        ]

        # Remover duplicatas e ordenar
        datas_filtradas = sorted(set(datas_filtradas))

        # Se precisar retornar as datas em formato string
        datas_filtradas_str = [data.strftime("%Y-%m-%d") for data in datas_filtradas]

        for dia in datas_filtradas_str:
            # Subconsulta para obter o último `datahora` de cada conta antes do dia especificado
            subquery = (
                ControleExtratosBancarios.objects.filter(
                    conta=OuterRef("conta"), datahora__lt=dia
                )
                .order_by("-datahora")
                .values("datahora")[:1]
            )

            # Filtra os registros que têm `datahora` igual à subconsulta (o último `datahora` para cada conta)
            last_entries = ControleExtratosBancarios.objects.filter(
                datahora=Subquery(subquery)
            )

            # Agrega o saldo desses registros
            saldo = last_entries.aggregate(total=Sum("saldo"))["total"] or 0

            receber = (
                ContaReceber.objects.filter(valor_pago=0, datavencimento=dia).aggregate(
                    total=Sum("valor")
                )["total"]
                or 0
            )
            pagar = (
                ContaPagar.objects.filter(valor_pago=0, datavencimento=dia).aggregate(
                    total=Sum("valor")
                )["total"]
                or 0
            )
            object_list.append(
                {
                    "dia": dia,
                    "saldo": saldo,
                    "a_receber": receber,
                    "a_pagar": pagar,
                    "balanco": (saldo + receber) - pagar,
                }
            )

    else:
        # Subquery para pegar o último registro de cada conta
        bd_saldo = (
            ControleExtratosBancarios.objects.filter(conta=OuterRef("conta"))
            .order_by("-datahora")
            .values("id")[:1]
        )

        # Query principal que anota com a última datahora e filtra
        ultimos_extratos_por_conta = ControleExtratosBancarios.objects.filter(
            id__in=Subquery(bd_saldo)
        )

        # Soma do saldo atual de todas as contas
        saldo_hoje = ultimos_extratos_por_conta.aggregate(Sum("saldo"))

        # A Receber => soma dos valores ContaReceber ainda não conciliados e não vencidos (excluídos com data de vencimento menor que data_atual )
        bd_a_receber = ContaReceber.objects.filter(
            datapagamento__isnull=True, valor_pago=0, datavencimento__gte=data_atual
        ).aggregate(Sum("valor"))

        # Vencidos => soma os valores sem data de pagamento e valor pago, filtrado até a data atual
        bd_areceber_vencidas = ContaReceber.objects.filter(
            datapagamento__isnull=True, valor_pago=0, datavencimento__lt=data_atual
        ).aggregate(Sum("valor"))

        # A Pagar => soma dos valores ContaPagar ainda não conciliados
        bd_a_pagar = ContaPagar.objects.filter(
            datapagamento__isnull=True, valor_pago=0
        ).aggregate(Sum("valor"))

        # Vencidos => soma os valores sem data de pagamento e valor pago, filtrado até a data atual
        bd_apagar_vencidas = ContaPagar.objects.filter(
            datapagamento__isnull=True, valor_pago=0, datavencimento__lt=data_atual
        ).aggregate(Sum("valor"))

        # Obtenha todas as datas de vencimento de ContaReceber e ContaPagar
        datas_vencimento = list(
            ContaReceber.objects.values_list("datavencimento", flat=True).distinct()
        ) + list(ContaPagar.objects.values_list("datavencimento", flat=True).distinct())

        datas_vencimento = sorted(
            list(set(datas_vencimento))
        )  # Remover duplicatas e ordenar

        for dia in datas_vencimento:
            # Subconsulta para obter o último `datahora` de cada conta antes do dia especificado
            subquery = (
                ControleExtratosBancarios.objects.filter(
                    conta=OuterRef("conta"), datahora__lt=dia
                )
                .order_by("-datahora")
                .values("datahora")[:1]
            )

            # Filtra os registros que têm `datahora` igual à subconsulta (o último `datahora` para cada conta)
            last_entries = ControleExtratosBancarios.objects.filter(
                datahora=Subquery(subquery)
            )

            # Agrega o saldo desses registros
            saldo = last_entries.aggregate(total=Sum("saldo"))["total"] or 0

            receber = (
                ContaReceber.objects.filter(valor_pago=0, datavencimento=dia).aggregate(
                    total=Sum("valor")
                )["total"]
                or 0
            )
            pagar = (
                ContaPagar.objects.filter(valor_pago=0, datavencimento=dia).aggregate(
                    total=Sum("valor")
                )["total"]
                or 0
            )
            object_list.append(
                {
                    "dia": dia,
                    "saldo": saldo,
                    "a_receber": receber,
                    "a_pagar": pagar,
                    "balanco": (saldo + receber) - pagar,
                }
            )

    # precisa retornar a soma dos últimos saldos de cada conta cuja data esteja entre data_ini e data_fim

    # Extraindo o valor total da soma
    saldo_hoje = saldo_hoje["saldo__sum"]

    # Extraindo o valor total da soma
    areceber_vencidas = bd_areceber_vencidas["valor__sum"]

    # verifica se bd_a_receber["valor__sum"] ou areceber_vencidas tem valor None e atribui valor para não quebrar o cálculo
    a_receber = (
        bd_a_receber["valor__sum"] if bd_a_receber["valor__sum"] is not None else 0
    )
    areceber_vencidas = areceber_vencidas if areceber_vencidas is not None else 0

    if a_receber > areceber_vencidas:
        a_receber = (
            a_receber - areceber_vencidas if areceber_vencidas is not None else 0
        )

    # verifica se bd_a_pagar["valor__sum"] ou apagar_vencidas tem valor None e atribui valor para não quebrar o cálculo
    a_pagar = bd_a_pagar["valor__sum"] if bd_a_pagar["valor__sum"] is not None else 0
    apagar_vencidas = (
        bd_apagar_vencidas["valor__sum"]
        if bd_apagar_vencidas["valor__sum"] is not None
        else 0
    )

    if a_pagar > apagar_vencidas:
        a_pagar = (
            (a_pagar + 25000) - apagar_vencidas if apagar_vencidas is not None else 0
        )

    if not saldo_hoje:
        saldo_hoje = 0

    balanco = (saldo_hoje + a_receber) - a_pagar

    template_name = "financeiro/fluxodecaixaextratobancario.html"

    context = {
        "data_ini": data_ini,
        "data_fim": data_fim,
        "saldo": saldo_hoje,
        "areceber": a_receber,
        "areceber_vencidas": areceber_vencidas,
        "apagar": a_pagar,
        "apagar_vencidas": apagar_vencidas,
        "balanco": balanco,
        "object_list": object_list,
    }
    return render(request, template_name, context)
