import datetime
import calendar
from decimal import Decimal
from typing import Any
from django.db.models.query import QuerySet
import json
from django.urls import reverse_lazy as _
from django.shortcuts import redirect, render, get_object_or_404
from django.forms import BaseFormSet, inlineformset_factory
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.db.models import Sum, Count, Q
from django.views.generic import ListView, DetailView
from django.views.generic.edit import DeleteView
import base64
from django.core import serializers
from django.core.serializers import serialize

from project.constantes import ESCOLHAS_ESTADO, ESCOLHAS_ESTADO2


from .models import (
    CondicaoVenda,
    Venda,
    VendaProduto,
    MaximoDesconto,
    Voltagem,
    Torneira,
    Adesivado,
)
from .forms import VendaForm, VendaProdutoForm
from cliente.models import Cliente
from produto.models import Produto
from financeiro.models import ContaReceber
from financeiro.forms import VendaContaReceberForm
from producao.models import LimiteProducaoDiaria
from empresa.models import DadosBancarios, Empresa
from transportadora.models import Transportadora

from .validacao import (
    valida_dados_obrigatorios_notafiscal,
    valida_dados_emissao_boleto,
)
from .boleto import (
    exibirBoleto,
    deletarBoleto,
)

from integracoes.banco.Itau.boleto import boleto
from .webmania import emite_nf

success_url_venda = _("venda:vendaList")
template_name_createupdate = "venda/vendaCreateUpdate.html"
template_name_nf = "venda/vendaNF.html"
template_name_expedicao = "venda/vendaExpedicao.html"
today = datetime.date.today()
date_time = datetime.datetime.now()


class VendaList(LoginRequiredMixin, ListView):
    model = Venda
    template_name = "venda/vendaList.html"

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Venda.objects.all().order_by("-data_pedido")
        else:
            return Venda.objects.filter(vendedor=self.request.user).order_by(
                "-data_pedido"
            )

    def get_context_data(self, **kwargs: Any):
        data = super().get_context_data(**kwargs)
        data["empresa"] = Empresa.objects.first()
        return data


vendaList = VendaList.as_view()


@login_required
def getVendasAjax(request):
    if request.user.is_superuser:
        bd_data = Venda.objects.all().order_by("-data_pedido")[0:1000]
    else:
        bd_data = Venda.objects.filter(vendedor=request.user).order_by("-data_pedido")[
            0:400
        ]

    data = []
    for d in bd_data:
        hash = d.get_hash()

        clone = f"<abbr title='Clonar documento de venda'><a href='{d}/clonevenda/'><i class='fa fa-files-o' aria-hidden='true'></i></a></abbr>"

        whatsapp = '<abbr title="Enviar Whatsapp"><a href="https://api.whatsapp.com/send?text=Ol%C3%A1!%20Segue%20o%20link%20para%20o%20pedido%20feito%20na%20Original Refrigeradores: http://original.crm.com.br/venda/{}/orcamento" target="_blank"/><i class="fa fa-whatsapp"></i></a></abbr>'.format(
            d.get_hash()
        )

        orcamento = f"<abbr title='Orçamento'><a href='{hash}/orcamento' target='_blank'><i class='fa fa-file-text-o'></i></a></abbr>"

        editar = f"<abbr title='Editar'><a class='px-1' href='{d.pk}/editar/'><i class='fa fa-edit'></i></a></abbr>"

        acoes = (whatsapp, orcamento, editar)
        numero_nf = "-"
        if d.numero_nf:
            numero_nf = str(d.numero_nf)
        data.append(
            {
                "cod": d.pk,
                "cliente": d.cliente.nome,
                "notafiscal": numero_nf,
                "cliente": f"<a href='/cliente/{d.cliente.id}/editar/' style='font-size: 12px;'>{d.cliente.nome[:30]}</a>",
                "pedido": d.data_pedido.strftime("%d/%m/%Y %H:%M"),
                "vendedor": d.vendedor.username,
                "subtotal": f"R$ {d.subtotal:,.2f}",
                "status": d.status_venda,
                "condicao": d.condicaopgto.nome,
                "clonar": clone,
                "acoes": acoes,
            }
        )
    return JsonResponse({"data": data})


class VendaDetails(LoginRequiredMixin, DetailView):
    model = Venda
    template_name = "venda/vendaDetails.html"


@login_required
@permission_required("venda.change_venda")
def vendaNF(request, pk):
    """
    venda nf
    """
    import locale

    erros = []
    locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")

    def get_aliq_imcs(estado, produto):
        icms = 7
        if estado == "MG":
            icms = produto.aliq_icms_interno
        elif estado in ("SP", "SC", "RS", "RJ", "PR"):
            icms = 12
        return icms

    def calcula_imposto_produtos(objeto, produtos):
        lista_produtos = []
        for o in produtos:
            _produtos = {}
            _produtos["quantidade"] = o.quantidade
            _produtos["preco"] = o.preco
            _produtos["subtotal"] = o.subtotal
            _produtos["codigoproduto"] = o.produto.codigoproduto
            _produtos["nome"] = o.produto.nome
            _produtos["ncm"] = o.produto.ncm
            _produtos["cst"] = o.produto.cst
            _produtos["cfop"] = o.produto.cfop
            _produtos["unimed"] = o.produto.unimed
            _produtos["aliq_ipi"] = o.produto.aliq_ipi
            total_ipi = float(o.subtotal / 100) * o.produto.aliq_ipi
            _produtos["valor_ipi"] = locale.currency(
                total_ipi, grouping=True, symbol=True
            )
            # valida ICMS
            aliq_icms = get_aliq_imcs(objeto.cliente.estado, o)
            total_icms = float(o.subtotal / 100) * aliq_icms
            _produtos["aliq_icms"] = aliq_icms
            _produtos["valor_icms"] = locale.currency(
                total_icms, grouping=True, symbol=True
            )
            _produtos["unimed"] = o.produto.unimed
            lista_produtos.append(_produtos)
        return lista_produtos

    objeto = get_object_or_404(Venda, pk=pk)

    empresa = Empresa.objects.first()
    produtos_com_imposto = calcula_imposto_produtos(
        objeto, objeto.vendaproduto_set.all()
    )
    # aliq_icms = get_aliq_imcs(objeto.cliente.estado, objeto.vendaproduto_set.all()[0])
    # total_icms = float(objeto.valor_venda / 100) * aliq_icms
    # total_ipi = (
    #    float(objeto.valor_venda / 100)
    #    * objeto.vendaproduto_set.all()[0].produto.aliq_ipi
    # )
    # valor_total_com_imposto = float(objeto.valor_venda) + total_icms + total_ipi
    # objeto.valortotalcomimposto = valor_total_com_imposto
    objeto.save()
    #    "basecalculoicms": locale.currency(objeto.subtotal, grouping=True, symbol=True),
    #    "valoricms": locale.currency(total_icms, grouping=True, symbol=True),
    #    "valoripi": locale.currency(total_ipi, grouping=True, symbol=True),
    #    "valorfrete": locale.currency(objeto.valor_frete, grouping=True, symbol=True),
    #    "valortotalcomimposto": locale.currency(
    #        objeto.valortotalcomimposto, grouping=True, symbol=True
    #    ),
    venda = {
        "totalprodutos": locale.currency(objeto.subtotal, grouping=True, symbol=True),
        "valortotal": locale.currency(objeto.valor_venda, grouping=True, symbol=True),
        "notafiscal": objeto.chave,
    }

    if request.method == "POST":
        # 1 valida dados
        # @TODO falta validar tamanho dos campos ou no model ou no validateion para nao estourar o tamanho maximo ao emitir nota
        # @TODO ve se retorna o proximo numero a ser usado na nota
        # 2 formata dict
        # 3 envia pro webservice
        # 4 se erro retorna msg erro
        # 5 se sucesso grava retorno, codigo
        # 6 gera url para abrir link da nota para impressao
        # 7 trava status venda para nao permitir cancelar
        # 8 habilita cancelar nota?
        form = VendaForm(request.POST or None, instance=objeto)
        errosNF = valida_dados_obrigatorios_notafiscal(form)
        if not errosNF:
            resposta, erros = emite_nf(pk)
        if not erros:
            return redirect(f"/venda/{pk}/editar/")

    context = {
        "id": pk,
        "erros": erros,
        "empresa": empresa,
        "cliente": objeto.cliente,
        "produtos": produtos_com_imposto,
        "venda": objeto,
        "vendadadostratado": venda,
    }
    return render(request, template_name_nf, context)


@login_required
@permission_required("venda.view_venda")
def expedicaoNF(request, pk):
    import locale

    erros = []
    locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")

    def get_aliq_imcs(estado, produto):
        icms = 7
        if estado == "MG":
            icms = produto.produto.aliq_icms_interno
        elif estado in ("SP", "SC", "RS", "RJ", "PR"):
            icms = 12
        return icms

    def calcula_imposto_produtos(objeto, produtos):
        lista_produtos = []
        for o in produtos:
            _produtos = {}
            _produtos["quantidade"] = o.quantidade
            _produtos["preco"] = o.preco
            _produtos["voltagem"] = o.voltagem
            _produtos["torneira"] = o.torneira
            _produtos["adesivado"] = o.adesivado
            _produtos["subtotal"] = o.subtotal
            _produtos["codigoproduto"] = o.produto.codigoproduto
            _produtos["nome"] = o.produto.nome
            _produtos["ncm"] = o.produto.ncm
            _produtos["cst"] = o.produto.cst
            _produtos["cfop"] = o.produto.cfop
            _produtos["unimed"] = o.produto.unimed
            _produtos["aliq_ipi"] = o.produto.aliq_ipi
            total_ipi = float(o.subtotal / 100) * o.produto.aliq_ipi
            _produtos["valor_ipi"] = locale.currency(
                total_ipi, grouping=True, symbol=True
            )
            # valida ICMS
            aliq_icms = get_aliq_imcs(objeto.cliente.estado, o)
            total_icms = float(o.subtotal / 100) * aliq_icms
            _produtos["aliq_icms"] = aliq_icms
            _produtos["valor_icms"] = locale.currency(
                total_icms, grouping=True, symbol=True
            )
            _produtos["unimed"] = o.produto.unimed
            lista_produtos.append(_produtos)
        return lista_produtos

    objeto = get_object_or_404(Venda, pk=pk)

    produtos_com_imposto = calcula_imposto_produtos(
        objeto, objeto.vendaproduto_set.all()
    )
    aliq_icms = get_aliq_imcs(objeto.cliente.estado, objeto.vendaproduto_set.all()[0])
    total_icms = float(objeto.valor_venda / 100) * aliq_icms
    total_ipi = (
        float(objeto.valor_venda / 100)
        * objeto.vendaproduto_set.all()[0].produto.aliq_ipi
    )
    valor_total_com_imposto = float(objeto.valor_venda) + total_icms + total_ipi
    objeto.valortotalcomimposto = valor_total_com_imposto
    objeto.save()
    venda = {
        "basecalculoicms": locale.currency(objeto.subtotal, grouping=True, symbol=True),
        "valoricms": locale.currency(total_icms, grouping=True, symbol=True),
        "vendedor": objeto.vendedor.get_username(),
        "valoripi": locale.currency(total_ipi, grouping=True, symbol=True),
        "valorfrete": locale.currency(objeto.valor_frete, grouping=True, symbol=True),
        "totalprodutos": locale.currency(objeto.subtotal, grouping=True, symbol=True),
        "valortotal": locale.currency(objeto.valor_venda, grouping=True, symbol=True),
        "valortotalcomimposto": locale.currency(
            objeto.valortotalcomimposto, grouping=True, symbol=True
        ),
        "notafiscal": objeto.chave,
    }

    form = VendaForm(request.POST or None, instance=objeto)
    errosNF = valida_dados_obrigatorios_notafiscal(form)

    if request.method == "GET":
        if request.GET.get("status_expedicao", ""):
            objeto.status_expedicao = request.GET.get("status_expedicao")
            objeto.data_status_expedicao = datetime.datetime.now()
            if request.GET.get("status_expedicao") == "Enviado":
                objeto.status_venda = "enviado"
            objeto.save()
            return redirect(f"/expedicao")
            # return redirect(f"/venda/{pk}/expedicao/")

    selectProdutos = VendaProduto.objects.filter(venda=pk)

    ufs = ESCOLHAS_ESTADO2
    if request.method == "POST":
        # 1 valida dados
        # @TODO falta validar tamanho dos campos ou no model ou no validateion para nao estourar o tamanho maximo ao emitir nota
        # @TODO ve se retorna o proximo numero a ser usado na nota
        # 2 formata dict
        # 3 envia pro webservice
        # 4 se erro retorna msg erro
        # 5 se sucesso grava retorno, codigo
        # 6 gera url para abrir link da nota para impressao
        # 7 trava status venda para nao permitir cancelar
        # 8 habilita cancelar nota?
        if request.POST.get("enviar_cotacao_tranportadora", "") == "Salvar":
            # salva cotacao
            numero_cotacao = request.POST.get("numero-cotacao", "")
            valor_frete = request.POST.get("valor-frete", "")
            transportadora = request.POST.get("transportadora", "")
            if numero_cotacao or valor_frete:
                objeto.cotacao_transportadora = numero_cotacao
                valor_frete = float(valor_frete.replace(",", "."))
                objeto.valor_frete = valor_frete
                objeto.transportadora_id = transportadora
                objeto.save()
            # print("salvar")
        elif request.POST.get("salvar") == "Salvar":
            cliente = objeto.cliente
            cliente.logradouro = request.POST.get("logradouro")
            cliente.numero = request.POST.get("numero")
            cliente.nome = request.POST.get("nome")
            cliente.nome_fantasia = request.POST.get("nome_fantasia")
            cliente.cnpj = request.POST.get("cnpj")
            cliente.nome_fantasia = request.POST.get("nome_fantasia")
            cliente.insc_estadual = request.POST.get("insc_estadual")
            cliente.bairro = request.POST.get("bairro")
            cliente.cidade = request.POST.get("cidade")
            cliente.estado = request.POST.get("estado")
            cliente.complemento = request.POST.get("complemento")
            cliente.tel_principal = request.POST.get("tel_principal")
            objeto.quemrecebe_mercadolivre = request.POST.get("quemrecebe_mercadolivre")
            objeto.telefonequemrecebe_mercadolivre = request.POST.get(
                "telefonequemrecebe_mercadolivre"
            )
            if request.POST.get("urgente") == "sim":
                objeto.urgente = True
            if request.POST.get("urgente") == "nao":
                objeto.urgente = False
            objeto.save()
            cliente.save()
        elif request.POST.get("EmitirNF", "") == "Emitir nota fiscal":
            if not errosNF:
                resposta, erros = emite_nf(pk)

        elif request.POST.get("saveComprovante") == "Salvar":
            objeto.comprovante = request.FILES["comprovante"]
            objeto.save()

        elif request.POST.get("salvarProdutos") == "Salvar":
            for item in selectProdutos:
                itemSelected = get_object_or_404(VendaProduto, id=item.id)
                volt = request.POST.get(f"voltagem{item.id}")
                try:
                    voltagem = get_object_or_404(Voltagem, id=volt)
                    itemSelected.voltagem = voltagem
                    itemSelected.save()
                except:
                    pass
                
                torn = request.POST.get(f"torneira{item.id}")
                try:
                    torneira = get_object_or_404(Torneira, id=torn)
                    itemSelected.torneira = torneira
                    itemSelected.save()
                except:
                    pass

                ades = request.POST.get(f"adesivado{item.id}")
                try:
                    adesivado = get_object_or_404(Adesivado, id=ades)
                    itemSelected.adesivado = adesivado
                    itemSelected.save()
                except:
                    pass


        if not erros:
            return redirect(f"/venda/{pk}/expedicao/")

    empresa = objeto.vendedor.extenduser.empresa
    transportadoras = Transportadora.objects.all().order_by("nome")
    voltagem = Voltagem.objects.all()
    torneira = Torneira.objects.all()
    adesivado = Adesivado.objects.all()
    context = {
        "id": pk,
        "ufs": ufs,
        "erros": erros,
        "erros_NF": errosNF,
        "empresa": empresa,
        "transportadoras": transportadoras,
        "cliente": objeto.cliente,
        "comprovante": objeto.comprovante,
        "produtos": produtos_com_imposto,
        "selectProdutos": selectProdutos,
        "voltagens": voltagem,
        "torneiras": torneira,
        "adesivado": adesivado,
        "venda": objeto,
        "vendadadostratado": venda,
    }
    return render(request, template_name_expedicao, context)


class VendaDelete(LoginRequiredMixin, DeleteView):
    model = Venda
    template_name = "venda/vendaDelete.html"
    success_url = success_url_venda

    def get(self, request, *args, **kwargs):
        if self.get_object().status_venda == "enviado":
            self.object = self.get_object()
            context = self.get_context_data(object=self.object)
            self.template_name = "venda/vendaRestrict.html"
            return self.render_to_response(context)
            # tem elemento, nao posso excluir
        else:
            self.object = self.get_object()
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)


vendaDelete = VendaDelete.as_view()


def produtoPrecoAjax(request):
    produto = request.GET.get("id_produto")
    preco = Produto.objects.filter(id=produto)

    data = []
    for preco in preco:
        data = preco.preco
        return JsonResponse({"data": data})


def condicaoAjax(request):
    condicao = request.GET.get("id_condicao")
    dados = CondicaoVenda.objects.filter(id=condicao)
    pgid = 0
    info = []
    for i in dados:
        pgid = i.formapgto.pk
        info.append(
            {
                "nome": i.nome,
                "parcelas": i.parcelas,
                "primeira": i.primeira,
                "demais": i.demais,
                "forpgto": i.formapgto.nome,
                "pgid": pgid,
            }
        )
    return JsonResponse({"info": info})


def clienteAjax(request):
    if request.is_ajax():
        term = request.GET.get("term")
        clientes = Cliente.objects.filter(
            Q(nome__icontains=term) | Q(nome_fantasia__icontains=term)
        )
        data = list(clientes.values())
        return JsonResponse(data, safe=False)


@login_required
@permission_required("venda.add_venda")
def vendaCreate(request):
    form = VendaForm(request.POST or None)
    Formset_VendaProduto_Factory = inlineformset_factory(
        Venda,
        VendaProduto,
        form=VendaProdutoForm,
        min_num=1,
        extra=0,
        can_delete=False,
    )
    produto_form = Formset_VendaProduto_Factory(request.POST or None)
    Formset_contaReceber_Factory = inlineformset_factory(
        Venda,
        ContaReceber,
        form=VendaContaReceberForm,
        extra=0,
        can_delete=False,
    )
    parcela_form = Formset_contaReceber_Factory(
        request.POST or None, request.FILES or None
    )

    maximodesconto = MaximoDesconto.objects.first()
    if maximodesconto:
        maximodesconto = maximodesconto.qtde
    else:
        maximodesconto = 0

    limiteproducaodiaria = 30

    if request.method == "POST":
        if form.is_valid() and produto_form.is_valid() and parcela_form.is_valid():
            venda = form.save(commit=False)
            venda.vendedor = request.user
            venda.atualizadopor = f"{request.user}-{date_time}"
            venda.save()
            # trava para vendedor nao colocar status acima de autorizado
            if not request.user.is_superuser:
                if venda.status_venda not in ("orcamento", "autorizado"):
                    venda.status_venda = "orcamento"
                    venda.save()
            produto_form.instance = venda
            produto_form.save()
            parcela_form.instance = venda
            parcela_form.save()
            return redirect("venda:vendaList")
        else:
            context = {
                "texto": "Novo",
                "form": form,
                "produto": produto_form,
                "parcela": parcela_form,
                "maximodesconto": maximodesconto,
                "limiteproducaodiaria": limiteproducaodiaria,
            }
            return render(request, template_name_createupdate, context)
    else:
        context = {
            "texto": "Novo",
            "form": form,
            "produto": produto_form,
            "parcela": parcela_form,
            "maximodesconto": maximodesconto,
            "limiteproducaodiaria": limiteproducaodiaria,
        }
        return render(request, template_name_createupdate, context)


@login_required
@permission_required("venda.change_venda")
def vendaUpdate(request, pk):
    objeto = get_object_or_404(Venda, pk=pk)
    form = VendaForm(request.POST or None, instance=objeto)
    Formset_VendaProduto_Factory = inlineformset_factory(
        Venda, VendaProduto, form=VendaProdutoForm, extra=0, min_num=1, can_delete=True
    )
    produto_form = Formset_VendaProduto_Factory(request.POST or None, instance=objeto)
    Formset_contaReceber_Factory = inlineformset_factory(
        Venda,
        ContaReceber,
        form=VendaContaReceberForm,
        extra=0,
        min_num=1,
        can_delete=False,
    )
    parcela_form = Formset_contaReceber_Factory(
        request.POST or None, request.FILES or None, instance=objeto
    )
    maximodesconto = MaximoDesconto.objects.first()
    if maximodesconto:
        maximodesconto = maximodesconto.qtde
    else:
        maximodesconto = 0
    limiteproducaodiaria = LimiteProducaoDiaria.objects.first()
    if limiteproducaodiaria:
        limiteproducaodiaria = limiteproducaodiaria.quantidade
    else:
        limiteproducaodiaria = 0
    boleto = ContaReceber.objects.filter(venda__id=pk)
    # informa os ids que possuem boletos
    codigo_boletos = []
    for b in boleto:
        if b.dados_boleto != {}:
            codigo_boletos.append(b.parcela[-0:])

    vend = User.objects.filter(id=objeto.vendedor.id)
    erros_NF = ""
    erros_boleto = ""
    erros_NF = valida_dados_obrigatorios_notafiscal(form)

    # ocorrencia = Ocorrencia.objects.filter(venda=pk)

    if request.method == "POST":
        if not request.user.is_superuser:
            if form.data["status_venda"] not in ["orcamento", "autorizado"]:
                if Venda.objects.get(id=pk).status_venda != form.data["status_venda"]:
                    erros_NF = [
                        "Voce não tem permissão para alterar pedido depois que ele saiu de Orcamento e Autorizado"
                    ]
                    codigo = False
                    context = {
                        "id": pk,
                        # "ocorrencia": ocorrencia,
                        "erros_boleto": erros_boleto,
                        "erros_NF": erros_NF,
                        "boletos": codigo_boletos,
                        "texto": "Alterar",
                        "codigo": codigo,
                        "form": form,
                        "produto": produto_form,
                        "parcela": parcela_form,
                        "maximodesconto": maximodesconto,
                        "limiteproducaodiaria": limiteproducaodiaria,
                    }
                    return render(request, template_name_createupdate, context)

        if request.POST.get("exibirBoleto"):
            objetos = request.POST.get("exibirBoleto")
            sep_venda_parcela = objetos.split(",")
            num_parcela = []
            num_parcela.append(sep_venda_parcela[0])
            num_parcela.append(sep_venda_parcela[1])
            exibirBoleto(num_parcela)

        if request.POST.get("deletarBoleto"):
            deletar_parcela = request.POST.get("deletarBoleto")
            deletarBoleto(deletar_parcela)
            return redirect(f"/venda/{pk}/editar")

        if form.is_valid() and produto_form.is_valid() and parcela_form.is_valid():
            venda = form.save(commit=False)
            venda.vendedor = vend[0]
            venda.atualizadopor = f"{request.user}-{date_time}"
            produto_form.save()
            parcela_form.save()
            venda.save()

            if request.POST.get("EmitirNF") or request.POST.get("validarBoleto"):
                erros_NF = ""
                erros_boleto = ""
                if not erros_NF:
                    erros_NF = emitir(form)

                if request.POST.get("validarBoleto"):
                    objetos = request.POST.get("validarBoleto")
                    sep_venda_parcela = objetos.split(",")
                    num_parcela = []
                    num_parcela.append(sep_venda_parcela[0])
                    num_parcela.append(sep_venda_parcela[1])
                    erros_boleto = valida_dados_emissao_boleto(num_parcela)

                codigo = True
                context = {
                    "id": pk,
                    # "ocorrencia": ocorrencia,
                    "erros_boleto": erros_boleto,
                    "erros_NF": erros_NF,
                    "boletos": codigo_boletos,
                    "texto": "Alterar",
                    "codigo": codigo,
                    "form": form,
                    "produto": produto_form,
                    "parcela": parcela_form,
                    "maximodesconto": maximodesconto,
                    "limiteproducaodiaria": limiteproducaodiaria,
                }
                return render(request, template_name_createupdate, context)

            else:
                if venda.status_venda == "expedicao":
                    return redirect(_("expedicao:listaExpedicao"))
                else:
                    return redirect(_("venda:vendaList"))

        else:
            erros_produto = []
            if produto_form.errors:
                for erro in produto_form.errors:
                    if "__all__" in erro:
                        erros_produto.append(erro["__all__"])
            codigo = True
            context = {
                "id": pk,
                # "ocorrencia": ocorrencia,
                "erros_NF": erros_NF,
                "erros_produto": erros_produto,
                "erros_boleto": erros_boleto,
                "boletos": codigo_boletos,
                "texto": "Alterar",
                "codigo": codigo,
                "form": form,
                "produto": produto_form,
                "parcela": parcela_form,
                "maximodesconto": maximodesconto,
                "limiteproducaodiaria": limiteproducaodiaria,
            }
        if produto_form.errors:
            context["msgerro"] = True
        return render(request, template_name_createupdate, context)

    else:
        venda = objeto
        codigo = True
        context = {
            "id": pk,
            # "ocorrencia": ocorrencia,
            "erros_NF": erros_NF,
            "venda": venda,
            "vendedor": objeto.vendedor,
            "boletos": codigo_boletos,
            "texto": "Alterar",
            "codigo": codigo,
            "form": form,
            "produto": produto_form,
            "parcela": parcela_form,
            "maximodesconto": maximodesconto,
            "limiteproducaodiaria": limiteproducaodiaria,
        }
    return render(request, template_name_createupdate, context)


@login_required
@permission_required("venda.add_venda")
def vendaClone(request, pk):
    venda_base_id = get_object_or_404(Venda, pk=pk)
    venda_base = Venda.objects.filter(pk=pk)
    cliente = venda_base_id.cliente

    venda = {}
    for vb in venda_base:
        venda.update(
            {
                "cliente": cliente,
                "transportadora": venda_base_id.transportadora,
                "status_venda": venda_base_id.status_venda,
                "valor_venda": vb.valor_venda,
                "valor_venda": vb.valor_venda,
                "porcentagem_desconto": vb.porcentagem_desconto,
                "condicaopgto": vb.condicaopgto,
                "dias_prim_par": vb.dias_prim_par,
                "dias_outras_par": vb.dias_outras_par,
                "parcelas": vb.parcelas,
                "formapgto": vb.formapgto,
                "detalhes": vb.detalhes,
            }
        )

    produto_base = VendaProduto.objects.filter(venda__pk=pk)
    prod = []
    for pb in produto_base:
        prod.append(
            {
                "produto": pb.produto,
                "voltagem": pb.voltagem,
                "torneira": pb.torneira,
                "adesivado": pb.adesivado,
                "quantidade": pb.quantidade,
                "preco": pb.preco,
                "subtotal": pb.subtotal,
            }
        )

    parcela_base = ContaReceber.objects.filter(venda__pk=pk)
    parc = []
    for pb in parcela_base:
        parc.append(
            {
                "parcela": pb.parcela,
                "receita": pb.receita,
                "valor": pb.valor,
                "datadocumento": pb.datadocumento,
                "datavencimento": pb.datavencimento,
                "datapagamento": pb.datapagamento,
                "formapgto": pb.formapgto,
                "detalhes": pb.detalhes,
            }
        )

    form = VendaForm(request.POST, initial=venda)

    Formset_VendaProduto_Factory = inlineformset_factory(
        Venda, VendaProduto, form=VendaProdutoForm, extra=len(prod)
    )
    produto_form = Formset_VendaProduto_Factory(request.POST or None, initial=prod)

    Formset_contaReceber_Factory = inlineformset_factory(
        Venda,
        ContaReceber,
        form=VendaContaReceberForm,
        extra=len(parc),
    )
    parcela_form = Formset_contaReceber_Factory(
        request.POST or None, request.FILES or None, initial=parc
    )

    if request.method == "POST":
        if form.is_valid() and produto_form.is_valid() and parcela_form.is_valid():
            venda = form.save(commit=False)
            venda.vendedor = str(request.user).capitalize()
            venda.save()
            produto_form.instance = venda
            produto_form.save()
            parcela_form.instance = venda
            parcela_form.save()
            return redirect(_("venda:vendaList"))
        else:
            context = {
                "form": form,
                "produto": produto_form,
                "parcela": parcela_form,
            }
            return render(request, template_name_createupdate, context)
    else:
        form = VendaForm(initial=venda)
        context = {
            "form": form,
            "produto": produto_form,
            "parcela": parcela_form,
        }
        return render(request, template_name_createupdate, context)


def orcamento(request, hash):
    str_decoded = base64.b64decode(hash)
    pk = str_decoded.decode("utf-8")

    venda = Venda.objects.filter(pk=pk)
    produtos = VendaProduto.objects.filter(venda__pk=pk)
    prestacoes = ContaReceber.objects.filter(venda__pk=pk)

    template_path = "venda/vendaOrcamento.html"
    context = {"venda": venda, "produtos": produtos, "prestacoes": prestacoes, "pk": pk}

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'filename="orçamento{pk}.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html,
        dest=response,
    )

    if pisa_status.err:
        return HttpResponse("We had some errors <pre>" + html + "</pre>")
    return response


def relatorios(request):
    template_name = "venda/vendaCharts.html"

    total_ano = Venda.objects.filter(data_pedido__year=today.year).aggregate(
        Sum("subtotal")
    )["subtotal__sum"]
    total_mes = (
        Venda.objects.filter(data_pedido__year=today.year)
        .filter(data_pedido__month=today.month)
        .aggregate(Sum("subtotal"))["subtotal__sum"]
    )

    vendas = Venda.objects.filter(data_pedido__year=today.year).aggregate(
        Count("subtotal")
    )["subtotal__count"]
    vendas_mes = (
        Venda.objects.filter(data_pedido__year=today.year)
        .filter(data_pedido__month=today.month)
        .aggregate(Count("subtotal"))["subtotal__count"]
    )
    produtos = VendaProduto.objects.filter(
        venda__data_pedido__year=today.year
    ).aggregate(Sum("quantidade"))["quantidade__sum"]
    produtos_mes = (
        VendaProduto.objects.filter(venda__data_pedido__year=today.year)
        .filter(venda__data_pedido__month=today.month)
        .aggregate(Sum("quantidade"))["quantidade__sum"]
    )
    if not total_ano:
        total_ano = vendas = produtos = 0

    if not total_mes:
        total_mes = vendas_mes = produtos_mes = 0

    meses = [
        "Janeiro",
        "Fevereiro",
        "Março",
        "Abril",
        "Maio",
        "Junho",
        "Julho",
        "Agosto",
        "Setembro",
        "Outubro",
        "Novembro",
        "Dezembro",
    ]

    str_month = meses[today.month - 1]
    try:
        month_next = meses[today.month]
    except:
        month_next = meses[today.month - 1]

    ano = today.year
    periodo = f"de {month_next}/{ano-1} a {str_month}/{ano}"
    mes_atual = periodo.upper()
    ano_label = str(ano)

    anos = []
    cont = 0
    for a in range(5):
        calc = ano - cont
        anos.append(str(calc))
        cont += 1

    meses = [
        "JANEIRO",
        "FEVEREIRO",
        "MARÇO",
        "ABRIL",
        "MAIO",
        "JUNHO",
        "JULHO",
        "AGOSTO",
        "SETEMBRO",
        "OUTUBRO",
        "NOVEMBRO",
        "DEZEMBRO",
    ]
    meses_lista = []
    mes = datetime.datetime.now().month + 1
    ano = datetime.datetime.now().year
    for i in range(12):
        mes -= 1
        if mes == 0:
            mes = 12
            ano -= 1
        meses_lista.append(meses[mes - 1])

    context = {
        "anos": anos,
        "ano": ano_label,
        "meses": meses_lista,
        "total_mes": total_mes,
        "total_ano": total_ano,
        "vendas": vendas,
        "vendas_mes": vendas_mes,
        "produtos": produtos,
        "produtos_mes": produtos_mes,
    }
    return render(request, template_name, context)


def total_vendido_ano(request):
    obj = Venda.objects.all()
    meses = [
        "jan",
        "fev",
        "mar",
        "abr",
        "mai",
        "jun",
        "jul",
        "ago",
        "set",
        "out",
        "nov",
        "dez",
    ]
    dados = []
    labels = []
    mes = datetime.datetime.now().month + 1
    ano = datetime.datetime.now().year
    for i in range(12):
        mes -= 1
        if mes == 0:
            mes = 12
            ano -= 1
        soma = sum(
            i.subtotal
            for i in obj
            if i.data_pedido.month == mes and i.data_pedido.year == ano
        )
        labels.append(meses[mes - 1])
        dados.append(soma)
    data_json = {"data": dados[::-1], "labels": labels[::-1]}
    return JsonResponse(data_json)


def total_vendido_mes(request):
    obj = Venda.objects.filter(data_pedido__month=today.month).filter(
        data_pedido__year=today.year
    )

    ref_dias = calendar.monthcalendar(today.year, today.month)
    dias = []
    for i in ref_dias:
        for j in i:
            if j != 0:
                data = datetime.date(year=today.year, month=today.month, day=j)
                dias.append(str(data))

    dados = []
    for i in range(len(dias)):
        data = datetime.date(year=today.year, month=today.month, day=i + 1)
        soma = sum(o.subtotal for o in obj if o.data_pedido.day == i + 1)
        dados.append(soma)

    data_json = {
        "data": dados,
        "labels": dias,
    }
    return JsonResponse(data_json)


def meses_ajax(request):
    ano = request.GET.get("ano")
    ano = int(ano)
    mes = request.GET.get("mes")

    meses = [
        "JANEIRO",
        "FEVEREIRO",
        "MARÇO",
        "ABRIL",
        "MAIO",
        "JUNHO",
        "JULHO",
        "AGOSTO",
        "SETEMBRO",
        "OUTUBRO",
        "NOVEMBRO",
        "DEZEMBRO",
    ]

    index = meses.index(mes)
    mes = index + 1

    obj = Venda.objects.filter(data_pedido__month=mes).filter(data_pedido__year=ano)

    vendas = (
        Venda.objects.filter(data_pedido__month=mes)
        .filter(data_pedido__year=ano)
        .aggregate(Count("subtotal"))["subtotal__count"]
    )
    produtos = (
        VendaProduto.objects.filter(venda__data_pedido__year=ano)
        .filter(venda__data_pedido__month=mes)
        .aggregate(Sum("quantidade"))["quantidade__sum"]
    )
    total_mes = (
        Venda.objects.filter(data_pedido__year=ano)
        .filter(data_pedido__month=mes)
        .aggregate(Sum("subtotal"))["subtotal__sum"]
    )
    mensagem = []
    if not total_mes:
        total_mes = vendas = produtos = 0
        mensagem = "Não há lançamento para o período!"

    ref_dias = calendar.monthcalendar(ano, mes)
    labels = []
    for i in ref_dias:
        for j in i:
            if j != 0:
                data = datetime.date(year=ano, month=mes, day=j)
                labels.append(str(data))

    dados = []
    for i in range(len(labels)):
        data = datetime.date(year=ano, month=mes, day=i + 1)
        soma = sum(o.subtotal for o in obj if o.data_pedido.day == i + 1)
        dados.append(soma)

    data_json = {
        "data": dados,
        "labels": labels,
        "vendas_mes_atual": vendas,
        "produtos_mes_atual": produtos,
        "total_mes": total_mes,
        "mensagem": mensagem,
    }

    return JsonResponse(data_json)


def boletoList(request):
    template_name = "venda/boletosList.html"
    boletos = ContaReceber.objects.exclude(dados_boleto={})
    if request.method == "POST":
        if request.POST.get("exibirBoleto"):
            exibir = request.POST.get("exibirBoleto")
            sep_venda_parcela = exibir.split(",")
            exibir_parcela = []
            exibir_parcela.append(sep_venda_parcela[0])
            exibir_parcela.append(sep_venda_parcela[1])
            exibirBoleto(exibir_parcela)
    context = {"boletos": boletos}
    return render(request, template_name, context)
