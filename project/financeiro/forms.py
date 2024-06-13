import datetime
from django import forms

from .models import ContaPagar, ContaReceber, Comissao, FormaPagamento

today = datetime.date.today()


class ContaPagarForm(forms.ModelForm):
    class Meta:
        model = ContaPagar
        fields = (
            "valor",
            "valor_pago",
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
            "valor_pago": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-sm text-end",
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
            "valor_pago",
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
            "valor_pago": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-sm text-end",
                    # "onchange": "recalcularParcelas(this.id)",
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
                    # "onchange": "dataPagamento(this.id)",
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
            "valor_pago",
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
                    "tabindex": "-1",
                    "readonly": "readonly",
                }
            ),
            "valor": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "tabindex": "-1",
                }
            ),
            "valor_pago": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-sm text-end",
                    "value": "0.00",
                    "onchange": "recalcularParcelas(this.id)",
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
                }
            ),
            "datapagamento": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "type": "date",
                    "onchange": "dataPagamento(this.id)",
                }
            ),
            "detalhes": forms.TextInput(
                attrs={"class": "form-control form-control-sm"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super(VendaContaReceberForm, self).__init__(*args, **kwargs)
        self.fields["valor"].widget.attrs["readonly"] = True
        self.fields["datavencimento"].label = "Data do Vencimento"
        self.fields["datapagamento"].label = "Data do Pagamento"
        self.fields["formapgto"].label = "Forma de Pagamento"
        self.fields["boleto"].widget.attrs["class"] = "form-control form-control-sm"
        self.fields["comprovante"].widget.attrs[
            "class"
        ] = "form-control form-control-sm"

        # Desabilitar formapgto se valor_pago for maior que 0
        if self.instance and self.instance.valor_pago > 0:
            self.fields["formapgto"].widget.attrs["disabled"] = "disabled"
            self.fields["formapgto"].required = (
                False  # Não obriga a preenchimento quando desabilitado
            )

    def clean_formapgto(self):
        formapgto = self.cleaned_data.get("formapgto")
        if not formapgto and self.instance:
            return self.instance.formapgto
        return formapgto


class ComissaoForm(forms.ModelForm):
    class Meta:
        model = Comissao
        fields = ("data_comissao",)
        widgets = {
            "data_comissao": forms.NumberInput(
                attrs={"class": "form-control form-control-sm w-50", "type": "date"}
            ),
        }


class CompraClienteContaReceberForm(forms.ModelForm):
    pgto_id_list = [1, 2]
    queryset_form = FormaPagamento.objects.filter(id__in=pgto_id_list).order_by("-id")
    formapgto = forms.ModelChoiceField(
        queryset=queryset_form,
        widget=forms.Select(
            attrs={"class": "form-select form-select-sm"},
        ),
    )

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
                    "tabindex": "-1",
                    "readonly": "readonly",
                }
            ),
            "valor": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "tabindex": "-1",
                    "readonly": "readonly",
                }
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
                    "onchange": "dataPagamento('input', this)",
                }
            ),
            "detalhes": forms.TextInput(
                attrs={"class": "form-control form-control-sm"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super(CompraClienteContaReceberForm, self).__init__(*args, **kwargs)
        self.fields["formapgto"].label = "Forma de Pagamento"
        self.fields["datavencimento"].label = "Data do Vencimento"
        self.fields["datapagamento"].label = "Data do Pagamento"
        self.fields["boleto"].widget.attrs["class"] = "form-control form-control-sm"
        self.fields["comprovante"].widget.attrs[
            "class"
        ] = "form-control form-control-sm"
        self.fields["formapgto"].initial = FormaPagamento.objects.get(id=2)
