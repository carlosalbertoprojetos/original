from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


from venda.models import Venda

STATUS_CHOICE = (("Aberto", "aberto"), ("Concluído", "concluido"))


class Suporte(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE)
    data = models.DateTimeField(default=now)
    status = models.CharField(max_length=30, choices=STATUS_CHOICE, default="Aberto")
    statusAtual = models.CharField(max_length=30, default="Iniciado")
    responsavel = models.ForeignKey(User, on_delete=models.RESTRICT)
    responsavelAtual = models.CharField(max_length=30)

    def __str__(self):
        # return f"{self.id}_venda:{self.venda}"
        return str(self.pk)


class Status(models.Model):
    nome = models.CharField(max_length=30)

    class Meta:
        verbose_name = "Status TimeLine"
        verbose_name_plural = "Status TimeLines"

    def __str__(self):
        return self.nome


class Timeline(models.Model):
    suporte = models.ForeignKey(Suporte, on_delete=models.CASCADE)
    data = models.DateTimeField(default=now)
    responsavel = models.ForeignKey(User, on_delete=models.RESTRICT)
    logado = models.CharField(max_length=255)
    descricao = models.CharField(max_length=255)
    status = models.ForeignKey(Status, on_delete=models.RESTRICT)

    class Meta:
        verbose_name = "TimeLine"
        verbose_name_plural = "TimeLines"
        ordering = ["-suporte"]

    def __str__(self):
        return str(self.suporte.venda)

    def save(self, *args, **kwargs):
        suporte = Suporte.objects.get(id=self.suporte.id)
        if self.status.nome == "Concluído":
            suporte.status = "Concluído"
        else:
            suporte.status = "Aberto"
        suporte.statusAtual = self.status.nome
        suporte.responsavelAtual = self.responsavel.username
        suporte.save()
        super(Timeline, self).save(*args, **kwargs)
