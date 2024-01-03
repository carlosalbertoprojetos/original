from django import forms


from .models import Timeline


class TimelineForm(forms.ModelForm):
    class Meta:
        model = Timeline
        fields = ["status", "responsavel", "descricao"]
        exclude = ["data", "suporte", "logado"]
        widgets = {
            "status": forms.Select(
                attrs={
                    "class": "hidden",
                },
            ),
            "responsavel": forms.Select(
                attrs={
                    "class": "form-select form-select-sm",
                },
            ),
            "descricao": forms.Textarea(
                attrs={
                    "class": "form-control form-control-sm",
                },
            ),
        }
        labels = {
            "status": "",
        }
