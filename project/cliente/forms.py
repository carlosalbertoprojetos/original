from django import forms

from .models import Cliente


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = "__all__"
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
            "numero": forms.TextInput(
                attrs={"class": "form-control form-control-sm"}
            ),
            "complemento": forms.TextInput(
                attrs={"class": "form-control form-control-sm"}
            ),
            "bairro": forms.TextInput(attrs={"class": "form-control form-control-sm"}),
            "estado": forms.Select(attrs={"class": "form-control form-control-sm"}),
            "cidade": forms.TextInput(attrs={"class": "form-control form-control-sm"}),
            "descricao": forms.TextInput(attrs={"class": "form-control form-control-sm"}),
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
