#### O usuário insere o faturamento dos últimos 5 meses (individualmente) e  o maior faturamento será informado pelo sistema.


for i in range (5):
    faturamento = float(input(f"informe o valor do faturamento no {i+1}° mes: "))
    if i == 0:
        maior = faturamento
    else:
        if faturamento > maior:
            maior = faturamento
print('R$',maior, 'foi o maior faturamento nos ultimos 5 meses!')


