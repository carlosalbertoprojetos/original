from django import forms

from .models import ContaPagar, ContaReceber, Comissao


class ContaPagarForm(forms.ModelForm):
    class Meta:
        model = ContaPagar
        fields = (
            "valor",
            "datadocumento",
            "datavencimento",
            "datapagamento",
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


class ContaReceberForm(forms.ModelForm):
    class Meta:
        model = ContaReceber
        fields = (
            "parcela",
            "valor",
            "datadocumento",
            "datavencimento",
            "datapagamento",
            # "imagem",
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
                    "onchange": "dataPagamento(this.id)",
                }
            ),
            "formapgto": forms.Select(attrs={"class": "form-control form-control-sm"}),
            "detalhes": forms.TextInput(
                attrs={"class": "form-control form-control-sm"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super(ContaReceberForm, self).__init__(*args, **kwargs)
        self.fields["datapagamento"].label = "Data do Pagamento"
        self.fields["formapgto"].label = "Forma de Pagamento"
        # self.fields["imagem"].widget.attrs["class"] = "form-control form-control-sm"


class VendaContaReceberForm(forms.ModelForm):
    class Meta:
        model = ContaReceber
        fields = (
            "parcela",
            "valor",
            "datadocumento",
            "datavencimento",
            "datapagamento",
            "imagem",
            "formapgto",
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
                attrs={"class": "form-control form-control-sm", "readonly": "readonly"}
            ),
            "datadocumento": forms.HiddenInput(),
            "datavencimento": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "type": "date",
                    "readonly": "readonly",
                }
            ),
            "datapagamento": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "type": "date",
                    "onchange": "dataPagamento(this.id)",
                }
            ),
            "formapgto": forms.Select(attrs={"class": "form-control form-control-sm"}),
            "detalhes": forms.TextInput(
                attrs={"class": "form-control form-control-sm"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super(VendaContaReceberForm, self).__init__(*args, **kwargs)
        self.fields["datapagamento"].label = "Data do Pagamento"
        self.fields["formapgto"].label = "Forma de Pagamento"
        self.fields["imagem"].widget.attrs["class"] = "form-control form-control-sm"


class ComissaoForm(forms.ModelForm):
    class Meta:
        model = Comissao
        fields = ("data_comissao",)
        widgets = {
            "data_comissao": forms.NumberInput(
                attrs={"class": "form-control form-control-sm w-50", "type": "date"}
            ),
        }
