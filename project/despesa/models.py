from django.db import models
from django.urls import reverse_lazy as _


from fornecedor.models import Fornecedor


class Saldo(models.Model):
    saldo = models.FloatField()
    limite = models.FloatField()


class Categoria2(models.Model):
    nome = models.CharField("Nome", max_length=200)
    descricao = models.TextField("Descrição", blank=True, null=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Categoria 2"
        verbose_name_plural = "Categorias 2"


class Categoria(models.Model):
    nome = models.CharField("Nome", max_length=200)
    descricao = models.TextField("Descrição", blank=True, null=True)
    categoria2 = models.ForeignKey(
        Categoria2, on_delete=models.RESTRICT, related_name="categoria2"
    )

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"


class Despesa(models.Model):
    nome = models.CharField(max_length=200)
    total = models.DecimalField(max_digits=11, decimal_places=2, default=0.00)
    criadoem = models.DateTimeField(auto_now_add=True)
    atualizadoem = models.DateTimeField(auto_now=True)
    categoria1 = models.ForeignKey(Categoria, on_delete=models.RESTRICT)
    num_parcelas = models.IntegerField(default=0)
    descricao = models.TextField(blank=True, null=True)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.RESTRICT)

    class Meta:
        verbose_name = "DESPESA"
        verbose_name_plural = "DESPESAS"
        ordering = ["criadoem"]

    def __str__(self):
        return self.nome

    def despesa_gau_detail(self):
        return _("despesa:despesaDetails", args=[self.pk])

    def despesa_gau_edit(self):
        return _("despesa:despesaUpdate", args=[self.pk])

    def despesa_gau_delete(self):
        return _("despesa:despesaDelete", args=[self.pk])
