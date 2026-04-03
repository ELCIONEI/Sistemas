produtos = ['tv', 'pc', 'teclado', 'mouse', 'notebook', 'ferro', 'panela']
valores = [1500, 1900, 250, 50, 2000, 450, 550 ]
vendas = [60, 350, 75, 50, 154, 85, 165]

produto = input('informe o nome do produto: ')

if produto in produtos :    
    i = produtos.index(produto)
    preco = valores[i]
    venda = vendas[i]
    print('você pesquisou pelo produto: ', produto)
    print('valor do produto é de: ', preco, 'Reais')
    print('O produto teve uma venda de : ',venda, 'Unidades mensal')
    
    comprar = input('Informe o nome do produto que deseja comprar? ')
    if comprar in produtos:        
        print('O produto escolhido foi: {}, o valor é de: {} ' . format(comprar, preco))
           
    else:
        print('Compra cancelada!')    
         
else:
    print('O produto {}: está em falta.'.format(produto))