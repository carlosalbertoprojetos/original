from django.db import models

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

