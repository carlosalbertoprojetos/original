from django.urls import reverse_lazy as _


ESCOLHAS_ESTADO = (
    ("AC", "AC"),
    ("AL", "AL"),
    ("AP", "AP"),
    ("AM", "AM"),
    ("BA", "BA"),
    ("CE", "CE"),
    ("DF", "DF"),
    ("ES", "ES"),
    ("GO", "GO"),
    ("MA", "MA"),
    ("MT", "MT"),
    ("MS", "MS"),
    ("MG", "MG"),
    ("PA", "PA"),
    ("PB", "PB"),
    ("PE", "PE"),
    ("PI", "PI"),
    ("PR", "PR"),
    ("RJ", "RJ"),
    ("RN", "RN"),
    ("RO", "RO"),
    ("RR", "RR"),
    ("RS", "RS"),
    ("SC", "SC"),
    ("SE", "SE"),
    ("SP", "SP"),
    ("TO", "TO"),
)

ESCOLHAS_ESTADO2 = [
    "AC",
    "AL",
    "AP",
    "AM",
    "BA",
    "CE",
    "DF",
    "ES",
    "GO",
    "MA",
    "MT",
    "MS",
    "MG",
    "PA",
    "PB",
    "PR",
    "PE",
    "PI",
    "RJ",
    "RN",
    "RS",
    "RO",
    "RR",
    "SC",
    "SP",
    "SE",
    "TO",
]

TIPO = (("Compra", "compra"), ("Venda", "venda"), ("Outros", "outros"))

ESCOLHAS_STATUS = (
    ("pendente", "Pendente"),
    ("aguardando", "Aguardando"),
    ("entregue", "Entregue"),
    ("cancelado", "Cancelado"),
)

FORMAS_PAGAMENTO = (
    ("Boleto", "Boleto"),
    ("Cheque", "Cheque"),
    ("Pix", "Pix"),
    ("Cartão", "Cartão"),
    ("Dinheiro", "Dinheiro"),
)

CONDICAO_PAGAMENTO = (
    ("15", "15/30/45"),
    ("30", "30/60/90"),
    ("45", "45/90/135"),
)

ESCOLHAS_STATUSVENDAS = (
    ("orcamento", "Orçamento"),
    ("autorizado", "Autorizado"),
    ("emproducao", "Em Produção"),
    ("expedicao", "Expedição"),
    ("nfemitida", "Nota Fiscal Emitida"),
    ("enviado", "Enviado"),
    ("cancelado", "Cancelado"),
)

ESCOLHAS_STATUSCOMPRAS = (
    ("solicitado", "Solicitado"),
    ("recebido", "Recebido"),
)

REGIMES_TRIBUTARIOS = (
    ("1", "Simples Nacional"),
    ("2", "Simples Nacional - excesso de sublimite de receita bruta"),
    ("3", "Regime Normal"),
)

CONTRIBUINTE_INSS = (
    ("1", "Simples Nacional"),
    ("2", "Simples Nacional - excesso de sublimite de receita bruta"),
    ("3", "Regime Normal"),
)


ESTADOS_NOME_SIGLA = {
    "ACRE": "AC",
    "ALAGOAS": "AL",
    "AMAPÁ": "AP",
    "AMAZONAS": "AM",
    "ACRE": "AC",
    "BAHIA": "BA",
    "CEARÁ": "CE",
    "ESPÍRITO SANTO": "ES",
    "GOIÁS": "GO",
    "MARANHÃO": "MA",
    "MATO GROSSO": "MT",
    "MATO GROSSO DO SUL": "MS",
    "MINAS GERAIS": "MG",
    "PARÁ": "PA",
    "PARAÍBA": "PB",
    "PARANÁ": "PR",
    "PERNAMBUCO": "PE",
    "PIAUÍ": "PI",
    "RIO DE JANEIRO": "RJ",
    "RIO GRANDE DO NORTE": "RN",
    "RIO GRANDE DO SUL": "RS",
    "RONDÔNIA": "RO",
    "RORAIMA": "RR",
    "SANTA CATARINA": "SC",
    "SÃO PAULO": "SP",
    "SERGIPE": "SE",
    "TOCANTINS": "TO",
    "DISTRITO FEDERAL": "DF",
}
