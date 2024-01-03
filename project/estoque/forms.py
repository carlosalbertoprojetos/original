from django import forms

from .models import EstoqueMateriaPrima, ConferenciaEstoque


class EstoqueMateriaPrimaForm(forms.ModelForm):
    class Meta:
        model = EstoqueMateriaPrima
        fields = "__all__"

        widgets = {
            "materiaprima": forms.Select(
                attrs={
                    "class": "form-control form-control-sm border-0 ps-0",
                    "readonly": "readonly",
                }
            ),
            "enderecoestoque": forms.Select(
                attrs={
                    "class": "form-control form-control-sm border-0 p-0",
                    "required": "required",
                }
            ),
            "qtde": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm border-0 p-0",
                    "readonly": "readonly",
                }
            ),
        }


class ConferenciaEstoqueForm(forms.ModelForm):
    class Meta:
        model = ConferenciaEstoque
        fields = "__all__"
        exclude = ("materiaprima", "usuario", "qtde")
        widgets = {
            "conferencia": forms.TextInput(
                attrs={"class": "form-control form-control-sm"}
            ),
            "data": forms.TextInput(
                attrs={
                    "class": "form-control-sm border-0 p-0",
                    "type": "date",
                    "readonly": "readonly",
                }
            ),
            "relatorio": forms.Textarea(
                attrs={
                    "rows": 1,
                    "class": "form-control form-control-sm",
                }
            ),
        }
