from django.shortcuts import render
from django.urls import reverse_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, UpdateView
from datetime import date

from .models import ContaReceber, ContaPagar, Comissao
from .forms import ComissaoForm


data_atual = date.today()


def comissaoVendedorList(request):
    template_name = "financeiro/comisAdminVendedorList.html"
    comissao = Comissao.objects.all()
    if request.user.is_superuser:
        mensagem = "Aguardar pagamento"
    else:
        comissao = Comissao.objects.filter(
            parcela__venda__vendedor=request.user.username.lower()
        )
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


FluxodeCaixa = FluxodeCaixa.as_view()


@login_required
def ContasaPagar(request):
    template_name = "financeiro/contasPagarList.html"

    object_list_All = ContaPagar.objects.all()
    object_list = object_list_All.filter(
        datavencimento__month=data_atual.month
    ).exclude(datapagamento__isnull=False)
    vencem_hoje_base = object_list.filter(datavencimento__day=data_atual.day)

    primeiro = data_atual.replace(day=1)
    data_ini = primeiro.strftime("%d/%m/%Y")
    data_fim = data_atual.strftime("%d/%m/%Y")

    vlr_mes = 0.00
    for valor in object_list:
        vlr_mes += int(valor.valor)

    vencem_hoje = 0.00
    if vencem_hoje_base:
        for valor in vencem_hoje_base:
            vencem_hoje += int(valor.valor)

    vencidos = 0.00
    for valor in object_list:
        if valor.datavencimento < data_atual:
            vencidos += int(valor.valor)

    pagos = 0.00
    for valor in object_list:
        if valor.datapagamento:
            pagos += int(valor.valor)

    data_ini = request.GET.get("data_ini")
    data_fim = request.GET.get("data_fim")
    if data_ini and data_fim:
        object_list = object_list_All.filter(
            datavencimento__range=[data_ini, data_fim]
        ).exclude(datapagamento__isnull=False)

        vlr_mes = 0.00
        for valor in object_list:
            vlr_mes += int(valor.valor)

        vencem_hoje = 0.00
        if vencem_hoje_base:
            for valor in vencem_hoje_base:
                vencem_hoje += int(valor.valor)

        vencidos = 0.00
        for valor in object_list:
            if valor.datavencimento > data_atual:
                vencidos += int(valor.valor)

        pagos = 0.00
        for valor in object_list:
            if valor.datapagamento:
                pagos += int(valor.valor)

    context = {
        "pagos": pagos,
        "vencidos": vencidos,
        "vlr_mes": vlr_mes,
        "vencem_hoje": vencem_hoje,
        "data_ini": data_ini,
        "data_fim": data_fim,
        "object_list": object_list,
    }
    return render(request, template_name, context)


@login_required
def ContasaReceber(request):
    template_name = "financeiro/contasReceberList.html"
    object_list_All = ContaReceber.objects.all()
    object_list = object_list_All.filter(datavencimento__month=data_atual.month)
    vencem_hoje_base = object_list_All.filter(datavencimento__day=data_atual.day)

    primeiro = data_atual.replace(day=1)
    data_ini = primeiro.strftime("%d/%m/%Y")
    data_fim = data_atual.strftime("%d/%m/%Y")

    vlr_mes = 0.00
    for valor in object_list:
        if valor.datavencimento < data_atual:
            vlr_mes += int(valor.valor)

    vencem_hoje = 0.00
    if vencem_hoje_base:
        for valor in vencem_hoje_base:
            vencem_hoje += int(valor.valor)

    avencer = 0.00
    for valor in object_list:
        if valor.datavencimento > data_atual:
            avencer += int(valor.valor)

    recebidos = 0.00
    for valor in object_list:
        if valor.datapagamento:
            recebidos += int(valor.valor)

    data_ini = request.GET.get("data_ini")
    data_fim = request.GET.get("data_fim")

    if data_ini and data_fim:
        # object_list = object_list_All.filter(datavencimento__range=[data_ini, data_fim]).exclude(data_pagamento__isnotnull=True)
        object_list = object_list_All.filter(datavencimento__range=[data_ini, data_fim])

        vlr_mes = 0.00
        for valor in object_list:
            if valor.datavencimento < data_atual:
                vlr_mes += int(valor.valor)

        vencem_hoje = 0.00
        for valor in object_list:
            if valor.datavencimento == data_atual:
                vencem_hoje += int(valor.valor)

        avencer = 0.00
        for valor in object_list:
            if valor.datavencimento > data_atual:
                avencer += int(valor.valor)

        recebidos = 0.00
        for valor in object_list:
            if valor.datapagamento:
                recebidos += int(valor.valor)

    context = {
        "recebidos": recebidos,
        "avencer": avencer,
        "vlr_mes": vlr_mes,
        "vencem_hoje": vencem_hoje,
        "data_ini": data_ini,
        "data_fim": data_fim,
        "object_list": object_list,
    }
    return render(request, template_name, context)
