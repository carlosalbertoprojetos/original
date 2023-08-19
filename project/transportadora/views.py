from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy as _

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView


from .models import Transportadora
from .forms import TransporteForm


success_url_transporte = _("transportadora:transporteList")


class TransporteListView(LoginRequiredMixin, ListView):
    model = Transportadora
    template_name = "transportadora/transporteList.html"


transporteList = TransporteListView.as_view()


class TransporteCreateView(LoginRequiredMixin, CreateView):
    model = Transportadora
    form_class = TransporteForm
    template_name = "transportadora/transporteCreateUpdate.html"
    success_url = success_url_transporte


transporteCreate = TransporteCreateView.as_view()


class TransporteDetailView(LoginRequiredMixin, DetailView):
    model = Transportadora
    template_name = "transportadora/transporteDetails.html"


transporteDetails = TransporteDetailView.as_view()


class TransporteUpdateView(LoginRequiredMixin, UpdateView):
    model = Transportadora
    form_class = TransporteForm
    template_name = "transportadora/transporteCreateUpdate.html"
    success_url = success_url_transporte
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["id"] = self.kwargs["pk"]
        return context


transporteUpdate = TransporteUpdateView.as_view()


class TransporteDeleteView(LoginRequiredMixin, DeleteView):
    model = Transportadora
    template_name = "transportadora/transporteDelete.html"
    success_url = success_url_transporte

    def get(self, request, *args, **kwargs):
            if self.get_object().venda_set.all():
                print('tem elemento')
                self.object = self.get_object()
                context = self.get_context_data(object=self.object)
                self.template_name = "transportadora/transporteRestrict.html"
                return self.render_to_response(context)
                # tem elemento, nao posso excluir
            else:
                self.object = self.get_object()
                context = self.get_context_data(object=self.object)
                return self.render_to_response(context)

transporteDelete = TransporteDeleteView.as_view()
