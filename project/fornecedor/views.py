from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy as _
from django.db.models.deletion import RestrictedError

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView


from .models import Fornecedor
from .forms import FornecedorForm


success_url_fornecedor = _("fornecedor:fornecedorList")


class FornecedorListView(LoginRequiredMixin, ListView):
    model = Fornecedor
    template_name = "fornecedor/fornecedorList.html"


fornecedorList = FornecedorListView.as_view()


class FornecedorCreateView(LoginRequiredMixin, CreateView):
    model = Fornecedor
    form_class = FornecedorForm
    template_name = "fornecedor/fornecedorCreateUpdate.html"
    success_url = success_url_fornecedor


fornecedorCreate = FornecedorCreateView.as_view()


class FornecedorDetailView(LoginRequiredMixin, DetailView):
    model = Fornecedor
    template_name = "fornecedor/fornecedorDetails.html"


fornecedorDetails = FornecedorDetailView.as_view()


class FornecedorUpdateView(LoginRequiredMixin, UpdateView):
    model = Fornecedor
    form_class = FornecedorForm
    template_name = "fornecedor/fornecedorCreateUpdate.html"
    success_url = success_url_fornecedor

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["id"] = self.kwargs["pk"]
        return context


fornecedorUpdate = FornecedorUpdateView.as_view()


class FornecedorDeleteView(LoginRequiredMixin, DeleteView):
    model = Fornecedor
    template_name = "fornecedor/fornecedorDelete.html"
    success_url = success_url_fornecedor
    def get(self, request, *args, **kwargs):
        if self.get_object().fornecedorNFCompra.all() or self.get_object().compra_set.all():
            print('tem elemento')
            self.object = self.get_object()
            context = self.get_context_data(object=self.object)
            self.template_name = "fornecedor/fornecedorRestrict.html"
            return self.render_to_response(context)
            # tem elemento, nao posso excluir
        else:
            self.object = self.get_object()
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)
        
        

fornecedorDelete = FornecedorDeleteView.as_view()
