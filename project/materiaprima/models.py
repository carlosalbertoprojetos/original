from django.db import models

from fornecedor.models import Fornecedor


class UnidadeMedida(models.Model):
    nome = models.CharField("Nome", max_length=255)
    descricao = models.CharField("Descricao", max_length=20)

    class Meta:
        verbose_name = "Unidade de Medida"
        verbose_name_plural = "Unidades de Medidas"
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class MateriaPrima(models.Model):
    nome = models.CharField(max_length=255)
    uni_med = models.ForeignKey(UnidadeMedida, on_delete=models.RESTRICT)
    descricao = models.CharField(max_length=255, null=True, blank=True)
    # criadoem = models.DateTimeField(auto_now_add=True)
    # atualizadoem = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Materia Prima"
        verbose_name_plural = "Materias Primas"
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class MateriaPrimaFornecedor(models.Model):
    materiaprima = models.ForeignKey(
        MateriaPrima, on_delete=models.RESTRICT, blank=True
    )
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.RESTRICT, null=False)
    codigoproduto = models.CharField(max_length=255)
    nome = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Fornecedor de Materia Prima"
        verbose_name_plural = "Fornecedor de Materias Prima"
        ordering = ["nome"]

    def __str__(self):
        return f'{self.materiaprima}"-"{self.codigoproduto}'
