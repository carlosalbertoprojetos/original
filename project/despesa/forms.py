from django import forms

from .models import Despesa


class DespesaForm(forms.ModelForm):
    class Meta:
        model = Despesa
        fields = (
            "nome",
            "total",
            "categoria1",
            "num_parcelas",
            "descricao",
            "fornecedor",
        )
        widgets = {
            "nome": forms.TextInput(
                attrs={
                    "class": "form-control form-control.sm",
                    "style": "font-size:12px;",
                }
            ),
            "total": forms.NumberInput(
                attrs={"class": "form-control form-control-sm text-end"}
            ),
            "categoria1": forms.Select(attrs={"class": "form-select form-select-sm"}),
            "num_parcelas": forms.NumberInput(
                attrs={"class": "form-control form-control-sm text-center"}
            ),
            "descricao": forms.TextInput(
                attrs={
                    "class": "form-control form-control.sm",
                    "style": "font-size:12px;",
                }
            ),
            "fornecedor": forms.Select(attrs={"class": "form-select form-select-sm"}),
        }

    def __init__(self, *args, **kwargs):
        super(DespesaForm, self).__init__(*args, **kwargs)
        self.fields["total"].widget.attrs["readonly"] = True
        self.fields["num_parcelas"].widget.attrs["readonly"] = True
