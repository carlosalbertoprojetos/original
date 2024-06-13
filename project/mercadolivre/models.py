from django.db import models
from venda.models import Torneira, Voltagem, Adesivado
# Create your models here.

class ContasMercadoLivre(models.Model):
    codigo = models.IntegerField("id", blank=True, null=True)
    email = models.EmailField("E-MAIL", max_length=254, blank=True, null=True)
    first_name = models.CharField("Primeiro Nome", max_length=254, blank=True, null=True)
    last_name = models.CharField("Ultimo Nome", max_length=254, blank=True, null=True)
    access_token = models.CharField("Access Token", max_length=254, blank=True, null=True)
    refresh_token =  models.CharField("Refresh Token", max_length=254, blank=True, null=True)
    expires_in = models.CharField("Expires IN", max_length=254, blank=True, null=True)
    expires_now = models.DateTimeField(null=True, blank=True)
    status = models.CharField("Status", max_length=254, blank=True, null=True)

    def __str__(self):
        return self.email


class AnunciosMercadoLivre(models.Model):
    conta = models.ForeignKey(
        ContasMercadoLivre, on_delete=models.RESTRICT, related_name="ContaMercadoLivre")
    anuncio = models.CharField("Anuncio", max_length=254, blank=True, null=True)
    voltagem = models.ForeignKey(Voltagem, on_delete=models.RESTRICT, blank=True, null=True)
    torneira = models.ForeignKey(Torneira, on_delete=models.RESTRICT, blank=True, null=True)
    adesivado = models.ForeignKey(Adesivado, on_delete=models.RESTRICT, blank=True, null=True)
    titulo = models.CharField("Titulo", max_length=254, blank=True, null=True)


class MensagensMercadoLivre(models.Model):
    identificador = models.IntegerField("identificador", blank=True, null=True)
    user_id = models.IntegerField("user_id", blank=True, null=True)
    text = models.TextField("Texto", max_length=254, blank=True, null=True)
    received = models.DateTimeField(null=True, blank=True)

class PacksMercadoLivre(models.Model):
    #controla os packets de mensagens ja baixados para nao ficar baixando repetivivamente
    url = models.IntegerField("url", blank=True, null=True)
