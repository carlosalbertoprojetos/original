from django import forms


from .models import Garantia, GarantiaTimeLine


class GarantiaForm(forms.ModelForm):
    class Meta:
        model = Garantia
        fields = ["status"]
        widgets = {
            "status": forms.Select(
                attrs={
                    "class": "form-select",
                },
            ),
        }
        labels = {
            "status": "",
        }


class GarantiaTimeLineForm(forms.ModelForm):
    class Meta:
        model = GarantiaTimeLine
        fields = "__all__"
        exclude = ["garantia", "atualizadopor", "data"]
        widgets = {
            "titulo": forms.TextInput(
                attrs={
                    "class": "form-control",
                },
            ),
            "descricao": forms.Textarea(
                attrs={
                    "class": "form-control",
                },
            ),
            "status": forms.Select(
                attrs={
                    "class": "form-select",
                },
            ),
        }
