from django.db import models
from django.urls import reverse_lazy as _
import datetime

from produto.models import Peca
from producao.models import ProdutoAcabado
from materiaprima.models import MateriaPrima

# from produto.models import ProdutoManufaturado


# Create your models here.
class EnderecoEstoque(models.Model):
    nome = models.CharField("Nome", max_length=200)

    def __str__(self):
        return self.nome


class EstoqueProdutoAcabado(models.Model):
    produtoacabado = models.ForeignKey(ProdutoAcabado, on_delete=models.RESTRICT)
    enderecoestoque = models.ForeignKey(EnderecoEstoque, on_delete=models.RESTRICT)
    qtde = models.FloatField()


class EstoqueMateriaPrima(models.Model):
    materiaprima = models.ForeignKey(MateriaPrima, on_delete=models.RESTRICT)
    enderecoestoque = models.ForeignKey(
        EnderecoEstoque, on_delete=models.RESTRICT, default=1
    )
    qtde = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        verbose_name = "Estoque de Materia Prima"
        verbose_name_plural = "Estoque de Materias Prima"
        ordering = ["materiaprima"]

    def __str__(self):
        return self.materiaprima.nome

    def estoque_mp_edit(self):
        return _("estoque:confereEstoque", args=[self.pk])


class ConferenciaEstoque(models.Model):
    materiaprima = models.ForeignKey(EstoqueMateriaPrima, on_delete=models.RESTRICT)
    usuario = models.CharField(max_length=255, null=True, blank=True)
    qtde = models.IntegerField()
    data = models.DateField(default=datetime.date.today)
    conferencia = models.IntegerField(default=0)
    relatorio = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.materiaprima.materiaprima.nome


class EstoquePecaAcabada(models.Model):
    peca = models.ForeignKey(Peca, on_delete=models.RESTRICT)
    usuario = models.CharField(max_length=255, null=True, blank=True)
    enderecoestoque = models.ForeignKey(
        EnderecoEstoque, on_delete=models.RESTRICT, default=1
    )
    quantidade = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    criadoem = models.DateTimeField(auto_now_add=True)
    atualizadoem = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = verbose_name_plural = "Estoque de Peças"
        ordering = ["peca"]

    def __str__(self):
        return self.peca.nome


class ConferenciaEstoquePeca(models.Model):
    peca = models.ForeignKey(Peca, on_delete=models.RESTRICT)
    usuario = models.CharField(max_length=255, null=True, blank=True)
    quantidade = models.IntegerField()
    data = models.DateField(default=datetime.date.today)
    conferencia = models.IntegerField(default=0)
    relatorio = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.peca.nome


{
    "@Id": "NFe35230164966559000153550010000458961077391001",
    "@versao": "4.00",
    "ide": {
        "cUF": "35",
        "cNF": "07739100",
        "natOp": "6.401 - Venda de producao do estabelec",
        "mod": "55",
        "serie": "1",
        "nNF": "45896",
        "dhEmi": "2023-01-03T00:00:00-02:00",
        "dhSaiEnt": "2023-01-03T00:00:00-02:00",
        "tpNF": "1",
        "idDest": "2",
        "cMunFG": "3547304",
        "tpImp": "1",
        "tpEmis": "1",
        "cDV": "1",
        "tpAmb": "1",
        "finNFe": "1",
        "indFinal": "0",
        "indPres": "0",
        "procEmi": "0",
        "verProc": "Hermes :795122",
    },
    "emit": {
        "CNPJ": "64966559000153",
        "xNome": "ZUFER TECNOLOGIA E FERRAMENTARIA LTDA",
        "xFant": "ZUFER",
        "enderEmit": {
            "xLgr": "RUA MATO GROSSO",
            "nro": "32",
            "xBairro": "CHACARA SOLAR",
            "cMun": "3547304",
            "xMun": "SANTANA DE PARNAIBA",
            "UF": "SP",
            "CEP": "06530445",
            "cPais": "1058",
            "xPais": "BRASIL",
            "fone": "41568800",
        },
        "IE": "623020769115",
        "CRT": "3",
    },
    "dest": {
        "CNPJ": "27980581000121",
        "xNome": "EDER SAULO COSTA 06073667612",
        "enderDest": {
            "xLgr": "RUA CLEMENTE NETO SILVA",
            "nro": "376",
            "xBairro": "Filadelfia",
            "cMun": "3106705",
            "xMun": "Betim",
            "UF": "MG",
            "CEP": "32670042",
            "cPais": "1058",
            "xPais": "BRASIL",
            "fone": "31988737892",
        },
        "indIEDest": "1",
        "IE": "0029868940028",
        "email": "alexsandrahelena@hotmail.com",
    },
    "det": {
        "@nItem": "1",
        "prod": {
            "cProd": "ZF2612",
            "cEAN": "7898413753452",
            "xProd": "KIT RALO COM SIFAO ANEL DE VEDACAO E PARAFUSO",
            "NCM": "84189900",
            "CFOP": "6401",
            "uCom": "PC",
            "qCom": "300.0000",
            "vUnCom": "7.04220000",
            "vProd": "2112.66",
            "cEANTrib": "7898413753452",
            "uTrib": "PC",
            "qTrib": "300.0000",
            "vUnTrib": "7.04220000",
            "indTot": "1",
        },
        "imposto": {
            "vTotTrib": "354.93",
            "ICMS": {
                "ICMS10": {
                    "orig": "0",
                    "CST": "10",
                    "modBC": "0",
                    "vBC": "2112.66",
                    "pICMS": "12.00",
                    "vICMS": "253.52",
                    "modBCST": "4",
                    "pMVAST": "51.15",
                    "pRedBCST": "0.00",
                    "vBCST": "3504.63",
                    "pICMSST": "18.00",
                    "vICMSST": "377.31",
                }
            },
            "IPI": {
                "CNPJProd": "00000000000000",
                "cSelo": "NA",
                "qSelo": "0",
                "cEnq": "999",
                "IPITrib": {
                    "CST": "50",
                    "vBC": "2112.66",
                    "pIPI": "9.75",
                    "vIPI": "205.98",
                },
            },
            "PIS": {
                "PISAliq": {
                    "CST": "01",
                    "vBC": "2112.66",
                    "pPIS": "0.65",
                    "vPIS": "13.73",
                }
            },
            "COFINS": {
                "COFINSAliq": {
                    "CST": "01",
                    "vBC": "2112.66",
                    "pCOFINS": "3.00",
                    "vCOFINS": "63.38",
                }
            },
        },
        "infAdProd": "Lote: 2098 Qtd: 300",
    },
    "total": {
        "ICMSTot": {
            "vBC": "2112.66",
            "vICMS": "253.52",
            "vICMSDeson": "0.00",
            "vFCP": "0.00",
            "vBCST": "3504.63",
            "vST": "377.31",
            "vFCPST": "0.00",
            "vFCPSTRet": "0.00",
            "vProd": "2112.66",
            "vFrete": "0.00",
            "vSeg": "0.00",
            "vDesc": "0.00",
            "vII": "0.00",
            "vIPI": "205.98",
            "vIPIDevol": "0.00",
            "vPIS": "13.73",
            "vCOFINS": "63.38",
            "vOutro": "0.00",
            "vNF": "2695.95",
            "vTotTrib": "354.93",
        }
    },
    "transp": {
        "modFrete": "1",
        "transporta": {
            "CNPJ": "06349754000138",
            "xNome": "J SEDA NETO TRANSPORTES ME",
            "IE": "140402077118",
            "xEnder": "RUA MINISTRO CARVALHO MOURAO 129",
            "xMun": "Sao Paulo",
            "UF": "SP",
        },
        "vol": {"qVol": "3", "esp": "CAIXA", "pesoL": "35.400", "pesoB": "35.400"},
    },
    "cobr": {
        "fat": {
            "nFat": "45896",
            "vOrig": "2695.95",
            "vDesc": "0.00",
            "vLiq": "2695.95",
        },
        "dup": {"nDup": "001", "dVenc": "2023-01-03", "vDup": "2695.95"},
    },
    "pag": {"detPag": {"indPag": "0", "tPag": "15", "vPag": "2695.95"}},
    "infAdic": {
        "infCpl": "N.Pedido: 077391 00    ||Valor Aprox Tributos (Fed) R$: 147.20, (Est) R$: 245.68, (Mun) R$: 0.00"
    },
    "infRespTec": {
        "CNPJ": "00767276000108",
        "xContato": "Departamento Fiscal",
        "email": "financeiro@khan.com.br",
        "fone": "01140404040",
    },
}
