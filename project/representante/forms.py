# forms.py
from django import forms

from produto.models import Produto
from .models import Representante, DadosBancarios, ServicoRepresentante


class RepresentanteForm(forms.ModelForm):
    class Meta:
        model = Representante
        fields = "__all__"
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control form-control-sm"}),
            "nome_fantasia": forms.TextInput(
                attrs={"class": "form-control form-control-sm"}
            ),
            "email": forms.EmailInput(attrs={"class": "form-control form-control-sm"}),
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
            "estado": forms.Select(attrs={"class": "form-control form-control-sm"}),
            "cidade": forms.TextInput(attrs={"class": "form-control form-control-sm"}),
            "status_representante": forms.CheckboxInput(
                attrs={"class": "form-check-input mt-2", "type": "checkbox"}
            ),
            "regiao": forms.Select(attrs={"class": "form-control form-control-sm"}),
        }

    def __init__(self, *args, **kwargs):
        super(RepresentanteForm, self).__init__(*args, **kwargs)
        self.fields["cpf"].widget.attrs.update(
            {"class": "form-control form-control-sm mask-cpf"}
        )
        self.fields["cnpj"].widget.attrs.update(
            {"class": "form-control form-control-sm mask-cnpj"}
        )
        self.fields["tel_principal"].widget.attrs.update(
            {"class": "form-control form-control-sm mask-telefone"}
        )
        self.fields["tel_contato"].widget.attrs.update(
            {"class": "form-control form-control-sm mask-telefone"}
        )
        self.fields["cep"].widget.attrs.update(
            {"class": "form-control form-control-sm mask-cep"}
        )


class DadosBancariosForm(forms.ModelForm):
    class Meta:
        model = DadosBancarios
        exclude = [
            "representante",
        ]
        # fields = "__all__"

        widgets = {
            "banco": forms.TextInput(attrs={"class": "form-control form-control-sm"}),
            "agencia": forms.NumberInput(
                attrs={"class": "form-control form-control-sm"}
            ),
            "conta": forms.NumberInput(attrs={"class": "form-control form-control-sm"}),
        }


class ServicosForm(forms.ModelForm):
    class Meta:
        model = ServicoRepresentante
        exclude = [
            "representante",
        ]
        # fields = "__all__"
        widgets = {
            "cliente": forms.Select(
                attrs={
                    "class": "form-select form-select-sm",
                },
            ),
            "produto": forms.CheckboxSelectMultiple(),
            "data_recebimento": forms.TextInput(
                attrs={"class": "form-control form-control-sm", "type": "date"}
            ),
            "data_entrega": forms.TextInput(
                attrs={"class": "form-control form-control-sm", "type": "date"}
            ),
            "valor": forms.NumberInput(
                attrs={"class": "form-control form-control-sm text-end"}
            ),
            "data_pagamento": forms.TextInput(
                attrs={"class": "form-control form-control-sm", "type": "date"}
            ),
        }
