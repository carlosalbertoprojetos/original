from django.contrib import admin
from .models import ContasMercadoLivre

# Register your models here.
class ContasMercadoLivreAdmin(admin.ModelAdmin):
    model = ContasMercadoLivre
    list_display = ("email", "first_name", "last_name", "codigo")
    fieldsets = [
        (
            "INFORMAÇÕES",
            {
                "fields": (
                    ("email", "first_name", "last_name", "codigo", "access_token", "expires_in"),
                )
            },
        ),
    ]
    readonly_fields = ["first_name", 'last_name', "codigo", "expires_in", "access_token"]

admin.site.register(ContasMercadoLivre, ContasMercadoLivreAdmin)