from django.db import models
from django.urls import reverse_lazy as _

from fornecedor.models import Fornecedor
from cliente.models import Cliente


class Categoria(models.Model):
    nome = models.CharField("Nome", max_length=200)
    descricao = models.TextField("Descrição", blank=True, null=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"


class Receita(models.Model):
    usuario = models.CharField(max_length=255, null=True, blank=True)
    nome = models.CharField(max_length=200, null=True, blank=True)
    total = models.DecimalField(max_digits=11, decimal_places=2, default=0.0)
    criadoem = models.DateTimeField(auto_now_add=True)
    atualizadoem = models.DateTimeField(auto_now=True)
    categoria1 = models.ForeignKey(Categoria, on_delete=models.RESTRICT)
    categoria2 = models.ForeignKey(
        Categoria, on_delete=models.RESTRICT, related_name="categoria2"
    )
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.RESTRICT, null=True)
    num_parcelas = models.IntegerField(default=0)
    descricao = models.TextField(blank=True, null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.RESTRICT)

    class Meta:
        verbose_name = "RECEITA"
        verbose_name_plural = "RECEITAS"

    def __str__(self):
        return self.nome

    def receita_gau_detail(self):
        return _("receita:receitaDetails", args=[self.pk])

    def receita_gau_edit(self):
        return _("receita:receitaUpdate", args=[self.pk])

    def receita_gau_delete(self):
        return _("receita:receitaDelete", args=[self.pk])
