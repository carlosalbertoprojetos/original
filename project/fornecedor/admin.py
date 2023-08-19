from django.contrib import admin


from .models import Fornecedor


# @admin.register(Fornecedor)
# class FornecedorAdmin(admin.ModelAdmin):
#     list_display = ('nome','telefone1', 'telefone2','email', 'cidade')
#     fieldsets = [
#         ('Contato',{
#             'fields':
#                 ('nome',('telefone1', 'telefone2'), 'email',)
#         }),
#         ('Documentos',{
#             'fields':
#                 (('cpf','cnpj'), ('mei', 'insc_estadual'),)
#         }),
#         ('Localização',{
#             'fields':
#                 (('logradouro','numero', 'complemento'), ('cidade', 'estado'),)
#         }),
#     ]
#     list_filter = ['nome', 'cpf', 'cnpj', 'cidade']
#     search_fields = ['nome', 'cpf', 'cnpj', 'cidade']
#     ordering = ('nome',)

#     from project.constantes import ESCOLHAS_ESTADO, TIPO, ESCOLHAS_PAGAMENTO
