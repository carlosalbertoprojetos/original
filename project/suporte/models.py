import os
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


from venda.models import Venda

STATUS_CHOICE = (("Aberto", "aberto"), ("Concluído", "concluido"))


class Suporte(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE)
    cliente_final = models.CharField(max_length=200, null=True, blank=True)
    tel_cliente_final = models.CharField(max_length=45, null=True, blank=True)
    data = models.DateTimeField(default=now)
    concluir = models.BooleanField(default=False, null=True, blank=True)
    conclusao = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICE, default="Aberto")
    statusAtual = models.CharField(max_length=100, default="Iniciado")
    responsavel = models.ForeignKey(User, on_delete=models.RESTRICT)
    # responsavelAtual = models.CharField(max_length=100)
    coordenador = models.TextField(max_length=255)
    dataalerta = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.pk)


def arquivo_suporte_path(instance, filename):
    # Este método define o caminho para salvar o arquivo, neste caso, na pasta 'uploads' dentro de 'media'
    return os.path.join(f"suporte{instance.suporte.id}/{filename}")


class ArquivosSuporte(models.Model):
    arquivo = models.FileField(upload_to=arquivo_suporte_path, null=True, blank=True)
    suporte = models.ForeignKey(
        Suporte,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        return str(self.suporte)


class Status(models.Model):
    nome = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Status TimeLine"
        verbose_name_plural = "Status TimeLines"

    def __str__(self):
        return self.nome


class WorkFlow(models.Model):
    nome = models.CharField(max_length=100)
    tempo = models.IntegerField(null=False, blank=False, default=4)

    class Meta:
        verbose_name = "Fluxo de trabalho"
        verbose_name_plural = "Fluxos de trabalho"

    def __str__(self):
        return self.nome


class Acoes(models.Model):
    nome = models.CharField(max_length=100)
    tempo = models.IntegerField(null=False, blank=False, default=4)
    workflow = models.ForeignKey(WorkFlow, on_delete=models.CASCADE)
    ordem = models.IntegerField(null=False, blank=False, default=10)
    proximaacao = models.CharField(max_length=100, null=True, blank=True)
    instrucoes = models.TextField(null=False, blank=False)
    cor = models.CharField(max_length=7)

    class Meta:
        verbose_name = "Ação"
        verbose_name_plural = "Ações"

    def __str__(self):
        return self.nome


class Timeline(models.Model):
    suporte = models.ForeignKey(Suporte, on_delete=models.CASCADE)
    fluxo = models.ForeignKey(
        WorkFlow, on_delete=models.RESTRICT, null=True, blank=True
    )
    desc_fluxo = models.CharField(max_length=255)
    acao = models.ForeignKey(Acoes, on_delete=models.RESTRICT, null=True, blank=True)
    data = models.DateTimeField(default=now)
    conclusao = models.DateField(null=True, blank=True)
    responsavel = models.ForeignKey(
        User, on_delete=models.RESTRICT, null=True, blank=True
    )
    logado = models.CharField(max_length=255)
    descricao = models.CharField(max_length=255, null=True, blank=True)
    visualizacao = models.BooleanField(default=True)
    # evidencia = models.FileField(
    #     models.FileField(upload_to="suporte/evidencia"), null=True, blank=True
    # )

    class Meta:
        verbose_name = "TimeLine"
        verbose_name_plural = "TimeLines"
        ordering = ["-suporte"]

    def __str__(self):
        return str(self.suporte.venda)


class Problema(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField(max_length=255)

    def __str__(self):
        return self.nome


class Subproblema(models.Model):
    problema = models.ForeignKey(Problema, on_delete=models.CASCADE)
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome


class ProblemaSuporte(models.Model):
    suporte = models.ForeignKey(Suporte, on_delete=models.CASCADE)
    problema = models.ForeignKey(Problema, on_delete=models.RESTRICT)
    subproblema = models.ForeignKey(Subproblema, on_delete=models.RESTRICT)
    prodescricao = models.TextField(max_length=255)

    def __str__(self):
        return f"{self.suporte} / {self.problema}"
