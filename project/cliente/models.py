from django.db import models
from django.urls import reverse_lazy as _
from project.constantes import ESCOLHAS_ESTADO


class Cliente(models.Model):
    nome = models.CharField("NOME COMPLETO", max_length=200)
    nome_fantasia = models.CharField("NOME FANTASIA", max_length=200)
    tel_principal = models.CharField("TELEFONE PRINCIPAL", max_length=15, blank=True)
    tel_contato = models.CharField("TELEFONE DE CONTATO", max_length=15, blank=True)
    email = models.EmailField("E-MAIL", max_length=254, blank=True)
    cpf = models.CharField("CPF", max_length=14, blank=True)
    cnpj = models.CharField("CNPJ", max_length=18, blank=True)
    insc_estadual = models.CharField("INSCRIÇÃO ESTADUAL", max_length=15, blank=True)
    logradouro = models.CharField("LOGRADURO", max_length=200, blank=True)
    numero = models.CharField("NÚMERO", max_length=30, blank=True)
    complemento = models.CharField("COMPLEMENTO", max_length=100, blank=True)
    bairro = models.CharField("BAIRRO", max_length=100, blank=True)
    cep = models.CharField("CEP", max_length=11, blank=True)
    estado = models.CharField(
        "ESTADO", choices=ESCOLHAS_ESTADO, max_length=2, blank=True
    )
    cidade = models.CharField("CIDADE", max_length=100, blank=True)
    status_cliente = models.BooleanField("ATIVO", default=True)

    class Meta:
        verbose_name = "CLIENTE"
        verbose_name_plural = "CLIENTES"

    # def __str__(self):
    #     return self.nome

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
