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
            print("tem elemento")
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


# pip install tabula-py

# import tabula

# # Caminho do arquivo PDF
# file_path = "caminho/do/seu/arquivo.pdf"

# # Use a função read_pdf para extrair tabelas do PDF
# # A função pode retornar várias tabelas, então use o argumento multiple_tables se necessário
# # pages define as páginas do PDF a serem analisadas
# tables = tabula.read_pdf(file_path, pages="all", multiple_tables=True)

# # Se houver várias tabelas nas páginas especificadas
# for i, table in enumerate(tables, start=1):
#     print(f"Tabela {i}:")
#     print(table)  # Isso imprimirá a tabela extraída como um DataFrame do pandas

#     # Você pode processar ou salvar a tabela como desejado
