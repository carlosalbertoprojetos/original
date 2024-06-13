from django.db import models
from django_cpf_cnpj.fields import CPFField, CNPJField
from django.urls import reverse_lazy as _


from cliente.models import Cliente
from project.constantes import ESCOLHAS_ESTADO
from produto.models import Produto


class Cidade(models.Model):
    estado = models.CharField(
        choices=ESCOLHAS_ESTADO, max_length=2, null=True, blank=True
    )
    nome = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Cidade"
        verbose_name_plural = "Cidades"
        ordering = ["estado"]

    def __str__(self):
        return f"{self.nome}/{self.estado}"


class Regiao(models.Model):
    nome = models.CharField(max_length=100)
    cidade = models.ManyToManyField(Cidade, related_name="CidadeRegião")

    class Meta:
        verbose_name = "Região"
        verbose_name_plural = "Regiões"

    def __str__(self):
        return str(self.nome)


class Representante(models.Model):
    nome = models.CharField(max_length=200)
    nome_fantasia = models.CharField(max_length=200)
    tel_principal = models.CharField(max_length=14, null=True, blank=True)
    tel_contato = models.CharField(max_length=14, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    cpf = CPFField(masked=True, blank=True, null=True)
    cnpj = CNPJField(masked=True, blank=True, null=True)
    mei = models.CharField(max_length=255, null=True, blank=True)
    insc_estadual = models.CharField(max_length=15, null=True, blank=True)
    logradouro = models.CharField(max_length=200, null=True, blank=True)
    numero = models.CharField(max_length=30, null=True, blank=True)
    complemento = models.CharField(max_length=100, null=True, blank=True)
    bairro = models.CharField(max_length=100, blank=True)
    cep = models.CharField(max_length=11, null=True, blank=True)
    estado = models.CharField(
        choices=ESCOLHAS_ESTADO, max_length=2, null=True, blank=True
    )
    cidade = models.CharField(max_length=100, null=True, blank=True)
    status_representante = models.BooleanField("Ativo", default=True)
    regiao = models.ForeignKey(Regiao, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = "Representante"
        verbose_name_plural = "Representantes"
        ordering = ["nome"]

    def __str__(self):
        return str(self.nome)

    def rep_gau_edit(self):
        return _("representante:representanteUpdate", args=[self.pk])

    def rep_gau_delete(self):
        return _("representante:representanteDelete", args=[self.pk])


class DadosBancarios(models.Model):
    representante = models.ForeignKey(
        Representante, on_delete=models.CASCADE, null=True
    )
    banco = models.CharField(max_length=50)
    agencia = models.CharField(max_length=20)
    conta = models.CharField(max_length=20)

    class Meta:
        verbose_name = "Dados Bancários"
        verbose_name_plural = "Dados Bancários"

    def __str__(self):
        return str(self.banco)


class ServicoRepresentante(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    representante = models.ForeignKey(Representante, on_delete=models.CASCADE)
    produto = models.ManyToManyField(Produto, related_name="ServiçoProdutos")
    data_recebimento = models.DateField(null=True, blank=True)
    data_entrega = models.DateField(null=True, blank=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_pagamento = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "Serviço"
        verbose_name_plural = "Serviços"
        ordering = ["data_recebimento"]

    def __str__(self):
        return f"{self.representante}-{self.cliente}"

    def serv_gau_edit(self):
        return _("representante:servicosUpdate", args=[self.pk])

    def serv_gau_delete(self):
        return _("representante:servicosDelete", args=[self.pk])
