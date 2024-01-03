from django import forms

from .models import NFCompra, NFItem


class NFCompraForm(forms.ModelForm):
    template_name_crete_update = "notafiscal/notafiscalCreateUpdate.html"

    class Meta:
        model = NFCompra
        fields = "__all__"
        widgets = {
            "fornecedor": forms.Select(
                attrs={
                    "class": "form-control form-control-sm border-0 bg-white p-0",
                    "readonly": "readonly",
                }
            ),
            "chavedeacesso": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm border-0 p-0",
                    "readonly": "readonly",
                }
            ),
            "naturezadaoperacao": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm border-0 p-0",
                    "readonly": "readonly",
                }
            ),
            "numeroserie": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm border-0 p-0",
                    "readonly": "readonly",
                }
            ),
            "protocoloautorizacaodeuso": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm border-0 p-0",
                    "readonly": "readonly",
                }
            ),
            "nome_destinatario": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm border-0 p-0",
                    "readonly": "readonly",
                }
            ),
            "cnpj_destinatario": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm border-0 p-0",
                    "readonly": "readonly",
                }
            ),
            "bairro_destinatario": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm border-0 p-0",
                    "readonly": "readonly",
                }
            ),
            "cep_destinatario": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm border-0 p-0",
                    "readonly": "readonly",
                }
            ),
            "data_emissao": forms.DateInput(
                attrs={
                    "class": "form-control form-control-sm border-0 p-0",
                    "readonly": "readonly",
                }
            ),
            "forma_pagamento": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm border-0 p-0",
                    "readonly": "readonly",
                }
            ),
            "base_calculo_icms": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm border-0 p-0",
                    "readonly": "readonly",
                }
            ),
            "valor_icms": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-sm border-0 p-0",
                    "readonly": "readonly",
                }
            ),
            "valor_pis": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-sm border-0 p-0",
                    "readonly": "readonly",
                }
            ),
            "valor_total_produtos": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-sm border-0 p-0",
                    "readonly": "readonly",
                }
            ),
            "valor_do_frete": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-sm border-0 p-0",
                    "readonly": "readonly",
                }
            ),
            "valor_do_seguro": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-sm border-0 p-0",
                    "readonly": "readonly",
                }
            ),
            "desconto": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-sm border-0 p-0",
                    "readonly": "readonly",
                }
            ),
            "outras_despesas": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-sm border-0 p-0",
                    "readonly": "readonly",
                }
            ),
            "valor_total_ipi": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-sm border-0 p-0",
                    "readonly": "readonly",
                }
            ),
            "valor_da_cofins": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-sm border-0 p-0",
                    "readonly": "readonly",
                }
            ),
            "valor_total_da_nota": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-sm border-0 p-0",
                    "readonly": "readonly",
                }
            ),
        }


class NFCompraProdutoForm(forms.ModelForm):
    class Meta:
        model = NFItem
        fields = [
            "codigo_produto",
            "materiaprima",
            "un",
            "valor_unitario",
            "quantidade",
            "ncm_sh",
            "cfop",
            "valor_total",
            "valor_icms",
            "valor_ipi",
        ]
        labels = {
            "codigo_produto": "",
            "materiaprima": "",
            "un": "",
            "valor_unitario": "",
            "quantidade": "",
            "ncm_sh": "",
            "cfop": "",
            "valor_total": "",
            "valor_icms": "",
            "valor_ipi": "",
        }
        widgets = {
            "materiaprima": forms.Select(
                attrs={"class": "form-control form-control-sm", "required": "required"}
            ),
            "codigo_produto": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm border-0 p-0",
                    "readonly": "readonly",
                }
            ),
            "materiaprima": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm border-0 p-0",
                    "readonly": "readonly",
                }
            ),
            "un": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm border-0 p-0",
                    "readonly": "readonly",
                }
            ),
            "valor_unitario": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-sm border-0 p-0",
                    "readonly": "readonly",
                }
            ),
            "quantidade": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-sm border-0 p-0",
                    "readonly": "readonly",
                }
            ),
            "ncm_sh": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm border-0 p-0",
                    "readonly": "readonly",
                }
            ),
            "cfop": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm border-0 p-0",
                    "readonly": "readonly",
                }
            ),
            "valor_total": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-sm border-0 p-0",
                    "readonly": "readonly",
                }
            ),
            # 'o_csqn': forms.TextInput(attrs={'class': 'form-control form-control-sm border-0 p-0','readonly':'readonly'}),
            # 'valor_desconto': forms.NumberInput(attrs={'class': 'form-control form-control-sm border-0 p-0','readonly':'readonly'}),
            # 'b_calc_imcs': forms.TextInput(attrs={'class': 'form-control form-control-sm border-0 p-0','readonly':'readonly'}),
            "valor_icms": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-sm border-0 p-0",
                    "readonly": "readonly",
                }
            ),
            "valor_ipi": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-sm border-0 p-0",
                    "readonly": "readonly",
                }
            ),
            # 'aliq_icms': forms.TextInput(attrs={'class': 'form-control form-control-sm border-0 p-0','readonly':'readonly'}),
            # 'aliq_ipi': forms.TextInput(attrs={'class': 'form-control form-control-sm border-0 p-0','readonly':'readonly'}),
        }

        # def __init__(self, *args, **kwargs):
        #     super(NFCompraForm, self).__init__(*args, **kwargs)
        #     self.fields['codigo_produto'].widget.attrs['readonly'] = True
        #     self.fields['materiaprima'].widget.attrs['readonly'] = True
        #     self.fields['un'].widget.attrs['readonly'] = True
        #     self.fields['valor_unitario'].widget.attrs['readonly'] = True
        #     self.fields['quantidade'].widget.attrs['readonly'] = True
        #     self.fields['ncm_sh'].widget.attrs['readonly'] = True
        #     self.fields['cfop'].widget.attrs['readonly'] = True
        #     self.fields['valor_total'].widget.attrs['readonly'] = True
        # self.fields['o_csqn'].widget.attrs['readonly'] = True
        # self.fields['valor_desconto'].widget.attrs['readonly'] = True
        # self.fields['b_calc_imcs'].widget.attrs['readonly'] = True
        # self.fields['valor_icms'].widget.attrs['readonly'] = True
        # self.fields['valor_ipi'].widget.attrs['readonly'] = True
        # self.fields['aliq_icms'].widget.attrs['readonly'] = True
        # self.fields['aliq_icms'].widget.attrs['readonly'] = True


# https://docs.djangoproject.com/en/4.1/ref/forms/api/
