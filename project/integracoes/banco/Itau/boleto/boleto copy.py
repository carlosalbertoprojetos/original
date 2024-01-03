import os
import json
from django.http import HttpResponseRedirect
from PIL import Image
import PIL.Image
from django.shortcuts import redirect

from reportlab.graphics.shapes import *

from reportlab.graphics.barcode.common import *
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4

from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Frame

# from gerarboleto import geraboleto
import unittest
import requests

# from extensoreal import real_por_extenso
from num2words import num2words

import datetime

# time = datetime.datetime.now()
date = datetime.datetime.now().strftime("%d/%m/%Y")


def geraboleto():
    """Gera o token"""
    client_id = "82e96e5c-7132-3add-8a6f-5dbd9d60d500"
    client_secret = "8183c235-61a0-470a-8584-aa2ccbca2dab"
    client = {"client_id": client_id, "client_secret": client_secret}
    url = "https://devportal.itau.com.br/api/jwt"
    headers = {"content-Type": "application/json"}
    request_token = requests.post(
        url,
        client,
        headers,
    )
    token = request_token.json()
    headers = {"x-sandbox-token": token["access_token"]}

    """ Gera os dados do boleto """
    boleto_data = requests.get(
        "https://devportal.itau.com.br/sandboxapi/itau-ep9-gtw-cash-management-ext-v2/v2/boletos?id_beneficiario=150000052061",
        headers=headers,
    )

    # print(boleto_data.text)
    return boleto_data.text


def real_por_extenso(number_p):
    if number_p.find(",") != -1:
        number_p = number_p.split(",")
        number_p1 = int(number_p[0].replace(".", ""))
        number_p2 = int(number_p[1])
    else:
        number_p1 = int(number_p.replace(".", ""))
        number_p2 = 0

    if number_p1 == 1:
        aux1 = " real"
    else:
        aux1 = " reais"

    if number_p2 == 1:
        aux2 = " centavo"
    else:
        aux2 = " centavos"

    text1 = ""
    if number_p1 > 0:
        text1 = num2words(number_p1, lang="pt_BR") + str(aux1)
    else:
        text1 = ""

    if number_p2 > 0:
        text2 = num2words(number_p2, lang="pt_BR") + str(aux2)
    else:
        text2 = ""

    if number_p1 > 0 and number_p2 > 0:
        result = text1 + " e " + text2
    else:
        result = text1 + text2

    return result


# Constantes
# Formulário
FONTE_FORM = "Helvetica"
FONTE_FORM_TAM = 6

FONTE_FORM_TAM_ID = 10

FONTE_DADOS = "Times-Roman"
FONTE_DADOS_TAM = 10

dados_boleto = geraboleto()

# transforma dados_boleto (str/json) em (dict)
dados_boleto = json.loads(dados_boleto)

id_boleto = dados_boleto["data"][0]["id_boleto"]
beneficiario = dados_boleto["data"][0]["beneficiario"]
dado_boleto = dados_boleto["data"][0]["dado_boleto"]
pagador = dado_boleto["pagador"]
des = dado_boleto["data_emissao"].split("-")[::-1]
data_emissao = f"{des[0]}/{des[1]}/{des[2]}"
sacador_avalista = dado_boleto["sacador_avalista"]
situacao_boleto = dado_boleto["dados_individuais_boleto"]
dados_agencia = dado_boleto["pagamentos_cobranca"]
linhadigitavel = situacao_boleto[0]["numero_linha_digitavel"]
base_codigobarra = situacao_boleto[0]["codigo_barras"]

# formata o número do código de pagamento
linha_digitavel = f"{linhadigitavel[:5]}.{linhadigitavel[5:10]} {linhadigitavel[10:15]}.{linhadigitavel[15:21]} {linhadigitavel[21:26]}.{linhadigitavel[26:32]} {linhadigitavel[32]} {linhadigitavel[33:47]}"
# 34191.56009 04386.391504 00520.610007 5 83390000210000

# dados para preenchimento do boleto
banco = dado_boleto["pagamentos_cobranca"][0]["codigo_instituicao_financeira_pagamento"]
localpagamento = "Pague este título preferencialmente nas agências do "
cedente = beneficiario["nome_cobranca"]
# do pagador (sacado)
telefone_empresa = "NÚMERO DE TELEFONE"
sacado = pagador["pessoa"]["nome_pessoa"]
endereco = pagador["endereco"]["nome_logradouro"]
endereco1 = f'{pagador["endereco"]["nome_bairro"]}, {pagador["endereco"]["nome_cidade"]}, {pagador["endereco"]["sigla_UF"]}, {pagador["endereco"]["numero_CEP"]}'

# cria valor por extenso
valor_real = situacao_boleto[0]["valor_titulo"]

# formata para valor em real
vlr_titulo = (
    "{:,.2f}".format(float(valor_real))
    .replace(",", "X")
    .replace(".", ",")
    .replace("X", ".")
)
vlr_extenso = real_por_extenso(vlr_titulo)

# Boleto
documento = "NÃO CONSTA"
emissao = data_emissao
valor = f"R$ {vlr_titulo}"
ven = situacao_boleto[0]["data_vencimento"].split("-")[::-1]
vencimento = f"{ven[0]}/{ven[1]}/{ven[2]}"
aceite = dado_boleto["codigo_aceite"]
especiedoc = dado_boleto["descricao_especie"][:3]
especiemon = "R$"

agencia = f'{dado_boleto["pagamentos_cobranca"][0]["numero_agencia_recebedora"]} + código do cedente'

carteira = dado_boleto["codigo_carteira"]
nossonumero = dado_boleto["dados_individuais_boleto"][0]["numero_nosso_numero"]

valorexpresso = "Valores expressos em Real(is)"
juros = "APÓS O VENCIMENTO COBRAR JUROS DE......... 0,55% AO MÊS"
observacao1 = "APÓS O VENCIMENTO COBRAR MULTA DE......... 0,05%"
observacao2 = "ATÉ 10.07.2020 CONCEDER DESCONTO DE 0,60%"
observacao3 = "CONCEDER ABATIMENTO DE.................... R$15,10"

usobanco = ""

logo = "logo_itau.jpg"


def formboleto(self):
    date_ = datetime.datetime.now().strftime("%d_%m_%Y")
    boleto_name = f"{sacado}-{date_}"
    boleto = Canvas(f"media/financeiro/boletos/itau/{boleto_name}.pdf")

    boleto.drawImage(
        image=os.path.join("./integracoes/banco/Itau/boleto/logo_itau.jpg"),
        x=7 * mm,
        y=280 * mm,
        width=30 * mm,
        height=7 * mm,
    )

    # imagem do recido do sacado
    boleto.drawImage(
        image=os.path.join("./integracoes/banco/Itau/boleto/logo_itau.jpg"),
        x=7 * mm,
        y=229 * mm,
        width=30 * mm,
        height=7 * mm,
    )

    # imagem do banco na ficha de compensação
    boleto.drawImage(
        image=os.path.join("./integracoes/banco/Itau/boleto/logo_itau.jpg"),
        x=7 * mm,
        y=112 * mm,
        width=30 * mm,
        height=7 * mm,
    )

    boleto.setStrokeColor(colors.black)
    boleto.setLineWidth(0.1)
    boleto.setFont("Helvetica-Bold", 14)
    global localpagamento, usobanco, impressora

    # codigo do banco
    boleto.drawString(43 * mm, 229 * mm, "341-7")
    boleto.drawString(43 * mm, 112 * mm, "341-7")
    localpagamento += "Itaú Unibanco Banco Múltiplo S/A"

    # telefone da empresa
    boleto.setFont("Helvetica-Bold", 12)
    boleto.drawString(7 * mm, 275 * mm, telefone_empresa)

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
    boleto.drawString(58 * mm, 229 * mm, linha_digitavel)

    boleto.setFont(FONTE_DADOS, FONTE_DADOS_TAM)
    boleto.drawString(20 * mm, 270 * mm, sacado)
    boleto.drawString(20 * mm, 266 * mm, endereco)
    boleto.drawString(20 * mm, 262 * mm, endereco1)
    boleto.drawString(20 * mm, 258 * mm, documento)
    boleto.drawString(20 * mm, 254 * mm, emissao)
    boleto.drawString(20 * mm, 250 * mm, date)
    boleto.drawString(96 * mm, 258 * mm, valor)
    boleto.drawString(96 * mm, 254 * mm, vencimento)
    boleto.drawString(7 * mm, 221 * mm, cedente)
    boleto.drawString(180 * mm, 221 * mm, vencimento)
    boleto.drawString(7 * mm, 213 * mm, emissao)
    boleto.drawString(41 * mm, 213 * mm, documento)
    boleto.drawString(71 * mm, 213 * mm, especiedoc)
    boleto.drawString(91 * mm, 213 * mm, aceite)
    boleto.drawString(114 * mm, 213 * mm, emissao)
    boleto.drawString(160 * mm, 213 * mm, agencia)
    boleto.drawString(7 * mm, 205 * mm, usobanco)
    boleto.drawString(41 * mm, 205 * mm, carteira)
    boleto.drawString(56 * mm, 205 * mm, especiemon)
    boleto.drawString(160 * mm, 189 * mm, "")
    boleto.drawString(160 * mm, 205 * mm, nossonumero)
    boleto.drawString(20 * mm, 197 * mm, valorexpresso)
    boleto.drawString(20 * mm, 191 * mm, f"{valor} - {vlr_extenso}")
    boleto.drawString(20 * mm, 185 * mm, juros)
    boleto.drawString(160 * mm, 181 * mm, "")
    boleto.drawString(20 * mm, 177 * mm, observacao1)
    boleto.drawString(20 * mm, 171 * mm, observacao2)
    boleto.drawString(20 * mm, 164 * mm, observacao3)
    boleto.drawString(160 * mm, 173 * mm, "")
    boleto.drawString(160 * mm, 165 * mm, "")
    boleto.drawString(160 * mm, 157 * mm, "")
    boleto.drawString(7 * mm, 151 * mm, sacado)
    boleto.drawString(7 * mm, 147 * mm, endereco)
    boleto.drawString(7 * mm, 144 * mm, endereco1)

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
    boleto.drawString(58 * mm, 112 * mm, linha_digitavel)

    boleto.setFont(FONTE_DADOS, FONTE_DADOS_TAM)
    boleto.drawString(7 * mm, 104 * mm, localpagamento)
    boleto.drawString(180 * mm, 104 * mm, vencimento)
    boleto.drawString(7 * mm, 96 * mm, cedente)
    boleto.drawString(7 * mm, 88 * mm, emissao)
    boleto.drawString(41 * mm, 88 * mm, documento)
    boleto.drawString(71 * mm, 88 * mm, especiedoc)
    boleto.drawString(91 * mm, 88 * mm, aceite)
    boleto.drawString(114 * mm, 88 * mm, emissao)
    boleto.drawString(160 * mm, 96 * mm, agencia)
    boleto.drawString(7 * mm, 80 * mm, usobanco)
    boleto.drawString(41 * mm, 80 * mm, carteira)
    boleto.drawString(56 * mm, 80 * mm, especiemon)
    boleto.drawString(71 * mm, 80 * mm, "")
    boleto.drawString(124 * mm, 80 * mm, "")
    boleto.drawString(160 * mm, 88 * mm, nossonumero)
    boleto.drawString(20 * mm, 72 * mm, valorexpresso)
    boleto.drawString(20 * mm, 66 * mm, f"{valor} - {vlr_extenso}")
    boleto.drawString(177 * mm, 80 * mm, valor)
    boleto.drawString(160 * mm, 72 * mm, "")
    boleto.drawString(20 * mm, 60 * mm, juros)
    boleto.drawString(20 * mm, 54 * mm, observacao1)
    boleto.drawString(20 * mm, 48 * mm, observacao2)
    boleto.drawString(20 * mm, 41 * mm, observacao3)
    boleto.drawString(160 * mm, 56 * mm, "")
    boleto.drawString(160 * mm, 48 * mm, "")
    boleto.drawString(160 * mm, 40 * mm, "")
    boleto.drawString(160 * mm, 32 * mm, "")
    boleto.drawString(7 * mm, 33 * mm, sacado)
    boleto.drawString(7 * mm, 29 * mm, endereco)
    boleto.drawString(7 * mm, 26 * mm, endereco1)

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
    f.addFromList([I2of5(linhadigitavel, xdim=0.3 * mm, checksum=0, bearers=0)], boleto)

    boleto.save()

    os.startfile(
        # f"media/financeiro/boletos/itau/{boleto_name}.pdf"
        f"C:/PROJETOS/TRABALHOS/INTIP/ERP/erp/project/media/financeiro/boletos/itau/{boleto_name}.pdf"
    )

    # return redirect("{% url 'despesa:fluxodecaixa' %}")
    return redirect("{{ venda.venda_gau_edit }}")
    # return HttpResponseRedirect("http://127.0.0.1:8000/despesa/fluxodecaixa")


if __name__ == "__main__":
    formboleto()
