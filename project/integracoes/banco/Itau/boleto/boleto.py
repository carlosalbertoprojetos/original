import os
import json
from django.http import HttpResponseRedirect
from PIL import Image
import PIL.Image
from django.shortcuts import redirect, render
from django.urls import reverse

from reportlab.graphics.shapes import *

from reportlab.graphics.barcode.common import *
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4

from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Frame

import unittest
import requests

from num2words import num2words

import datetime

# from cliente.models import Cliente
# from empresa.models import DadosBancarios
# from financeiro.models import ContaReceber

date = datetime.datetime.now().strftime("%d/%m/%Y")

# Constantes
FONTE_FORM = "Helvetica"
FONTE_FORM_TAM = 6

FONTE_FORM_TAM_ID = 10

FONTE_DADOS = "Times-Roman"
FONTE_DADOS_TAM = 10


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
    return boleto_data.text


def real_por_extenso(number_p):
    if number_p.find(",") == -1:
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


def validaDadosBoleto(request, venda, parcela):
    bd_banco = DadosBancarios.objects.filter(empresa=1)
    parcela_qs = ContaReceber.objects.filter(id=parcela)
    bd_boleto = {}

    id_beneficiario = []  # agencia(4 dígitos) + conta(7 dígitos) + DAC (1 dígito)
    beneficiario = []
    beneficiario_codigo_tipo_pessoa = []
    cpf_cnpj_beneficiario = []
    codigo_tipo_protesto = []
    codigo_tipo_negativacao = []
    codigo_instrucao_cobranca = []
    pagador = []
    pagador_nomefantasia = []
    pagador_codigo_tipo_pessoa = []
    cpf_cnpj_pagador = []
    data_emissao = []
    data_emissao_f = []
    dados_agencia = []
    num_banco = []
    banco = []
    cedente = []
    telefone_empresa = []
    endereco_pagador = []
    nome_logradouro = []
    nome_bairro = []
    nome_cidade = []
    sigla_UF = []
    numero_CEP = []
    valor_real = []
    data_vencimento = []
    data_vencimento_f = []

    for b in bd_banco:
        id_beneficiario.append(f"{b.agencia}{b.conta}{b.dac}")
        beneficiario.append(b.empresa.nome)
        num_banco.append(b.num_banco)
        banco.append(b.banco)
        cedente.append(b.empresa.nome)
        dados_agencia.append(f"{b.agencia} + código do cedente")
        if (b.empresa.cpf and b.empresa.cnpj) or b.empresa.cnpj:
            beneficiario_codigo_tipo_pessoa.append("J")
            cpf_cnpj_beneficiario.append(b.empresa.cnpj)
        elif b.empresa.cpf:
            beneficiario_codigo_tipo_pessoa.append("F")
            cpf_cnpj_beneficiario.append(b.empresa.cpf)
        codigo_tipo_protesto = (1, 2, 3)
        codigo_tipo_negativacao = (3, 2, 1)
        codigo_instrucao_cobranca = 5
        if (b.empresa.cpf and b.empresa.cnpj) or b.empresa.cnpj:
            bd_boleto.update({"beneficiario_codigo_tipo_pessoa": "J"})
        elif b.empresa.cpf:
            bd_boleto.update({"beneficiario_codigo_tipo_pessoa": "F"})

    for p in parcela_qs:
        telefone_empresa.append(p.venda.cliente.tel_principal)
        pagador.append(p.venda.cliente.nome)
        pagador_nomefantasia.append(p.venda.cliente.nome_fantasia)
        endereco_pagador.append(
            f"{p.venda.cliente.logradouro}, Nº {p.venda.cliente.numero} - {p.venda.cliente.complemento}, Bairro: {p.venda.cliente.bairro}, CEP: {p.venda.cliente.cep}, {p.venda.cliente.cidade}/{p.venda.cliente.estado}"
        )
        nome_logradouro.append(p.venda.cliente.logradouro)
        nome_bairro.append(p.venda.cliente.bairro)
        nome_cidade.append(p.venda.cliente.cidade)
        sigla_UF.append(p.venda.cliente.estado)
        numero_CEP.append(p.venda.cliente.cep)
        if (p.venda.cliente.cpf and p.venda.cliente.cnpj) or p.venda.cliente.cnpj:
            pagador_codigo_tipo_pessoa.append("J")
            bd_boleto.update({"pagador_codigo_tipo_pessoa": "J"})
            cpf_cnpj_pagador.append(p.venda.cliente.cnpj)
        elif b.empresa.cpf:
            pagador_codigo_tipo_pessoa.append("F")
            cpf_cnpj_pagador.append(p.venda.cliente.cpf)
            bd_boleto.update({"pagador_codigo_tipo_pessoa": "F"})
        valor_real.append(p.valor)
        data_emissao.append(p.datadocumento)
        data_emissao_f.append(p.datadocumento.strftime("%d/%m/%Y"))
        data_vencimento.append(p.datavencimento)
        data_vencimento_f.append(p.datavencimento.strftime("%d/%m/%Y"))
        id_cliente = p.venda.cliente.id

    vlr_titulo = valor_real
    valor = f"R$ {vlr_titulo[0]}"

    lista_alerta = []
    if not beneficiario:
        lista_alerta.append("Cadastre o nome do cedente")
    if not beneficiario_codigo_tipo_pessoa:
        lista_alerta.append("Cadastre CPF ou CNPJ do cedente")
    if not pagador:
        lista_alerta.append("Cadastre o nome do cliente")
    if not pagador_nomefantasia:
        lista_alerta.append("Cadastre o nome fantasia do cliente")
    if not pagador_codigo_tipo_pessoa:
        lista_alerta.append("Cadastre CPF ou CNPJ do cliente")
    if not endereco_pagador:
        lista_alerta.append("Cadastre o endereço do cliente")
    if not dados_agencia:
        lista_alerta.append("Cadastre o número da agência")
    if not num_banco:
        lista_alerta.append("Cadastre o número do banco")
    if not banco:
        lista_alerta.append("Cadastre o nome do banco")
    if not cedente:
        lista_alerta.append("Cadastre o nome do cendente")
    if not telefone_empresa:
        lista_alerta.append("Cadastre o telefone do cendente")
    if not data_vencimento:
        lista_alerta.append("Cadastre a data do vencimento")
    if not codigo_tipo_protesto:
        lista_alerta.append("Informe o tipo de protesto")
    if not codigo_tipo_negativacao:
        lista_alerta.append("Informe o código de negativação")
    if not codigo_instrucao_cobranca:
        lista_alerta.append("Informe a instrução de cobrança")

    documento = "NÃO CONSTA"
    linha_digitavel = "34191.56009 04386.391504 00520.610007 5 83390000210000"
    especiedoc = "ESP DOC"
    aceite = "ACEITE"
    carteira = "CART"
    especiemon = "R$"
    nossonumero = "2000000"
    juros = "APÓS O VENCIMENTO COBRAR JUROS DE......... 0,55% AO MÊS"
    observacao1 = "APÓS O VENCIMENTO COBRAR MULTA DE......... 0,05%"
    observacao2 = "ATÉ 10.07.2020 CONCEDER DESCONTO DE 0,60%"
    observacao3 = "CONCEDER ABATIMENTO DE.................... R$15,10"
    id_cliente = []

    teste = {}
    true = "true"
    false = "false"
    teste.update(
        {
            "data": {
                "etapa_processo_boleto": "efetivacao",
                "codigo_canal_operacao": "API",
                "beneficiario": {"id_beneficiario": id_beneficiario},
                "dado_boleto": {
                    "descricao_instrumento_cobranca": "boleto",
                    "tipo_boleto": "a vista",
                    "codigo_carteira": "109",
                    "valor_total_titulo": valor_real,
                    "codigo_especie": "01",
                    "valor_abatimento": "000",
                    "data_emissao": data_emissao,
                    "indicador_pagamento_parcial": true,
                    "quantidade_maximo_parcial": 0,
                    "pagador": {
                        "pessoa": {
                            "nome_pessoa": pagador,
                            "tipo_pessoa": {
                                "codigo_tipo_pessoa": pagador_codigo_tipo_pessoa,
                                "numero_cadastro_pessoa_fisica": cpf_cnpj_pagador,
                            },
                        },
                        "endereco": {
                            "nome_logradouro": nome_logradouro,
                            "nome_bairro": nome_bairro,
                            "nome_cidade": nome_cidade,
                            "sigla_UF": sigla_UF,
                            "numero_CEP": numero_CEP,
                        },
                    },
                    "dados_individuais_boleto": [
                        {
                            "numero_nosso_numero": nossonumero,
                            "data_vencimento": data_vencimento,
                            "valor_titulo": valor_real,
                            "texto_uso_beneficiario": "2",
                            "texto_seu_numero": "2",
                        }
                    ],
                    "multa": {
                        "codigo_tipo_multa": "02",
                        "data_multa": "2024-09-21",
                        "percentual_multa": "000000100000",
                    },
                    "juros": {
                        "codigo_tipo_juros": 90,
                        "data_juros": "2024-09-21",
                        "percentual_juros": "000000100000",
                    },
                    "recebimento_divergente": {"codigo_tipo_autorizacao": "01"},
                    "instrucao_cobranca": [
                        {
                            "codigo_instrucao_cobranca": "2",
                            "quantidade_dias_apos_vencimento": 10,
                            "dia_util": false,
                        }
                    ],
                    "protesto": {"protesto": true, "quantidade_dias_protesto": 10},
                    "desconto_expresso": false,
                },
            }
        }
    )
    print(teste)
    return lista_alerta


def formboleto(bd_boleto):
    date_ = datetime.datetime.now().strftime("%d.%m.%Y")
    # boleto_name = f"{bd_boleto['pagador']}-{date_}"
    boleto_nome = f"{bd_boleto['nome_arquivo_boleto']}-{date_}"
    boleto = Canvas(f"media/financeiro/boletos/itau/{boleto_nome}.pdf")

    logo = os.path.join("./integracoes/banco/Itau/boleto/logo_itau.jpg")

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
    localpagamento = "Pague este título preferencialmente nas agências do "
    usobanco = ""

    # codigo do banco
    boleto.drawString(43 * mm, 229 * mm, "341-7")
    boleto.drawString(43 * mm, 112 * mm, "341-7")
    localpagamento += "Itaú Unibanco Banco Múltiplo S/A"

    # telefone da empresa
    boleto.setFont("Helvetica-Bold", 12)
    boleto.drawString(7 * mm, 275 * mm, bd_boleto["telefone_empresa"][0])

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
    boleto.drawString(58 * mm, 229 * mm, bd_boleto["linha_digitavel"])

    boleto.setFont(FONTE_DADOS, FONTE_DADOS_TAM)
    boleto.drawString(20 * mm, 270 * mm, bd_boleto["pagador"][0])
    boleto.drawString(20 * mm, 266 * mm, bd_boleto["endereco_pagador"][0])
    # boleto.drawString(20 * mm, 262 * mm, bd_boleto["endereco_pagador"][0])
    boleto.drawString(20 * mm, 258 * mm, bd_boleto["documento"])
    boleto.drawString(20 * mm, 254 * mm, bd_boleto["data_emissao"])
    boleto.drawString(20 * mm, 250 * mm, date)
    boleto.drawString(96 * mm, 258 * mm, bd_boleto["valor"])
    boleto.drawString(96 * mm, 254 * mm, bd_boleto["data_vencimento"])
    boleto.drawString(7 * mm, 221 * mm, bd_boleto["cedente"][0])
    boleto.drawString(180 * mm, 221 * mm, bd_boleto["data_vencimento"])
    boleto.drawString(7 * mm, 213 * mm, bd_boleto["data_emissao"])
    boleto.drawString(41 * mm, 213 * mm, bd_boleto["documento"])
    boleto.drawString(71 * mm, 213 * mm, bd_boleto["especiedoc"])
    boleto.drawString(91 * mm, 213 * mm, bd_boleto["aceite"])
    boleto.drawString(114 * mm, 213 * mm, bd_boleto["data_emissao"])
    boleto.drawString(160 * mm, 213 * mm, bd_boleto["dados_agencia"][0])
    boleto.drawString(7 * mm, 205 * mm, usobanco)
    boleto.drawString(41 * mm, 205 * mm, bd_boleto["carteira"])
    boleto.drawString(56 * mm, 205 * mm, bd_boleto["especiemon"])
    boleto.drawString(160 * mm, 189 * mm, "")
    boleto.drawString(160 * mm, 205 * mm, bd_boleto["nossonumero"])
    # boleto.drawString(20 * mm, 197 * mm, valorexpresso)
    # boleto.drawString(20 * mm, 191 * mm, f"{valor} - {vlr_extenso}")
    boleto.drawString(177 * mm, 197 * mm, bd_boleto["valor"])
    boleto.drawString(20 * mm, 185 * mm, bd_boleto["juros"])
    boleto.drawString(160 * mm, 181 * mm, "")
    boleto.drawString(20 * mm, 177 * mm, bd_boleto["observacao1"])
    boleto.drawString(20 * mm, 171 * mm, bd_boleto["observacao2"])
    boleto.drawString(20 * mm, 164 * mm, bd_boleto["observacao3"])
    boleto.drawString(160 * mm, 173 * mm, "")
    boleto.drawString(160 * mm, 165 * mm, "")
    boleto.drawString(160 * mm, 157 * mm, "")
    boleto.drawString(7 * mm, 151 * mm, bd_boleto["pagador"][0])
    boleto.drawString(7 * mm, 147 * mm, bd_boleto["endereco_pagador"][0])
    # boleto.drawString(7 * mm, 144 * mm, bd_boleto["endereco_pagador"][0])

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
    boleto.drawString(58 * mm, 112 * mm, bd_boleto["linha_digitavel"])

    boleto.setFont(FONTE_DADOS, FONTE_DADOS_TAM)
    boleto.drawString(7 * mm, 104 * mm, localpagamento)
    boleto.drawString(180 * mm, 104 * mm, bd_boleto["data_vencimento"])
    boleto.drawString(7 * mm, 96 * mm, bd_boleto["cedente"][0])
    boleto.drawString(7 * mm, 88 * mm, bd_boleto["data_emissao"])
    boleto.drawString(41 * mm, 88 * mm, bd_boleto["documento"])
    boleto.drawString(71 * mm, 88 * mm, bd_boleto["especiedoc"])
    boleto.drawString(91 * mm, 88 * mm, bd_boleto["aceite"])
    boleto.drawString(114 * mm, 88 * mm, bd_boleto["data_emissao"])
    boleto.drawString(160 * mm, 96 * mm, bd_boleto["dados_agencia"][0])
    boleto.drawString(7 * mm, 80 * mm, usobanco)
    boleto.drawString(41 * mm, 80 * mm, bd_boleto["carteira"])
    boleto.drawString(56 * mm, 80 * mm, bd_boleto["especiemon"])
    boleto.drawString(71 * mm, 80 * mm, "")
    boleto.drawString(124 * mm, 80 * mm, "")
    boleto.drawString(160 * mm, 88 * mm, bd_boleto["nossonumero"])
    # boleto.drawString(20 * mm, 72 * mm, valorexpresso)
    # boleto.drawString(20 * mm, 66 * mm, f"{valor} - {vlr_extenso}")
    boleto.drawString(177 * mm, 80 * mm, bd_boleto["valor"])
    boleto.drawString(160 * mm, 72 * mm, "")
    boleto.drawString(20 * mm, 60 * mm, bd_boleto["juros"])
    boleto.drawString(20 * mm, 54 * mm, bd_boleto["observacao1"])
    boleto.drawString(20 * mm, 48 * mm, bd_boleto["observacao2"])
    boleto.drawString(20 * mm, 41 * mm, bd_boleto["observacao3"])
    boleto.drawString(160 * mm, 56 * mm, "")
    boleto.drawString(160 * mm, 48 * mm, "")
    boleto.drawString(160 * mm, 40 * mm, "")
    boleto.drawString(160 * mm, 32 * mm, "")
    boleto.drawString(7 * mm, 33 * mm, bd_boleto["pagador"][0])
    boleto.drawString(7 * mm, 29 * mm, bd_boleto["endereco_pagador"][0])
    # boleto.drawString(7 * mm, 26 * mm, bd_boleto["endereco_pagador"][0])

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
        [I2of5(bd_boleto["linha_digitavel"], xdim=0.3 * mm, checksum=0, bearers=0)],
        boleto,
    )

    boleto.save()

    # for caminho, diretorios, arquivos in os.walk():
    #     print(caminho)
    #     print(diretorios)
    #     print(arquivos)

    # pathname = os.path.join("root", "directory1", "directory2")
    # print(pathname)

    # image=logo,
    # nome_arquivo_boleto = os.open(
    #     f"./media/financeiro/boletos/itau/{boleto_nome}.pdf", os.O_CREAT | os.O_RDWR
    # )
    # base = f"C:/PROJETOS/TRABALHOS/INTIP/ERP/erp/project/media/financeiro/boletos/itau/{boleto_nome}.pdf"
    base = f"../media/financeiro/boletos/itau/{boleto_nome}.pdf"
    # media\financeiro\boletos\itau\8-52_107-20.09.2023.pdf

    # nome_arquivo_boleto = os.path.join(
    #     f"../media/financeiro/boletos/itau/{boleto_nome}.pdf"
    # )
    os.startfile(
        base
        # f"media/financeiro/boletos/itau/{boleto_nome}.pdf"
        # f"C:/PROJETOS/TRABALHOS/INTIP/ERP/erp/project/media/financeiro/boletos/itau/{boleto_nome}.pdf"
    )

    return redirect(f"/venda/{bd_boleto['venda']}/editar")


# if __name__ == "__main__":
#     formboleto()


def validarBoleto():
    """Gera o token"""
    client_id = "82e96e5c-7132-3add-8a6f-5dbd9d60d500"
    client_secret = "8183c235-61a0-470a-8584-aa2ccbca2dab"
    client = {"client_id": client_id, "client_secret": client_secret}
    url = "https://api.itau.com.br/cash_management/v2/boletos"
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
        headers=headers,
    )
    return boleto_data.text


# formato dados a serem enviados para validação no isBoxAnchor
# {
#     "data": {
#         "etapa_processo_boleto": "efetivacao",
#         "codigo_canal_operacao": "API",
#         "beneficiario": {"id_beneficiario": id_beneficiario},
#         "dado_boleto": {
#             "descricao_instrumento_cobranca": "boleto",
#             "tipo_boleto": "a vista",
#             "codigo_carteira": "109",
#             "valor_total_titulo": valor_real,
#             "codigo_especie": "01",
#             "valor_abatimento": "000",
#             "data_emissao": data_emissao,
#             "indicador_pagamento_parcial": true,
#             "quantidade_maximo_parcial": 0,
#             "pagador": {
#                 "pessoa": {
#                     "nome_pessoa": pagador,
#                     "tipo_pessoa": {
#                         "codigo_tipo_pessoa": pagador_codigo_tipo_pessoa,
#                         "numero_cadastro_pessoa_fisica": cpf_cnpj_pagador,
#                     },
#                 },
#                 "endereco": {
#                     "nome_logradouro": nome_logradouro,
#                     "nome_bairro": nome_bairro,
#                     "nome_cidade": nome_cidade,
#                     "sigla_UF": sigla_UF,
#                     "numero_CEP": numero_CEP,
#                 },
#             },
#             "dados_individuais_boleto": [
#                 {
#                     "numero_nosso_numero": nossonumero,
#                     "data_vencimento": data_vencimento,
#                     "valor_titulo": valor_real,
#                     "texto_uso_beneficiario": "2",
#                     "texto_seu_numero": "2",
#                 }
#             ],
#             "multa": {
#                 "codigo_tipo_multa": "02",
#                 "data_multa": "2024-09-21",
#                 "percentual_multa": "000000100000",
#             },
#             "juros": {
#                 "codigo_tipo_juros": 90,
#                 "data_juros": "2024-09-21",
#                 "percentual_juros": "000000100000",
#             },
#             "recebimento_divergente": {"codigo_tipo_autorizacao": "01"},
#             "instrucao_cobranca": [
#                 {
#                     "codigo_instrucao_cobranca": "2",
#                     "quantidade_dias_apos_vencimento": 10,
#                     "dia_util": false,
#                 }
#             ],
#             "protesto": {"protesto": true, "quantidade_dias_protesto": 10},
#             "desconto_expresso": false,
#         },
#     }
# }


# {
#     "data": {
#         "etapa_processo_boleto": "efetivacao",
#         "codigo_canal_operacao": "API",
#         "beneficiario": {"id_beneficiario": []},
#         "dado_boleto": {
#             "descricao_instrumento_cobranca": "boleto",
#             "tipo_boleto": "a vista",
#             "codigo_carteira": "109",
#             "valor_total_titulo": [],
#             "codigo_especie": "01",
#             "valor_abatimento": "000",
#             "data_emissao": [],
#             "indicador_pagamento_parcial": "true",
#             "quantidade_maximo_parcial": 0,
#             "pagador": {
#                 "pessoa": {
#                     "nome_pessoa": [],
#                     "tipo_pessoa": {
#                         "codigo_tipo_pessoa": [],
#                         "numero_cadastro_pessoa_fisica": [],
#                     },
#                 },
#                 "endereco": {
#                     "nome_logradouro": [],
#                     "nome_bairro": [],
#                     "nome_cidade": [],
#                     "sigla_UF": [],
#                     "numero_CEP": [],
#                 },
#             },
#             "dados_individuais_boleto": [
#                 {
#                     "numero_nosso_numero": "NOSSO NÚM",
#                     "data_vencimento": [],
#                     "valor_titulo": [],
#                     "texto_uso_beneficiario": "2",
#                     "texto_seu_numero": "2",
#                 }
#             ],
#             "multa": {
#                 "codigo_tipo_multa": "02",
#                 "data_multa": "2024-09-21",
#                 "percentual_multa": "000000100000",
#             },
#             "juros": {
#                 "codigo_tipo_juros": 90,
#                 "data_juros": "2024-09-21",
#                 "percentual_juros": "000000100000",
#             },
#             "recebimento_divergente": {"codigo_tipo_autorizacao": "01"},
#             "instrucao_cobranca": [
#                 {
#                     "codigo_instrucao_cobranca": "2",
#                     "quantidade_dias_apos_vencimento": 10,
#                     "dia_util": "false",
#                 }
#             ],
#             "protesto": {"protesto": "true", "quantidade_dias_protesto": 10},
#             "desconto_expresso": "false",
#         },
#     }
# }
