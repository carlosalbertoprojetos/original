from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class Users(LoginRequiredMixin, ListView):
    class Meta:
        verbose_name = "Vendedor"
        verbose_name_plural = "Vendedores"

    def __str__(self):
        return self

    pass
