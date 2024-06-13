from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView
from django.urls import reverse, reverse_lazy as _
from datetime import date


from .models import Representante, DadosBancarios
from .models import ServicoRepresentante
from .forms import RepresentanteForm, DadosBancariosForm, ServicosForm


data_atual = date.today()

template_name_create_update = "representante/representanteCreateUpdate.html"
success_url_representante = _("representante:representantesList")
template_conta_create_update = "representante/representanteContaCreateUpdate.html"
template_servico_create_update = "representante/servicoCreateUpdate.html"


class RepresentanteList(LoginRequiredMixin, ListView):
    model = Representante
    template_name = "representante/representantesList.html"
    context_object_name = "representantes"


representantesList = RepresentanteList.as_view()


class RepresentanteCreateView(LoginRequiredMixin, CreateView):
    model = Representante
    template_name = template_name_create_update
    form_class = RepresentanteForm
    success_url = success_url_representante


representanteCreate = RepresentanteCreateView.as_view()


@login_required
# @permission_required
def representanteUpdate(request, pk):
    representante = get_object_or_404(Representante, id=pk)
    context = {}

    conta = DadosBancarios.objects.filter(representante__id=pk)
    if conta:
        print(conta.get().id)
        url = "/representante/conta/%s/editar/" % (conta.get().id)
    else:
        url = "/representante/%s/conta/cadastrar/" % (pk)

    if request.method == "POST":
        form = RepresentanteForm(request.POST or None, instance=representante)
        if form.is_valid():
            form.save()
            return redirect("representante:representanteUpdate", pk)
        else:
            context = {"form": form, "url": url, "Alterar": True}
            return render(request, template_name_create_update, context)
    else:
        form = RepresentanteForm(instance=representante)
        context = {"form": form, "url": url, "Alterar": True}
        return render(request, template_name_create_update, context)


class RepresentanteDelete(LoginRequiredMixin, DeleteView):
    template_name = "representante/representanteDelete.html"
    model = Representante
    success_url = success_url_representante


representanteDelete = RepresentanteDelete.as_view()


# class RegiaoList(LoginRequiredMixin, ListView):
#     model = Regiao
#     template_name = "representante/regiaoList.html"
#     context_object_name = "regiao"


# regiaoList = RegiaoList.as_view()


# class RegiaoCreateView(LoginRequiredMixin, CreateView):
#     template_name = template_name_regiao_create_update
#     model = Regiao
#     fields = "__all__"
#     success_url = success_url_regiao


# regiaoCreate = RegiaoCreateView.as_view()


# class RegiaoUpdateView(LoginRequiredMixin, UpdateView):
#     template_name = template_name_regiao_create_update
#     model = Regiao
#     fields = "__all__"
#     success_url = success_url_regiao


# regiaoUpdate = RegiaoUpdateView.as_view()


# class RegiaoDelete(LoginRequiredMixin, DeleteView):
#     template_name = "representante/regiaoDelete.html"
#     model = Regiao
#     success_url = success_url_regiao


# regiaoDelete = RegiaoDelete.as_view()


@login_required
# @permission_required
def representanteContaCreate(request, pk):
    representante = get_object_or_404(Representante, id=pk)

    form = DadosBancariosForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form = form.save(commit=False)
            form.representante = representante
            form.save()
            return redirect("/representante/%s/editar/" % (representante.id))
        else:
            context = {"form": form}
            return render(request, template_conta_create_update, context)
    else:
        form = DadosBancariosForm()
        context = {"form": form}
        return render(request, template_conta_create_update, context)


@login_required
# @permission_required
def representanteContaUpdate(request, pk):
    objeto = get_object_or_404(DadosBancarios, id=pk)
    if request.method == "POST":
        form = DadosBancariosForm(request.POST or None, instance=objeto)
        if form.is_valid():
            form = form.save(commit=False)
            form.representante = objeto.representante
            form.save()
            return redirect("representantes:representantesList")
        else:
            context = {"form": form, "id": pk}
            return render(request, template_conta_create_update, context)
    else:
        form = DadosBancariosForm(instance=objeto)
        context = {"form": form, "id": pk}
        return render(request, template_conta_create_update, context)


class RepresentanteContaDelete(LoginRequiredMixin, DeleteView):
    template_name = "representante/representanteContaDelete.html"
    model = DadosBancarios
    success_url = _("representantes:representantesList")

    # def get_success_url(self):
    #     return reverse(
    #         "representante:representanteUpdate",
    #         kwargs={"pk": self.object.representante.id},
    #     )


representanteContaDelete = RepresentanteContaDelete.as_view()


@login_required
def servicosList(request, pk):
    template_name = "representante/servicosList.html"
    servicos = ServicoRepresentante.objects.filter(representante__id=pk)
    representante = Representante.objects.filter(id=pk)

    data_ini = request.GET.get("data_ini")
    data_fim = request.GET.get("data_fim")
    if data_ini and data_fim:
        servicos = servicos.filter(data_pagamento__range=[data_ini, data_fim])

    apagar = 0.00
    pagas = 0.00
    for valor in servicos:
        if valor.data_pagamento == None or valor.data_pagamento > data_atual:
            apagar += int(valor.valor)
        if valor.data_pagamento != None and valor.data_pagamento <= data_atual:
            pagas += int(valor.valor)

    context = {
        "apagar": apagar,
        "pagas": pagas,
        "data_ini": data_ini,
        "data_fim": data_fim,
        "servicos": servicos,
        "representante": representante,
        "id": pk,
    }
    return render(request, template_name, context)


@login_required
def servicoCreate(request, pk):
    representante = get_object_or_404(Representante, id=pk)

    form = ServicosForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            service = form.save(commit=False)
            service.representante = representante
            service.save()
            form.save_m2m()
            return redirect("representante:servicosList", representante.id)
        else:
            context = {"form": form, "id": pk}
            return render(request, template_servico_create_update, context)
    else:
        context = {"form": form, "id": pk}
        return render(request, template_servico_create_update, context)


@login_required
def servicoUpdate(request, pk):
    objeto = get_object_or_404(ServicoRepresentante, id=pk)

    form = ServicosForm(request.POST or None, instance=objeto)
    if request.method == "POST":
        if form.is_valid():
            form.save(commit=False)
            form.save()
            form.save_m2m()
            return redirect("representante:servicosList", objeto.representante.id)
        else:
            context = {"form": form, "id": pk}
            return render(request, template_servico_create_update, context)
    else:
        form = ServicosForm(instance=objeto)
        context = {"form": form, "id": pk}
        return render(request, template_servico_create_update, context)


class ServicoDelete(LoginRequiredMixin, DeleteView):
    template_name = "representante/servicoDelete.html"
    model = ServicoRepresentante

    def get_success_url(self):
        return reverse(
            "representante:servicosList", kwargs={"pk": self.object.representante.id}
        )


servicoDelete = ServicoDelete.as_view()


# @login_required
# def servicosPagamento(request):
#     template_name = "financeiro/contasPagarList.html"
#     object_list_All = ServicoRepresentante.objects.all()
#     object_list = object_list_All.filter(data_pagamento__month=data_atual.month)
#     print(object_list)

#     data_ini = request.GET.get("data_ini")
#     data_fim = request.GET.get("data_fim")
#     if data_ini and data_fim:
#         object_list = object_list_All.filter(data_pagamento__range=[data_ini, data_fim])

#     apagar = 0.00
#     for valor in object_list:
#         if valor.data_pagamento > data_atual or valor.data_pagamento == None:
#             avencer += int(valor.valor)

#     pagas = 0.00
#     for valor in object_list:
#         if valor.data_pagamento <= data_atual:
#             pagas += int(valor.valor)

#     context = {
#         "apagar": apagar,
#         "pagas": pagas,
#         "data_ini": data_ini,
#         "data_fim": data_fim,
#         "object_list": object_list,
#     }
#     return render(request, template_name, context)
