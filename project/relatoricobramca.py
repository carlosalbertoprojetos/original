from venda.models import Venda

vendas =  Venda.objects.filter(vendedor__id=2,data_pedido__gt='2024-01-01')

for venda in vendas:
    print(venda.id)
