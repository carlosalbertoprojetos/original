from django import forms
from producao.models import LimiteProducaoDiaria


class QuantidadeProducaoForm(forms.ModelForm):
    class Meta:
        model = LimiteProducaoDiaria
        fields = ("produto", "quantidade")
        widgets = {
            "produto": forms.Select(
                attrs={"class": "form-control form-control-sm text-end w-50"}
            ),
            "quantidade": forms.NumberInput(
                attrs={"class": "form-control form-control-sm text-center w-25"}
            ),
        }
        labels = {
            "produto": "",
            "quantidade": "",
        }

    def __init__(self, *args, **kwargs):
        super(QuantidadeProducaoForm, self).__init__(*args, **kwargs)
        # self.fields["produto"].widget.attrs["readonly"] = True
        # self.fields["produto"].widget.attrs["disable"] = True
