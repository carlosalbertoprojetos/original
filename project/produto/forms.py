from django import forms
from .models import Produto, ProdutoMatPri, Peca


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = "__all__"
        widgets = {
            "xped": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                }
            ),
            "ordem": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                }
            ),
            "codigoproduto": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                }
            ),
            "nome": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                }
            ),
            "ncm": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                }
            ),
            "cst": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                }
            ),
            "cfop": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                }
            ),
            "unimed": forms.Select(
                attrs={
                    "class": "form-select form-select-sm",
                }
            ),
            "preco": forms.NumberInput(attrs={"class": "form-control form-control-sm"}),
            "peso": forms.NumberInput(attrs={"class": "form-control form-control-sm"}),
            "estoque_127": forms.NumberInput(
                attrs={"class": "form-control form-control-sm"}
            ),
            "estoque_220": forms.NumberInput(
                attrs={"class": "form-control form-control-sm"}
            ),
            "aliq_icms_interno": forms.NumberInput(
                attrs={"class": "form-control form-control-sm"}
            ),
            "aliq_ipi": forms.NumberInput(
                attrs={"class": "form-control form-control-sm"}
            ),
            "status_produto": forms.CheckboxInput(
                attrs={"class": "required checkbox form-control form-control-sm"}
            ),
            "altura": forms.NumberInput(
                attrs={"class": "form-control form-control-sm"}
            ),
            "largura": forms.NumberInput(
                attrs={"class": "form-control form-control-sm"}
            ),
            "comprimento": forms.NumberInput(
                attrs={"class": "form-control form-control-sm"}
            ),
            "descricao": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                }
            ),
        }


class ProdutoMatPriForm(forms.ModelForm):
    class Meta:
        model = ProdutoMatPri
        fields = "__all__"
        widgets = {
            "materiaprima": forms.Select(
                attrs={
                    "class": "form-select form-select-sm",
                }
            ),
            "produto": forms.Select(
                attrs={
                    "class": "form-select form-select-sm",
                }
            ),
            "quantidade": forms.NumberInput(
                attrs={"class": "form-control form-control-sm"}
            ),
        }


class PecaForm(forms.ModelForm):
    class Meta:
        model = Peca
        fields = "__all__"
        widgets = {
            "codigoproduto": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                }
            ),
            "nome": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                }
            ),
            "unimed": forms.Select(
                attrs={
                    "class": "form-select form-select-sm",
                }
            ),
            "peso": forms.NumberInput(attrs={"class": "form-control form-control-sm"}),
            "estoque_ini": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-sm text-center",
                    "readonly": "",
                }
            ),
            "status_produto": forms.CheckboxInput(
                attrs={"class": "required checkbox form-control form-control-sm"}
            ),
            "produto": forms.Select(
                attrs={
                    "class": "form-select form-select-sm",
                }
            ),
            "quantidade": forms.NumberInput(
                attrs={"class": "form-control form-control-sm text-center"}
            ),
            "descricao": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                }
            ),
        }


class PecaMatPriForm(forms.ModelForm):
    class Meta:
        model = ProdutoMatPri
        fields = "__all__"
        widgets = {
            "materiaprima": forms.Select(
                attrs={
                    "class": "form-select form-select-sm",
                }
            ),
            "peca": forms.Select(
                attrs={
                    "class": "form-select form-select-sm",
                }
            ),
            "quantidade": forms.NumberInput(
                attrs={"class": "form-control form-control-sm text-center"}
            ),
        }
