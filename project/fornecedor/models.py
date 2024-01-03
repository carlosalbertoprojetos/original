from django.db import models
from django.urls import reverse_lazy as _
from django_cpf_cnpj.fields import CPFField, CNPJField

from project.constantes import ESCOLHAS_ESTADO


class UfsCidades(models.Model):
    uf = models.CharField(max_length=2)
    cidade = models.CharField(max_length=200)

    def __str__(self):
        return self.uf / self.cidade


class Fornecedor(models.Model):
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
    status_fornecedor = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Fornecedor"
        verbose_name_plural = "Fornecedores"
        ordering = ["nome"]

    def __str__(self):
        return str(self.nome)

    def forn_gau_edit(self):
        return _("fornecedor:fornecedorUpdate", args=[self.pk])

    def forn_gau_delete(self):
        return _("fornecedor:fornecedorDelete", args=[self.pk])
