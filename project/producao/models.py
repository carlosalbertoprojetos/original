from django.db import models
from datetime import datetime
from pytz import timezone

from produto.models import Produto
from materiaprima.models import MateriaPrima
from funcionario.models import Funcionario

StatusProdutoAcabado = (
    ("faltandomateriaprima", "Faltando Materia Prima"),
    ("montagem", "Montagem"),
    ("eletrica", "Elétrica"),
    ("refrigeracao", "Refrigeração"),
    ("acabamento", "Acabamento"),
    ("embalagem", "Embalagem"),
    ("estoque", "Estoque"),
)


class LimiteProducaoDiaria(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=0)

    def __str__(self):
        return str(self.produto.nome)


# Create your models here.
class Setor(models.Model):
    nome = models.CharField(max_length=200)


class ProdutoAcabado(models.Model):
    numeroserie = models.CharField(max_length=200, null=False, blank=True)
    valor_venda = models.DecimalField(max_digits=11, decimal_places=2, default=0.00)
    valor_custototal = models.FloatField(null=True, blank=True)
    valor_custo_material = models.FloatField(null=True, blank=True)
    valor_custo_imposto = models.FloatField(null=True, blank=True)
    valor_custo_producao = models.FloatField(null=True, blank=True)
    valor_custo_administracao = models.FloatField(null=True, blank=True)
    valor_custo_venda = models.FloatField(null=True, blank=True)
    data_producao = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        choices=StatusProdutoAcabado, default="montagem", max_length=255
    )
    produto = models.ForeignKey(
        Produto, on_delete=models.RESTRICT, null=True, blank=True
    )
    hora_inicio = models.DateTimeField(blank=False, null=False)
    hora_fim = models.DateTimeField(auto_now=True, blank=False, null=False)
    hora_momento = models.DateTimeField(auto_now=True, blank=False, null=False)
    duracao = models.FloatField(default=0, blank=False, null=False)

    class Meta:
        verbose_name = "PRODUTO ACABADO"
        verbose_name_plural = "PRODUTOS ACABADOS"

    def __str__(self):
        if not self.produto:
            import pdb

            pdb.set_trace()
        return str(self.produto.nome)

    def get_nome_abreviado(self):
        return self.produto.nome.replace("Bebedouro", "")

    def get_hora_inicio(self):
        return self.hora_inicio.strftime("%H:%M")

    def get_tempo(self):
        diferenca = datetime.now().astimezone(
            timezone("America/Sao_Paulo")
        ) - self.hora_momento.astimezone(timezone("America/Sao_Paulo"))
        return str(round(diferenca.total_seconds() / 60 / 60, 2)).replace(".", ":")

    def get_tempototal(self):
        diferenca = datetime.now().astimezone(
            timezone("America/Sao_Paulo")
        ) - self.hora_inicio.astimezone(timezone("America/Sao_Paulo"))
        return str(round(diferenca.total_seconds() / 60 / 60, 2)).replace(".", ":")

    def get_momento(self):
        diferenca = datetime.now().astimezone(
            timezone("America/Sao_Paulo")
        ) - self.hora_momento.astimezone(timezone("America/Sao_Paulo"))
        diferenca_atual = diferenca.total_seconds() / 60  # minutos
        diferenca_esperada = TempoDesejadoProducao.objects.filter(status=self.status)
        if diferenca_esperada:
            diferenca_esperada = diferenca_esperada[0]
            if diferenca_atual < diferenca_esperada.tempo_verde:
                return "green"
            elif diferenca_atual < diferenca_esperada.tempo_amarelo:
                return "yellow"
            else:
                return "red"


class HistoricoMontagem(models.Model):
    produtoacabado = models.ForeignKey(
        ProdutoAcabado, on_delete=models.CASCADE, verbose_name="PRODUTOACABADO"
    )
    hora_inicio = models.DateTimeField(auto_now=True, blank=False, null=False)
    hora_fim = models.DateTimeField(auto_now=True, blank=False, null=False)
    duracao = models.FloatField(default=0, blank=False, null=False)
    status = models.CharField(
        choices=StatusProdutoAcabado, default="montagem", max_length=255
    )


class TempoDesejadoProducao(models.Model):
    status = models.CharField(
        choices=StatusProdutoAcabado, default="montagem", max_length=255
    )
    tempo_verde = models.FloatField(default=0, blank=False, null=False)
    tempo_amarelo = models.FloatField(default=0, blank=False, null=False)


class MateriaPrimaProdutoAcabado(models.Model):
    produtoacabado = models.ForeignKey(
        ProdutoAcabado, on_delete=models.RESTRICT, verbose_name="PRODUTO"
    )
    materiaprimausada = models.ForeignKey(
        MateriaPrima, on_delete=models.RESTRICT, verbose_name="MATERIA PRIMA"
    )
    valor = models.DecimalField(
        "VALOR CUSTO", max_digits=9, decimal_places=2, default=0, null=True, blank=True
    )

    class Meta:
        verbose_name = "MATÉRIA PRIMA PRODUTO ACABADO"
        verbose_name_plural = "MATÉRIA PRIMA PRODUTOS ACABADOS"

    def __str__(self):
        return str(self.produtoacabado)


# class MateriaPrimaProduto(models.Model):
#     produto = models.ForeignKey(
#         Produto, on_delete=models.RESTRICT, related_name="mpproduto"
#     )
#     materiaprimausada = models.ForeignKey(
#         MateriaPrima, on_delete=models.RESTRICT, related_name="mpusado"
#     )
#     quant = models.DecimalField(max_digits=5, decimal_places=2)
#     valor = models.DecimalField(
#         max_digits=9, decimal_places=2, default=0, null=True, blank=True
#     )

#     class Meta:
#         verbose_name = "Matéria prima Produto"
#         verbose_name_plural = "Matéria prima Produtos"

#     def __str__(self):
#         return str(self.materiaprimausada)


class Montadores(models.Model):
    funcionario = models.ForeignKey(Funcionario, on_delete=models.RESTRICT, null=True)
    setor_montagem = models.ForeignKey(Setor, on_delete=models.RESTRICT, null=True)


class PrevisaoEstoque(models.Model):
    producao = models.IntegerField()
