import datetime
import calendar
from typing import Any
from django.urls import reverse_lazy as _
from django.shortcuts import redirect, render, get_object_or_404
from django.forms import inlineformset_factory
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.db.models import Sum, Count, Q
from django.db.models.functions import ExtractMonth
from django.views.generic import ListView, DetailView
from django.views.generic.edit import DeleteView
import base64


from project.constantes import ESCOLHAS_ESTADO2


from .models import (
    CondicaoVenda,
    Venda,
    VendaProduto,
    MaximoDesconto,
    Voltagem,
    Torneira,
    Adesivado,
    VendaCotacao,
    ArquivosVenda,
)
from .forms import VendaForm, VendaProdutoForm
from cliente.models import Cliente
from produto.models import Produto
from producao.models import LimiteProducaoDiaria
from empresa.models import Empresa
from transportadora.models import Transportadora
from financeiro.models import ContaReceber
from financeiro.forms import VendaContaReceberForm

from .validacao import (
    valida_dados_obrigatorios_notafiscal,
    valida_dados_emissao_boleto,
)
from .boleto import (
    exibirBoleto,
    deletarBoleto,
)

# from integracoes.banco.Itau.boleto import boleto
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
        bd_data = Venda.objects.all().order_by("-data_pedido")[0 : 100 + 100]
    else:
        bd_data = Venda.objects.filter(vendedor=request.user).order_by("-data_pedido")[
            0 : 100 + 100
        ]

    data = []
    for d in bd_data:
        hash = d.get_hash()

        clone = f"<abbr title='Clonar documento de venda'><a href='{d}/clonevenda/'><i class='fa fa-files-o' aria-hidden='true'></i></a></abbr>"

        whatsapp = '<abbr title="Enviar Whatsapp"><a href="https://api.whatsapp.com/send?text=Ol%C3%A1!%20Segue%20o%20link%20para%20o%20pedido%20feito%20na%20Original Refrigeradores: http://original.crm.com.br/venda/{}/orcamento" target="_blank"/><i class="fa fa-whatsapp"></i></a></abbr>'.format(
            d.get_hash()
        )

        orcamento = f"<abbr title='Orçamento'><a href='{hash}/orcamento/{d.pk}' target='_blank'><i class='fa fa-file-text-o'></i></a></abbr>"

        editar = f"<abbr title='Editar'><a class='px-1' href='{d.pk}/editar/'><i class='fa fa-edit'></i></a></abbr>"

        acoes = (whatsapp, orcamento, editar)
        numero_nf = "-"
        if d.numero_nf:
            numero_nf = str(d.numero_nf)
        data.append(
            {
                "cod": d.pk,
                "cliente": d.cliente.nome,
                "cliente": f"<a href='/cliente/{d.cliente.id}/editar/' style='font-size: 12px;'>{d.cliente.nome[:30]}</a>",
                "notafiscal": numero_nf,
                "pedido": d.data_pedido.strftime("%d/%m/%Y"),
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

    all_arquivos = ArquivosVenda.objects.all()
    bd_arquivos = ArquivosVenda.objects.filter(venda=pk)

    if request.method == "GET":
        if request.GET.get("status_expedicao", ""):
            if request.GET.get("status_expedicao", "") == "Concluido":
                if not request.user.is_superuser:
                    return "sem permissao"
                    # return redirect(f"/expedicao")
            if objeto.status_venda == "enviado":
                objeto.status_posvenda = request.GET.get("status_expedicao")
                objeto.data_status_expedicao = datetime.datetime.now()
            else:
                objeto.status_expedicao = request.GET.get("status_expedicao")
                objeto.data_status_expedicao = datetime.datetime.now()
            if request.GET.get("status_expedicao") == "Enviado":
                objeto.status_venda = "enviado"
                objeto.status_expedicao = request.GET.get("status_expedicao")
                objeto.status_posvenda = "Conferir Dados"
            objeto.save()
            # return redirect(f"/expedicao")
            # return redirect(f"/venda/{pk}/expedicao/")

    selectProdutos = VendaProduto.objects.filter(venda=pk)

    quantProdutos = 0
    pesoTotal = 0
    produto = {}

    for sp in selectProdutos:
        quantProdutos += sp.quantidade
        if sp.produto.peso:
            pesoTotal += sp.quantidade * float(sp.produto.peso)
            produto.update(
                {
                    sp.produto.nome: {
                        "altura": sp.produto.altura,
                        "largura": sp.produto.largura,
                        "comprimento": sp.produto.comprimento,
                    }
                }
            )

    ufs = ESCOLHAS_ESTADO2
    # seta que a nota ja foi impressa
    if request.method == "GET":
        if request.GET.get("nota", ""):
            objeto.nfjaimpressa = True
            objeto.save()
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
        # 8 habilita cancelar nota?a
        if request.POST.get("enviar_cotacao_tranportadora", "") == "Salvar":
            # salva cotacao
            numero_cotacao = request.POST.get("numero-cotacao", "")
            transportadora = request.POST.get("transportadora", "")
            prazo = request.POST.get("prazo", "")
            valor_frete = request.POST.get("valor-frete", "")

            redespacho_transportadora = request.POST.get(
                "redesp_cotacao_transportadora", ""
            )
            redespacho_prazo = request.POST.get("redesp_prazo", "")
            redespacho_valor_frete = request.POST.get("redesp_valor_frete", "")

            if numero_cotacao or valor_frete:
                objeto.cotacao_transportadora = numero_cotacao
                valor_frete = float(valor_frete.replace(",", "."))
                objeto.valor_frete = valor_frete
                objeto.transportadora_id = transportadora
                objeto.prazo = prazo

                objeto.redesp_cotacao_transportadora_id = redespacho_transportadora
                objeto.redesp_prazo = redespacho_prazo
                redespacho_valor_frete = float(redespacho_valor_frete.replace(",", "."))
                objeto.redesp_valor_frete = redespacho_valor_frete

                objeto.save()
        elif request.POST.get("salvar") == "Salvar":
            cliente = objeto.cliente
            cliente.logradouro = request.POST.get("logradouro")
            cliente.numero = request.POST.get("numero")
            cliente.nome = request.POST.get("nome")
            cliente.nome_fantasia = request.POST.get("nome_fantasia")
            cpfcnpj = request.POST.get("cpf/cnpj", "")
            if not cpfcnpj:
                if request.POST.get("cpf", ""):
                    cpfcnpj = request.POST.get("cpf", "")
                else:
                    cpfcnpj = request.POST.get("cnpj", "")
            if len(cpfcnpj) > 12:
                cliente.cnpj = cpfcnpj
                cliente.save()
            else:
                cliente.cpf = cpfcnpj
                cliente.save()

            cliente.nome_fantasia = request.POST.get("nome_fantasia")
            cliente.insc_estadual = request.POST.get("insc_estadual")
            cliente.bairro = request.POST.get("bairro")
            cliente.cidade = request.POST.get("cidade")
            cliente.estado = request.POST.get("estado")
            cliente.cep = request.POST.get("cep")
            objeto.comentario = request.POST.get("comentario")
            objeto.informacao_adicional_notafiscal = request.POST.get(
                "informacao_adicional_notafiscal"
            )
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
        elif request.POST.get("EmitirNF", "") == "Emitir Nota Fiscal":
            if not errosNF:
                resposta, erros = emite_nf(pk)
        elif request.POST.get("salvarArquivos") == "Salvar":
            arquivos = request.FILES.getlist("arquivo")
            if arquivos:
                for arquivo in arquivos:
                    all_arquivos.create(arquivo=arquivo, venda=objeto)
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

    cotacoes = objeto.vendacotacao_set.all()
    voltagem = Voltagem.objects.all()
    torneira = Torneira.objects.all()
    adesivado = Adesivado.objects.all()
    context = {
        "id": pk,
        "ufs": ufs,
        "erros": erros,
        "arquivos": bd_arquivos,
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
        "cotacoes": cotacoes,
        "quantProdutos": quantProdutos,
        "pesoTotal": int(pesoTotal),
        "produto": produto,
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
    # if request.is_ajax():
    term = request.GET.get("term")
    clientes = Cliente.objects.filter(
        Q(nome__icontains=term) | Q(nome_fantasia__icontains=term)
    )
    data = list(clientes.values())
    return JsonResponse(data, safe=False)


def deletarCotacao(request, venda, cotacao):
    cotacao = VendaCotacao.objects.get(id=cotacao)
    cotacao.delete()
    return redirect("venda:expedicaoNF", venda)


@login_required
@permission_required("venda.add_venda")
def vendaCreate(request):
    form = VendaForm(request.POST or None, request.FILES or None)
    Formset_VendaProduto_Factory = inlineformset_factory(
        Venda,
        VendaProduto,
        form=VendaProdutoForm,
        extra=0,
        min_num=1,
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

    limiteproducaodiaria = 3000

    if request.method == "POST":
        if form.is_valid() and produto_form.is_valid() and parcela_form.is_valid():
            venda = form.save(commit=False)
            venda.vendedor = request.user
            venda.atualizadopor = f"{request.user}-{date_time}"
            venda.save()

            # trava para vendedor nao colocar status acima de autorizado
            if not request.user.is_superuser:
                if venda.status_venda not in ("orcamento", "autorizado", "expedicao"):
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
    form = VendaForm(request.POST or None, request.FILES or None, instance=objeto)
    Formset_VendaProduto_Factory = inlineformset_factory(
        Venda, VendaProduto, form=VendaProdutoForm, extra=0, min_num=1, can_delete=True
    )
    produto_form = Formset_VendaProduto_Factory(request.POST or None, instance=objeto)
    Formset_contaReceber_Factory = inlineformset_factory(
        Venda,
        ContaReceber,
        form=VendaContaReceberForm,
        extra=0,
        can_delete=True,
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

    vendedor = objeto.vendedor
    erros_NF = ""
    erros_NF = valida_dados_obrigatorios_notafiscal(form)

    all_arquivos = ArquivosVenda.objects.all()
    bd_arquivos = ArquivosVenda.objects.filter(venda=pk)

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
                        "vendedor": vendedor,
                        "erros_NF": erros_NF,
                        "texto": "Alterar",
                        "codigo": codigo,
                        "form": form,
                        "produto": produto_form,
                        "parcela": parcela_form,
                        "maximodesconto": maximodesconto,
                        "limiteproducaodiaria": limiteproducaodiaria,
                    }
                    return render(request, template_name_createupdate, context)

        if form.is_valid() and produto_form.is_valid() and parcela_form.is_valid():
            venda = form.save(commit=False)
            venda.vendedor = vendedor
            venda.atualizadopor = f"{request.user}-{date_time}"
            venda.save()

            arquivos = request.FILES.getlist("arquivo")
            if arquivos:
                for arquivo in arquivos:
                    all_arquivos.create(arquivo=arquivo, venda=venda)

            produto_form.instance = venda
            produto_form.save()
            parcela_form.instance = venda
            parcela_form.save()

            if request.POST.get("EmitirNF"):
                erros_NF = ""
                if not erros_NF:
                    erros_NF = emitir(form)

                codigo = True
                context = {
                    "id": pk,
                    "erros_NF": erros_NF,
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
            print(parcela_form.errors)
            codigo = True
            context = {
                "id": pk,
                "erros_NF": erros_NF,
                "vendedor": vendedor,
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
        venda = objeto
        codigo = True
        context = {
            "id": pk,
            "erros_NF": erros_NF,
            "venda": venda,
            "vendedor": vendedor,
            "texto": "Alterar",
            "arquivos": bd_arquivos,
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


@login_required
def orcamento(request, hash, id):
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


@login_required
def relatorios(request):
    template_name = "venda/vendaCharts.html"
    mensagem_ano = mensagem_mes = ""

    total_ano = Venda.objects.filter(data_pedido__year=today.year).aggregate(
        Sum("subtotal")
    )["subtotal__sum"]
    vendas_ano = Venda.objects.filter(data_pedido__year=today.year).aggregate(
        Count("subtotal")
    )["subtotal__count"]
    produtos_ano = VendaProduto.objects.filter(
        venda__data_pedido__year=today.year
    ).aggregate(Sum("quantidade"))["quantidade__sum"]

    total_mes = (
        Venda.objects.filter(data_pedido__year=today.year)
        .filter(data_pedido__month=today.month)
        .aggregate(Sum("subtotal"))["subtotal__sum"]
    )
    vendas_mes = (
        Venda.objects.filter(data_pedido__year=today.year)
        .filter(data_pedido__month=today.month)
        .aggregate(Count("subtotal"))["subtotal__count"]
    )
    produtos_mes = (
        VendaProduto.objects.filter(venda__data_pedido__year=today.year)
        .filter(venda__data_pedido__month=today.month)
        .aggregate(Sum("quantidade"))["quantidade__sum"]
    )

    if not total_ano:
        total_ano = vendas_ano = produtos_ano = 0
        mensagem_ano = "Não há lançamentos para o período!"

    if not total_mes:
        total_mes = vendas_mes = produtos_mes = 0
        mensagem_mes = "Não há lançamentos para o período!"

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

    ano = today.year
    anos = []
    cont = 0
    for a in range(5):
        calc = ano - cont
        anos.append(str(calc))
        cont += 1

    meses_lista = []
    mes = datetime.datetime.now().month + 1
    for i in range(12):
        mes -= 1
        if mes == 0:
            mes = 12
            ano -= 1
        meses_lista.append(meses[mes - 1])

    # Obtém uma lista de tuplas contendo o id e o nome do vendedor
    bd_vendedores = Venda.objects.values_list(
        "vendedor__id", "vendedor__username"
    ).distinct()
    vendedores = {
        id_vendedor: nome_vendedor for id_vendedor, nome_vendedor in bd_vendedores
    }

    context = {
        "vendedores": vendedores,
        "anos": anos,
        "meses": meses_lista,
        "total_mes": total_mes,
        "total_ano": total_ano,
        "vendas_ano": vendas_ano,
        "vendas_mes": vendas_mes,
        "produtos_ano": produtos_ano,
        "produtos_mes": produtos_mes,
        "mensagem_ano": mensagem_ano,
        "mensagem_mes": mensagem_mes,
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
    vendedor = request.GET.get("vendedor")
    ano = request.GET.get("ano")
    ano = int(ano)
    mes = request.GET.get("mes")

    # mensagem = "Não há lançamentos para o período!"
    mensagem_ano = mensagem_mes = ""

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

    # alterações charts ano
    # ano_label = str(ano)
    meses_lista = []

    # se ano atual, lista os últimos 12 meses
    if ano == today.year:
        mes_label = datetime.datetime.now().month + 1
        for i in range(12):
            mes_label -= 1
            if mes_label == 0:
                mes_label = 12
            meses_lista.append(meses[mes_label - 1])
    else:
        meses_lista = meses

    index = meses.index(mes)
    mes = index + 1

    if vendedor == "0":
        vendas_ano = Venda.objects.filter(data_pedido__year=ano).count()
        produtos_ano = VendaProduto.objects.filter(
            venda__data_pedido__year=ano,
        ).aggregate(Sum("quantidade"))["quantidade__sum"]
        total_ano = Venda.objects.filter(
            data_pedido__year=ano,
        ).aggregate(
            Sum("subtotal")
        )["subtotal__sum"]
    else:
        vendas_ano = Venda.objects.filter(
            vendedor__id=vendedor, data_pedido__year=ano
        ).count()
        produtos_ano = VendaProduto.objects.filter(
            venda__vendedor__id=vendedor,
            venda__data_pedido__year=ano,
        ).aggregate(Sum("quantidade"))["quantidade__sum"]
        total_ano = Venda.objects.filter(
            vendedor__id=vendedor,
            data_pedido__year=ano,
        ).aggregate(Sum("subtotal"))["subtotal__sum"]

    if not total_ano:
        total_ano = vendas_ano = produtos_ano = 0
        mensagem_ano = "Não há lançamentos para o período!"

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

    dados_ano = []
    labels_ano = meses
    mes_ano = mes + 1

    # soma subtotal por mes no ano selecionado
    vendas_por_mes = (
        Venda.objects.filter(data_pedido__year=ano)
        .annotate(mes=ExtractMonth("data_pedido"))
        .values("mes")
        .annotate(total_valor=Sum("subtotal"))
        .order_by("mes")
    )
    # print(labels_ano)
    dados_ano = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(len(vendas_por_mes)):
        dados_ano[i] = vendas_por_mes[i]["total_valor"]

    if ano == today.year:
        labels_ano = []
        mes_ano = datetime.datetime.now().month + 1
        for i in range(12):
            mes_ano -= 1
            if mes_ano == 0:
                mes_ano = 12
            labels_ano.append(meses[mes_ano - 1])

    # alterações charts mes
    if vendedor == "0":
        obj_mes = Venda.objects.filter(data_pedido__month=mes, data_pedido__year=ano)
        vendas_mes = Venda.objects.filter(
            data_pedido__month=mes, data_pedido__year=ano
        ).count()
        produtos_mes = VendaProduto.objects.filter(
            venda__data_pedido__year=ano, venda__data_pedido__month=mes
        ).aggregate(Sum("quantidade"))["quantidade__sum"]
        total_mes = Venda.objects.filter(
            data_pedido__year=ano, data_pedido__month=mes
        ).aggregate(Sum("subtotal"))["subtotal__sum"]
    else:
        obj_mes = Venda.objects.filter(
            vendedor__id=vendedor, data_pedido__month=mes, data_pedido__year=ano
        )
        vendas_mes = Venda.objects.filter(
            vendedor__id=vendedor, data_pedido__month=mes, data_pedido__year=ano
        ).count()
        produtos_mes = VendaProduto.objects.filter(
            venda__vendedor__id=vendedor,
            venda__data_pedido__year=ano,
            venda__data_pedido__month=mes,
        ).aggregate(Sum("quantidade"))["quantidade__sum"]
        total_mes = Venda.objects.filter(
            vendedor__id=vendedor, data_pedido__year=ano, data_pedido__month=mes
        ).aggregate(Sum("subtotal"))["subtotal__sum"]

    if not total_mes:
        total_mes = vendas_mes = produtos_mes = 0
        mensagem_mes = "Não há lançamentos para o período!"

    ref_dias = calendar.monthcalendar(ano, mes)

    labels_mes = []
    for i in ref_dias:
        for j in i:
            if j != 0:
                data = datetime.date(year=ano, month=mes, day=j)
                labels_mes.append(str(data))

    dados_mes = []
    for i in range(len(labels_mes)):
        soma = sum(o.subtotal for o in obj_mes if o.data_pedido.day == i + 1)
        dados_mes.append(soma)

    # print(labels_mes)
    # print(dados_mes)
    data_json = {
        "meses": meses_lista,
        "data_ano": dados_ano,
        "data_mes": dados_mes,
        "labels_ano": labels_ano,
        "labels_mes": labels_mes,
        "vendas_ano": vendas_ano,
        "vendas_mes": vendas_mes,
        "produtos_ano": produtos_ano,
        "produtos_mes": produtos_mes,
        "total_ano": total_ano,
        "total_mes": total_mes,
        "mensagem_ano": mensagem_ano,
        "mensagem_mes": mensagem_mes,
    }

    return JsonResponse(data_json)


@login_required
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


def listaConferenciaTransporteExpedicao(request, transportadora):
    template_name = "venda/listaConferenciaTransporteExpedicao.html"
    # objeto = Venda.objects.filter(transportadora__id=transportadora).exclude(
    #     data_entrega__isnull=True
    # )
    objeto = Venda.objects.filter(transportadora__id=transportadora).exclude(
        data_entrega__isnull=True
    ).filter(valor_frete__gt=0.00) | Venda.objects.filter(
        transportadora__id=transportadora
    ).exclude(
        cotacao_transportadora__isnull=True
    ).filter(
        valor_frete__gt=0.00
    )
    # objeto = Venda.objects.filter(transportadora__id=transportadora)
    transportadora = Transportadora.objects.filter(id=transportadora)
    context = {"object_list": objeto, "transportadora": transportadora}
    return render(request, template_name, context)
