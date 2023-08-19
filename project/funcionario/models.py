from django.db import models

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
