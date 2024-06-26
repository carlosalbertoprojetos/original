from django.urls import reverse_lazy as _
from django.shortcuts import redirect, render
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.views.generic.edit import DeleteView
from django.http import JsonResponse
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin

from datetime import datetime, timedelta
from .models import Despesa, Saldo
from .forms import DespesaForm
from financeiro.models import ContaPagar, ContaReceber
from financeiro.forms import ContaPagarForm
from django.db.models import Q

success_url_despesa = _("despesa:despesaList")
template_name_createdespesa = "despesa/despesaCreateUpdate.html"


# @login_required
def fluxodecaixa_edit_day_ajax(request):
    """ """
    id = request.GET.get("id")
    delta = request.GET.get("delta")

    tipo, id, pai = id.split("_")
    # self.end_date = self.start_date + datetime.timedelta(days=self.duration)

    if tipo in ["despesa", "compra"]:
        conta = ContaPagar.objects.get(id=id)
    elif tipo in ["receita", "venda"]:
        conta = ContaReceber.objects.get(id=id)

    conta.datavencimento = conta.datavencimento + timedelta(int(delta))
    conta.save()

    data = {}
    return JsonResponse(data, safe=False)


@login_required
def fluxodecaixa_eventos_ajax(request):
    """
    retorna as contas a receber e contas a pagar
    alem disso calcula se após pagar as contas o dia fica com o
    saldo positivo ou negativo
    """
    import locale

    locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")
    hoje = datetime.now()
    contas_a_pagar = ContaPagar.objects.all()
    contas_a_receber = ContaReceber.objects.all()
    data = []

    _saldo = Saldo.objects.first()
    if _saldo:
        saldo = _saldo.saldo
        limite = _saldo.limite
    else:
        saldo = 0
        limite = 0
    hoje = datetime.now()
    hoje = hoje.replace(day=1)
    calculo_dias = 60
    for delta in range(0, calculo_dias):
        # calcula o saldo ao longo de x(calculo_dias)
        _dia = hoje + timedelta(delta)
        for conta in ContaPagar.objects.filter(
            Q(datavencimento=_dia) | Q(datapagamento=_dia)
        ):
            if conta.datapagamento:
                if conta.datapagamento == _dia.date():
                    saldo -= float(conta.valor)
            else:
                saldo -= float(conta.valor)
        for conta in ContaReceber.objects.filter(
            Q(datavencimento=_dia) | Q(datapagamento=_dia)
        ):
            if conta.datapagamento:
                if conta.datapagamento == _dia.date():
                    saldo += float(conta.valor)
            else:
                saldo += float(conta.valor)

        if request.user.has_perm("financeiro.view_contareceber"):
            valor = locale.currency(saldo, grouping=True, symbol=None)
            dicionario = {
                "id": 1,
                "title": "saldo: R$ " + valor,
                "start": _dia.strftime("%Y-%m-%dT08:%M:%S"),
                "constraint": "businessHours",
                "color": "blue",
            }
            data.append(dicionario)

            if saldo > 0:
                color = "#e0fee0"
            elif saldo < limite:
                color = "#ffc6bd"
            elif saldo < 0:
                color = "#ffff70"
            else:
                color = "white"

            dia = {
                "start": _dia.strftime("%Y-%m-%d"),
                "end": _dia.strftime("%Y-%m-%d"),
                "overlap": False,
                "display": "background",
                "color": color,
            }
            data.append(dia)
    if request.user.has_perm("financeiro.view_contapagar"):
        for conta in contas_a_pagar:
            if conta.despesa:
                titulo = conta.despesa.nome
                tipo = "despesa"
                pai = conta.despesa.id
            else:
                titulo = conta.compra.fornecedor.nome
                tipo = "compra"
                pai = conta.compra.id
            valor = locale.currency(conta.valor, grouping=True, symbol=None)
            if conta.datapagamento:
                start = conta.datapagamento.strftime("%Y-%m-%dT09:%M:%S")
            else:
                start = conta.datavencimento.strftime("%Y-%m-%dT09:%M:%S")

            dicionario = {
                "id": tipo + "_" + str(conta.id) + "_" + str(pai),
                "title": titulo + " R$ " + valor,
                "start": start,
                "constraint": "businessHours",
                "color": "red",
            }
            if conta.datapagamento:
                dicionario["className"] = "underline"
            data.append(dicionario)

    if request.user.has_perm("financeiro.view_contareceber"):
        for conta in contas_a_receber:
            if conta.receita:
                titulo = conta.receita.nome
                tipo = "receita"
                pai = conta.receita.id
            else:
                titulo = conta.venda.cliente.nome
                tipo = "venda"
                pai = conta.venda.id

            valor = locale.currency(conta.valor, grouping=True, symbol=None)

            if conta.datapagamento:
                start = conta.datapagamento.strftime("%Y-%m-%dT09:%M:%S")
            else:
                start = conta.datavencimento.strftime("%Y-%m-%dT09:%M:%S")

            dicionario = {
                "id": tipo + "_" + str(conta.id) + "_" + str(pai),
                "title": titulo + " R$ " + valor,
                "start": start,
                "constraint": "businessHours",
                "color": "green",
                "className": "",
            }
            if conta.datapagamento:
                dicionario["className"] = "underline"
            data.append(dicionario)
    data2 = [
        {
            "title": "Business Lunch",
            "start": "2023-05-15T13:00:00",
            "constraint": "businessHours",
        },
        {
            "title": "Meeting",
            "start": "2023-01-13T11:00:00",
            "constraint": "availableForMeeting",
            "color": "#257e4a",
        },
        {"title": "Conference", "start": "2023-01-18", "end": "2023-01-20"},
        {"title": "Party", "start": "2023-01-29T20:00:00"},
        {
            "groupId": "availableForMeeting",
            "start": "2023-01-11T10:00:00",
            "end": "2023-01-11T16:00:00",
            "display": "background",
        },
        {
            "groupId": "availableForMeeting",
            "start": "2023-01-13T10:00:00",
            "end": "2023-01-13T16:00:00",
            "display": "background",
        },
        {
            "start": "2023-01-24",
            "end": "2023-01-24",
            "overlap": False,
            "display": "background",
            "color": "#ff9f89",
        },
        {
            "start": "2023-01-06",
            "end": "2023-01-08",
            "overlap": False,
            "display": "background",
            "color": "#ff9f89",
        },
    ]
    if len(data) == 1:
        data = data[0]

    return JsonResponse(data, safe=False)


@login_required
@permission_required("despesa.add_despesa")
def despesaCreate(request):
    titulo = "Nova Despesa"
    form = DespesaForm(request.POST or None, request.FILES or None)
    Formset_contaPagar_Factory = inlineformset_factory(
        Despesa, ContaPagar, form=ContaPagarForm, min_num=1, extra=0, can_delete=False
    )
    parcela_form = Formset_contaPagar_Factory(
        request.POST or None, request.FILES or None
    )

    if request.method == "POST":
        if form.is_valid() and parcela_form.is_valid():
            despesa = form.save()
            parcela_form.instance = despesa
            parcela_form.save()
            return redirect(success_url_despesa)
        else:
            context = {
                "titulo": titulo,
                "form": form,
                "parcela": parcela_form,
            }
            return render(request, template_name_createdespesa, context)
    else:
        context = {
            "titulo": titulo,
            "form": form,
            "parcela": parcela_form,
        }
        return render(request, template_name_createdespesa, context)


@login_required
@permission_required("despesa.change_despesa")
def despesaUpdate(request, pk):
    titulo = "Editar Despesa"
    objeto = get_object_or_404(Despesa, pk=pk)
    form = DespesaForm(request.POST or None, request.FILES or None, instance=objeto)
    Formset_contaPagar_Factory = inlineformset_factory(
        Despesa, ContaPagar, form=ContaPagarForm, extra=0, can_delete=False
    )
    parcela_form = Formset_contaPagar_Factory(
        request.POST or None, request.FILES or None, instance=objeto
    )

    if request.method == "POST":
        if form.is_valid() and parcela_form.is_valid():
            despesa = form.save()
            parcela_form.instance = despesa
            parcela_form.save()
            return redirect(success_url_despesa)
        else:
            codigo = True
            context = {
                "codigo": codigo,
                "titulo": titulo,
                "form": form,
                "parcela": parcela_form,
            }
            return render(request, template_name_createdespesa, context)
    else:
        codigo = True
        context = {
            "codigo": codigo,
            "titulo": titulo,
            "form": form,
            "parcela": parcela_form,
        }
        return render(request, template_name_createdespesa, context)


# @permission_required("despesa.view_despesa")
class DespesaList(LoginRequiredMixin, ListView):
    model = Despesa
    template_name = "despesa/despesaList.html"


despesaList = DespesaList.as_view()


class FluxodeCaixa(LoginRequiredMixin, ListView):
    model = Despesa
    template_name = "despesa/fluxodecaixa.html"


fluxodecaixa = FluxodeCaixa.as_view()


class DespesaDetails(LoginRequiredMixin, DetailView, PermissionRequiredMixin):
    model = Despesa
    template_name = "despesa/despesaDetails.html"
    permission_required = "despesa.view_despesa"


despesaDetails = DespesaDetails.as_view()


class DespesaDelete(LoginRequiredMixin, DeleteView, PermissionRequiredMixin):
    model = Despesa
    template_name = "despesa/despesaDelete.html"
    success_url = success_url_despesa
    permission_required = "despesa.delete_despesa"


despesaDelete = DespesaDelete.as_view()
