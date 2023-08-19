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

TIPO = (("Compra", "compra"), ("Venda", "venda"), ("Outros", "outros"))

ESCOLHAS_STATUS = (
    ("Pendente", "pendente"),
    ("Aguardando", "aguardando"),
    ("Entregue", "entregue"),
    ("Cancelado", "cancelado"),
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
    ("enviado", "Enviado"),
)

ESCOLHAS_STATUSCOMPRAS = (
    ("solicitado", "Solicitado"),
    ("recebido", "Recebido"),
)