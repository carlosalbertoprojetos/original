from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .models import Produto


class ProdutoList(LoginRequiredMixin, ListView):
    model = Produto
    template_name = "produto/produtoList.html"


produtoList = ProdutoList.as_view()
