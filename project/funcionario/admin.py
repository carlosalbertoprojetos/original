from django.contrib import admin


from .models import Funcionario


class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('nome', )
    ...

admin.site.register(Funcionario, FuncionarioAdmin)
