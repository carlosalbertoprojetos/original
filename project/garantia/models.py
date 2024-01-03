from django.db import models
from django.utils.timezone import now


from venda.models import VendaProduto


class StatusGarantia(models.Model):
    nome = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Status Garantia"
        verbose_name_plural = "Status Garantias"

    def __str__(self):
        return self.nome


class Garantia(models.Model):
    produto = models.ForeignKey(VendaProduto, on_delete=models.CASCADE)
    data = models.DateTimeField(default=now)
    status = models.ForeignKey(StatusGarantia, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.produto} - {self.produto.venda}_{self.produto.venda.cliente}"


class StatusTimeLineGarantia(models.Model):
    nome = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Status TimeLine"
        verbose_name_plural = "Status TimeLines"

    def __str__(self):
        return self.nome


class GarantiaTimeLine(models.Model):
    garantia = models.ForeignKey(Garantia, on_delete=models.CASCADE)
    titulo = models.TextField()
    descricao = models.TextField()
    data = models.DateTimeField(default=now)
    status = models.ForeignKey(StatusTimeLineGarantia, on_delete=models.CASCADE)
    atualizadopor = models.CharField(max_length=255)

    class Meta:
        verbose_name = "TimeLine"
        verbose_name_plural = "TimeLines"
        ordering = ["-garantia"]

    def __str__(self):
        return f"Garantia({self.garantia.id}) - {self.garantia.produto.produto.nome} - TimeLine({self.id})"

    def save(self, *args, **kwargs):
        garantia = Garantia.objects.get(id=self.garantia.id)
        if self.status.nome == "Concluído":
            garantia.status = StatusGarantia.objects.get(nome=self.status.nome)
        else:
            garantia.status = StatusGarantia.objects.get(nome="Aberto")
        garantia.save()
        super(GarantiaTimeLine, self).save(*args, **kwargs)
