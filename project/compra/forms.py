from django import forms

from .models import Compra, CompraMateriaPrima
import datetime


class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = (
            "data",
            "fornecedor",
            "previsaoentrega",
            "total",
            "status_compra",
            "pedido",
        )
        widgets = {
            "data": forms.NumberInput(
                attrs={"class": "form-control form-control-sm", "type": "date"}
            ),
            "fornecedor": forms.Select(
                attrs={
                    "class": "form-select form-select-sm",
                    "style": "width: 100%;",
                }
            ),
            "previsaoentrega": forms.NumberInput(
                attrs={"class": "form-control form-control-sm", "type": "date"}
            ),
            "total": forms.NumberInput(
                attrs={"class": "form-control form-control-sm text-end"}
            ),
            "status_compra": forms.Select(
                attrs={"class": "form-select form-select-sm"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super(CompraForm, self).__init__(*args, **kwargs)
        self.fields["total"].widget.attrs["readonly"] = True
        self.fields["data"].initial = datetime.date.today()
        self.fields["pedido"].widget.attrs["class"] = "form-control form-control-sm"


class CompraMateriaPrimaForm(forms.ModelForm):
    class Meta:
        model = CompraMateriaPrima
        fields = ("produto", "quantidade", "detalhes")
        widgets = {
            "produto": forms.Select(
                attrs={
                    "class": "form-select form-select-sm",
                }
            ),
            "quantidade": forms.NumberInput(
                attrs={"class": "form-control form-control-sm text-center"}
            ),
            "detalhes": forms.TextInput(
                attrs={"class": "form-control form-control-sm"}
            ),
        }
