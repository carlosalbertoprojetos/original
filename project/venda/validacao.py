from reportlab.graphics.shapes import *
from reportlab.graphics.barcode.common import *
import glob

import datetime

from itertools import cycle
import json

from empresa.models import DadosBancarios
from financeiro.models import ContaReceber
from empresa.models import Empresa
from venda.boleto import formboleto, emitirBoleto

date = datetime.datetime.now().strftime("%d/%m/%Y")

# Constantes
# Formulário
FONTE_FORM = "Helvetica"
FONTE_FORM_TAM = 6

FONTE_FORM_TAM_ID = 10

FONTE_DADOS = "Times-Roman"
FONTE_DADOS_TAM = 10


def validate_cnpj(cnpj: str) -> bool:
    LENGTH_CNPJ = 14
    if len(cnpj) != LENGTH_CNPJ:
        return False

    if cnpj in (c * LENGTH_CNPJ for c in "1234567890"):
        return False

    cnpj_r = cnpj[::-1]
    for i in range(2, 0, -1):
        cnpj_enum = zip(cycle(range(2, 10)), cnpj_r[i:])
        dv = sum(map(lambda x: int(x[1]) * x[0], cnpj_enum)) * 10 % 11
        if cnpj_r[i - 1 : i] != str(dv % 10):
            return False

    return True


def validate_cpf(numbers):
    #  Obtém os números do CPF e ignora outros caracteres
    cpf = [int(char) for char in numbers if char.isdigit()]

    #  Verifica se o CPF tem 11 dígitos
    if len(cpf) != 11:
        return False

    #  Verifica se o CPF tem todos os números iguais, ex: 111.111.111-11
    #  Esses CPFs são considerados inválidos mas passam na validação dos dígitos
    #  Antigo código para referência: if all(cpf[i] == cpf[i+1] for i in range (0, len(cpf)-1))
    if cpf == cpf[::-1]:
        return False

    #  Valida os dois dígitos verificadores
    for i in range(9, 11):
        value = sum((cpf[num] * ((i + 1) - num) for num in range(0, i)))
        digit = ((value * 10) % 11) % 10
        if digit != cpf[i]:
            return False
    return True


def valida_dados_emissao_boleto(num_parcela):
    """exclui os arquivos pdf gerados"""
    # directory = "media/financeiro/boletos/"
    # files = glob.glob(directory)

    # for file in files:
    #     if os.path.exists(file):
    #         os.remove(file)

    """valida os dados do formulario a fim de obter todos os campos obrigatorios para a emissão de boletos"""
    erros_boleto = []
    # sep_venda_parcela = num_parcela.split(",")
    # venda = sep_venda_parcela[0]
    # parcela = sep_venda_parcela[1]
    venda = num_parcela[0]
    parcela = num_parcela[1]
    parcela_qs = ContaReceber.objects.filter(venda__id=venda)
    id_parcela = 0
    id_cliente = []

    for p in parcela_qs:
        id_cliente = p.venda.cliente.id
        if p.parcela == parcela:
            id_parcela = p.id

    dados_parcela = ContaReceber.objects.filter(id=id_parcela)
    bd_data_banco = DadosBancarios.objects.filter(empresa=1)

    nome_arquivo_boleto = f"{id_cliente}-{venda}_{id_parcela}"

    id_beneficiario = []
    beneficiario = []
    beneficiario_codigo_tipo_pessoa = []
    cpf_cnpj_beneficiario = []
    cpf_cnpj_pagador = []
    num_documento = []
    codigo_tipo_protesto = []
    codigo_tipo_negativacao = []
    codigo_instrucao_cobranca = []
    pagador = []
    pagador_nomefantasia = []
    pagador_codigo_tipo_pessoa = []
    data_emissao = []
    nome_banco_destinatario = []
    num_banco = []
    banco = []
    dados_agencia = []
    d_agencia = []
    conta = []
    telefone_empresa = []
    endereco_pagador = []
    nome_logradouro = []
    nome_bairro = []
    nome_cidade = []
    sigla_UF = []
    numero_CEP = []
    valor_titulo = []
    valor = []
    data_vencimento = []
    fator_vencimento = []
    documento_beneficiario = []
    documento_pagador = []
    codigo_carteira = "157"

    true = "true"
    false = "false"

    codigo_tipo_protesto = (1, 2, 3)
    codigo_tipo_negativacao = (3, 2, 1)
    codigo_instrucao_cobranca = 5

    especiedoc = "ESP DOC"
    aceite = "ACEITE"
    especiemon = "R$"
    juros = "APÓS O VENCIMENTO COBRAR JUROS DE......... 0,55% AO MÊS"
    valor_juros = ""  # Valor dos juros a ser cobrado. Obrigatório para codigo_tipo_juros ‘93’. Valor deve ser superior a R$0,01. Formato do campo: 15 dígitos inteiros e 2 casas decimais. Exemplo: 99999999999999900
    observacao1 = "APÓS O VENCIMENTO COBRAR MULTA DE......... 0,05%"
    observacao2 = "ATÉ 10.07.2020 CONCEDER DESCONTO DE 0,60%"
    observacao3 = "CONCEDER ABATIMENTO DE.................... R$15,10"

    # Orientações 'Como montar o seu boleto?' https://devportal.itau.com.br/nossas-apis/itau-ep9-gtw-cash-management-ext-v2#subheading-5-1

    local_pagamento = "Pague pelo aplicativo, internet ou em agências e correspondentes"
    data_documento = []
    num_documento = "Para as carteiras de 15 dígitos (nas quais são utilizadas 15 posições numéricas para identificação do título liquidado), há a obrigatoriedade de preenchimento deste campo, que se compõe de 7 dígitos mais o respectivo DAC, calculado pelo critério do Módulo 10. Para as demais carteiras, caso não haja necessidade de protesto, este campo pode ser deixado em branco."
    especie = "R$"

    "Os dados deverão ser preenchidos de forma a ser facilmente identificados, conforme layout do Banco, ou seja, “1234/56789-7” e “123/45678901-5”, respectivamente. => max 8 caracteres"
    instrucoes = []
    numero_nosso_numero = f'{codigo_carteira}{datetime.datetime.now().strftime("%d%m")}'

    for b in bd_data_banco:
        if not b.banco:
            erros_boleto.append(f"Cadastre nome do banco")
        else:
            nome_banco_destinatario.append(b.banco)
        if not b.agencia or not b.conta or not b.dac:
            falta = []
            if not b.agencia:
                falta.append("agência")
            if not b.conta:
                falta.append("conta")
            if not b.dac:
                falta.append("DAC")
            num_ = len(falta)
            if num_ == 1:
                erros_boleto.append(f"Cadastre {falta[0]}, em banco")
            elif num_ == 2:
                erros_boleto.append(f"Cadastre {falta[0]} e {falta[1]}")
            else:
                erros_boleto.append("Cadastre agência, conta e dac.")
        else:
            id_beneficiario.append(f"{b.agencia}{b.conta}{b.dac}")
        if not b.empresa.nome:
            erros_boleto.append("Cadastre o nome do beneficiario")
        else:
            beneficiario.append(b.empresa.nome)
        if not b.num_banco:
            erros_boleto.append("Cadastre o número da instituição bancária")
        else:
            num_banco.append(b.num_banco)
        if not b.banco:
            erros_boleto.append("Cadastre o nome da instituição bancária")
        else:
            banco.append(b.banco)
        if not b.conta:
            erros_boleto.append("Cadastre o número da conta bancária")
        else:
            conta.append(b.conta)
        dados_agencia.append(f"{b.agencia} / {b.conta}-{b.dac}")
        d_agencia.append(b.agencia + b.conta)
        if not b.empresa.cpf and not b.empresa.cnpj:
            erros_boleto.append("Cadastre CPF ou CNPJ do beneficiario")
        else:
            if (b.empresa.cpf and b.empresa.cnpj) or b.empresa.cnpj:
                beneficiario_codigo_tipo_pessoa.append("J")
                cpf_cnpj_beneficiario.append(b.empresa.cnpj)
            elif b.empresa.cpf:
                beneficiario_codigo_tipo_pessoa.append("F")
                cpf_cnpj_beneficiario.append(b.empresa.cpf)

    for p in dados_parcela:
        telefone_empresa.append(p.venda.cliente.tel_principal)
        if not p.venda.cliente.nome:
            erros_boleto.append("Cadastre o nome do cliente")
        else:
            pagador.append(p.venda.cliente.nome[0:50])
        if 0: #not p.venda.cliente.nome_fantasia:
            erros_boleto.append("Cadastre o nome fantasia do cliente")
        else:
            pagador_nomefantasia.append(p.venda.cliente.nome_fantasia[0:50])
        if not p.venda.cliente.cpf and not p.venda.cliente.cnpj:
            erros_boleto.append("Cadastre CPF ou CNPJ do cliente")
        else:
            if (p.venda.cliente.cpf and p.venda.cliente.cnpj) or p.venda.cliente.cnpj:
                pagador_codigo_tipo_pessoa.append("J")
                cpf_cnpj_pagador.append(p.venda.cliente.cnpj)
            elif p.venda.cliente.cpf:
                pagador_codigo_tipo_pessoa.append("F")
                cpf_cnpj_pagador.append(p.venda.cliente.cpf)
        valor.append(str(p.valor).replace(".", ","))
        valor_titulo.append(
            "0" * (11 - len(str(p.valor))) + str(p.valor).replace(".", "")
        )
        data_emissao.append(str(p.datadocumento))
        data_vencimento.append(str(p.datavencimento))
        fator_vencimento = (p.datavencimento - p.datadocumento).days
        endereco_pagador.append(
            f"{p.venda.cliente.logradouro}, Nº {p.venda.cliente.numero} - {p.venda.cliente.complemento}, Bairro: {p.venda.cliente.bairro}, CEP: {p.venda.cliente.cep}, {p.venda.cliente.cidade}/{p.venda.cliente.estado}"
        )
        nome_logradouro.append(p.venda.cliente.logradouro)
        nome_bairro.append(p.venda.cliente.bairro)
        nome_cidade.append(p.venda.cliente.cidade)
        sigla_UF.append(p.venda.cliente.estado)
        numero_CEP.append(p.venda.cliente.cep)
        if not endereco_pagador:
            erros_boleto.append("Cadastre o endereço do cliente")

    agencia_cc_dac = d_agencia[0] + conta[0]

    base_cod_barras = (
        num_banco[0][0:3]
        + "9"
        + str(fator_vencimento)
        + str(valor_titulo[0])
        + numero_nosso_numero
        + agencia_cc_dac
        + "00"
    )
    mod_11 = "4329876543298765432987654329876543298765432"

    soma = 0
    for i in range(len(mod_11)):
        soma += int(mod_11[i]) * int(base_cod_barras[i])
    resultado = 11 - (soma % 11)
    base_cod_barras = str(base_cod_barras)
    # print(base_cod_barras)
    # 341916000 00500001570 6106505009 9 572009957200

    ncod_barras = []
    for i in range(len(base_cod_barras)):
        if (i + 1) == 5:
            ncod_barras.append(resultado)
        ncod_barras.append(base_cod_barras[i])

    format_cod_barras = list(map(int, ncod_barras))
    cod_barras = (
        str(format_cod_barras)
        .replace(",", "")
        .replace(" ", "")
        .replace("[", "")
        .replace("]", "")
    )

    # base_cod_barras = "34191101234567880057123457000616670000012345"

    mod10_1 = "212121212"
    mod10_2 = "1212121212"
    campo1 = base_cod_barras[0:9]
    campo2 = base_cod_barras[9:19]
    campo3 = base_cod_barras[19:29]
    campo4 = base_cod_barras[29:30]
    campo5 = base_cod_barras[30:48]

    c1 = []
    c2 = []
    c3 = []

    for i in range(len(campo1)):
        calc1 = int(campo1[i]) * int(mod10_1[i])
        lencalc1 = len(str(calc1))
        if lencalc1 == 2:
            calc1 = str(calc1)
            for j in range(lencalc1):
                c1.append(int(calc1[j]))
        else:
            c1.append(int(campo1[i]) * int(mod10_1[i]))

    for i in range(len(campo2)):
        calc2 = int(campo2[i]) * int(mod10_2[i])
        lencalc2 = len(str(calc2))
        if lencalc2 == 2:
            calc2 = str(calc2)
            for j in range(lencalc2):
                c2.append(int(calc2[j]))
        else:
            c2.append(int(campo2[i]) * int(mod10_2[i]))

    for i in range(len(campo3)):
        calc3 = int(campo3[i]) * int(mod10_2[i])
        lencalc3 = len(str(calc3))
        if lencalc3 == 2:
            calc3 = str(calc3)
            for j in range(lencalc3):
                c3.append(int(calc3[j]))
        else:
            c3.append(int(campo3[i]) * int(mod10_2[i]))

    c1a = 0
    c2a = 0
    c3a = 0

    for i in c1:
        c1a += i
    for i in c2:
        c2a += i
    for i in c3:
        c3a += i

    dac1 = 10 - (c1a % 10)
    dac2 = 10 - (c2a % 10)
    dac3 = 10 - (c3a % 10)

    base_linha_digitavel = campo1 + campo2 + campo3 + campo4 + campo5
    base_dac = [dac1, dac2, dac3]
    numero_linha_digitavel = (
        f"{campo1}{dac1}{campo2}{dac2}{campo3}{dac3}{campo4}{campo5}"
    )
    id_boleto_individual = nome_arquivo_boleto

    num_documento = []
    # gera numero do documento
    calc_venda = 5 - len(venda)
    num_documento.append("0" * calc_venda + venda + "/" + parcela)

    bd_boleto = {
        "venda": venda,
        "nome_arquivo_boleto": nome_arquivo_boleto,
        "nome_banco_destinatario": nome_banco_destinatario[0],
        "num_banco": num_banco[0],
        "codigo_canal_operacao": "BKL",
        "codigo_operador": "889911348",
        "etapa_processo_boleto": "efetivacao",
        "valor": valor[0],
        "base_linha_digitavel": base_linha_digitavel,
        "base_dac": base_dac,
        "parcela": (venda, parcela),
        "beneficiario": {
            "id_beneficiario": id_beneficiario[0],
            "nome_cobranca": beneficiario[0],
            "dados_agencia": dados_agencia[0],
            "conta": str(conta[0]),
            "tipo_pessoa": {
                "codigo_tipo_pessoa": beneficiario_codigo_tipo_pessoa[0],
                "cpf_cnpj_beneficiario": str(cpf_cnpj_beneficiario[0]),
            },
            "endereco": {
                "nome_logradouro": "R PORTUGAL, 13, EDF T NOVO 1 AN",
                "nome_bairro": "COMERCIO",
                "nome_cidade": "SALVADOR",
                "sigla_UF": "BA",
                "numero_CEP": "40015000",
            },
        },
        "dado_boleto": {
            "descricao_instrumento_cobranca": "boleto",
            "forma_envio": "impressao",
            "tipo_boleto": "a vista",
            "pagador": {
                "pessoa": {
                    "nome_pessoa": pagador[0],
                    "nome_fantasia": pagador_nomefantasia[0],
                    "tipo_pessoa": {
                        "codigo_tipo_pessoa": pagador_codigo_tipo_pessoa,
                        "cpf_cnpj_pagador": str(cpf_cnpj_pagador),
                    },
                },
                "endereco": {
                    "nome_logradouro": nome_logradouro[0],
                    "nome_bairro": nome_bairro[0],
                    "nome_cidade": nome_cidade[0],
                    "sigla_UF": sigla_UF[0],
                    "numero_CEP": numero_CEP[0],
                },
                "mensagem_email": "Refere-se ao produto/serviço prestado ",  # O campo pode ser preenchido de forma personalizada. Máximo caracteres: 200
                "assunto_email": "Boleto Itaú",  # O campo pode ser preenchido de forma personalizada. Máximo caracteres: 50
                "texto_endereco_email": "joao@itau.com.br",  # 	Caso seja informado 'email' no campo dado_boleto > forma_envio, é obrigatório informar um e-mail válido no campo dado_boleto > pagador > texto_endereço_email. Máximo caracteres: 200
                "pagador_eletronico_DDA": false,
                "praca_protesto": true,
                "telefone_empresa": telefone_empresa[0],
            },
            "sacador_avalista": {
                "pessoa": {
                    "nome_pessoa": pagador[0],
                    "nome_fantasia": pagador_nomefantasia[0],
                    "tipo_pessoa": {
                        "codigo_tipo_pessoa": pagador_codigo_tipo_pessoa,
                        "cpf_cnpj_pagador": str(cpf_cnpj_pagador),
                    },
                },
                "endereco": {
                    "nome_logradouro": nome_logradouro[0],
                    "nome_bairro": nome_bairro[0],
                    "nome_cidade": nome_cidade[0],
                    "sigla_UF": sigla_UF[0],
                    "numero_CEP": numero_CEP[0],
                },
            },
            "codigo_carteira": codigo_carteira,
            "codigo_tipo_vencimento": 3,
            "valor_total_titulo": valor_titulo[
                0
            ],  # Valor total a ser cobrado. Sendo 15 dígitos inteiros e 2 casas decimais. Exemplo: 99999999999999900
            "dados_individuais_boleto": [
                {
                    "id_boleto_individual": id_boleto_individual,  # "8835353e-ecb5-43f8-adeb-4cbf796f6be4",
                    "numero_documento": num_documento,
                    "numero_nosso_numero": numero_nosso_numero,  # Número de identificação do título. De livre utilização do usuário seguindo as regras da carteira do produto contratado. Não pode ser repetido se nosso número ainda estiver ativo ou tiver menos de 45 dias de sua baixa/liquidação. Nosso número é obrigatório para carteira 109. Máximo: 08 caracteres.
                    "dac_titulo": "8",
                    "data_vencimento": data_vencimento[
                        0
                    ],  # Data máxima para pagamento do título sem que haja acréscimo de juros e multa. Formato: AAAA-MM-DD
                    "valor_titulo": valor_titulo[
                        0
                    ],  # Valor a ser cobrado. Formato do campo: 15 dígitos inteiros e 2 casas decimais
                    "codigo_barras": cod_barras,
                    # "34192863800000100011570000105681500052061000",
                    "numero_linha_digitavel": numero_linha_digitavel,  # "34191570070010568150600520610007286380000010001",
                    "data_limite_pagamento": "2031-06-01",  # Data limite para pagamento do título. Após esta data, o título não poderá ser pago. Informar, no mínimo a data de vencimento, e no máximo data futura de 10 anos. Caso não seja informada a data, será assumido como 10 anos. Formato: AAAA-MM-DD
                    "lista_mensagens_cobranca": [],
                }
            ],
            "multa": {
                "codigo_tipo_multa": "02",  # Código da multa '01' - Quando se deseja cobrar um valor fixo de multa após o vencimento. '02' - Quando se deseja cobrar um percentual do valor do título de multa após o vencimento. '03' - Quando não se deseja cobrar multa caso o pagamento seja feito após o vencimento (isento)
                "valor_multa": "",  # Valor da multa cobrada. Obrigatório para codigo_tipo_multa 01. Valor calculado deve ser superior a R$0,01. Formato do campo: 15 dígitos inteiros e 2 casas decimais. Exemplo: 99999999999999900.
                "percentual_multa": "000000100000",  # Percentual da multa cobrada. Obrigatório para tipo_multa 02. Valor calculado deve ser superior a R$0,01. Formato do campo: 7 dígitos inteiros e 5 casas decimais. Exemplo: 999999900000.
                "data_multa": "2024-09-21",  # Data de início de cobrança de multa. Caso o campo esteja vazio, será automaticamente assumido que a cobrança de multa se inicia logo após o vencimento. Formato: AAAA-MM-DD
            },
            "juros": {
                "codigo_tipo_juros": 90,
                "data_juros": "2024-09-21",
                "percentual_juros": "000000100000",  # 	Percentual dos juros a ser cobrado. Valor calculado deve ser superior a R$0,01. Obrigatório para tipo_juros ‘90’, ‘91’ e ‘92’. Formato do campo: 7 dígitos inteiros e 5 casas decimais. Exemplo: 999999900000
            },
            "recebimento_divergente": {"codigo_tipo_autorizacao": "01"},
            "instrucao_cobranca": [
                {
                    "codigo_instrucao_cobranca": "2",  # Códigos das instruções de protesto. Só podem ser enviadas até 4 instruções. Se houverem mais comandos, iremos descartar um instrução aleatoriamente. Ver "Tabela de Instruções".
                    "quantidade_dias_apos_vencimento": 10,
                    "dia_util": false,
                }
            ],
            "protesto": {
                "protesto": true,  # Em caso de protesto informar "true". Em caso de não protesto não enviar o bloco de protesto OU enviar "false".
                "quantidade_dias_protesto": 10,  # 	Em caso de protesto "true" (campo acima) enviar a quantidade de dias, mínimo 1 e máximo 99. Em caso de protesto "false" não enviar quantidade de dias OU enviar valor zero.
            },
            "codigo_especie": "01",
            "data_emissao": data_emissao[0],
            "valor_abatimento": "000",  # Valor do abatimento do título. Este valor não pode superar o valor da cobrança. Formato do campo: 15 dígitos inteiros e 2 casas decimais
            "pagamento_parcial": false,
            "quantidade_maximo_parcial": "0",
            "indicador_pagamento_parcial": true,  # Indicador de pagamento parcial. Caso não seja enviado, assume-se o padrão 'false'. 'true' - Aceita pagamento parcial. 'false' - Não aceita pagamento parcial.
            "lista_mensagem_cobranca": [
                {"mensagem": "jaime3 desconto fixo percentual"},
                {"mensagem": "teste2"},
            ],
            "recebimento_divergente": {
                "codigo_tipo_autorizacao": "03",
                "codigo_tipo_recebimento": "P",
                "percentual_minimo": "00000000000000000",
                "percentual_maximo": "00000000000000000",
            },
            "desconto": {
                "codigo_tipo_desconto": "90",  # Código do desconto. Caso exista mais de um desconto, todos os tipo_desconto deverão ter o mesmo código. '00' - Quando não houver condição de desconto – sem desconto '01' - Quando o desconto for um valor fixo se o título for pago até a data informada (data_desconto) '02' - Quando o desconto for um percentual do valor do título e for pago até a data informada (data_desconto) '90' - Percentual por antecipação(utilizando parâmetros do cadastro de beneficiário para dias úteis ou corridos)" '91' -Valor por antecipação (utilizando parâmetros do cadastro de beneficiário para dias úteis ou corridos)"
                "data_desconto": "",  # Data limite de cobrança de desconto. Caso o campo esteja vazio, será automaticamente assumido que a cobrança de desconto é até a data de vencimento. Formato: AAAA-MM-DD
                "descontos": [
                    {
                        "valor_desconto": "",  # 	Valor do desconto a ser cobrado. Obrigatório para codigo_tipo_desconto 1 ou 91. Valor calculado deve ser superior a R$0,01. Formato do campo: 15 dígitos inteiros e 2 casas decimais
                        "percentual_desconto": "10.00000",  # Percentual do desconto concedido. Obrigatório para codigo_tipo_desconto 2 ou 90. Valor calculado deve ser superior a R$0,01. Formato do campo: 7 dígitos inteiros e 5 casas decimais
                    }
                ],
            },
            "desconto_expresso": true,
        },
        "valor_juros": "",  # Valor dos juros a ser cobrado. Obrigatório para codigo_tipo_juros ‘93’. Valor deve ser superior a R$0,01. Formato do campo: 15 dígitos inteiros e 2 casas decimais. Exemplo: 99999999999999900
        "juros": "APÓS O VENCIMENTO COBRAR JUROS DE......... 0,55% AO MÊS",
        "observacao1": "APÓS O VENCIMENTO COBRAR MULTA DE......... 0,05%",
        "observacao2": "ATÉ 10.07.2020 CONCEDER DESCONTO DE 0,60%",
        "observacao3": "CONCEDER ABATIMENTO DE.................... R$15,10",
    }

    if erros_boleto:
        erros_boleto.append("para gerar o boleto")
        return erros_boleto
    else:
        dados_json = json.dumps(bd_boleto)
        dados_gerais = ContaReceber.objects.get(id=id_parcela)
        dados_gerais.dados_boleto = dados_json
        dados_gerais.save()
        emitirBoleto(bd_boleto)


def valida_dados_obrigatorios_notafiscal(form):
    """valida os dados do formulario para
    ter todos os campos obrigatorios
    conforme api
    https://focusnfe.com.br/doc/#nfe_campos-obrigatorios-de-uma-nfe

    """
    erros = []
    """ validacao
        Emitente
        cnpj_emitente: CNPJ do emitente da nota. Deve ser usado esse campo ou o "cpf_emitente".
        cpf_emitente: CPF do emitente da nota. Deve ser usado esse campo ou o "cnpj_emitente".
        inscricao_estadual_emitente: Informar a Inscrição Estadual do emitente.
        logradouro_emitente: Logradouro do emitente.
        numero_emitente: Número do logradouro do emitente.
        bairro_emitente: Bairro do emitente.
        municipio_emitente: Município do emitente.
        uf_emitente: UF do emitente.
        regime_tributario_emitente: Informar qual o regime tributário do emitente. Valores possíveis:
        1  Simples Nacional;

        2  Simples Nacional excesso de sublimite de receita bruta;

        3  Regime Normal.
    """

    remetente = Empresa.objects.first()
    destinatario = form.instance.cliente
    venda = form.instance
    if not remetente:
        erros.append("O cadastro do emitente está vazio")

    if remetente:
        if remetente.cpf and remetente.cnpj:
            erros.append(
                "O cadastro do emitente está com cpf e cnpj preenchido, preencha apenas um deles."
            )
        else:
            if remetente.cpf:
                if not validate_cpf(remetente.cpf.number):
                    erros.append("O cpf do emitente está inválido")
            if remetente.cnpj:
                if not validate_cnpj(remetente.cnpj.number):
                    erros.append("O cnpj do emitente está inválido")
        if not remetente.insc_estadual:
            erros.append("O cadastro do emitente está sem inscrição estadual.")
        if not remetente.logradouro:
            erros.append("O cadastro do emitente está sem logradouro.")
        if not remetente.numero:
            erros.append("O cadastro do emitente está sem numero.")
        if not remetente.bairro:
            erros.append("O cadastro do emitente está sem bairro.")
        if not remetente.estado:
            erros.append("O cadastro do emitente está sem estado.")
        if not remetente.cidade:
            erros.append("O cadastro do emitente está sem cidade.")
        if not remetente.regimetributario:
            erros.append("O cadastro do emitente está sem regimetributario.")
    #
    # fim validacao remetente
    #
    """ validacao
        Destinatário
        nome_destinatario: Nome completo do destinatário.
        cnpj_destinatario: CNPJ da empresa destinatária.
        cpf_destinatario: CPF do destinatário. Caso utilize este campo, não enviar o campo “cnpf_destinatario”.
        inscricao_estadual_destinatario: Informar a Inscrição Estadual do destinatário.
        logradouro_destinatario: Logradouro do destinatário.
        numero_destinatario: Número do logradouro do destinatário.
        bairro_destinatario: Bairro do destinatário.
        municipio_destinatario: Município do destinatário.
        uf_destinatario: UF do destinatário.
        indicador_inscricao_estadual_destinatario: Indicador da Inscrição Estadual do destinatário. Valores possíveis:
        1  Contribuinte ICMS (informar a IE do destinatário);

        2  Contribuinte isento de Inscrição no cadastro de Contribuintes do ICMS;

        9  Não Contribuinte, que pode ou não possuir Inscrição Estadual no Cadastro de Contribuintes do ICMS.
    """
    if not destinatario.nome:
        erros.append("O nome da empresa está vazio.")
    if not destinatario.cpf and not destinatario.cnpj:
        erros.append("O cliente está sem cpf e cnpj preenchido, preencha um deles.")
    elif destinatario.cpf and destinatario.cnpj:
        erros.append(
            "O cliente está com cpf e cnpj preenchido, preencha apenas um deles."
        )
    else:
        if destinatario.cpf:
            if not validate_cpf(destinatario.cpf.number):
                erros.append("O cpf do cliente está inválido")
        if destinatario.cnpj:
            if not validate_cnpj(destinatario.cnpj.number):
                erros.append("O cnpj do cliente está inválido")
            #if not destinatario.nome_fantasia:
            #    erros.append("O cliente está sem nome fantasia")
            if not destinatario.insc_estadual:
                erros.append("O cliente está sem inscrição estadual")

    if not destinatario.logradouro:
        erros.append("O cadastro do cliente está sem logradouro.")
    if not destinatario.cep:
        erros.append("O cadastro do cliente está sem cep.")
    if not destinatario.numero:
        erros.append("O cadastro do cliente está sem numero.")
    if not destinatario.bairro:
        erros.append("O cadastro do cliente está sem bairro.")
    if not destinatario.cidade:
        erros.append("O cadastro do cliente está sem cidade.")
    if not destinatario.estado:
        erros.append("O cadastro do cliente está sem estado.")
    if not destinatario.contribuinte_inss:
        erros.append("O cadastro do cliente está sem estado.")

    """
    valida se impostos do produto estão preenchidos
    
    """
    produtos = form.instance.vendaproduto_set.all()
    _produtos = {}
    for o in produtos:
        _produtos["quantidade"] = o.quantidade
        _produtos["preco"] = o.preco
        _produtos["subtotal"] = o.subtotal
        _produtos["codigoproduto"] = o.produto.codigoproduto
        _produtos["nome"] = o.produto.nome
        _produtos["ncm"] = o.produto.ncm
        _produtos["cst"] = o.produto.cst
        _produtos["cfop"] = o.produto.cfop
        _produtos["unimed"] = o.produto.unimed

    lista_produtos = _produtos
    # validando produtos
    for o in produtos:
        if o.quantidade < 1:
            erros.append("O produto " + o.produto.nome + " está sem quantidade.")
        if o.preco < 1:
            erros.append("O produto " + o.produto.nome + " está sem preco.")
        if o.subtotal < 1:
            erros.append("O produto " + o.produto.nome + " está sem total.")
        if not o.produto.codigoproduto:
            erros.append("O produto " + o.produto.nome + " está sem código do produto.")
        if not o.produto.nome:
            erros.append("O produto " + o.produto.nome + " está sem nome.")
        if not o.produto.ncm:
            erros.append("O produto " + o.produto.nome + " está sem ncm.")
        if not o.produto.cst:
            erros.append("O produto " + o.produto.nome + " está sem cst.")
        if not o.produto.cfop:
            erros.append("O produto " + o.produto.nome + " está sem cfop.")
        if not o.produto.unimed:
            erros.append("O produto " + o.produto.nome + " está sem unidade de medida.")
        #if not o.produto.aliq_ipi:
        #    erros.append("O produto " + o.produto.nome + " está sem ipi.")
        if not o.produto.aliq_icms_interno:
            erros.append("O produto " + o.produto.nome + " está sem imcs.")

    # validando transportadora
    if venda.transportadora:
        if venda.transportadora.nome not in ("Cliente Retira", "Fabrica entrega") :
            if venda.transportadora.cnpj:
                if not validate_cnpj(venda.transportadora.cnpj.number):
                    erros.append("O cnpj da transportadora está inválido")
            if not venda.transportadora.insc_estadual:
                erros.append("A Inscrição estadual da transportadora não foi informado")


    return erros
