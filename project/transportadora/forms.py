from django import forms

from .models import Transportadora


class TransporteForm(forms.ModelForm):
    class Meta:
        model = Transportadora
        fields = "__all__"
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control form-control-sm"}),
            "nome_fantasia": forms.TextInput(
                attrs={"class": "form-control form-control-sm"}
            ),
            "tel_principal": forms.NumberInput(
                attrs={"class": "form-control form-control-sm"}
            ),
            "tel_contato": forms.NumberInput(
                attrs={"class": "form-control form-control-sm"}
            ),
            "email": forms.EmailInput(attrs={"class": "form-control form-control-sm"}),
            "cpf": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-sm",
                }
            ),
            "cnpj": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-sm",
                }
            ),
            "mei": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-sm",
                }
            ),
            "insc_estadual": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-sm",
                }
            ),
            "logradouro": forms.TextInput(
                attrs={"class": "form-control form-control-sm"}
            ),
            "numero": forms.NumberInput(
                attrs={"class": "form-control form-control-sm"}
            ),
            "complemento": forms.NumberInput(
                attrs={"class": "form-control form-control-sm"}
            ),
            "bairro": forms.TextInput(attrs={"class": "form-control form-control-sm"}),
            "cep": forms.TextInput(attrs={"class": "form-control form-control-sm"}),
            "estado": forms.TextInput(attrs={"class": "form-control form-control-sm"}),
            "cidade": forms.TextInput(attrs={"class": "form-control form-control-sm"}),
            "status_transportadora": forms.CheckboxInput(
                attrs={"class": "form-check-input mt-2", "type": "checkbox"}
            ),
        }
