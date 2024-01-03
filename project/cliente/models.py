from django.db import models
from django.urls import reverse_lazy as _
from project.constantes import ESCOLHAS_ESTADO, CONTRIBUINTE_INSS
from django_cpf_cnpj.fields import CPFField, CNPJField


class Cliente(models.Model):
    nome = models.CharField("NOME COMPLETO", max_length=100)
    nome_fantasia = models.CharField("NOME FANTASIA", max_length=100)
    tel_principal = models.CharField("TELEFONE PRINCIPAL", max_length=45, blank=True)
    tel_contato = models.CharField("TELEFONE DE CONTATO", max_length=45, blank=True)
    email = models.EmailField("E-MAIL", max_length=100, blank=True)
    cpf = CPFField(masked=True, blank=True, null=True)
    cnpj = CNPJField(masked=True, blank=True, null=True)
    insc_estadual = models.CharField("INSCRIÇÃO ESTADUAL", max_length=15, blank=True)
    logradouro = models.CharField("LOGRADURO", max_length=100, blank=True)
    numero = models.CharField("NÚMERO", max_length=30, blank=True)
    complemento = models.CharField("COMPLEMENTO", max_length=60, blank=True, null=True)
    bairro = models.CharField("BAIRRO", max_length=60, blank=True)
    cep = models.CharField("CEP", max_length=10, blank=True)
    estado = models.CharField(
        "ESTADO", choices=ESCOLHAS_ESTADO, max_length=2, blank=True
    )
    pais = models.CharField("PAIS", max_length=60, null=True, blank=True)
    cidade = models.CharField("CIDADE", max_length=60, blank=True)
    status_cliente = models.BooleanField("ATIVO", default=True)
    contribuinte_inss = models.CharField(
        "Contribuinte INSS",
        choices=CONTRIBUINTE_INSS,
        default="1",
        max_length=255,
        blank=True,
    )
    mercadolivre_id = models.CharField("MERCADOLIVRE_ID", max_length=60, blank=True)
    descricao = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "CLIENTE"
        verbose_name_plural = "CLIENTES"

    def __str__(self):
        try:
            return "%s" % self.nome
        except:
            return "%s" % self.pk

    def cliente_gau_details(self):
        return _("cliente:clienteDetails", args=[self.pk])

    def cliente_gau_edit(self):
        return _("cliente:clienteUpdate", args=[self.pk])

    def cliente_gau_delete(self):
        return _("cliente:clienteDelete", args=[self.pk])
