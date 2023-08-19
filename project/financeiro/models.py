import os
from decimal import Decimal
from django.db import models
from django.urls import reverse_lazy as _
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import datetime

from compra.models import Compra
from despesa.models import Despesa
from receita.models import Receita
from venda.models import FormaPagamento, Venda

today = datetime.date.today


def path_and_rename(instance, filename):
    upload_to = "financeiro"
    time = datetime.datetime.now()
    hour = time.strftime("%H")
    minute = time.strftime("%M")
    printar = f"{hour}H{minute}m"
    if instance.venda.id:
        filename = "{}_{}.jpg".format(instance.venda.vendedor, printar)
    else:
        filename = "{}_{}.jpg".format(instance.receita.vendedor, printar)
    return os.path.join(upload_to, filename)


class ContaReceber(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.RESTRICT, null=True)
    parcela = models.CharField(
        max_length=11, null=True, blank=True
    )  # número da parcela
    receita = models.ForeignKey(Receita, on_delete=models.RESTRICT, null=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    datadocumento = models.DateField(default=today)
    datavencimento = models.DateField("Data do vencimento")
    datapagamento = models.DateField(blank=True, null=True)
    imagem = models.ImageField(upload_to=path_and_rename, null=True, blank=True)
    responsavel = models.CharField(max_length=255, null=True, blank=True)
    formapgto = models.ForeignKey(FormaPagamento, on_delete=models.RESTRICT)
    detalhes = models.CharField(max_length=300, null=True, blank=True)

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
    Comissao.objects.get(parcela=instance).delete()


class Comissao(models.Model):
    parcela = models.ForeignKey(ContaReceber, on_delete=models.CASCADE)
    comissao = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    data_comissao = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = "Comissão"
        verbose_name_plural = "Comissões"

    def __str__(self):
        return f"{self.parcela.venda.cliente} - {self.parcela.venda} - parcela: {self.parcela}"

    def comissao_edit(self):
        return _("financeiro:updateDataComissao", args=[self.pk])


class ContaPagar(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, null=True)
    despesa = models.ForeignKey(Despesa, on_delete=models.CASCADE, null=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    datadocumento = models.DateField(default=today)
    datavencimento = models.DateField()
    datapagamento = models.DateField(null=True, blank=True)
    formapgto = models.ForeignKey(FormaPagamento, on_delete=models.RESTRICT)
    detalhes = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        if self.despesa:
            return "%s - %s" % (self.despesa.nome, self.valor)
        if self.compra:
            return "%s - %s" % (self.compra.fornecedor, self.valor)


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
