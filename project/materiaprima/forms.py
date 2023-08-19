from django import forms

from .models import MateriaPrima, MateriaPrimaFornecedor


class MateriaPrimaForm(forms.ModelForm):
    class Meta:
        model = MateriaPrima
        fields = "__all__"
        # widgets = {
        #     'data': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'type': 'date'}),
        #     'fornecedor': forms.Select(attrs={'class': 'form-select form-select-sm'}),
        #     'previsaoentrega': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'type': 'date'}),
        #     'total': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
        # }


class MPFForm(forms.ModelForm):
    class Meta:
        model = MateriaPrimaFornecedor
        fields = "__all__"
        labels = {
            "materiaprima": "",
            "fornecedor": "",
            "codigoproduto": "",
            "nome": "",
        }
        widgets = {
            "materiaprima": forms.Select(
                attrs={
                    "class": "form-control form-control-sm border-0",
                    "required": "required",
                }
            ),
            "fornecedor": forms.Select(
                attrs={
                    "class": "form-control form-control-sm border-0 p-0",
                    "readonly": "readonly",
                }
            ),
            "codigoproduto": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm border-0 p-0",
                    "readonly": "readonly",
                }
            ),
            "nome": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm border-0 p-0",
                    "readonly": "readonly",
                }
            ),
        }
