from django.db import models
from django.urls import reverse_lazy as _
from project.constantes import ESCOLHAS_STATUSCOMPRAS

from fornecedor.models import Fornecedor
from materiaprima.models import MateriaPrima


class Compra(models.Model):
    data = models.DateField()
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.RESTRICT)
    criadoem = models.DateTimeField(auto_now_add=True)
    atualizadoem = models.DateTimeField(auto_now=True)
    num_parcelas = models.IntegerField(default=0)
    previsaoentrega = models.DateField()
    total = models.DecimalField(max_digits=11, decimal_places=2, default=0.00)
    status_compra = models.CharField(
        choices=ESCOLHAS_STATUSCOMPRAS, null=False, blank=False, max_length=50
    )
    pedido = models.FileField(upload_to="compra/pedido/", null=True, blank=True)

    class Meta:
        verbose_name = "Compra"
        verbose_name_plural = "Compras"

    def __str__(self):
        return self.fornecedor.nome

    def compra_gau_detail(self):
        return _("compra:compraDetails", args=[self.pk])

    def compra_gau_edit(self):
        return _("compra:compraUpdate", args=[self.pk])

    def compra_gau_delete(self):
        return _("compra:compraDelete", args=[self.pk])


class CompraMateriaPrima(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    produto = models.ForeignKey(MateriaPrima, on_delete=models.RESTRICT)
    quantidade = models.IntegerField(default=1)
    detalhes = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return str(self.produto)
