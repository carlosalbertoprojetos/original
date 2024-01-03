from django.db import models
from django.urls import reverse_lazy as _
from django.core.exceptions import ValidationError


from materiaprima.models import MateriaPrima
from empresa.models import Empresa


def validate_campos(value):
    if not value.isdigit():
        raise ValidationError("O campo deve conter apenas números")


class UnidadeMedida(models.Model):
    unidade = models.CharField("UNIDADE", max_length=10)
    descricao = models.TextField("DESCRIÇÃO", blank=True)

    class Meta:
        verbose_name = "UNIDADE DE MEDIDA"
        verbose_name_plural = "UNIDADES DE MEDIDA"

    def __str__(self):
        return self.unidade


class Produto(models.Model):
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.DO_NOTHING,
        null=False,
        blank=False,
        max_length=255,
    )
    xped = models.CharField(max_length=15)
    ordem = models.CharField(max_length=6)
    codigoproduto = models.CharField(max_length=60)
    nome = models.CharField(max_length=120)
    ncm = models.CharField(
        max_length=8, validators=[validate_campos], null=True, blank=True
    )
    cst = models.CharField(
        max_length=3, validators=[validate_campos], null=True, blank=True, default=0
    )
    cest = models.CharField(
        max_length=7, validators=[validate_campos], null=True, blank=True
    )
    cfop = models.CharField(
        max_length=4, validators=[validate_campos], null=True, blank=True
    )
    unimed = models.ForeignKey(
        UnidadeMedida,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        max_length=6,
    )
    preco = models.DecimalField(max_digits=11, decimal_places=2, default=0.00)
    peso = models.IntegerField(null=True, blank=True)
    estoque_ini = models.FloatField(default=0, null=True, blank=True)

    aliq_icms_interno = models.FloatField(default=0, null=True, blank=True)
    aliq_ipi = models.FloatField(default=0, null=True, blank=True)

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

    def prod_gau_edit(self):
        return _("produto:produtoUpdate", args=[self.pk])

    def prod_gau_del(self):
        return _("produto:produtoDelete", args=[self.pk])

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


# peças produzidos/fabricados com objetivo de utilizar na fabricação do produto final
class Peca(models.Model):
    codigoproduto = models.CharField(max_length=60)
    nome = models.CharField(max_length=120)
    unimed = models.ForeignKey(
        UnidadeMedida,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        max_length=6,
    )
    peso = models.DecimalField(decimal_places=2, max_digits=6, null=True, blank=True)
    produto = models.ForeignKey(
        Produto,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )
    quantidade = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        default=1,
    )
    estoque_ini = models.FloatField(default=0, null=True, blank=True)
    status_produto = models.BooleanField(default=True)
    descricao = models.CharField(max_length=255, null=True, blank=True)
    criadoem = models.DateTimeField(auto_now_add=True)
    atualizadoem = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "PEÇA"
        verbose_name_plural = "PECAS"

    def __str__(self):
        return str(self.nome)

    def peca_gau_edit(self):
        return _("produto:pecaUpdate", args=[self.pk])

    def peca_gau_del(self):
        return _("produto:pecaDelete", args=[self.pk])


# registra a quantidade de matéria prima consumida para cada peça/produto
class ProdutoMatPri(models.Model):
    materiaprima = models.ForeignKey(MateriaPrima, on_delete=models.RESTRICT)
    peca = models.ForeignKey(Peca, on_delete=models.RESTRICT, null=True, blank=True)
    produto = models.ForeignKey(
        Produto,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
    )
    quantidade = models.DecimalField(
        decimal_places=2,
        max_digits=10,
    )

    class Meta:
        verbose_name = "QUANTIDADE DE MATÉRIA PRIMA POR PRODUTO"
        verbose_name = "QUANTIDADE DE MATÉRIAS PRIMAS POR PRODUTO"
        unique_together = ["materiaprima", "peca"], ["materiaprima", "produto"]

    def __str__(self):
        if self.peca:
            return f"{self.peca.nome}"
        else:
            return f"{self.produto.nome}"
