from django import forms
from allauth.account.forms import SignupForm


from .models import Cliente
from venda.models import Venda, VendaProduto


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = "__all__"
        exclude = ["username"]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control form-control-sm"}),
            "nome_fantasia": forms.TextInput(
                attrs={"class": "form-control form-control-sm"}
            ),
            "email": forms.EmailInput(attrs={"class": "form-control form-control-sm"}),
            "insc_estadual": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-sm",
                }
            ),
            "logradouro": forms.TextInput(
                attrs={"class": "form-control form-control-sm"}
            ),
            "numero": forms.TextInput(attrs={"class": "form-control form-control-sm"}),
            "complemento": forms.TextInput(
                attrs={"class": "form-control form-control-sm"}
            ),
            "bairro": forms.TextInput(attrs={"class": "form-control form-control-sm"}),
            "estado": forms.Select(attrs={"class": "form-control form-control-sm"}),
            "cidade": forms.TextInput(attrs={"class": "form-control form-control-sm"}),
            "descricao": forms.TextInput(
                attrs={"class": "form-control form-control-sm"}
            ),
            "status_cliente": forms.CheckboxInput(
                attrs={"class": "form-check-input mt-2", "type": "checkbox"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super(ClienteForm, self).__init__(*args, **kwargs)
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


class CustomSignupForm(SignupForm):
    def signup(self, request, user):
        return user


class CompraForm(forms.ModelForm):
    class Meta:
        model = Venda
        fields = "__all__"
        # widgets = {
        #     "detalhes": forms.TextInput(
        #         attrs={
        #             "class": "form-control form-control-sm",
        #         }
        #     ),
        #     "subtotal": forms.NumberInput(
        #         attrs={
        #             "class": "form-control form-control-sm text-end",
        #             "readonly": "readonly",
        #         }
        #     ),
        # }

    # def __init__(self, *args, **kwargs):
    #     super(CompraForm, self).__init__(*args, **kwargs)


class CompraProdutoForm(forms.ModelForm):
    class Meta:
        model = VendaProduto
        fields = "__all__"
        widgets = {
            "produto": forms.Select(
                attrs={
                    "class": "form-select form-select-sm",
                }
            ),
            "voltagem": forms.Select(
                attrs={
                    "class": "form-select form-select-sm pe-1",
                }
            ),
            "quantidade": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-sm text-center",
                    "onchange": "change()",
                }
            ),
            "preco": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-sm text-end",
                    "readonly": "readonly",
                }
            ),
            "subtotal": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-sm text-end",
                    "readonly": "readonly",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(CompraProdutoForm, self).__init__(*args, **kwargs)
        self.fields["produto"].disabled = True
