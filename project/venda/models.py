from decimal import Decimal
import os
from django.db import models
from django.urls import reverse_lazy as _
import datetime
from django.db.models import Sum
from django.db.models.signals import post_delete
from django.dispatch import receiver
import base64

from cliente.models import Cliente
from produto.models import Produto
from transportadora.models import Transportadora
from project.constantes import ESCOLHAS_STATUSVENDAS

from django.contrib.auth.models import User


time = datetime.datetime.now()
date = time.strftime("%d-%m-%y")
hour = time.strftime("%H")
minute = time.strftime("%M")
seconds = time.strftime("%S")
printar = f"{hour}H{minute}m{seconds}s"


def path_and_receita_comprovante(instance, filename):
    ext = filename.split(".")
    filename = "{}_{}_{}.{}".format(filename[:-4], date, printar, ext[-1])
    return os.path.join(filename)


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
        # related_name="clientevenda",
        # verbose_name="CLIENTE",
    )
    data_pedido = models.DateTimeField(default=datetime.date.today)
    data_entrega = models.DateField(null=True, blank=True)
    transportadora = models.ForeignKey(
        Transportadora, on_delete=models.CASCADE, verbose_name="TRANSPORTADORA"
    )
    valor_frete = models.DecimalField(max_digits=11, decimal_places=2, default=0.00)
    vendedor = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, blank=True)
    valor_venda = models.DecimalField(max_digits=11, decimal_places=2, default=0.00)
    taxa_mercadolivre = models.IntegerField(null=True, blank=True)
    porcentagem_desconto = models.IntegerField(default=0.00)
    subtotal = models.DecimalField(max_digits=11, decimal_places=2, default=0.00)
    status_venda = models.CharField(
        choices=ESCOLHAS_STATUSVENDAS, null=False, blank=False, max_length=50
    )
    status_expedicao = models.CharField(
        null=True, blank=True, max_length=60, default="Conferir dados"
    )
    data_status_expedicao = models.DateTimeField(auto_now=True)
    condicaopgto = models.ForeignKey(CondicaoVenda, on_delete=models.RESTRICT)
    dias_prim_par = models.IntegerField()
    dias_outras_par = models.IntegerField()
    parcelas = models.IntegerField()
    formapgto = models.ForeignKey(FormaPagamento, on_delete=models.RESTRICT)
    detalhes = models.CharField(max_length=255, null=True, blank=True)
    atualizadoem = models.DateTimeField(auto_now=True)
    atualizadopor = models.CharField(max_length=255)
    valortotalcomimposto = models.DecimalField(
        max_digits=11, decimal_places=2, default=0.00, blank=True, null=True
    )
    chave = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=55, null=True, blank=True)
    motivo = models.CharField(max_length=255, null=True, blank=True)
    uuid = models.CharField(max_length=55, null=True, blank=True)
    numero_nf = models.IntegerField(null=True, blank=True)
    xml = models.CharField(max_length=255, null=True, blank=True)
    danfe = models.CharField(max_length=255, null=True, blank=True)
    danfe_simples = models.CharField(max_length=255, null=True, blank=True)
    danfe_etiqueta = models.CharField(max_length=255, null=True, blank=True)
    codigo_mercadolivre = models.CharField(max_length=255, null=True, blank=True)
    nickname_mercadolivre = models.CharField(max_length=255, null=True, blank=True)
    cotacao_transportadora = models.CharField(max_length=100, null=True, blank=True)
    quemrecebe_mercadolivre = models.CharField(max_length=255, null=True, blank=True)
    telefonequemrecebe_mercadolivre = models.CharField(
        max_length=25, null=True, blank=True
    )
    etiqueta_impressa = models.BooleanField(blank=True, null=True, default=False)
    urgente = models.BooleanField(blank=True, null=True, default=False)
    comprovante = models.FileField(
        upload_to=path_and_receita_comprovante, null=True, blank=True
    )

    class Meta:
        verbose_name = "VENDA"
        verbose_name_plural = "VENDAS"

    def __str__(self) -> str:
        return str(self.id)

    def get_hash(self):
        """codifica o pk para envio do orçamento"""
        pk_string = str(self.pk)
        hash = base64.b64encode(pk_string.encode("utf-8")).decode("utf-8")
        return str(hash)

    def venda_gau_edit(self):
        return _("venda:vendaUpdate", args=[self.pk])

    def venda_expedicao_edit(self):
        return _("venda:expedicaoNF", args=[self.pk])

    def venda_gau_delete(self):
        return _("venda:vendaDelete", args=[self.pk])

    def qtde_produtos(self):
        if self.vendaproduto_set.aggregate(Sum("quantidade"))["quantidade__sum"]:
            return int(
                self.vendaproduto_set.aggregate(Sum("quantidade"))["quantidade__sum"]
            )
        else:
            return 0

    def get_lista_produtos_to_iniciar_producao(self):
        lista_produtos = []
        for produto in Produto.objects.all():
            qtde = 0
            _produto = self.vendaproduto_set.filter(produto=produto)
            if _produto.count() > 0:
                _produto = _produto[0]
                qtde = _produto.quantidade
            lista_produtos.append(
                {"cod": produto.codigoproduto, "produto": produto.get_nome_abreviado()}
            )
        return lista_produtos

    def status_expedicao_backgroundcolor(self):
        "retorna cor para colocar coluna"
        retorno = ""
        if self.status_expedicao == "Parado":
            retorno = "bg-secondary"
        if self.status_expedicao == "Fazer Cotação":
            retorno = "bg-info"
        if self.status_expedicao == "Agendar Transportadora":
            retorno = "bg-info"
        if self.status_expedicao == "Informar cliente p/ buscar":
            retorno = "bg-info"
        if self.status_expedicao == "Aguardando transportadora":
            retorno = "bg-warning"
        if self.status_expedicao == "Aguardando Cliente":
            retorno = "bg-warning"
        if self.status_expedicao == "Aguardando Concluir Produtos":
            retorno = "bg-danger"
        if self.status_expedicao == "Enviado":
            retorno = "bg-success"
        if self.status_expedicao == "Conferir dados":
            retorno = "bg-danger"
        if self.status_expedicao == "Combinar Entrega":
            retorno = "bg-danger"
        if self.status_expedicao == "Emitir Boleto":
            retorno = "bg-danger"
        if self.status_expedicao == "Aguardando Pagamento":
            retorno = "bg-danger"

        # status venda diferente status expedicao
        if self.status_venda == "enviado":
            retorno = "bg-success"

        return retorno


class Voltagem(models.Model):
    nome = models.CharField(max_length=10)

    class Meta:
        verbose_name = "VOLTAGEM"
        verbose_name_plural = "VOLTAGENS"

    def __str__(self):
        return self.nome


class Torneira(models.Model):
    nome = models.CharField(max_length=100)

    class Meta:
        verbose_name = "TORNEIRA"
        verbose_name_plural = "TORNEIRAS"

    def __str__(self):
        return self.nome


class Adesivado(models.Model):
    nome = models.CharField(max_length=100)

    class Meta:
        verbose_name = "ADESIVADO"
        verbose_name_plural = "ADESIVADOS"

    def __str__(self):
        return self.nome


class VendaProduto(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.RESTRICT)
    quantidade = models.IntegerField(default=1)
    preco = models.DecimalField(max_digits=11, decimal_places=2, default=0.00)
    subtotal = models.DecimalField(max_digits=11, decimal_places=2, default=0.00)
    voltagem = models.ForeignKey(Voltagem, on_delete=models.RESTRICT)
    torneira = models.ForeignKey(Torneira, on_delete=models.RESTRICT)
    adesivado = models.ForeignKey(Adesivado, on_delete=models.RESTRICT)

    def __str__(self):
        return str(self.produto)

    def get_qtde_list_for_loop(self):
        """
        funcao criada para retornar um vetor da qtde pro loop na template
        """
        if self.quantidade > 1:
            return range(1, self.quantidade + 1)
        else:
            return range(0, self.quantidade)


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
