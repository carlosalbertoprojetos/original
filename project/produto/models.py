from django.db import models
from django.urls import reverse_lazy as _
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from materiaprima.models import MateriaPrima


def validate_campos(value):
    if not value.isdigit():
        raise ValidationError("O campo deve conter apenas números")


class UnidadeMedida(models.Model):
    unidade = models.CharField("UN", max_length=10)
    descricao = models.TextField("DESCRIÇÃO", blank=True)

    class Meta:
        verbose_name = "UNIDADE DE MEDIDA"
        verbose_name_plural = "UNIDADES DE MEDIDA"

    def __str__(self):
        return self.unidade


class Produto(models.Model):
    codigoproduto = models.CharField(max_length=255)
    nome = models.CharField(max_length=255)
    ncm = models.CharField(
        max_length=10, validators=[validate_campos], null=True, blank=True
    )
    cst = models.CharField(
        max_length=3, validators=[validate_campos], null=True, blank=True, default=0
    )
    cfop = models.CharField(
        max_length=4, validators=[validate_campos], null=True, blank=True
    )
    unimed = models.ForeignKey(
        UnidadeMedida,
        on_delete=models.DO_NOTHING,
        verbose_name="UNIDADE",
        null=True,
        blank=True,
    )
    preco = models.DecimalField(max_digits=11, decimal_places=2, default=0.00)
    estoque_ini = models.FloatField(default=0, null=True, blank=True)
    status_produto = models.BooleanField(default=True)
    descricao = models.CharField(max_length=255, null=True, blank=True)
    criadoem = models.DateTimeField(auto_now_add=True)
    atualizadoem = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "PRODUTO"
        verbose_name_plural = "PRODUTOS"
        ordering = ["nome"]

    def __str__(self):
        return str(self.nome)

    def get_nome_abreviado(self):
        return (
            self.nome.replace("Bebedouros", "")
            .replace("Bebedouro", "")
            .replace("Refrigerador", "")
        )

    def quantidade_em_producao(self):
        from producao.models import ProdutoAcabado

        return (
            ProdutoAcabado.objects.filter(produto=self.id)
            .exclude(status="estoque")
            .count()
        )


# para cada matéria prima um ou mais produtos
class MateriaPrimaProduto(models.Model):
    materiaprima = models.ForeignKey(
        MateriaPrima, on_delete=models.PROTECT, verbose_name="MATERIA PRIMA"
    )
    produto = models.ManyToManyField(Produto, through="ProdutosMatPri", blank=True)
    valor = models.DecimalField(
        "VALOR CUSTO", max_digits=9, decimal_places=2, default=0, null=True, blank=True
    )
    criadoem = models.DateTimeField(auto_now_add=True)
    atualizadoem = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "MATÉRIA PRIMA PRODUTO"
        verbose_name_plural = "MATÉRIA PRIMA PRODUTOS"

    def __str__(self):
        return str(self.materiaprima.nome)

    # def mp_prod_edit(self):
    #     return _("producao:previsaoEstoque", {"id_produto": self.id})


class ProdutosMatPri(models.Model):
    mp = models.ForeignKey(MateriaPrimaProduto, on_delete=models.RESTRICT)
    prod = models.ForeignKey(Produto, on_delete=models.RESTRICT)
    quant = models.DecimalField(
        "QUANTIDADE",
        max_digits=10,
        decimal_places=2,
        default=0.0,
        null=True,
        blank=True,
    )
