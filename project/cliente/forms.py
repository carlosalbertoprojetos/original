from django import forms

from .models import Cliente


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = (
            "nome",
            "nome_fantasia",
            "tel_principal",
            "tel_contato",
            "email",
            "cpf",
            "cnpj",
            "insc_estadual",
            "logradouro",
            "numero",
            "complemento",
            "bairro",
            "cep",
            "estado",
            "cidade",
            "status_cliente",
        )
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
            "status_cliente": forms.CheckboxInput(
                attrs={"class": "form-check-input mt-2", "type": "checkbox"}
            ),
        }
