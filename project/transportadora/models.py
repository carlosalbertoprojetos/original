from django.db import models
from django.urls import reverse_lazy as _
from project.constantes import ESCOLHAS_ESTADO
from django_cpf_cnpj.fields import CPFField, CNPJField


from cliente.models import Cliente


class Transportadora(models.Model):
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
    status_transportadora = models.BooleanField(default=True)
    atuacao = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "Transportadora"
        verbose_name_plural = "Transportadoras"
        ordering = ["nome"]

    def __str__(self):
        return self.nome

    def transp_gau_edit(self):
        return _("transportadora:transporteUpdate", args=[self.pk])

    def transp_gau_delete(self):
        return _("transportadora:transporteDelete", args=[self.pk])

class Rotas(models.Model):
    """ classe para definir rotas """
    cidade = models.TextField(
         null=True, blank=True
    )
    estado = models.CharField(
        choices=ESCOLHAS_ESTADO, max_length=2, null=True, blank=True
    )
    transportadoras = models.ManyToManyField(Transportadora)
    como_cotar = models.TextField(null=True, blank=True)

    def get_transportadoras(self):
        return "\n".join([p.nome for p in self.transportadoras.all()])

# class CotacaoTransporte(models.Model):
#     cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
#     transportadora = models.ForeignKey(Transportadora, on_delete=models.CASCADE)
#     origem = models.CharField(max_length=100)
#     destino = models.CharField(max_length=100)
#     valor = models.DecimalField(max_digits=10, decimal_places=2)
#     data_criacao = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Cotação de {self.origem} para {self.destino} - Valor: {self.valor}"
