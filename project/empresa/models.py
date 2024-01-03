from django.db import models
from django.urls import reverse_lazy as _
from project.constantes import ESCOLHAS_ESTADO, REGIMES_TRIBUTARIOS
from django_cpf_cnpj.fields import CPFField, CNPJField


class Empresa(models.Model):
    nome = models.CharField(max_length=200)
    nome_fantasia = models.CharField(max_length=200)
    tel_principal = models.CharField(max_length=14, null=True, blank=True)
    tel_contato = models.CharField(max_length=14, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    cpf = CPFField(masked=True, blank=True, null=True)
    cnpj = CNPJField(masked=True, blank=True, null=True)
    # cpf = models.CharField(max_length=14, null=True, blank=True)
    # cnpj = models.CharField(max_length=18, null=True, blank=True)
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
    regimetributario = models.CharField(choices=REGIMES_TRIBUTARIOS, max_length=100, null=True, blank=True)
    presenca = models.IntegerField(default=3, null=True, blank=True)
    modalidade_frete = models.IntegerField(default=0, null=True, blank=True)
    natureza_operacao = models.CharField(max_length=100, null=True, blank=True)

    webmania_consumerkey = models.CharField(max_length=255, null=True, blank=True)
    webmania_consumersecret = models.CharField(max_length=255, null=True, blank=True)
    webmania_accesstoken = models.CharField(max_length=255, null=True, blank=True)
    webmania_accesstokensecret = models.CharField(max_length=255, null=True, blank=True)
    webmania_bearer = models.CharField(max_length=255, null=True, blank=True)
    webmania_classedeimposto = models.CharField(max_length=255, null=True, blank=True)


    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresa"
        ordering = ["nome"]

    def __str__(self):
        return str(self.nome)

    def emp_gau_edit(self):
        return _("empresa:empresaUpdate", args=[self.pk])

    def emp_gau_delete(self):
        return _("empresa:empresaDelete", args=[self.pk])


class DadosBancarios(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.RESTRICT)
    banco = models.CharField(max_length=200)
    num_banco = models.CharField(max_length=200)
    agencia = models.CharField(max_length=200)
    conta = models.CharField(max_length=200)
    dac = models.IntegerField()

    class Meta:
        verbose_name = "Banco"
        verbose_name_plural = "Bancos"

    def __str__(self):
        return f"{self.banco}_{self.empresa.nome_fantasia}"
