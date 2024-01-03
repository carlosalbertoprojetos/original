
from django.urls import path


from . import views as v


app_name = 'notafiscal'


urlpatterns = [
    # path('', TemplateView.as_view(template_name="notafiscal/uploadxml.html")),
    path('lista/', v.nfcompraList, name='nfcompraList'),
    path('lista/baixar/', v.notafiscalList, name='notafiscalList'),
    path('baixar/<chave>/', v.checkXml, name='checkXml'),
    path('baixar/xml/', v.baixarxml, name='baixarxml'),
    path('<int:pk>/deletar/', v.nfcompraDelete, name='nfcompraDelete'),
]