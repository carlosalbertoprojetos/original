from django import forms
from producao.models import LimiteProducaoDiaria


class QuantidadeProducaoForm(forms.ModelForm):
    class Meta:
        model = LimiteProducaoDiaria
        fields = ("produto", "quantidade")
        widgets = {
            "produto": forms.Select(
                attrs={
                    "class": "form-control form-control-sm fw-bold text-end w-50 m-1"
                }
            ),
            "quantidade": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-sm fw-bold text-center w-25 m-1"
                }
            ),
        }
        labels = {
            "produto": "",
            "quantidade": "",
        }


# class QuantidadePecaForm(forms.ModelForm):
#     class Meta:
#         model = LimiteProducaoDiariaPeca
#         fields = ("peca", "quantidade")
#         widgets = {
#             "peca": forms.Select(
#                 attrs={
#                     "class": "form-control form-control-sm fw-bold text-end w-50 m-1"
#                 }
#             ),
#             "quantidade": forms.NumberInput(
#                 attrs={
#                     "class": "form-control form-control-sm fw-bold text-center w-25 m-1"
#                 }
#             ),
#         }
#         labels = {
#             "peca": "",
#             "quantidade": "",
#         }
