from django import forms

from .models import Receita


class ReceitaForm(forms.ModelForm):
    class Meta:
        model = Receita
        fields = (
            "nome",
            "total",
            "categoria1",
            "categoria2",
            "num_parcelas",
            "descricao",
            "cliente",
        )
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control form-control.sm"}),
            "total": forms.NumberInput(
                attrs={"class": "form-control form-control-sm text-end"}
            ),
            "categoria1": forms.Select(attrs={"class": "form-select form-select-sm"}),
            "categoria2": forms.Select(attrs={"class": "form-select form-select-sm"}),
            "num_parcelas": forms.NumberInput(
                attrs={"class": "form-control form-control-sm text-center"}
            ),
            "descricao": forms.TextInput(
                attrs={"class": "form-control form-control.sm"}
            ),
            # 'fornecedor': forms.Select(attrs={'class': 'form-select form-select-sm'}),
            "cliente": forms.Select(attrs={"class": "form-select form-select-sm"}),
        }

    def __init__(self, *args, **kwargs):
        super(ReceitaForm, self).__init__(*args, **kwargs)
        self.fields["total"].widget.attrs["readonly"] = True
        self.fields["num_parcelas"].widget.attrs["readonly"] = True
