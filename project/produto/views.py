from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import redirect, render, get_object_or_404
from django.forms import inlineformset_factory
from django.views.generic import ListView, DeleteView
from django.urls import reverse_lazy as _


from .models import Produto, ProdutoMatPri, Peca
from .forms import ProdutoForm, ProdutoMatPriForm, PecaForm, PecaMatPriForm
from materiaprima.models import MateriaPrima
from compra.models import Compra, CompraMateriaPrima

templateProdutoCreateUpdate = "produto/produtoCreateUpdate.html"
templatePecaCreateUpdate = "produto/pecaCreateUpdate.html"


class ProdutoList(LoginRequiredMixin, ListView):
    model = Produto
    template_name = "produto/produtoList.html"


produtoList = ProdutoList.as_view()


@login_required
def produtoCreate(request):
    form = ProdutoForm(request.POST or None)
    Formset_ProdutoMatPri_Factory = inlineformset_factory(
        Produto,
        ProdutoMatPri,
        form=ProdutoMatPriForm,
        can_delete=False,
        min_num=1,
        extra=0,
    )
    formset = Formset_ProdutoMatPri_Factory(request.POST or None)

    if request.method == "POST":
        if form.is_valid() and formset.is_valid():
            form = form.save()
            formset.instance = form
            formset.save()
            return redirect("produto:produtoList")
        else:
            context = {"form": form, "formset": formset}
            return render(request, templateProdutoCreateUpdate, context)
    else:
        context = {"form": form, "formset": formset}
        return render(request, templateProdutoCreateUpdate, context)


@login_required
def produtoUpdate(request, pk):
    objeto = get_object_or_404(Produto, pk=pk)
    form = ProdutoForm(request.POST or None, instance=objeto)
    Formset_ProdutoMatPri_Factory = inlineformset_factory(
        Produto, ProdutoMatPri, form=ProdutoMatPriForm, min_num=1, extra=0
    )
    formset = Formset_ProdutoMatPri_Factory(request.POST or None, instance=objeto)

    if request.method == "POST":
        if form.is_valid() and formset.is_valid():
            form = form.save()
            formset.save()
            return redirect("produto:produtoList")
    else:
        context = {"codigo": True, "form": form, "formset": formset}
        return render(request, templateProdutoCreateUpdate, context)


class ProdutoDelete(LoginRequiredMixin, DeleteView):
    model = Produto
    template_name = "produto/produtoDelete.html"
    success_url = _("produto:produtoList")


produtoDelete = ProdutoDelete.as_view()


class PecaList(LoginRequiredMixin, ListView):
    model = Peca
    template_name = "produto/pecaList.html"


pecaList = PecaList.as_view()


@login_required
def pecaCreate(request):
    form = PecaForm(request.POST or None)
    Formset_ProdutoMatPri_Factory = inlineformset_factory(
        Peca,
        ProdutoMatPri,
        form=PecaMatPriForm,
        can_delete=False,
        min_num=1,
        extra=0,
    )
    formset = Formset_ProdutoMatPri_Factory(request.POST or None)

    if request.method == "POST":
        if form.is_valid() and formset.is_valid():
            form = form.save()
            formset.instance = form
            formset.save()
            return redirect("produto:pecaList")
    else:
        context = {"form": form, "formset": formset}
        return render(request, templatePecaCreateUpdate, context)


@login_required
def pecaUpdate(request, pk):
    objeto = get_object_or_404(Peca, pk=pk)
    form = PecaForm(request.POST or None, instance=objeto)
    Formset_PecaMatPri_Factory = inlineformset_factory(
        Peca, ProdutoMatPri, form=PecaMatPriForm, min_num=1, extra=0
    )
    formset = Formset_PecaMatPri_Factory(request.POST or None, instance=objeto)

    if request.method == "POST":
        if form.is_valid() and formset.is_valid():
            form = form.save()
            formset.save()
            return redirect("produto:pecaList")
    else:
        context = {"codigo": True, "form": form, "formset": formset}
        return render(request, templatePecaCreateUpdate, context)


class PecaDelete(LoginRequiredMixin, DeleteView):
    model = Peca
    template_name = "produto/pecaDelete.html"
    success_url = "produto:pecaList"


pecaDelete = PecaDelete.as_view()


@login_required
def produtoCustoList(request):
    template = "produto/produtoCustoList.html"
    prod_compras = CompraMateriaPrima.objects.all()
    produto = MateriaPrima.objects.all()
    dict_produtos = {}
    result = {}
    for p in produto:
        comprado = list(
            CompraMateriaPrima.objects.filter(produto__nome=p.nome).order_by("compra")[
                :10
            ]
        )
        soma = (
            CompraMateriaPrima.objects.filter(produto__nome=p.nome)
            .order_by("compra")[:10]
            .aggregate(Sum("quantidade"))["quantidade__sum"]
        )

        for c in comprado:
            if p.nome == c.produto.nome:
                dict_produtos.update({p.nome: soma})

        calc_total = 0
        for co in prod_compras:
            if co.produto == p:
                calc_total += co.compra.total

        if soma == 0 or calc_total == 0:
            calc_peca = 0
        else:
            calc_peca = calc_total / soma

        if soma == None:
            soma = 0

        result.update({p.nome: {soma: {float(calc_total): float(calc_peca)}}})

    context = {"dict_produtos": result}

    return render(request, template, context)


@login_required
def produtoCustoDetails(request, produto):
    template = "produto/produtoCustoDetails.html"
    compra = CompraMateriaPrima.objects.all()
    data = CompraMateriaPrima.objects.filter(produto__nome=produto).order_by("compra")[
        :10
    ]

    fornecedores = []
    id_compra = []
    for c in data:
        id_compra.append(c.compra.id)
        fornecedores.append(c.compra.fornecedor.nome)
    fornecedores = set(fornecedores)

    soma = (
        CompraMateriaPrima.objects.filter(produto__nome=produto)
        .order_by("compra")[:10]
        .aggregate(Sum("quantidade"))["quantidade__sum"]
    )

    calc_total = 0
    for co in compra:
        if co.produto.nome == produto:
            calc_total += co.compra.total

    valor_por_produto = {}
    calc = 0
    for id in id_compra:
        quant = CompraMateriaPrima.objects.filter(compra=id).aggregate(
            Sum("quantidade")
        )["quantidade__sum"]
        bd_total = Compra.objects.filter(id=id)
        total = 0
        for t in bd_total:
            total = t.total
        calc = total / quant
        valor_por_produto.update({id: float(calc)})

    if soma == 0 or calc_total == 0:
        calc_peca = 0
    else:
        calc_peca = calc_total / soma

    if soma == None:
        soma = 0

    calc_total = f"R$ {calc_total}"
    calc_peca = f"R$ {calc_peca:.2f}"

    context = {
        "data": data,
        "fornecedores": fornecedores,
        "compra": compra,
        "produto": produto,
        "quantidade": soma,
        "total": calc_total,
        "peca": calc_peca,
        "valor": valor_por_produto,
    }

    return render(request, template, context)
