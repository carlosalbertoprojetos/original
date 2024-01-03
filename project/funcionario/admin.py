from django.contrib import admin


from .models import Funcionario, ExtendUser


class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('nome', )
    ...

admin.site.register(Funcionario, FuncionarioAdmin)


class ExtendUserAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'empresa','mercadolivre_user')
    ...
admin.site.register(ExtendUser, ExtendUserAdmin)

