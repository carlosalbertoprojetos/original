from django import forms
from django.forms.widgets import TextInput
from .models import Acoes, ArquivosSuporte


# class ArquivosSuporteForm(forms.ModelForm):
#     arquivos = forms.FileField(
#         widget=forms.ClearableFileInput(attrs={"multiple": True})
#     )

#     class Meta:
#         model = ArquivosSuporte
#         fields = ("arquivos",)

#     def __init__(self, *args, **kwargs):
#         super(ArquivosSuporteForm, self).__init__(*args, **kwargs)
#         self.fields["arquivos"].widget.attrs["class"] = "form-control form-control-sm"
#         self.fields["arquivos"].required = False


class AcoesForm(forms.ModelForm):
    class Meta:
        model = Acoes
        fields = "__all__"
        widgets = {
            "cor": TextInput(attrs={"type": "color"}),
        }
