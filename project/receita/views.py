from django.urls import reverse_lazy as _
from django.shortcuts import redirect, render
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.views.generic.edit import DeleteView


from .models import Receita
from .forms import ReceitaForm
from financeiro.models import ContaReceber
from financeiro.forms import ContaReceberForm


success_url_receita = _("receita:receitaList")
template_name_createreceita = "receita/receitaCreateUpdate.html"


@login_required
def receitaCreate(request):
    titulo = "Nova Receita"
    form = ReceitaForm(request.POST or None)
    Formset_contaReceber_Factory = inlineformset_factory(
        Receita,
        ContaReceber,
        form=ContaReceberForm,
        min_num=1,
        extra=0,
        can_delete=False,
    )
    parcela_form = Formset_contaReceber_Factory(
        request.POST or None, request.FILES or None
    )

    if request.method == "POST":
        if form.is_valid() and parcela_form.is_valid():
            # form.save()
            usuario = form.save(commit=False)
            usuario.usuario = str(request.user)
            usuario.save()
            # receita = form.save()
            parcela_form.instance = usuario
            parcela_form.save()
            return redirect(success_url_receita)
        else:
            context = {
                "titulo": titulo,
                "form": form,
                "parcela": parcela_form,
            }
            return render(request, template_name_createreceita, context)
    else:
        context = {
            "titulo": titulo,
            "form": form,
            "parcela": parcela_form,
        }
        return render(request, template_name_createreceita, context)


@login_required
def receitaUpdate(request, pk):
    titulo = "Editar Receita"
    objeto = get_object_or_404(Receita, pk=pk)
    form = ReceitaForm(request.POST or None, instance=objeto)
    Formset_contaReceber_Factory = inlineformset_factory(
        Receita, ContaReceber, form=ContaReceberForm, extra=0, can_delete=False
    )
    parcela_form = Formset_contaReceber_Factory(
        request.POST or None,
        request.FILES or None,
        instance=objeto,
    )

    if request.method == "POST":
        if form.is_valid() and parcela_form.is_valid():
            receita = form.save()
            parcela_form.instance = receita
            parcela_form.save()
            return redirect(success_url_receita)
        else:
            codigo = True
            context = {
                "codigo": codigo,
                "titulo": titulo,
                "form": form,
                "parcela": parcela_form,
            }
            return render(request, template_name_createreceita, context)
    else:
        codigo = True
        context = {
            "codigo": codigo,
            "titulo": titulo,
            "form": form,
            "parcela": parcela_form,
        }
        return render(request, template_name_createreceita, context)


class ReceitaList(LoginRequiredMixin, ListView):
    model = Receita
    template_name = "receita/receitaList.html"


receitaList = ReceitaList.as_view()


class ReceitaDetails(LoginRequiredMixin, DetailView):
    model = Receita
    template_name = "receita/receitaDetails.html"


receitaDetails = ReceitaDetails.as_view()


class ReceitaDelete(LoginRequiredMixin, DeleteView):
    model = Receita
    template_name = "receita/receitaDelete.html"
    success_url = success_url_receita


receitaDelete = ReceitaDelete.as_view()
