from typing import Any, Dict
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy as _

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import Cliente
from .forms import ClienteForm


success_url_cliente = _("cliente:clienteList")


class ClienteListView(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = "cliente/clienteList.html"


clienteList = ClienteListView.as_view()


def getClientesAjax(request):
    bd_data = Cliente.objects.all()
    data = []
    for d in bd_data:
        if d.cpf == None:
            cpf = " "
        else:
            cpf = str(d.cpf)
        if d.cnpj == None:
            cnpj = " "
        else:
            cnpj = str(d.cnpj)
        data.append(
            {
                "nome_fantasia": d.nome_fantasia[:20],
                "nome": d.nome[:40],
                "tel_principal": d.tel_principal,
                "tel_contato": d.tel_contato,
                "email": d.email[:20],
                "cpf": cpf,
                "cnpj": cnpj,
                "estado": d.estado,
                "acoes": f'<a class="px-1" href="{d.pk}/editar/"><i class=" fa fa-edit"></i></a></abbr>',
            }
        )
    return JsonResponse({"data": data})


class ClienteCreateView(LoginRequiredMixin, CreateView, PermissionRequiredMixin):
    model = Cliente
    form_class = ClienteForm
    template_name = "cliente/clienteCreateUpdate.html"
    success_url = success_url_cliente
    permission_required = "cliente.add_cliente"


clienteCreate = ClienteCreateView.as_view()


class ClienteDetailView(LoginRequiredMixin, DetailView):
    model = Cliente
    template_name = "cliente/clienteDetails.html"
    context_object_name = "clientes"


clienteDetails = ClienteDetailView.as_view()


class ClienteUpdateView(LoginRequiredMixin, UpdateView, PermissionRequiredMixin):
    model = Cliente
    form_class = ClienteForm
    template_name = "cliente/clienteCreateUpdate.html"
    success_url = success_url_cliente
    permission_required = "cliente.change_cliente"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["id"] = self.kwargs["pk"]
        return context


clienteUpdate = ClienteUpdateView.as_view()


class ClienteDeleteView(LoginRequiredMixin, DeleteView, PermissionRequiredMixin):
    model = Cliente
    template_name = "cliente/clienteDelete.html"
    success_url = success_url_cliente
    permission_required = "cliente.delete_cliente"

    def get(self, request, *args, **kwargs):
        if self.get_object().clientevenda.all() or self.get_object().receita_set.all():
            print("tem elemento")
            self.object = self.get_object()
            context = self.get_context_data(object=self.object)
            self.template_name = "cliente/clienteRestrict.html"
            return self.render_to_response(context)
            # tem elemento, nao posso excluir
        else:
            self.object = self.get_object()
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)


clienteDelete = ClienteDeleteView.as_view()
