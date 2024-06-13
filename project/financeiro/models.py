import os
import datetime
from decimal import Decimal
from django.db import models
from django.urls import reverse_lazy as _
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User

from compra.models import Compra
from despesa.models import Despesa
from receita.models import Receita
from venda.models import FormaPagamento, Venda
from empresa.models import DadosBancarios


today = datetime.date.today
time = datetime.datetime.now()
date = time.strftime("%d-%m-%y")
hour = time.strftime("%H")
minute = time.strftime("%M")
seconds = time.strftime("%S")
printar = f"{hour}H{minute}m{seconds}s"


class ControleExtratosBancarios(models.Model):
    responsavel = models.ForeignKey(User, on_delete=models.RESTRICT)
    arquivo = models.FileField(upload_to="extrato/")
    datahora = models.DateTimeField()  # data/hora registrada no extrato
    conta = models.ForeignKey(DadosBancarios, on_delete=models.RESTRICT)
    upload = models.DateTimeField(default=time)  # data/hora do upload
    saldo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    conciliado = models.BooleanField(default=False)

    class Meta:
        unique_together = [["datahora", "conta"]]

    def __str__(self):
        return str(self.conta)


class ExtratoBancario(models.Model):
    controle = models.ForeignKey(ControleExtratosBancarios, on_delete=models.CASCADE)
    data = models.DateField()
    lancamento = models.CharField(max_length=255)
    origem = models.CharField(max_length=255, null=True, blank=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    saldo = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    conciliado = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = [["data", "lancamento", "origem", "valor"]]


def path_and_receita_boleto(instance, filename):
    ext = filename.split(".")
    if instance.venda:
        filename = "{}_{}_{}.{}".format(instance.venda.vendedor, date, printar, ext[-1])
    else:
        filename = "{}_{}_{}.{}".format(instance.receita.nome, date, printar, ext[-1])
    return os.path.join(filename)


def path_and_receita_comprovante(instance, filename):
    ext = filename.split(".")
    if instance.venda:
        filename = "{}_{}_{}.{}".format(instance.venda.vendedor, date, printar, ext[-1])
    else:
        filename = "{}_{}_{}.{}".format(instance.receita.nome, date, printar, ext[-1])
    return os.path.join(filename)


def path_and_despesa_boleto(instance, filename):
    ext = filename.split(".")
    if instance.compra:
        filename = "{}_{}_{}.{}".format(
            instance.compra.fornecedor, date, printar, ext[-1]
        )
    else:
        filename = "{}_{}_{}.{}".format(instance.despesa.nome, date, printar, ext[-1])
    return os.path.join(filename)


def path_and_despesa_comprovante(instance, filename):
    ext = filename.split(".")
    if instance.compra:
        filename = "{}_{}_{}.{}".format(
            instance.compra.fornecedor, date, printar, ext[-1]
        )
    else:
        filename = "{}_{}_{}.{}".format(instance.despesa.nome, date, printar, ext[-1])
    return os.path.join(filename)


class ContaReceber(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, null=True)
    parcela = models.CharField(
        max_length=11, null=True, blank=True
    )  # número da parcela
    receita = models.ForeignKey(Receita, on_delete=models.CASCADE, null=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    datadocumento = models.DateField(default=today)
    datavencimento = models.DateField("Data do vencimento")
    datapagamento = models.DateField(blank=True, null=True)
    boleto = models.FileField(upload_to=path_and_receita_boleto, null=True, blank=True)
    comprovante = models.FileField(
        upload_to=path_and_receita_comprovante, null=True, blank=True
    )
    responsavel = models.CharField(max_length=255, null=True, blank=True)
    formapgto = models.ForeignKey(FormaPagamento, on_delete=models.RESTRICT)
    # dados_boleto = models.JSONField(default=dict, null=True, blank=True)
    detalhes = models.CharField(max_length=300, null=True, blank=True)
    conciliado = models.ForeignKey(
        ExtratoBancario, on_delete=models.RESTRICT, null=True, blank=True
    )

    class Meta:
        verbose_name = "Contas a receber"
        verbose_name_plural = "Contas a receber"

    def __str__(self):
        if self.receita:
            return "%s - %s" % (self.receita.nome, self.valor)
        if self.venda:
            return "%s - %s" % (self.venda.cliente, self.valor)


@receiver(post_save, sender=ContaReceber)
def comissaoAdd(sender, instance, **kwargs):
    comissao = Comissao.objects.filter(parcela__venda=instance.venda).filter(
        parcela__parcela=instance.parcela
    )
    if instance.venda:
        percent_comis = Decimal(0.03)
        comissao_vlr = instance.valor * percent_comis
        if not comissao:
            Comissao.objects.create(parcela=instance, comissao=comissao_vlr)


@receiver(post_delete, sender=ContaReceber)
def comissaoDel(sender, instance, **kwargs):
    if Comissao.objects.filter(parcela=instance):
        Comissao.objects.get(parcela=instance).delete()


class Comissao(models.Model):
    parcela = models.ForeignKey(ContaReceber, on_delete=models.CASCADE)
    comissao = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    data_comissao = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = "Comissão"
        verbose_name_plural = "Comissões"

    def __str__(self):
        return str(self.parcela)

    def comissao_edit(self):
        return _("financeiro:updateDataComissao", args=[self.pk])


class ContaPagar(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, null=True, blank=True)
    despesa = models.ForeignKey(
        Despesa, on_delete=models.CASCADE, null=True, default=""
    )
    valor = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    valor_pago = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.0, null=True, blank=True
    )
    datadocumento = models.DateField(default=today)
    datavencimento = models.DateField()
    datapagamento = models.DateField(null=True, blank=True)
    boleto = models.FileField(upload_to=path_and_despesa_boleto, null=True, blank=True)
    comprovante = models.FileField(
        upload_to=path_and_despesa_comprovante, null=True, blank=True
    )
    formapgto = models.ForeignKey(FormaPagamento, on_delete=models.RESTRICT)
    detalhes = models.CharField(max_length=300, null=True, blank=True)
    conciliado = models.ForeignKey(
        ExtratoBancario, on_delete=models.RESTRICT, null=True, blank=True
    )

    class Meta:
        verbose_name = "Contas a pagar"
        verbose_name_plural = "Contas a pagar"

    def __str__(self):
        if self.despesa:
            return "%s - %s" % (self.despesa.nome, self.datadocumento)
        if self.compra:
            return "%s - %s" % (self.compra.fornecedor, self.datadocumento)

    def parcela_gau_delete(self):
        return _("financeiro:parcelaDelete", args=[self.pk])


@receiver(post_save, sender=ContaPagar)
def totalContaPagarAdd(sender, instance, **kwargs):
    if instance.compra:
        num_parc = ContaPagar.objects.filter(compra__id=instance.compra.id)
        instance.compra.num_parcelas = num_parc.count()
        soma = 0
        for p in num_parc:
            soma += p.valor
        instance.compra.total = soma
        instance.compra.save()
    elif instance.despesa:
        num_parc = ContaPagar.objects.filter(despesa__id=instance.despesa.id)
        instance.despesa.num_parcelas = num_parc.count()
        soma = 0
        for p in num_parc:
            soma += p.valor
        instance.despesa.total = soma
        instance.despesa.save()


@receiver(post_delete, sender=ContaPagar)
def totalContaPagarDel(sender, instance, **kwargs):
    try:
        if instance.compra:
            num_parc = ContaPagar.objects.filter(compra__id=instance.compra.id)
            instance.compra.num_parcelas = num_parc.count()
            soma = 0
            for p in num_parc:
                soma += p.valor
            instance.compra.total = soma
            instance.compra.save()
        elif instance.despesa:
            num_parc = ContaPagar.objects.filter(despesa__id=instance.despesa.id)
            instance.despesa.num_parcelas = num_parc.count()
            soma = 0
            for p in num_parc:
                soma += p.valor
            instance.despesa.total = soma
            instance.despesa.save()
    except:
        num_parc = None
