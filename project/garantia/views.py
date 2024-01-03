import datetime
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.http import HttpResponseRedirect
from django.utils import timezone


from venda.models import Venda, VendaProduto
from .models import StatusGarantia, Garantia, GarantiaTimeLine
from .forms import GarantiaTimeLineForm


date_time = datetime.datetime.now().strftime(("%d/%m/%y %H:%M"))
today = timezone.now()


# lista de produtos na garantia(conserto)
class ProdutosEmGarantia(LoginRequiredMixin, ListView):
    template_name = "garantia/garantiaList.html"
    model = Garantia

    def get_queryset(self):
        status = StatusGarantia.objects.get(nome="Concluído")
        queryset = Garantia.objects.all().exclude(status=status)
        return queryset


produtosEmGarantia = ProdutosEmGarantia.as_view()


# lista de vendas com produtos na garantia
class VendasGarantiaList(LoginRequiredMixin, ListView):
    template_name = "garantia/vendasList.html"
    model = Venda


vendasGarantiaList = VendasGarantiaList.as_view()


# cria pedido de garantia do produto
# se o produto, referente à mesma venda, já estiver em garantia não aparece na lista
@login_required
def produtosVenda(request, venda):
    template_name = "garantia/produtosListCreate.html"
    # bdGarantia = Garantia.objects.filter(produto__venda=venda)
    bdProdutos = VendaProduto.objects.filter(venda=venda)
    # listaGarantia = []
    # for g in bdGarantia:
    #     listaGarantia.append(g.produto.produto.nome)
    produtos = {}
    for p in bdProdutos:
        # if not p.produto.nome in listaGarantia:
        produtos.update({p.id: p.produto})

    # mensagem = []
    # if not produtos:
    #     mensagem = "Todos os produtos desta venda já estão cadastrados para conserto."

    # context = {"produtos": produtos, "mensagem": mensagem}
    context = {"produtos": produtos}
    return render(request, template_name, context)


@login_required
def produtoCreateGarantia(request, produto):
    bd_produto = VendaProduto.objects.filter(pk=produto)
    status = get_object_or_404(StatusGarantia, nome="Aberto")
    for p in bd_produto:
        Garantia.objects.create(produto=p, status=status).save()
    return redirect("garantia:produtosEmGarantia")


def garantiaTimeLineList(request, garantia):
    template_name = "garantia/garantiaTimeline.html"
    dados = Garantia.objects.filter(pk=garantia)
    timeLine = GarantiaTimeLine.objects.filter(garantia=garantia).order_by("-id")

    bdDias = 0
    for i in timeLine:
        if i.status.nome == "Concluído":
            bdDias = i.data
    for d in dados:
        bdDias = d.data
    dias = abs((today - bdDias).days)

    form = GarantiaTimeLineForm(request.POST or None)
    garantiaForm = get_object_or_404(Garantia, pk=garantia)
    if request.method == "POST":
        if form.is_valid():
            form = form.save(commit=False)
            form.garantia = garantiaForm
            form.atualizadopor = f"por {request.user}_{date_time}"
            form.save()
            return HttpResponseRedirect(f"/garantia/{garantia}/list/timeline/")
        else:
            context = {
                "form": form,
                "dados": dados,
                "dias": dias,
                "garantia": garantia,
                "timeLine": timeLine,
            }
            return render(request, template_name, context)
    else:
        context = {
            "form": form,
            "dados": dados,
            "dias": dias,
            "garantia": garantia,
            "timeLine": timeLine,
        }
        return render(request, template_name, context)


def garantiaTimeLineUpdate(request, timeline):
    dados = GarantiaTimeLine.objects.filter(pk=timeline)
    objeto = get_object_or_404(GarantiaTimeLine, pk=timeline)
    template_name = "garantia/garantiaTimelineUpdate.html"

    bdDias = 0
    for d in dados:
        if d.garantia.status.nome == "Concluído":
            bdDias = d.data
        else:
            bdDias = d.garantia.data
    dias = abs((today - bdDias).days)

    idGarantia = 0
    for d in dados:
        idGarantia = d.garantia.id

    if request.method == "POST":
        form = GarantiaTimeLineForm(request.POST or None, instance=objeto)
        if form.is_valid():
            form = form.save(commit=False)
            form.garantia = objeto.garantia
            form.atualizadopor = f"por {request.user}_{date_time}"
            form.save()
            return HttpResponseRedirect(f"/garantia/{idGarantia}/list/timeline/")
        else:
            context = {
                "form": form,
                "dados": dados,
                "dias": dias,
                "garantia": idGarantia,
            }
            return render(request, template_name, context)
    else:
        form = GarantiaTimeLineForm(instance=objeto)
        context = {
            "form": form,
            "dados": dados,
            "dias": dias,
            "garantia": idGarantia,
        }
        return render(request, template_name, context)
