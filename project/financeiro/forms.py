import datetime
from django import forms

from .models import ContaPagar, ContaReceber, Comissao

today = datetime.date.today()


class ContaPagarForm(forms.ModelForm):
    class Meta:
        model = ContaPagar
        fields = (
            "valor",
            "datadocumento",
            "datavencimento",
            "datapagamento",
            "boleto",
            "comprovante",
            "formapgto",
            "detalhes",
        )
        widgets = {
            "valor": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-sm text-end",
                    "onchange": "somaTotal()",
                }
            ),
            "datadocumento": forms.HiddenInput(),
            "datavencimento": forms.NumberInput(
                attrs={"class": "form-control form-control-sm", "type": "date"}
            ),
            "datapagamento": forms.NumberInput(
                attrs={"class": "form-control form-control-sm", "type": "date"}
            ),
            "formapgto": forms.Select(attrs={"class": "form-control form-control-sm"}),
            "detalhes": forms.TextInput(
                attrs={"class": "form-control form-control-sm"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super(ContaPagarForm, self).__init__(*args, **kwargs)
        self.fields["datavencimento"].label = "Data do Vencimento"
        self.fields["datapagamento"].label = "Data do Pagamento"
        self.fields["formapgto"].label = "Forma de Pagamento"
        self.fields["boleto"].widget.attrs["class"] = "form-control form-control-sm"
        self.fields["comprovante"].widget.attrs[
            "class"
        ] = "form-control form-control-sm"


class ContaReceberForm(forms.ModelForm):
    class Meta:
        model = ContaReceber
        fields = (
            "parcela",
            "valor",
            "datadocumento",
            "datavencimento",
            "datapagamento",
            "boleto",
            "comprovante",
            "formapgto",
            "detalhes",
        )
        widgets = {
            "parcela": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                }
            ),
            "valor": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-sm text-end",
                    "onchange": "somaTotal()",
                }
            ),
            "datadocumento": forms.HiddenInput(),
            "datavencimento": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "type": "date",
                }
            ),
            "datapagamento": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "type": "date",
                    "onchange": "dataPagamento()",
                }
            ),
            "formapgto": forms.Select(attrs={"class": "form-control form-control-sm"}),
            "detalhes": forms.TextInput(
                attrs={"class": "form-control form-control-sm"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super(ContaReceberForm, self).__init__(*args, **kwargs)
        self.fields["datavencimento"].label = "Data do Vencimento"
        self.fields["datapagamento"].label = "Data do Pagamento"
        self.fields["formapgto"].label = "Forma de Pagamento"
        self.fields["boleto"].widget.attrs["class"] = "form-control form-control-sm"
        self.fields["comprovante"].widget.attrs[
            "class"
        ] = "form-control form-control-sm"


class VendaContaReceberForm(forms.ModelForm):
    class Meta:
        model = ContaReceber
        fields = (
            "parcela",
            "valor",
            "datadocumento",
            "datavencimento",
            "datapagamento",
            "boleto",
            "comprovante",
            "formapgto",
            "dados_boleto",
            "detalhes",
        )
        widgets = {
            "parcela": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "readonly": "readonly",
                }
            ),
            "valor": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "onchange": "recalcularParcelas()",
                }
            ),
            "datadocumento": forms.HiddenInput(),
            "datavencimento": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "type": "date",
                }
            ),
            "formapgto": forms.Select(
                attrs={
                    "class": "form-control form-control-sm",
                    "onchange": "boleto()",
                }
            ),
            "datapagamento": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "type": "date",
                    "onchange": "dataPagamento('input', this)",
                }
            ),
            "detalhes": forms.TextInput(
                attrs={"class": "form-control form-control-sm"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super(VendaContaReceberForm, self).__init__(*args, **kwargs)
        self.fields["datavencimento"].label = "Data do Vencimento"
        self.fields["datapagamento"].label = "Data do Pagamento"
        self.fields["formapgto"].label = "Forma de Pagamento"
        self.fields["boleto"].widget.attrs["class"] = "form-control form-control-sm"
        self.fields["comprovante"].widget.attrs[
            "class"
        ] = "form-control form-control-sm"


class ComissaoForm(forms.ModelForm):
    class Meta:
        model = Comissao
        fields = ("data_comissao",)
        widgets = {
            "data_comissao": forms.NumberInput(
                attrs={"class": "form-control form-control-sm w-50", "type": "date"}
            ),
        }
