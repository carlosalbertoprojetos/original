import os
from django.shortcuts import redirect
from reportlab.graphics.shapes import *
from reportlab.graphics.barcode.common import *
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Frame

import datetime

import json
import requests

from financeiro.models import ContaReceber

date = datetime.datetime.now().strftime("%d/%m/%Y")

# Constantes
# Formulário
FONTE_FORM = "Helvetica"
FONTE_FORM_TAM = 6

FONTE_FORM_TAM_ID = 10

FONTE_DADOS = "Times-Roman"
FONTE_DADOS_TAM = 10


def gerarToken():
    pass
    """Gera o token"""
    # client_id = "c4c6b6b6-dbba-41db-96b0-f23bd0a363f3"
    # client_secret = "8183c235-61a0-470a-8584-aa2ccbca2dab"
    # client = {"client_id": client_id, "client_secret": client_secret}
    # url = "https://devportal.itau.com.br/api/jwt"
    # headers = {"content-Type": "application/json"}
    # request_token = requests.post(
    #     url,
    #     client,
    #     headers,
    # )
    # token = request_token.json()
    # headers = {"x-sandbox-token": token["access_token"]}
    # return token


def formboleto(bd_boleto):
    """cria arquivo no formato de boleto em pdf"""
    boleto_nome = f"{bd_boleto['nome_arquivo_boleto']}"
    boleto = Canvas(f"media/financeiro/boletos/{boleto_nome}.pdf")
    logo = os.path.join("./integracoes/banco/Itau/boleto/logo_itau.jpg")

    valor = f"R$ {bd_boleto['valor']}"
    endereco_pagador = f'{bd_boleto["dado_boleto"]["pagador"]["endereco"]["nome_logradouro"]}, {bd_boleto["dado_boleto"]["pagador"]["endereco"]["nome_bairro"]}, {bd_boleto["dado_boleto"]["pagador"]["endereco"]["nome_cidade"]}, {bd_boleto["dado_boleto"]["pagador"]["endereco"]["sigla_UF"]}, {bd_boleto["dado_boleto"]["pagador"]["endereco"]["numero_CEP"]}'
    num_documento = bd_boleto["dado_boleto"]["dados_individuais_boleto"][0][
        "numero_documento"
    ][0]

    e = bd_boleto["dado_boleto"]["data_emissao"]
    emissao = f"{e[8:10]}/{e[5:7]}/{e[0:4]}"
    v = bd_boleto["dado_boleto"]["dados_individuais_boleto"][0]["data_vencimento"]
    vencimento = f"{v[8:10]}/{v[5:7]}/{v[0:4]}"

    blie = bd_boleto["base_linha_digitavel"]
    # bd = bd_boleto["base_dac"]
    # linha_digitavel = f"{blie[0:5]}.{blie[5:9]} {bd[0]} {blie[9:14]}.{blie[14:19]} {bd[1]} {blie[19:24]}.{blie[24:29]} {bd[2]} {blie[29:30]} {blie[30:47]}"

    linha_digitavel = f"{blie[0:5]}.{blie[5:9]} {blie[9:14]}.{blie[14:19]} {blie[19:24]}.{blie[24:29]} {blie[29:30]} {blie[30:47]}"

    boleto.drawImage(
        image=logo,
        x=7 * mm,
        y=280 * mm,
        width=30 * mm,
        height=7 * mm,
    )

    # imagem do recido do sacado
    boleto.drawImage(
        image=logo,
        x=7 * mm,
        y=229 * mm,
        width=30 * mm,
        height=7 * mm,
    )

    # imagem do banco na ficha de compensação
    boleto.drawImage(
        image=logo,
        x=7 * mm,
        y=112 * mm,
        width=30 * mm,
        height=7 * mm,
    )

    boleto.setStrokeColor(colors.black)
    boleto.setLineWidth(0.1)
    boleto.setFont("Helvetica-Bold", 14)
    global localpagamento, usobanco, impressora
    localpagamento = (
        "Pague pelo aplicativo, internet ou em agências e correspondentes do "
    )
    usobanco = ""

    # codigo do banco
    boleto.drawString(43 * mm, 229 * mm, bd_boleto["num_banco"])
    boleto.drawString(43 * mm, 112 * mm, bd_boleto["num_banco"])
    localpagamento += str(bd_boleto["nome_banco_destinatario"])

    # telefone da empresa
    boleto.setFont("Helvetica-Bold", 12)
    boleto.drawString(
        7 * mm, 275 * mm, bd_boleto["dado_boleto"]["pagador"]["telefone_empresa"]
    )

    # Recibo do sacado
    # retícula com cinza (Vencimento)
    boleto.setFillColor(colors.lightgrey)
    boleto.setStrokeColor(colors.white)
    boleto.rect(158 * mm, 220 * mm, 42 * mm, 8 * mm, stroke=1, fill=1)
    # retícula com cinza (Valor do documento)
    boleto.rect(158 * mm, 196 * mm, 42 * mm, 8 * mm, stroke=1, fill=1)

    # Ficha de compensação
    # retícula com cinza (Vencimento)
    boleto.setFillColor(colors.lightgrey)
    boleto.setStrokeColor(colors.lightgrey)
    boleto.rect(158 * mm, 103 * mm, 42 * mm, 8 * mm, stroke=1, fill=1)
    # retícula com cinza (Valor do documento)
    boleto.rect(158 * mm, 79 * mm, 42 * mm, 8 * mm, stroke=1, fill=1)

    boleto.setStrokeColor(colors.black)
    boleto.setFillColor(colors.black)

    # Recibo de entrega
    boleto.setFont(FONTE_FORM, FONTE_FORM_TAM)
    boleto.drawString(7 * mm, 270 * mm, "Sacado:")
    boleto.drawString(7 * mm, 266 * mm, "Endereço:")
    boleto.drawString(7 * mm, 258 * mm, "Documento:")
    boleto.drawString(7 * mm, 254 * mm, "Emissão:")
    boleto.drawString(7 * mm, 250 * mm, "Data:")
    boleto.drawString(80 * mm, 258 * mm, "Valor:")
    boleto.drawString(80 * mm, 254 * mm, "Vencimento:")
    boleto.drawString(80 * mm, 250 * mm, "Assinatura: _______________________________")

    boleto.drawString(7 * mm, 217 * mm, "Data do documento")
    boleto.drawString(41 * mm, 217 * mm, "No. do documento")
    boleto.drawString(71 * mm, 217 * mm, "Espécie doc")
    boleto.drawString(91 * mm, 217 * mm, "Aceite")
    boleto.drawString(114 * mm, 217 * mm, "Data do processamento")
    boleto.drawString(160 * mm, 217 * mm, "Agência/Código do cedente")
    boleto.drawString(7 * mm, 209 * mm, "Uso do banco")
    boleto.drawString(7 * mm, 225 * mm, "Cedente")
    boleto.drawString(160 * mm, 225 * mm, "Vencimento")
    boleto.drawString(41 * mm, 209 * mm, "Carteira")
    boleto.drawString(56 * mm, 209 * mm, "Espécie")
    boleto.drawString(71 * mm, 209 * mm, "Quantidade")
    boleto.drawString(71 * mm, 205 * mm, "")
    boleto.drawString(123 * mm, 206 * mm, "x")
    boleto.drawString(124 * mm, 209 * mm, "Valor")
    boleto.drawString(124 * mm, 205 * mm, "")
    boleto.drawString(160 * mm, 209 * mm, "Nosso número")
    boleto.drawString(160 * mm, 201 * mm, "(=) Valor do documento")
    boleto.drawString(160 * mm, 193 * mm, "(-) Desconto/Abatimento")
    boleto.drawString(160 * mm, 185 * mm, "(-) Outras deduções")
    boleto.drawString(160 * mm, 177 * mm, "(+) Mora/Multa")
    boleto.drawString(160 * mm, 169 * mm, "(+) Outros acréscimos")
    boleto.drawString(160 * mm, 161 * mm, "(=) Valor cobrado")
    boleto.drawString(7 * mm, 154 * mm, "Sacado")
    boleto.drawString(7 * mm, 140 * mm, "Sacador/avalista")
    boleto.drawString(135 * mm, 140 * mm, "Código de baixa")
    boleto.drawString(161 * mm, 134 * mm, "Autenticação mecânica")

    boleto.setFont("Helvetica-Bold", 14)
    boleto.drawString(
        58 * mm,
        229 * mm,
        linha_digitavel,
    )

    boleto.setFont(FONTE_DADOS, FONTE_DADOS_TAM)
    boleto.drawString(
        20 * mm,
        270 * mm,
        bd_boleto["dado_boleto"]["pagador"]["pessoa"]["nome_pessoa"],
    )
    boleto.drawString(20 * mm, 266 * mm, endereco_pagador)
    # boleto.drawString(20 * mm, 262 * mm, endereco_pagador)
    boleto.drawString(20 * mm, 258 * mm, num_documento)
    boleto.drawString(20 * mm, 254 * mm, emissao)
    boleto.drawString(20 * mm, 250 * mm, date)
    boleto.drawString(96 * mm, 258 * mm, valor)
    boleto.drawString(
        96 * mm,
        254 * mm,
        vencimento,
    )
    boleto.drawString(7 * mm, 221 * mm, bd_boleto["beneficiario"]["nome_cobranca"])
    boleto.drawString(
        180 * mm,
        221 * mm,
        vencimento,
    )
    boleto.drawString(7 * mm, 213 * mm, emissao)
    boleto.drawString(41 * mm, 213 * mm, num_documento)
    boleto.drawString(71 * mm, 213 * mm, "ESP DOC")
    boleto.drawString(91 * mm, 213 * mm, "ACEITE")
    boleto.drawString(114 * mm, 213 * mm, emissao)
    boleto.drawString(160 * mm, 213 * mm, bd_boleto["beneficiario"]["dados_agencia"])
    boleto.drawString(7 * mm, 205 * mm, usobanco)
    boleto.drawString(41 * mm, 205 * mm, bd_boleto["dado_boleto"]["codigo_carteira"])
    boleto.drawString(56 * mm, 205 * mm, "R$")
    boleto.drawString(160 * mm, 189 * mm, "")
    boleto.drawString(
        160 * mm,
        205 * mm,
        bd_boleto["dado_boleto"]["dados_individuais_boleto"][0]["numero_nosso_numero"],
    )
    boleto.drawString(177 * mm, 197 * mm, valor)
    boleto.drawString(20 * mm, 185 * mm, bd_boleto["juros"])
    boleto.drawString(160 * mm, 181 * mm, "")
    boleto.drawString(20 * mm, 177 * mm, bd_boleto["observacao1"])
    boleto.drawString(20 * mm, 171 * mm, bd_boleto["observacao2"])
    boleto.drawString(20 * mm, 164 * mm, bd_boleto["observacao3"])
    boleto.drawString(160 * mm, 173 * mm, "")
    boleto.drawString(160 * mm, 165 * mm, "")
    boleto.drawString(160 * mm, 157 * mm, "")
    boleto.drawString(
        7 * mm,
        151 * mm,
        bd_boleto["dado_boleto"]["pagador"]["pessoa"]["nome_pessoa"],
    )
    boleto.drawString(7 * mm, 147 * mm, endereco_pagador)

    # linha dividindo o canhoto
    boleto.setStrokeColor(colors.gray)
    boleto.line(0, 240 * mm, 210 * mm, 240 * mm)
    # linha dividindo o recibo do sacado e ficha de compensação
    boleto.line(0, 122 * mm, 210 * mm, 122 * mm)

    boleto.setStrokeColor(colors.black)
    boleto.setFillColor(colors.black)

    # abaixo da logo do banco
    boleto.line(7 * mm, 228 * mm, 200 * mm, 228 * mm)
    # separadores cedente, data do documento e uso do banco
    boleto.line(7 * mm, 220 * mm, 200 * mm, 220 * mm)
    boleto.line(7 * mm, 212 * mm, 200 * mm, 212 * mm)
    boleto.line(7 * mm, 204 * mm, 200 * mm, 204 * mm)
    # separador do número do banco
    boleto.line(42 * mm, 228 * mm, 42 * mm, 234 * mm)
    boleto.line(56 * mm, 228 * mm, 56 * mm, 234 * mm)
    # separador coluna cedente e vencimento
    boleto.line(158 * mm, 228 * mm, 158 * mm, 156 * mm)
    # separadores do bloco acima
    boleto.line(40 * mm, 204 * mm, 40 * mm, 220 * mm)
    boleto.line(55 * mm, 204 * mm, 55 * mm, 212 * mm)
    boleto.line(70 * mm, 204 * mm, 70 * mm, 220 * mm)
    boleto.line(90 * mm, 212 * mm, 90 * mm, 220 * mm)
    boleto.line(113 * mm, 212 * mm, 113 * mm, 220 * mm)
    boleto.line(123 * mm, 204 * mm, 123 * mm, 212 * mm)

    # separador em branco da quantidade e valor
    boleto.setStrokeColor(colors.white)
    boleto.line(123 * mm, 205 * mm, 123 * mm, 208 * mm)
    boleto.setStrokeColor(colors.black)

    boleto.line(158 * mm, 196 * mm, 200 * mm, 196 * mm)
    boleto.line(158 * mm, 188 * mm, 200 * mm, 188 * mm)
    boleto.line(158 * mm, 180 * mm, 200 * mm, 180 * mm)
    boleto.line(158 * mm, 172 * mm, 200 * mm, 172 * mm)
    boleto.line(158 * mm, 164 * mm, 200 * mm, 164 * mm)
    boleto.line(7 * mm, 156 * mm, 200 * mm, 156 * mm)

    # Divisor Recibo sacado e autenticação mecânica
    boleto.line(7 * mm, 139 * mm, 200 * mm, 139 * mm)
    boleto.line(144 * mm, 126 * mm, 144 * mm, 133 * mm)
    boleto.line(144 * mm, 133 * mm, 200 * mm, 133 * mm)
    boleto.line(200 * mm, 126 * mm, 200 * mm, 133 * mm)

    # Ficha de compensação
    boleto.setFont(FONTE_FORM, FONTE_FORM_TAM)
    boleto.drawString(7 * mm, 108 * mm, "Local de pagamento")
    boleto.drawString(160 * mm, 108 * mm, "Vencimento")
    boleto.drawString(7 * mm, 100 * mm, "Cedente")
    boleto.drawString(7 * mm, 92 * mm, "Data do documento")
    boleto.drawString(41 * mm, 92 * mm, "No. do documento")
    boleto.drawString(71 * mm, 92 * mm, "Espécie doc")
    boleto.drawString(91 * mm, 92 * mm, "Aceite")
    boleto.drawString(114 * mm, 92 * mm, "Data do processamento")
    boleto.drawString(160 * mm, 100 * mm, "Agência/Código do cedente")
    boleto.drawString(7 * mm, 84 * mm, "Uso do banco")
    boleto.drawString(41 * mm, 84 * mm, "Carteira")
    boleto.drawString(56 * mm, 84 * mm, "Espécie")
    boleto.drawString(71 * mm, 84 * mm, "Quantidade")
    boleto.drawString(123 * mm, 81 * mm, "x")
    boleto.drawString(124 * mm, 84 * mm, "Valor")
    boleto.drawString(160 * mm, 92 * mm, "Nosso número")
    boleto.drawString(160 * mm, 84 * mm, "(=) Valor do documento")
    boleto.drawString(160 * mm, 76 * mm, "(-) Desconto/Abatimento")
    boleto.drawString(160 * mm, 68 * mm, "(-) Outras deduções")
    boleto.drawString(160 * mm, 60 * mm, "(+) Mora/Multa")
    boleto.drawString(160 * mm, 52 * mm, "(+) Outros acréscimos")
    boleto.drawString(160 * mm, 44 * mm, "(=) Valor cobrado")
    boleto.drawString(7 * mm, 36 * mm, "Sacado")
    boleto.drawString(7 * mm, 23 * mm, "Sacador/avalista")
    boleto.drawString(135 * mm, 23 * mm, "Código de baixa")
    boleto.drawString(161 * mm, 20 * mm, "Autenticação mecânica")

    boleto.setFont("Helvetica-Bold", 14)
    boleto.drawString(
        58 * mm,
        112 * mm,
        linha_digitavel,
    )

    boleto.setFont(FONTE_DADOS, FONTE_DADOS_TAM)
    boleto.drawString(7 * mm, 104 * mm, localpagamento)
    boleto.drawString(
        180 * mm,
        104 * mm,
        vencimento,
    )
    boleto.drawString(7 * mm, 96 * mm, bd_boleto["beneficiario"]["nome_cobranca"])
    boleto.drawString(7 * mm, 88 * mm, emissao)
    boleto.drawString(41 * mm, 88 * mm, num_documento)
    boleto.drawString(71 * mm, 88 * mm, "ESP DOC")
    boleto.drawString(91 * mm, 88 * mm, "ACEITE")
    boleto.drawString(114 * mm, 88 * mm, emissao)
    boleto.drawString(160 * mm, 96 * mm, bd_boleto["beneficiario"]["dados_agencia"])
    boleto.drawString(7 * mm, 80 * mm, usobanco)
    boleto.drawString(41 * mm, 80 * mm, bd_boleto["dado_boleto"]["codigo_carteira"])
    boleto.drawString(56 * mm, 80 * mm, "R$")
    boleto.drawString(71 * mm, 80 * mm, "")
    boleto.drawString(124 * mm, 80 * mm, "")
    boleto.drawString(
        160 * mm,
        88 * mm,
        bd_boleto["dado_boleto"]["dados_individuais_boleto"][0]["numero_nosso_numero"],
    )
    boleto.drawString(177 * mm, 80 * mm, valor)
    boleto.drawString(160 * mm, 72 * mm, "")
    boleto.drawString(20 * mm, 60 * mm, bd_boleto["juros"])
    boleto.drawString(20 * mm, 54 * mm, bd_boleto["observacao1"])
    boleto.drawString(20 * mm, 48 * mm, bd_boleto["observacao2"])
    boleto.drawString(20 * mm, 41 * mm, bd_boleto["observacao3"])
    boleto.drawString(160 * mm, 56 * mm, "")
    boleto.drawString(160 * mm, 48 * mm, "")
    boleto.drawString(160 * mm, 40 * mm, "")
    boleto.drawString(160 * mm, 32 * mm, "")
    boleto.drawString(
        7 * mm,
        33 * mm,
        bd_boleto["dado_boleto"]["pagador"]["pessoa"]["nome_pessoa"],
    )
    boleto.drawString(7 * mm, 29 * mm, endereco_pagador)

    # Identificação das partes
    boleto.setFont(FONTE_FORM, FONTE_FORM_TAM_ID)
    boleto.drawString(165 * mm, 140 * mm, "Recibo do sacado")
    boleto.drawString(163 * mm, 23 * mm, "Ficha de compensação")
    boleto.setFont(FONTE_FORM, FONTE_FORM_TAM)

    # abaixo da logo do banco
    boleto.line(7 * mm, 111 * mm, 200 * mm, 111 * mm)
    # separador do número do banco
    boleto.line(42 * mm, 111 * mm, 42 * mm, 116 * mm)
    boleto.line(56 * mm, 111 * mm, 56 * mm, 116 * mm)
    # separador coluna local de pagamento e vencimento
    boleto.line(158 * mm, 39 * mm, 158 * mm, 111 * mm)
    # separadores local de pagamento, cedente, data do documento e uso do banco
    boleto.line(7 * mm, 103 * mm, 200 * mm, 103 * mm)
    boleto.line(7 * mm, 95 * mm, 200 * mm, 95 * mm)
    boleto.line(7 * mm, 87 * mm, 200 * mm, 87 * mm)
    boleto.line(7 * mm, 79 * mm, 200 * mm, 79 * mm)
    # separadores do bloco acima
    boleto.line(40 * mm, 79 * mm, 40 * mm, 95 * mm)
    boleto.line(55 * mm, 79 * mm, 55 * mm, 87 * mm)
    boleto.line(70 * mm, 79 * mm, 70 * mm, 95 * mm)
    boleto.line(90 * mm, 87 * mm, 90 * mm, 95 * mm)
    boleto.line(113 * mm, 87 * mm, 113 * mm, 95 * mm)
    boleto.line(123 * mm, 79 * mm, 123 * mm, 87 * mm)

    # separador em branco da quantidade e valor
    boleto.setStrokeColor(colors.white)
    boleto.line(123 * mm, 80 * mm, 123 * mm, 83 * mm)
    boleto.setStrokeColor(colors.black)

    # separadora valor documento, desconto abatimento
    boleto.line(158 * mm, 71 * mm, 200 * mm, 71 * mm)
    boleto.line(158 * mm, 63 * mm, 200 * mm, 63 * mm)
    boleto.line(158 * mm, 55 * mm, 200 * mm, 55 * mm)

    boleto.setLineWidth(0.2)
    boleto.line(158 * mm, 47 * mm, 200 * mm, 47 * mm)
    boleto.line(7 * mm, 39 * mm, 200 * mm, 39 * mm)

    # Divisor Ficha de compensação e autenticação mecânica
    boleto.setLineWidth(0.1)
    boleto.line(7 * mm, 22 * mm, 200 * mm, 22 * mm)

    boleto.line(144 * mm, 12 * mm, 144 * mm, 19 * mm)
    boleto.line(144 * mm, 19 * mm, 200 * mm, 19 * mm)
    boleto.line(200 * mm, 12 * mm, 200 * mm, 19 * mm)

    f = Frame(mm, mm, 5 * mm, 20 * mm, showBoundary=0)
    f.addFromList(
        [
            I2of5(
                linha_digitavel,
                xdim=0.3 * mm,
                checksum=0,
                bearers=0,
            )
        ],
        boleto,
    )

    boleto.save()
    os.startfile(
        # base
        # f"media/financeiro/boletos/itau/{boleto_nome}.pdf"
        f"C:/PROJETOS/TRABALHOS/INTIP/ERP/erp/project/media/financeiro/boletos/{boleto_nome}.pdf"
    )
    # return redirect(f"/venda/{bd_boleto['venda']}/editar")


def emitirBoleto(bd_boleto):
    token = gerarToken()
    url = "https://devportal.itau.com.br/sandboxapi/itau-ep9-gtw-cash-management-ext-v2/v2/boletos"
    headers = {
        "Content-Type": "application/json",
        "x-sandbox-token": token,
        "x-itau-apikey": "82e96e5c-7132-3add-8a6f-5dbd9d60d500",
    }
    response = requests.post("https://httpbin.org/post", data=bd_boleto)
    exibirBoleto(bd_boleto["parcela"])
    return response


def exibirBoleto(exibir_parcela):
    venda = exibir_parcela[0]
    parcela = exibir_parcela[1]
    parcela_qs = ContaReceber.objects.filter(venda__id=venda)
    id_parcela = []
    for p in parcela_qs:
        if p.parcela == parcela:
            id_parcela = p.id
    dados_gerais = ContaReceber.objects.filter(id=id_parcela)

    for dg in dados_gerais:
        dump = json.loads(dg.dados_boleto)

    formboleto(dump)
    return redirect(f"/venda/{venda}/editar")


def deletarBoleto(deletar_parcela):
    sep_venda_parcela = deletar_parcela.split(",")
    venda = sep_venda_parcela[0]
    parcela = sep_venda_parcela[1]
    parcela_qs = ContaReceber.objects.filter(venda__id=venda)
    id_parcela = []
    for p in parcela_qs:
        if p.parcela == parcela:
            id_parcela = p.id
    dados_gerais = ContaReceber.objects.filter(id=id_parcela)
    for dg in dados_gerais:
        dg.dados_boleto = {}
        dg.save()
    return redirect(f"/venda/{venda}/editar")



