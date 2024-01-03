import datetime
from django import forms

from cliente.models import Cliente
from .data import dataAgendaProducao, ChoiceMaximoDesconto
from project.constantes import ESCOLHAS_STATUSVENDAS
from .models import Venda, VendaProduto, MaximoDesconto, Voltagem, Torneira, Adesivado
from django.core.exceptions import ValidationError
from produto.models import Produto

today = datetime.date.today()


def ChoiceMaximoDesconto():
    maximodesconto = MaximoDesconto.objects.first()
    if not maximodesconto:
        return [(0, "0%")]
    else:
        maximodesconto = maximodesconto.qtde
        retorno = []
        for o in range(0, maximodesconto):
            retorno.append((o, "%s %%" % o))
        return retorno


class VendaForm(forms.ModelForm):
    data_entrega = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                "class": "form-control-sm form-select form-select-sm",
                "onchange": "change()",
            }
        ),
    )
    choice = dataAgendaProducao()

    class Meta:
        model = Venda
        fields = (
            "cliente",
            "data_pedido",
            "data_entrega",
            "transportadora",
            "valor_frete",
            "vendedor",
            "valor_venda",
            "porcentagem_desconto",
            "subtotal",
            "status_venda",
            "condicaopgto",
            "dias_prim_par",
            "dias_outras_par",
            "parcelas",
            "formapgto",
            "detalhes",
            "codigo_mercadolivre",
            "nickname_mercadolivre",
            "cotacao_transportadora",
            "telefonequemrecebe_mercadolivre",
            "quemrecebe_mercadolivre"
        )

        widgets = {
            "cliente": forms.Select(
                attrs={
                    "class": "form-select form-select-sm",
                    "style": "width: 100%;",
                },
            ),
            "data_pedido": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "readonly": "readonly",
                }
            ),
            "codigo": forms.NumberInput(
                attrs={"class": "form-control form-control-sm"}
            ),
            "transportadora": forms.Select(
                attrs={"class": "form-select form-select-sm"}
            ),
            "valor_frete": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-sm text-end",
                    "onchange": "change()",
                }
            ),
            "valor_venda": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-sm text-end",
                }
            ),
            "porcentagem_desconto": forms.Select(
                attrs={
                    "class": "form-select form-select-sm",
                    "onchange": "change()",
                },
                choices=ChoiceMaximoDesconto(),
            ),
            "subtotal": forms.NumberInput(
                attrs={"class": "form-control form-control-sm text-end"}
            ),
            "status_venda": forms.Select(
                attrs={"class": "form-select form-select-sm"},
            ),
            "condicaopgto": forms.Select(
                attrs={
                    "class": "form-select form-select-sm",
                    "onChange": "condicao()",
                }
            ),
            "dias_prim_par": forms.NumberInput(
                attrs={"class": "form-control form-control-sm"}
            ),
            "dias_outras_par": forms.NumberInput(
                attrs={"class": "form-control form-control-sm"}
            ),
            "parcelas": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-sm text-center",
                }
            ),
            "vendedor": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm text-center",
                }
            ),
            "formapgto": forms.Select(attrs={"class": "form-control form-control-sm"}),
            "detalhes": forms.TextInput(
                attrs={"class": "form-control form-control-sm"}
            ),
            "codigo_mercadolivre": forms.TextInput(
                attrs={"class": "form-control form-control-sm text-center"}
            ),
            "nickname_mercadolivre": forms.TextInput(
                attrs={"class": "form-control form-control-sm text-center"}
            ),
            "cotacao_transportadora": forms.TextInput(
                attrs={"class": "form-control form-control-sm text-center"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super(VendaForm, self).__init__(*args, **kwargs)
        # inclui a data da venda na lista de data da produção
        if self.choice:
            if self.choice[0][0] != str(today):
                self.choice.remove(self.choice[0])

        data = self.instance.data_entrega
        if data and self.choice:
            for ch in range(len(self.choice)):
                if data.strftime("%d/%m/%Y") == self.choice[ch][1][:10]:
                    data_id = (data.strftime("%Y-%m-%d"), self.choice[ch])

        self.fields["dias_prim_par"].widget.attrs["readonly"] = True
        self.fields["dias_outras_par"].widget.attrs["readonly"] = True
        self.fields["parcelas"].widget.attrs["readonly"] = True
        self.fields["valor_venda"].widget.attrs["readonly"] = True
        self.fields["vendedor"].widget.attrs["readonly"] = True
        if self.choice:
            self.fields["data_entrega"].choices = self.choice

        if self.instance:
            self.fields["status_venda"].queryset = ESCOLHAS_STATUSVENDAS


class VendaProdutoForm(forms.ModelForm):
    class Meta:
        model = VendaProduto
        fields = (
            "produto",
            "voltagem",
            "torneira",
            "adesivado",
            "quantidade",
            "subtotal",
            "preco",
        )
        widgets = {
            "produto": forms.Select(
                attrs={
                    "class": "form-select form-select-sm",
                    "onchange": "filtroPreco(this.id)",
                }
            ),
            "voltagem": forms.Select(
                attrs={
                    "class": "form-select form-select-sm",
                }
            ),
            "torneira": forms.Select(
                attrs={
                    "class": "form-select form-select-sm",
                }
            ),
            "adesivado": forms.Select(
                attrs={
                    "class": "form-select form-select-sm",
                }
            ),
            "quantidade": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-sm text-center",
                    "onchange": "agendaProd()",
                }
            ),
            "preco": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-sm text-end",
                    "onblur": "preco_min(this)",
                    "onchange": "agendaProd()",
                }
            ),
            "subtotal": forms.NumberInput(
                attrs={"class": "form-control form-control-sm text-end"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super(VendaProdutoForm, self).__init__(*args, **kwargs)
        self.fields["subtotal"].widget.attrs["readonly"] = True

    def clean(self):
        if (
            self.cleaned_data["preco"]
            < Produto.objects.get(id=self.cleaned_data["produto"].id).preco
        ):
            raise ValidationError(
                "O Preco do produto não pode ser menor que o valor cadastrado."
            )


class AnoForm(forms.Form):
    today = datetime.date.today()

    ANO_CHOICES = []
    for a in range(3):
        anos = [today.year + a, today.year + a]
        ANO_CHOICES.append(anos)

    MES_CHOICES = [
        "Janeiro",
        "Fevereiro",
        "Março",
        "Abril",
        "Maio",
        "Junho",
        "Julho",
        "Agosto",
        "Setembro",
        "Outubro",
        "Novembro",
        "Dezembro",
    ]

    ano = forms.ChoiceField(choices=ANO_CHOICES, label="Ano")
    mes = forms.ChoiceField(choices=MES_CHOICES, label="Mês")

    class Meta:
        fields = ("ano", "mes")
