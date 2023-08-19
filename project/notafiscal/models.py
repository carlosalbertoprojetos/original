from django.db import models
from django.urls import reverse_lazy as _
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from decimal import Decimal

from fornecedor.models import Fornecedor
from materiaprima.models import MateriaPrima, MateriaPrimaFornecedor
from estoque.models import EstoqueMateriaPrima, EnderecoEstoque


class NFCompra(models.Model):
    fornecedor = models.ForeignKey(
        Fornecedor, on_delete=models.CASCADE, related_name="fornecedorNFCompra"
    )
    chavedeacesso = models.CharField("Chave de Acesso", max_length=255)
    naturezadaoperacao = models.CharField(
        "Natureza da Operação", max_length=255, null=True
    )
    numeroserie = models.CharField("Numero de Serie", max_length=255, null=True)
    protocoloautorizacaodeuso = models.CharField(
        "Protocolo de Autorização", max_length=255, null=True
    )
    nome_destinatario = models.CharField("Nome", max_length=255, null=True)
    cnpj_destinatario = models.CharField("Cnpj", max_length=255)
    bairro_destinatario = models.CharField("Bairro", max_length=255, null=True)
    cep_destinatario = models.CharField("Cep", max_length=255, null=True)
    data_emissao = models.DateField("Data Emissão", max_length=255)
    forma_pagamento = models.CharField("Forma de Pagamento", max_length=255, null=True)
    base_calculo_icms = models.CharField("Base Calculo Icms", max_length=255, null=True)
    valor_icms = models.DecimalField(max_digits=11, decimal_places=2, default=0.00)
    # base_calculo_icms_st = models.CharField('Base Calculo Icms St',max_length=200, null=True)
    # valor_icms_subs = models.DecimalField('Valor Icms Subs', null=True)
    # valor_importacao = models.DecimalField('Valor Importação', null=True)
    # valor_imcs_uf_remetente = models.DecimalField('Valor Icms UF Remetente', null=True)
    # valor_fcp_uf_dest = models.DecimalField('Valor Fcp Uf Dest', null=True)
    valor_pis = models.DecimalField(max_digits=11, decimal_places=2, default=0.00)
    valor_total_produtos = models.DecimalField(
        max_digits=11, decimal_places=2, default=0.00
    )
    valor_do_frete = models.DecimalField(max_digits=11, decimal_places=2, default=0.00)
    valor_do_seguro = models.DecimalField(max_digits=11, decimal_places=2, default=0.00)
    desconto = models.DecimalField(max_digits=11, decimal_places=2, default=0.00)
    outras_despesas = models.DecimalField(max_digits=11, decimal_places=2, default=0.00)
    valor_total_ipi = models.DecimalField(max_digits=11, decimal_places=2, default=0.00)
    # valor_icms_uf_dest = models.DecimalField('Valor Icms Uf Dest', null=True)
    # valor_total_trib = models.DecimalField('Valor Total Trib', null=True)
    valor_da_cofins = models.DecimalField(max_digits=11, decimal_places=2, default=0.00)
    valor_total_da_nota = models.DecimalField(
        max_digits=11, decimal_places=2, default=0.00
    )

    class Meta:
        verbose_name = "Nota Fiscal Compra"
        verbose_name_plural = "Notas Fiscais de compra"
        # ordering = ['numeroserie']

    def __str__(self):
        return str(self.fornecedor)

    def nfcompra_gau_detail(self):
        return _("notafiscal:nfcompraDetails", args=[self.pk])

    def nfcompra_gau_edit(self):
        return _("notafiscal:nfcompraUpdate", args=[self.pk])

    def nfcompra_gau_delete(self):
        return _("notafiscal:nfcompraDelete", args=[self.pk])


class NFItem(models.Model):
    notafiscal = models.ForeignKey(NFCompra, on_delete=models.CASCADE, null=False)
    materiaprima = models.CharField("Produto", max_length=255)
    codigo_produto = models.CharField("Codigo Produto", max_length=255)
    descricao = models.TextField("Descrição", max_length=255)
    ncm_sh = models.CharField("Ncm Sh", max_length=255)
    o_csqn = models.CharField("O Csqn", max_length=255)
    cfop = models.CharField("Cfop", max_length=255)
    un = models.CharField("Unidade", max_length=255)
    quantidade = models.DecimalField(max_digits=11, decimal_places=2, default=0.00)
    valor_unitario = models.DecimalField(max_digits=11, decimal_places=2, default=0.00)
    valor_total = models.DecimalField(max_digits=11, decimal_places=2, default=0.00)
    valor_desconto = models.DecimalField(max_digits=11, decimal_places=2, default=0.00)
    b_calc_imcs = models.CharField("Base Calculo Icms", max_length=255)
    valor_icms = models.DecimalField(max_digits=11, decimal_places=2, default=0.00)
    valor_ipi = models.DecimalField(max_digits=11, decimal_places=2, default=0.00)
    aliq_icms = models.CharField("Aliq Icms", max_length=255)
    aliq_ipi = models.CharField("Aliq Ipi", max_length=255)

    def __str__(self):
        return self.materiaprima


# verifica se a materia prima do fornecedor recebida tem registro com nome previamente cadastrado
@receiver(post_save, sender=NFItem)
def estoque_entrada(sender, instance, **kwargs):
    prod = MateriaPrimaFornecedor.objects.filter(codigoproduto=instance.codigo_produto)

    for p in prod:
        mp = EstoqueMateriaPrima.objects.filter(materiaprima=p.materiaprima.id)
        if mp.exists():
            for mp in mp:
                mp.qtde += Decimal(instance.quantidade)
                mp.save()
        else:
            mp2 = MateriaPrima.objects.get(id=p.materiaprima.id)
            EstoqueMateriaPrima.objects.create(
                materiaprima=mp2,
                qtde=instance.quantidade,
            )


@receiver(post_delete, sender=NFItem)
def estoque_delete(sender, instance, **kwargs):
    prod = MateriaPrimaFornecedor.objects.filter(codigoproduto=instance.codigo_produto)

    for p in prod:
        mp = EstoqueMateriaPrima.objects.filter(materiaprima=p.materiaprima.id)
        if mp.exists():
            for mp in mp:
                mp.qtde -= Decimal(instance.quantidade)
                mp.save()
