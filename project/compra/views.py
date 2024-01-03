from django.urls import reverse_lazy as _
from django.shortcuts import redirect, render
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models.deletion import RestrictedError
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import DeleteView
from django.db.models import Q

from .models import Compra, CompraMateriaPrima
from .forms import CompraForm, CompraMateriaPrimaForm
from fornecedor.models import Fornecedor
from financeiro.models import ContaPagar
from financeiro.forms import ContaPagarForm


success_url_compra = _("compra:compraList")
template_name_crete_update = "compra/compraCreateUpdate.html"


class CompraList(LoginRequiredMixin, ListView):
    model = Compra
    template_name = "compra/compraList.html"


compraList = CompraList.as_view()


class CompraDetails(LoginRequiredMixin, DetailView):
    model = Compra
    template_name = "compra/compraDetails.html"


compraDetails = CompraDetails.as_view()


class CompraDelete(LoginRequiredMixin, DeleteView):
    model = Compra
    template_name = "compra/compraDelete.html"
    success_url = success_url_compra


compraDelete = CompraDelete.as_view()


def fornecedorAjax(request):
    if request.is_ajax():
        term = request.GET.get("term")
        clientes = Fornecedor.objects.filter(
            Q(nome__icontains=term) | Q(nome_fantasia__icontains=term)
        )
        data = list(clientes.values())
        return JsonResponse(data, safe=False)


@login_required
def compraCreate(request):
    form = CompraForm(request.POST or None)
    Formset_compraMateriaPrima_Factory = inlineformset_factory(
        Compra,
        CompraMateriaPrima,
        form=CompraMateriaPrimaForm,
        extra=0,
        can_delete=False,
        min_num=1,
    )
    produto_form = Formset_compraMateriaPrima_Factory(request.POST or None)
    Formset_contaPagar_Factory = inlineformset_factory(
        Compra, ContaPagar, form=ContaPagarForm, extra=1, can_delete=False
    )
    parcela_form = Formset_contaPagar_Factory(
        request.POST or None, request.FILES or None
    )

    if request.method == "POST":
        if form.is_valid() and produto_form.is_valid() and parcela_form.is_valid():
            compra = form.save()
            produto_form.instance = compra
            produto_form.save()
            parcela_form.instance = compra
            parcela_form.save()
            return redirect("compra:compraList")
        else:
            context = {
                "texto": "Novo",
                "form": form,
                "produto": produto_form,
                "parcela": parcela_form,
            }
            return render(request, template_name_crete_update, context)
    else:
        context = {
            "texto": "Novo",
            "form": form,
            "produto": produto_form,
            "parcela": parcela_form,
        }
        return render(request, template_name_crete_update, context)


@login_required
def compraUpdate(request, pk):
    objeto = get_object_or_404(Compra, pk=pk)
    dados_compra = Compra.objects.filter(pk=pk)
    status = []
    for obj in dados_compra:
        status = obj.status_compra
    dados_produto = CompraMateriaPrima.objects.filter(compra=objeto)
    dados_parcelas = ContaPagar.objects.filter(compra=objeto)

    form = CompraForm(request.POST or None, instance=objeto)

    Formset_compraMateriaPrima_Factory = inlineformset_factory(
        Compra,
        CompraMateriaPrima,
        form=CompraMateriaPrimaForm,
        extra=0,
        can_delete=False,
        min_num=1,
    )
    produto_form = Formset_compraMateriaPrima_Factory(
        request.POST or None, instance=objeto
    )

    Formset_contaPagar_Factory = inlineformset_factory(
        Compra, ContaPagar, form=ContaPagarForm, extra=0, can_delete=False
    )
    parcela_form = Formset_contaPagar_Factory(
        request.POST or None, request.FILES or None, instance=objeto
    )

    if request.method == "POST":
        if form.is_valid() and produto_form.is_valid() and parcela_form.is_valid():
            form.save()
            produto_form.save()
            parcela_form.save()
            return redirect("compra:compraList")
        else:
            codigo = True
            context = {
                "texto": "Alterar",
                "codigo": codigo,
                "status": status,
                "dados_compra": dados_compra,
                "dados_produto": dados_produto,
                "dados_parcelas": dados_parcelas,
                "form": form,
                "produto": produto_form,
                "parcela": parcela_form,
            }
            return render(request, template_name_crete_update, context)
    else:
        codigo = True
        context = {
            "texto": "Alterar",
            "codigo": codigo,
            "status": status,
            "dados_compra": dados_compra,
            "dados_produto": dados_produto,
            "dados_parcelas": dados_parcelas,
            "form": form,
            "produto": produto_form,
            "parcela": parcela_form,
        }
        return render(request, template_name_crete_update, context)
