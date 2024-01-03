from django.db import models
from django.db import models
from django.contrib.auth.models import User
from empresa.models import Empresa
# from django.contrib.auth import get_user_model
# User = get_user_model()
# users = User.objects.all()


# Create your models here.
class Funcionario(models.Model):
    nome = models.CharField("Nome", max_length=200)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Funcionário"
        verbose_name_plural = "Funcionários"




class ExtendUser(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.RESTRICT)
    mercadolivre_user=models.CharField(null=True,blank=True, max_length=255)

    def __str__(self):
        return self.usuario.username