from django.shortcuts import render
from django.urls import reverse_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from datetime import date
from django.db.models import Sum

from .models import ContaReceber, ContaPagar, Comissao
from .forms import ComissaoForm


data_atual = date.today()


# Lista a comissão de todos os vendedores
def comissaoVendedorList(request):
    template_name = "financeiro/comisAdminVendedorList.html"
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
        mensagem = "Aguardar pagamento"
    else:
        comissao = Comissao.objects.filter(parcela__venda__vendedor=request.user)
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


FluxodeCaixa = FluxodeCaixa.as_view()


@login_required
def ContasaPagar(request):
    template_name = "financeiro/contasPagarList.html"
    object_list_All = ContaPagar.objects.all()
    object_list = object_list_All.filter(datavencimento__month=data_atual.month)

    data_ini = request.GET.get("data_ini")
    data_fim = request.GET.get("data_fim")
    if data_ini and data_fim:
        object_list = object_list_All.filter(datavencimento__range=[data_ini, data_fim])

    vencidos = 0.00
    for valor in object_list:
        if valor.datavencimento < data_atual and valor.datapagamento == None:
            vencidos += int(valor.valor)

    vencem_hoje = 0.00
    for valor in object_list:
        if valor.datavencimento == data_atual:
            vencem_hoje += int(valor.valor)

    avencer = 0.00
    for valor in object_list:
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
def ContasaReceber(request):
    template_name = "financeiro/contasReceberList.html"
    object_list_All = ContaReceber.objects.all()
    object_list = object_list_All.filter(datavencimento__month=data_atual.month)

    data_ini = request.GET.get("data_ini")
    data_fim = request.GET.get("data_fim")
    if data_ini and data_fim:
        object_list = object_list_All.filter(datavencimento__range=[data_ini, data_fim])

    vencidos = 0.00
    for valor in object_list:
        if valor.datavencimento < data_atual and valor.datapagamento == None:
            vencidos += int(valor.valor)

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
        "vencidos": vencidos,
        "vencem_hoje": vencem_hoje,
        "data_ini": data_ini,
        "data_fim": data_fim,
        "object_list": object_list,
    }
    return render(request, template_name, context)
