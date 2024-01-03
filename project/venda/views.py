import datetime
import calendar
from django.urls import reverse_lazy as _
from django.shortcuts import redirect, render
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.db.models import Sum, Count
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import DeleteView

from .models import CondicaoVenda, Venda, VendaProduto, MaximoDesconto
from .forms import AnoForm, VendaForm, VendaProdutoForm

from produto.models import Produto
from financeiro.models import ContaReceber
from financeiro.forms import VendaContaReceberForm
from producao.models import LimiteProducaoDiaria


success_url_venda = _("venda:vendaList")
template_name_createupdate = "venda/vendaCreateUpdate.html"
today = datetime.date.today()


# venda  --------------------------------------------------------------------
class VendaList(LoginRequiredMixin, ListView):
    model = Venda
    template_name = "venda/vendaList.html"


vendaList = VendaList.as_view()


class VendaDetails(LoginRequiredMixin, DetailView):
    model = Venda
    template_name = "venda/vendaDetails.html"


vendaDetails = VendaDetails.as_view()


class VendaDelete(LoginRequiredMixin, DeleteView):
    model = Venda
    template_name = "venda/vendaDelete.html"
    success_url = success_url_venda

    def get(self, request, *args, **kwargs):
        if self.get_object().status_venda == "enviado":
            print("tem elemento")
            self.object = self.get_object()
            context = self.get_context_data(object=self.object)
            self.template_name = "venda/vendaRestrict.html"
            return self.render_to_response(context)
            # tem elemento, nao posso excluir
        else:
            self.object = self.get_object()
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)


vendaDelete = VendaDelete.as_view()


def produtoPrecoAjax(request):
    produto = request.GET.get("id_produto")
    preco = Produto.objects.filter(id=produto)

    data = []
    for preco in preco:
        data = preco.preco
        return JsonResponse({"data": data})


def condicaoAjax(request):
    condicao = request.GET.get("id_condicao")
    dados = CondicaoVenda.objects.filter(id=condicao)
    pgid = 0
    info = []
    for i in dados:
        pgid = i.formapgto.pk
        info.append(
            {
                "nome": i.nome,
                "parcelas": i.parcelas,
                "primeira": i.primeira,
                "demais": i.demais,
                "forpgto": i.formapgto.nome,
                "pgid": pgid,
            }
        )
    return JsonResponse({"info": info})


@login_required
@permission_required("venda.add_venda")
def vendaCreate(request):
    form = VendaForm(request.POST or None)

    Formset_VendaProduto_Factory = inlineformset_factory(
        Venda, VendaProduto, form=VendaProdutoForm, extra=0, min_num=1, can_delete=False
    )
    produto_form = Formset_VendaProduto_Factory(request.POST or None)

    Formset_contaReceber_Factory = inlineformset_factory(
        Venda, ContaReceber, form=VendaContaReceberForm, extra=0, can_delete=False
    )
    parcela_form = Formset_contaReceber_Factory(
        request.POST or None, request.FILES or None
    )

    maximodesconto = MaximoDesconto.objects.first()
    if maximodesconto:
        maximodesconto = maximodesconto.qtde
    else:
        maximodesconto = 0

    limiteproducaodiaria = LimiteProducaoDiaria.objects.first()
    if limiteproducaodiaria:
        limiteproducaodiaria = limiteproducaodiaria.quantidade
    else:
        limiteproducaodiaria = 0

    if request.method == "POST":
        if form.is_valid() and produto_form.is_valid() and parcela_form.is_valid():
            venda = form.save(commit=False)
            venda.vendedor = str(request.user)
            venda.save()
            produto_form.instance = venda
            produto_form.save()
            parcela_form.instance = venda
            parcela_form.save()
            return redirect(_("venda:vendaList"))
        else:
            context = {
                "texto": "Novo",
                "form": form,
                "produto": produto_form,
                "parcela": parcela_form,
                "maximodesconto": maximodesconto,
                "limiteproducaodiaria": limiteproducaodiaria,
            }
            return render(request, template_name_createupdate, context)
    else:
        context = {
            "texto": "Novo",
            "form": form,
            "produto": produto_form,
            "parcela": parcela_form,
            "maximodesconto": maximodesconto,
            "limiteproducaodiaria": limiteproducaodiaria,
        }
        return render(request, template_name_createupdate, context)


@login_required
@permission_required("venda.change_venda")
def vendaUpdate(request, pk):
    objeto = get_object_or_404(Venda, pk=pk)
    form = VendaForm(request.POST or None, instance=objeto)

    Formset_VendaProduto_Factory = inlineformset_factory(
        Venda, VendaProduto, form=VendaProdutoForm, extra=0, min_num=1, can_delete=False
    )
    produto_form = Formset_VendaProduto_Factory(request.POST or None, instance=objeto)

    Formset_contaReceber_Factory = inlineformset_factory(
        Venda, ContaReceber, form=VendaContaReceberForm, extra=0, can_delete=False
    )
    parcela_form = Formset_contaReceber_Factory(
        request.POST or None, request.FILES or None, instance=objeto
    )

    maximodesconto = MaximoDesconto.objects.first()
    if maximodesconto:
        maximodesconto = maximodesconto.qtde
    else:
        maximodesconto = 0

    limiteproducaodiaria = LimiteProducaoDiaria.objects.first()
    if limiteproducaodiaria:
        limiteproducaodiaria = limiteproducaodiaria.quantidade
    else:
        limiteproducaodiaria = 0

    if request.method == "POST":
        if form.is_valid() and produto_form.is_valid() and parcela_form.is_valid():
            venda = form.save(commit=False)
            venda.vendedor = str(request.user).capitalize()
            venda.save()
            produto_form.instance = venda
            produto_form.save()
            parcela_form.instance = venda
            parcela_form.save()

            if venda.status_venda == "expedicao":
                return redirect(_("expedicao:listaExpedicao"))
            else:
                return redirect(_("venda:vendaList"))
        else:
            codigo = True
            context = {
                "id": pk,
                "texto": "Alterar",
                "codigo": codigo,
                "form": form,
                "produto": produto_form,
                "parcela": parcela_form,
                "maximodesconto": maximodesconto,
                "limiteproducaodiaria": limiteproducaodiaria,
            }
            if produto_form.errors:
                context["msgerro"] = True

            return render(request, template_name_createupdate, context)
    else:
        codigo = True
        context = {
            "id": pk,
            "texto": "Alterar",
            "pk": pk,
            "codigo": codigo,
            "form": form,
            "produto": produto_form,
            "parcela": parcela_form,
            "maximodesconto": maximodesconto,
            "limiteproducaodiaria": limiteproducaodiaria,
        }
        return render(request, template_name_createupdate, context)


@login_required
@permission_required("venda.add_venda")
def vendaClone(request, pk):
    venda_base_id = get_object_or_404(Venda, pk=pk)
    venda_base = Venda.objects.filter(pk=pk)
    cliente = venda_base_id.cliente

    venda = {}
    for vb in venda_base:
        venda.update(
            {
                "cliente": cliente,
                "transportadora": venda_base_id.transportadora,
                "status_venda": venda_base_id.status_venda,
                "valor_venda": vb.valor_venda,
                "valor_venda": vb.valor_venda,
                "porcentagem_desconto": vb.porcentagem_desconto,
                "condicaopgto": vb.condicaopgto,
                "dias_prim_par": vb.dias_prim_par,
                "dias_outras_par": vb.dias_outras_par,
                "parcelas": vb.parcelas,
                "formapgto": vb.formapgto,
                "detalhes": vb.detalhes,
            }
        )

    produto_base = VendaProduto.objects.filter(venda__pk=pk)
    prod = []
    for pb in produto_base:
        prod.append(
            {
                "produto": pb.produto,
                "quantidade": pb.quantidade,
                "preco": pb.preco,
                "subtotal": pb.subtotal,
            }
        )

    parcela_base = ContaReceber.objects.filter(venda__pk=pk)
    parc = []
    for pb in parcela_base:
        parc.append(
            {
                "parcela": pb.parcela,
                "receita": pb.receita,
                "valor": pb.valor,
                "datadocumento": pb.datadocumento,
                "datavencimento": pb.datavencimento,
                "datapagamento": pb.datapagamento,
                "formapgto": pb.formapgto,
                "detalhes": pb.detalhes,
            }
        )

    form = VendaForm(request.POST, initial=venda)

    Formset_VendaProduto_Factory = inlineformset_factory(
        Venda, VendaProduto, form=VendaProdutoForm, extra=len(prod)
    )
    produto_form = Formset_VendaProduto_Factory(request.POST or None, initial=prod)

    Formset_contaReceber_Factory = inlineformset_factory(
        Venda,
        ContaReceber,
        form=VendaContaReceberForm,
        extra=len(parc),
    )
    parcela_form = Formset_contaReceber_Factory(request.POST or None, initial=parc)

    if request.method == "POST":
        if form.is_valid() and produto_form.is_valid() and parcela_form.is_valid():
            venda = form.save(commit=False)
            venda.vendedor = str(request.user)
            venda.save()
            produto_form.instance = venda
            produto_form.save()
            parcela_form.instance = venda
            parcela_form.save()
            return redirect(_("venda:vendaList"))
        else:
            context = {
                "form": form,
                "produto": produto_form,
                "parcela": parcela_form,
            }
            return render(request, template_name_createupdate, context)
    else:
        form = VendaForm(initial=venda)
        context = {
            "form": form,
            "produto": produto_form,
            "parcela": parcela_form,
        }
        return render(request, template_name_createupdate, context)


def orcamento(request, pk):
    venda = Venda.objects.filter(pk=pk)
    produtos = VendaProduto.objects.filter(venda__pk=pk)
    prestacoes = ContaReceber.objects.filter(venda__pk=pk)

    template_path = "venda/vendaOrcamento.html"
    context = {"venda": venda, "produtos": produtos, "prestacoes": prestacoes, "pk": pk}

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'filename="orçamento{pk}.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html,
        dest=response,
    )

    if pisa_status.err:
        return HttpResponse("We had some errors <pre>" + html + "</pre>")
    return response


def relatorios(request):
    template_name = "venda/vendaCharts.html"
    # today = datetime.date.today()

    total_ano = Venda.objects.filter(data_pedido__year=today.year).aggregate(
        Sum("subtotal")
    )["subtotal__sum"]
    total_mes = (
        Venda.objects.filter(data_pedido__year=today.year)
        .filter(data_pedido__month=today.month)
        .aggregate(Sum("subtotal"))["subtotal__sum"]
    )

    vendas = Venda.objects.filter(data_pedido__year=today.year).aggregate(
        Count("subtotal")
    )["subtotal__count"]
    vendas_mes = (
        Venda.objects.filter(data_pedido__year=today.year)
        .filter(data_pedido__month=today.month)
        .aggregate(Count("subtotal"))["subtotal__count"]
    )
    produtos = VendaProduto.objects.filter(
        venda__data_pedido__year=today.year
    ).aggregate(Sum("quantidade"))["quantidade__sum"]
    produtos_mes = (
        VendaProduto.objects.filter(venda__data_pedido__year=today.year)
        .filter(venda__data_pedido__month=today.month)
        .aggregate(Sum("quantidade"))["quantidade__sum"]
    )
    if not total_ano:
        total_ano = vendas = produtos = 0

    if not total_mes:
        total_mes = vendas_mes = produtos_mes = 0

    meses = [
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
    ]

    str_month = meses[today.month - 1]
    month_next = meses[today.month]

    ano = today.year
    periodo = f"de {month_next}/{ano-1} a {str_month}/{ano}"
    mes_atual = periodo.upper()
    ano_label = str(ano)

    anos = []
    cont = 0
    for a in range(5):
        calc = ano - cont
        anos.append(str(calc))
        cont += 1

    meses = [
        "JANEIRO",
        "FEVEREIRO",
        "MARÇO",
        "ABRIL",
        "MAIO",
        "JUNHO",
        "JULHO",
        "AGOSTO",
        "SETEMBRO",
        "OUTUBRO",
        "NOVEMBRO",
        "DEZEMBRO",
    ]
    meses_lista = []
    mes = datetime.datetime.now().month + 1
    ano = datetime.datetime.now().year
    for i in range(12):
        mes -= 1
        if mes == 0:
            mes = 12
            ano -= 1
        meses_lista.append(meses[mes - 1])

    context = {
        "anos": anos,
        "ano": ano_label,
        "meses": meses_lista,
        "total_mes": total_mes,
        "total_ano": total_ano,
        "vendas": vendas,
        "vendas_mes": vendas_mes,
        "produtos": produtos,
        "produtos_mes": produtos_mes,
    }
    return render(request, template_name, context)


def total_vendido_ano(request):
    obj = Venda.objects.all()
    meses = [
        "jan",
        "fev",
        "mar",
        "abr",
        "mai",
        "jun",
        "jul",
        "ago",
        "set",
        "out",
        "nov",
        "dez",
    ]
    dados = []
    labels = []
    mes = datetime.datetime.now().month + 1
    ano = datetime.datetime.now().year
    for i in range(12):
        mes -= 1
        if mes == 0:
            mes = 12
            ano -= 1
        soma = sum(
            i.subtotal
            for i in obj
            if i.data_pedido.month == mes and i.data_pedido.year == ano
        )
        labels.append(meses[mes - 1])
        dados.append(soma)
    data_json = {"data": dados[::-1], "labels": labels[::-1]}
    return JsonResponse(data_json)


def total_vendido_mes(request):
    obj = Venda.objects.filter(data_pedido__month=today.month).filter(
        data_pedido__year=today.year
    )

    ref_dias = calendar.monthcalendar(today.year, today.month)
    dias = []
    for i in ref_dias:
        for j in i:
            if j != 0:
                data = datetime.date(year=today.year, month=today.month, day=j)
                dias.append(str(data))

    dados = []
    for i in range(len(dias)):
        data = datetime.date(year=today.year, month=today.month, day=i + 1)
        soma = sum(o.subtotal for o in obj if o.data_pedido.day == i + 1)
        dados.append(soma)

    data_json = {
        "data": dados,
        "labels": dias,
    }
    return JsonResponse(data_json)


def meses_ajax(request):
    ano = request.GET.get("ano")
    ano = int(ano)
    mes = request.GET.get("mes")

    meses = [
        "JANEIRO",
        "FEVEREIRO",
        "MARÇO",
        "ABRIL",
        "MAIO",
        "JUNHO",
        "JULHO",
        "AGOSTO",
        "SETEMBRO",
        "OUTUBRO",
        "NOVEMBRO",
        "DEZEMBRO",
    ]

    index = meses.index(mes)
    mes = index + 1

    obj = Venda.objects.filter(data_pedido__month=mes).filter(data_pedido__year=ano)

    vendas = (
        Venda.objects.filter(data_pedido__month=mes)
        .filter(data_pedido__year=ano)
        .aggregate(Count("subtotal"))["subtotal__count"]
    )
    produtos = (
        VendaProduto.objects.filter(venda__data_pedido__year=ano)
        .filter(venda__data_pedido__month=mes)
        .aggregate(Sum("quantidade"))["quantidade__sum"]
    )
    total_mes = (
        Venda.objects.filter(data_pedido__year=ano)
        .filter(data_pedido__month=mes)
        .aggregate(Sum("subtotal"))["subtotal__sum"]
    )
    # print(f"{total_mes:.2f}")
    # print("{:.2f}".format(total_mes))
    # total_mes = f"{total_mes:.2f}"
    mensagem = []
    if not total_mes:
        total_mes = vendas = produtos = 0
        mensagem = "Não há lançamento para o período!"

    ref_dias = calendar.monthcalendar(ano, mes)
    labels = []
    for i in ref_dias:
        for j in i:
            if j != 0:
                data = datetime.date(year=ano, month=mes, day=j)
                labels.append(str(data))

    dados = []
    for i in range(len(labels)):
        data = datetime.date(year=ano, month=mes, day=i + 1)
        soma = sum(o.subtotal for o in obj if o.data_pedido.day == i + 1)
        dados.append(soma)

    data_json = {
        "data": dados,
        "labels": labels,
        "vendas_mes_atual": vendas,
        "produtos_mes_atual": produtos,
        "total_mes": total_mes,
        "mensagem": mensagem,
    }

    return JsonResponse(data_json)
