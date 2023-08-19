from decimal import Decimal
from django.db import models
from django.urls import reverse_lazy as _
import datetime
from django.db.models import Sum
from django.db.models.signals import post_delete
from django.dispatch import receiver

from cliente.models import Cliente
from produto.models import Produto
from transportadora.models import Transportadora
from project.constantes import ESCOLHAS_STATUSVENDAS


class MaximoDesconto(models.Model):
    qtde = models.IntegerField(default=10, null=False)

    def __str__(self):
        return str(self.qtde)


class FormaPagamento(models.Model):
    nome = models.CharField("Forma de Pagamento", max_length=255)
    descricao = models.TextField()

    def __str__(self):
        return self.nome


class CondicaoVenda(models.Model):
    nome = models.CharField(max_length=255)
    parcelas = models.IntegerField()
    primeira = models.IntegerField()
    demais = models.IntegerField()
    formapgto = models.ForeignKey(FormaPagamento, on_delete=models.RESTRICT)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Condição de pagamento"
        verbose_name_plural = "Condições de pagamento"


class Venda(models.Model):
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.RESTRICT,
        related_name="clientevenda",
        verbose_name="CLIENTE",
    )
    data_pedido = models.DateField(default=datetime.date.today)
    data_entrega = models.DateField(null=True, blank=True)
    transportadora = models.ForeignKey(
        Transportadora, on_delete=models.CASCADE, verbose_name="TRANSPORTADORA"
    )
    valor_frete = models.DecimalField(max_digits=11, decimal_places=2, default=0.00)
    vendedor = models.CharField(max_length=255, null=True, blank=True)
    valor_venda = models.DecimalField(max_digits=11, decimal_places=2, default=0.00)
    porcentagem_desconto = models.IntegerField()
    subtotal = models.DecimalField(max_digits=11, decimal_places=2, default=0.00)
    status_venda = models.CharField(
        choices=ESCOLHAS_STATUSVENDAS, null=False, blank=False, max_length=50
    )
    condicaopgto = models.ForeignKey(CondicaoVenda, on_delete=models.RESTRICT)
    dias_prim_par = models.IntegerField()
    dias_outras_par = models.IntegerField()
    parcelas = models.IntegerField()
    formapgto = models.ForeignKey(FormaPagamento, on_delete=models.RESTRICT)
    detalhes = models.CharField(max_length=255, null=True, blank=True)
    atualizadoem = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "VENDA"
        verbose_name_plural = "VENDAS"

    def __str__(self) -> str:
        return str(self.id)

    def venda_gau_detail(self):
        return _("venda:vendaDetails", args=[self.pk])

    def venda_gau_edit(self):
        return _("venda:vendaUpdate", args=[self.pk])

    def venda_gau_delete(self):
        return _("venda:vendaDelete", args=[self.pk])

    def qtde_produtos(self):
        if self.vendaproduto_set.aggregate(Sum("quantidade"))["quantidade__sum"]:
            return int(
                self.vendaproduto_set.aggregate(Sum("quantidade"))["quantidade__sum"]
            )
        else:
            return 0

    def get_lista_produtos(self):
        lista_produtos = []
        for produto in Produto.objects.all():
            qtde = 0
            _produto = self.vendaproduto_set.filter(produto=produto)
            if _produto.count() > 0:
                _produto = _produto[0]
                qtde = _produto.quantidade
            lista_produtos.append(
                {"produto": produto.get_nome_abreviado(), "qtde": qtde}
            )
        return lista_produtos


# =====================================================================================
# VOLTAGEM


class Voltagem(models.Model):
    nome = models.CharField(max_length=10)

    class Meta:
        verbose_name = "VOLTAGEM"
        verbose_name_plural = "VOLTAGENS"

    def __str__(self):
        return self.nome


# =====================================================================================
# TORNEIRAS


class Torneira(models.Model):
    nome = models.CharField(max_length=100)

    class Meta:
        verbose_name = "TORNEIRA"
        verbose_name_plural = "TORNEIRAS"

    def __str__(self):
        return self.nome


# =====================================================================================
# ADESIVADO


class Adesivado(models.Model):
    nome = models.CharField(max_length=100)

    class Meta:
        verbose_name = "ADESIVADO"
        verbose_name_plural = "ADESIVADOS"

    def __str__(self):
        return self.nome


class VendaProduto(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.DO_NOTHING)
    quantidade = models.IntegerField(default=1)
    preco = models.DecimalField(max_digits=11, decimal_places=2, default=0.00)
    subtotal = models.DecimalField(max_digits=11, decimal_places=2, default=0.00)
    voltagem = models.ForeignKey(Voltagem, on_delete=models.RESTRICT)
    torneira = models.ForeignKey(Torneira, on_delete=models.RESTRICT)
    adesivado = models.ForeignKey(Adesivado, on_delete=models.RESTRICT)

    class Meta:
        verbose_name = "PRODUTO DA VENDA"
        verbose_name_plural = "PRODUTOS DA VENDA"

    def __str__(self):
        return str(self.produto.nome)


@receiver(post_delete, sender=VendaProduto)
def totalVendaProdutoDel(sender, instance, **kwargs):
    valor = VendaProduto.objects.filter(venda__id=instance.venda.id)
    soma = 0
    for p in valor:
        soma += p.subtotal
    percentual = Decimal(instance.venda.porcentagem_desconto / 100)
    calc = percentual * soma
    instance.venda.valor_venda = soma
    instance.venda.subtotal = soma - calc
    instance.venda.save()
