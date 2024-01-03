from datetime import date, datetime
from django.shortcuts import redirect, render
from django.urls import reverse_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.views.generic import ListView
from django.views.generic.edit import DeleteView
import xmltodict
from django.core.files.storage import FileSystemStorage
import os

from notafiscal.models import NFCompra, NFItem
from fornecedor.models import Fornecedor
from materiaprima.models import MateriaPrimaFornecedor
from materiaprima.forms import MPFForm

from integracoes.integracaonf import descompacta_dados_listagem_nota

data_atual = date.today()

success_url_nfcompra = _("notafiscal:nfcompraList")
template_name_baixar_nf = "notafiscal/nfcompraDetails.html"


class NFCompraList(LoginRequiredMixin, ListView):
    model = NFCompra
    template_name = "notafiscal/nfcompraList.html"


nfcompraList = NFCompraList.as_view()


class NFCompraDelete(LoginRequiredMixin, DeleteView):
    model = NFCompra
    template_name = "notafiscal/nfcompraDelete.html"
    success_url = success_url_nfcompra


nfcompraDelete = NFCompraDelete.as_view()


@login_required
def notafiscal_list(request):
    template_name = "notafiscal/notafiscalList.html"
    baixadas = NFCompra.objects.all()

    ob = []
    for nota in descompacta_dados_listagem_nota():
        nf = {}
        for nk, nv in nota.items():
            nf.update({nk: nv})
            if nk == "dhEmi":
                datenf = nv[:10]
                date = datetime.strptime(datenf, "%Y-%m-%d").date()
                nf.update({nk: date})
        ob.append(nf)

    # lista de chaves já baixadas
    chaves = []
    for i in baixadas:
        chaves.append(i.chavedeacesso)

    # criar lista das notas a serem baixadas
    object_list = []
    for ol in ob:
        if ol["chNFe"] != chaves:
            object_list.append(ol)
    context = {"object_list": object_list}
    return render(request, template_name, context)


# verifica se os dados baixados do xml estão completos
def check_xml(request, chave):
    try:
        from integracoes.transf import xml

        # verifica se os dados baixados da sefaz contém os produtos
        for i in xml.values():
            op = 1
            return baixar_notafiscal(request, chave, op)
    except:
        # verifica se já existe o arquivo xml na pasta media
        key = f"{chave}.xml"
        arquivos = os.listdir("media/")
        if not key in arquivos:
            return baixar_xml(request, chave)
        else:
            op = 2
            return baixar_notafiscal(request, chave, op)


def baixar_xml(request, chave):
    show_modal = True
    if request.method == "POST" and request.FILES["filexml"]:
        myfile = request.FILES.get("filexml")
        fs = FileSystemStorage()
        fs.save(myfile.name, myfile)
        return redirect("notafiscal:notafiscalList")

    context = {"chave": chave, "show_modal": show_modal}

    return render(request, "notafiscal/notafiscalList.html", context)


@login_required
def baixar_notafiscal(request, chave, op):
    xml = []
    if op == 1:
        # xml = retorna_dados_nota(chave)
        from integracoes.transf import xml
    elif op == 2:
        caminho = f"media\\{chave}.xml"
        with open(caminho, "r", encoding="utf-8") as file:
            dict = file.read()
            xml = xmltodict.parse(dict)

    a = {}
    protNFe = {}

    for i in xml.values():
        a = i["NFe"]
        protNFe = i["protNFe"]

    b = a["infNFe"]

    fornecedor = b["emit"]["xNome"]
    cnpj_fornecedor = b["emit"]["CNPJ"]
    ie_fornecedor = b["emit"]["IE"]
    logradouro_forn = b["emit"]["enderEmit"]["xLgr"]
    num_end_fornecedor = b["emit"]["enderEmit"]["nro"]
    comp_end_fornecedor = 0
    # comp_end_fornecedor = b['emit']['enderEmit']['xCpl']
    bairro_fornecedor = b["emit"]["enderEmit"]["xBairro"]
    cidade_fornecedor = b["emit"]["enderEmit"]["xMun"]
    uf_fornecedor = b["emit"]["enderEmit"]["UF"]
    cep_fornecedor = b["emit"]["enderEmit"]["CEP"]
    chavedeacesso = protNFe["infProt"]["chNFe"]
    naturezadaoperacao = b["ide"]["natOp"]
    numeroserie = b["ide"]["serie"]
    protocoloautorizacaodeuso = protNFe["infProt"]["nProt"]
    nome_destinatario = b["dest"]["xNome"]
    cnpj_destinatario = b["dest"]["CNPJ"]
    logradouro_dest = b["dest"]["enderDest"]["xLgr"]
    num_end_destinatario = b["dest"]["enderDest"]["nro"]
    bairro_destinatario = b["dest"]["enderDest"]["xBairro"]
    cidade_destinatario = b["dest"]["enderDest"]["xMun"]
    uf_destinatario = b["dest"]["enderDest"]["UF"]
    cep_destinatario = b["dest"]["enderDest"]["CEP"]
    nota_fiscal = b["ide"]["cNF"]
    data_emissao = date.fromisoformat(b["ide"]["dhEmi"][:10])
    forma_pagamento = b["pag"]["detPag"]["tPag"]
    base_calculo_icms = b["total"]["ICMSTot"]["vBC"]
    valor_icms = b["total"]["ICMSTot"]["vICMS"]
    valor_pis = b["total"]["ICMSTot"]["vPIS"]
    valor_total_produtos = b["total"]["ICMSTot"]["vProd"]
    valor_do_frete = b["total"]["ICMSTot"]["vFrete"]
    valor_do_seguro = b["total"]["ICMSTot"]["vSeg"]
    desconto = b["total"]["ICMSTot"]["vDesc"]
    outras_despesas = b["total"]["ICMSTot"]["vOutro"]
    valor_total_ipi = b["total"]["ICMSTot"]["vIPI"]
    valor_da_cofins = b["total"]["ICMSTot"]["vCOFINS"]
    valor_total_da_nota = b["total"]["ICMSTot"]["vNF"]

    produtos = b["det"]

    dataemissao = data_emissao.strftime("%d/%m/%Y")

    # listar informações da nf para o destinatário para a invoice
    list = ["CNPJ", "xNome", "xLgr", "nro", "xBairro", "xMun", "UF"]
    tab = b["dest"]

    bddest = {}
    for key, i in tab.items():
        if key in list:
            bddest.update({key: i})
    for key, i in tab["enderDest"].items():
        if key in list:
            bddest.update({key: i})
    bddest.update({"total": valor_total_da_nota})
    bddest.update({"natop": naturezadaoperacao})
    bddest.update({"serie": numeroserie})
    bddest.update({"chave": chavedeacesso})
    bddest.update({"autuso": protocoloautorizacaodeuso})
    bddest.update({"forpgto": forma_pagamento})
    bddest.update({"bcicms": base_calculo_icms})
    bddest.update({"vlricms": valor_icms})
    bddest.update({"vlrpis": valor_pis})
    bddest.update({"vlrfrete": valor_do_frete})
    bddest.update({"vlrseguro": valor_do_seguro})
    bddest.update({"subtotal": ""})
    bddest.update({"desconto": desconto})
    bddest.update({"odespesas": outras_despesas})
    bddest.update({"vlripi": valor_total_ipi})
    bddest.update({"vlrcofins": valor_da_cofins})

    dest = []
    dest.append(bddest)

    # cadastra fornecedor, caso o CNPJ não esteja cadastrado
    queryForn = Fornecedor.objects.filter(cnpj=cnpj_fornecedor)
    if not queryForn:
        Fornecedor.objects.create(
            nome=fornecedor,
            cnpj=cnpj_fornecedor,
            insc_estadual=ie_fornecedor,
            logradouro=logradouro_forn,
            numero=num_end_fornecedor,
            complemento=comp_end_fornecedor,
            cep=cep_fornecedor,
            estado=uf_fornecedor,
            cidade=cidade_destinatario,
        )

    id_forn = Fornecedor.objects.get(cnpj=cnpj_fornecedor)

    # lista códigos dos produtos do cnpj do xml
    matprimas = MateriaPrimaFornecedor.objects.filter(fornecedor__id=id_forn.id)

    # lista os codigos dos produtos em MateriaPrimaFornecedor
    codigosmatpri = []
    for i in matprimas:
        codigosmatpri.append(i.codigoproduto)

    # lista items/produtos do xml
    items = []

    # consultar se o código do produto existe
    initial = []

    # abre modal para cadastrar itens/produtos do xml quando não cadastrados em MateriaPrimaFornecedor
    show_modal = False

    # abre modal para cadastrar estoque
    show_modal_estoque = False

    # salva em NFItem os produtos do xml
    b_calc_imcs = 0
    valor_icms = 0
    valor_ipi = 0
    aliq_icms = 0
    aliq_ipi = 0

    esp = [f"{type(produtos)}"]
    var = ["<class 'dict'>"]
    if esp == var:
        produtos = [produtos]
    itensxml = []

    for prod in produtos:
        codigo_produto = prod["prod"]["cProd"]
        itensxml.append(codigo_produto)
        materiaprima = prod["prod"]["xProd"]
        un = prod["prod"]["uCom"]
        quantidade = prod["prod"]["qCom"][:-2]

        items.append(
            {
                "materiaprima": materiaprima,
                "codigo_produto": codigo_produto,
                "un": un,
                "quantidade": quantidade,
                "valor_unitario": prod["prod"]["vUnCom"],
                "ncm": prod["prod"]["NCM"],
                "cfop": prod["prod"]["CFOP"],
            }
        )

        if not codigo_produto in codigosmatpri:
            show_modal = True
            initial.append(
                {
                    "fornecedor": id_forn,
                    "codigoproduto": codigo_produto,
                    "nome": materiaprima,
                }
            )

    formset = formset_factory(MPFForm, extra=0)
    form = formset(initial=initial)

    context = {
        "data_emissao": dataemissao,
        "num_nf": nota_fiscal,
        "fornec": queryForn,
        "dest": dest,
        "items": items,
        "show_modal": show_modal,
        "formset": form,
    }

    if request.method == "POST":
        form = formset(request.POST or None, initial=initial)
        if form.is_valid():
            for form in form:
                form.save()
            return redirect("notafiscal:checkXml", chave=chave)

    elif request.method == "GET":
        # verifica se há itens do xml não cadastrados em MateriaPrimaFornecedor
        for i in itensxml:
            if i in codigosmatpri:
                # verifica se a nota fiscal está cadastrada, se não, cadastra
                nfsalva = NFCompra.objects.filter(chavedeacesso=chavedeacesso)
                if not nfsalva.exists():
                    NFCompra.objects.create(
                        fornecedor=id_forn,
                        chavedeacesso=chavedeacesso,
                        naturezadaoperacao=naturezadaoperacao,
                        numeroserie=numeroserie,
                        protocoloautorizacaodeuso=protocoloautorizacaodeuso,
                        nome_destinatario=nome_destinatario,
                        cnpj_destinatario=cnpj_destinatario,
                        bairro_destinatario=bairro_destinatario,
                        cep_destinatario=cep_destinatario,
                        data_emissao=data_emissao,
                        forma_pagamento=forma_pagamento,
                        base_calculo_icms=base_calculo_icms,
                        valor_icms=valor_icms,
                        valor_pis=valor_pis,
                        valor_total_produtos=valor_total_produtos,
                        valor_do_frete=valor_do_frete,
                        valor_do_seguro=valor_do_seguro,
                        desconto=desconto,
                        outras_despesas=outras_despesas,
                        valor_total_ipi=valor_total_ipi,
                        valor_da_cofins=valor_da_cofins,
                        valor_total_da_nota=valor_total_da_nota,
                    )

                # salva os itens da nota fiscal
                id_nfcomp = NFCompra.objects.get(chavedeacesso=chavedeacesso)
                for prod in produtos:
                    codigo_produto = prod["prod"]["cProd"]
                    coditem = NFItem.objects.filter(codigo_produto=codigo_produto)
                    if not coditem.exists():
                        try:
                            if prod["imposto"]["ICMS"]["ICMS00"]:
                                try:
                                    if prod["imposto"]["ICMS"]["ICMS00"]["vBC"]:
                                        b_calc_imcs = produtos["imposto"]["ICMS"][
                                            "ICMS00"
                                        ]["vBC"]
                                        aliq_icms = prod["imposto"]["ICMS"]["ICMS00"][
                                            "pICMS"
                                        ]
                                        valor_icms = prod["imposto"]["ICMS"]["ICMS00"][
                                            "vICMS"
                                        ]
                                except:
                                    pass
                                try:
                                    if prod["imposto"]["IPI"]["IPITrib"]["vIPI"]:
                                        aliq_ipi = prod["imposto"]["IPI"]["IPITrib"][
                                            "pIPI"
                                        ]
                                        valor_ipi = prod["imposto"]["IPI"]["IPITrib"][
                                            "vIPI"
                                        ]
                                except:
                                    pass
                        except:
                            pass

                        NFItem.objects.create(
                            codigo_produto=codigo_produto,
                            materiaprima=prod["prod"]["xProd"],
                            un=prod["prod"]["uCom"],
                            quantidade=prod["prod"]["qCom"][:-2],
                            valor_unitario=prod["prod"]["vUnCom"],
                            notafiscal=id_nfcomp,
                            descricao="0",
                            ncm_sh=prod["prod"]["NCM"],
                            o_csqn="0",
                            cfop=prod["prod"]["CFOP"],
                            valor_total=prod["prod"]["vProd"],
                            valor_desconto="0",
                            b_calc_imcs=b_calc_imcs,
                            valor_icms=valor_icms,
                            valor_ipi=valor_ipi,
                            aliq_icms=aliq_icms,
                            aliq_ipi=aliq_ipi,
                        )

    return render(request, template_name_baixar_nf, context)
