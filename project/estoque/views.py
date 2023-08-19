from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .models import EstoqueMateriaPrima, ConferenciaEstoque
from .forms import ConferenciaEstoqueForm


class EstoqueMPList(LoginRequiredMixin, ListView):
    model = EstoqueMateriaPrima
    template_name = "estoque/estoqueList.html"


estoqueList = EstoqueMPList.as_view()


def confereEstoque(request, pk):
    template_name = "estoque/estoqueUpdate.html"

    estoque = get_object_or_404(EstoqueMateriaPrima, pk=pk)
    confere = ConferenciaEstoque.objects.filter(produto=estoque)

    if request.method == "POST":
        forms = ConferenciaEstoqueForm(request.POST)
        if forms.is_valid():
            forms = forms.save(commit=False)
            forms.produto = estoque
            forms.usuario = request.user
            forms.qtde = estoque.qtde
            forms.save()
            return redirect(request.path)

    else:
        forms = ConferenciaEstoqueForm()
        context = {
            "form": estoque,
            "forms": forms,
            "object_list": confere,
        }
        return render(request, template_name, context)


class ConferenciaEstoqueList(LoginRequiredMixin, ListView):
    model = ConferenciaEstoque
    template_name = "estoque/conferenciaEstoqueList.html"


confEstoqueList = ConferenciaEstoqueList.as_view()
