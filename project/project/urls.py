from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include


from django.views.generic.base import TemplateView

# from .views import index

urlpatterns = [
    path("", TemplateView.as_view(template_name="account/login.html")),
    path("admin/", admin.site.urls),
    path(
        "index/",
        login_required(TemplateView.as_view(template_name="index.html")),
        name="index",
    ),
    path("accounts/", include("allauth.urls")),
    path("select2/", include("django_select2.urls")),
    path("compra/", include("compra.urls"), name="compra"),
    path("venda/", include("venda.urls"), name="venda"),
    path("mercadolivre/", include("mercadolivre.urls"), name="mercadolivre"),
    path("cliente/", include("cliente.urls"), name="cliente"),
    path("notafiscal/", include("notafiscal.urls"), name="notafiscal"),
    path("estoque/", include("estoque.urls"), name="estoque"),
    path("financeiro/", include("financeiro.urls"), name="financeiro"),
    path("despesa/", include("despesa.urls"), name="despesa"),
    path("receita/", include("receita.urls"), name="receita"),
    path("materiaprima/", include("materiaprima.urls"), name="materiaprima"),
    path("producao/", include("producao.urls"), name="producao"),
    path("transporte/", include("transportadora.urls"), name="transportadora"),
    path("expedicao/", include("expedicao.urls"), name="expedicao"),
    path("fornecedor/", include("fornecedor.urls"), name="fornecedor"),
    path("produto/", include("produto.urls"), name="produto"),
    path("suporte/", include("suporte.urls"), name="suporte"),
    path("representante/", include("representante.urls"), name="representante"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
