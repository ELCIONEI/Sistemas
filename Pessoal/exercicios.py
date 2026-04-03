#\Solicita uma nota
# informa nota invalida se estiver fora dos padroes
# continua solicitando uma nota valida, caso continuem digitando uma nota invalida.\#

nota = float(input('informe a nota:'))

while not (0 <= nota <= 10):
    print('nota invalida: ')
    nota = float(input('informe a nota:'))
"""
#### 2. Faça um programa que leia um nome de usuário e a sua senha:
# e não aceite a senha igual ao nome do usuário, 
# mostrando uma mensagem de erro e voltando a pedir as informações.
"""
login = input('informe o login: ')
senha = input('informe a senha: ')

while login == senha:
    print('login e senha são iguais, acesso invalido:')
    login = input("informe o login:! ")
    senha = input('Informe a senha diferente do login:! ')
"""
#### 3. Faça um programa que leia e valide as seguintes informações:
# continue pedindo a informação até o usuário inserir corretamente):
##### Nome: maior que 3 caracteres;
##### Idade: entre 0 e 150;
##### Salário: maior que zero;
##### Sexo: 'f' ou 'm';
##### Estado Civil: 's', 'c', 'v', 'd';

"""
nome = input('Informe o nome! ')

while len(nome)  < 4:
    print('Informe um nome com mais de 4 carateres')
    nome = input('Informe o nome! ')

idade = int(input('Informe a idade:! '))

while not ( 0 <=  idade <= 150):
    print('Idade invalida:! ')
    idade = int(input('Informe a idade:! '))
    
"""
#### 4. Supondo que a população de um país A seja da ordem de 80000 habitantes 
# com uma taxa anual de crescimento de 3% 
# e que a população de B seja 200000 habitantes 
# com uma taxa de crescimento de 1.5%. 
# Faça um programa que calcule e escreva o número de anos necessários 
# para que a população do país A ultrapasse ou iguale a população do país B, 
# mantidas as taxas de crescimento.
"""
populacao_A = 80000
populacao_B = 200000
tempo = 0

while populacao_A < populacao_B:
    populacao_A *= 1.03
    populacao_B *= 1.015
    tempo += 1
print('São necessários', tempo, 'anos para a população A igualar ou superar a população B:')
"""
#### 5. Altere o programa anterior permitindo ao usuário informar as populações e as taxas de crescimento iniciais. 
# Valide a entrada e permita repetir a operação.

"""
repete = 's'

while repete == 's':

    populacao_A = int(input('Informe a população A: '))
    populacao_B = int(input('Informe a população B: '))

    while populacao_A <= 0 or populacao_B <= 0:
        print('As populações precisam ser maiores que zero')
        populacao_A = int(input('Informe a população A: '))
        populacao_B = int(input('Informe a população B: '))

    taxa_A = float(input('Informe a taxa de crescimento da população A em porcentagem (exemplo: entre 3 para 3%): '))
    taxa_B = float(input('Informe a taxa de crescimento da população A em porcentagem (exemplo: entre 3 para 3%): '))

    while taxa_A <= 0 or taxa_B <= 0:
        print('As taxas precisam ser maiores que zero')
        taxa_A = float(input('Informe a taxa de crescimento da população A em porcentagem (exemplo: entre 3 para 3%): '))
        taxa_B = float(input('Informe a taxa de crescimento da população A em porcentagem (exemplo: entre 3 para 3%): '))

    taxa_A = taxa_A / 100 + 1
    taxa_B = taxa_B / 100 + 1

    tempo = 0

    while populacao_A < populacao_B:
        populacao_A *= taxa_A
        populacao_B *= taxa_B
        tempo += 1

    print('São necessários', tempo, 'anos para a população A igualar ou superar a população B')
    
    repete = input('Deseja repetir a operação? Tecle "s" para sim, qualquer outra tecla para não.')

"""

#### 6. Faça um programa que peça para o usuário inserir o faturamento dos últimos 5 meses 
# (individualmente) e informe o maior faturamento
 
"""   
for i in range (5):
    faturamento = float(input('Informe o faturamento do mês: '))
    if i == 0:
        maior = faturamento
    else:
        if faturamento > maior:
            maior = faturamento
print('O faturamento maior foi de: R$',maior)
"""
"""
#### 7. Faça um programa que peça para o usuário inserir o faturamento dos últimos 5 meses
# (individualmente) e informe o faturamento total (soma) e o faturamento médio por mês (média).
total = 0
for i in range(5):
    faturamento = float(input(f'Informe o faturamento do {i+1}ª mês: '))
    total += faturamento
print('O faturamento total foi de: R$',total, 'mensal.')
print('A media mensal do faturamento foi de: R$',total / 5)
"""

#### 8. Faça um programa que consiga categorizar a idade das equipes de uma empresa. 
# Faça um programa que peça para n pessoas a sua idade, 
# ao final o programa devera verificar se a média de idade da equipe varia entre:
# 0 e 25 (jovem) ,26 e 60 (sênior) e maior que 60 (idosa); 
# e então, dizer se a equipe é jovem, sênior ou idosa, conforme a média calculada.

"""
qtdade = int(input('Informe quantos membros terá a equipe: '))
total = 0
for i in range(qtdade):
    idade = int(input(f'Informe a idade do {i+1}ª membro: '))
    total += idade
media = total / qtdade
if 0 <=  media <= 25:
    print('Equipe jovem:')
    print('A media de idade da equipe é de: ',media, 'anos.')

elif 25 < media <= 60:
    print('Equipe adulta:')
    print('A media de idade da equipe é de: ',media,'anos.')
elif 60 < media:
    print('Equipe idosa.')
    print('A media de idade da equipe é de: ',media, 'anos')

"""
"""
#### 9. Numa eleição existem três candidatos. 
# Faça um programa que peça o número total de eleitores. 
# Peça para cada eleitor votar e ao final mostrar o número de votos de cada candidato.

qtdade = int(input('Informe o numero de eleitores: '))

candidato1 = 0
candidato2 = 0
candidato3 = 0

for i in range(qtdade):
    votar = int(input(f'Voto do {i+1}º eleitor: candidato 1, 2, ou 3.'))
    
    if votar == 1:
        candidato1 += 1
    elif votar == 2:
        candidato2 += 1
    elif votar == 3:
        candidato3 += 1
print('O candidato - 1 obteve: ',candidato1, 'votos.')
print('O candidato - 2 obteve: ',candidato2, 'votos.')
print('O candidato - 3 obteve: ',candidato3, 'votos.')


#### 10. Faça um programa que calcule o valor total investido por um colecionador em sua coleção de CDs
#e o valor médio gasto em cada um deles. 
# O usuário deverá informar a quantidade de CDs e o valor para em cada um.

qtdade = int(input('informe a quantidade de CDs comprados: '))

for i in range(qtdade):
    valor = float(input(f'Informe o valor pago {i+1}º CD: '))
    valortotal = valor *qtdade
print('O valor total gasto em CDs foi de: R$',valortotal, 'Reais')
print('Foi gasto uma media de: R$',valortotal / qtdade, 'Reais por CD.')

"""

#### 11. O Sr. Manoel Joaquim possui uma grande loja de artigos de R\\$ 1,99, 
# com cerca de 10 caixas. 
# Para agilizar o cálculo de quanto cada cliente deve pagar 
# ele desenvolveu uma tabela que contém o número de itens que o cliente comprou 
# e ao lado o valor da conta. 
# Desta forma a atendente do caixa precisa apenas contar quantos itens o cliente está levando 
# e olhar na tabela de preços. 
# Você foi contratado para desenvolver o programa que monta esta tabela de preços, 
# que conterá os preços de 1 até 50 produtos, conforme o exemplo abaixo:
"""
"""
<pre>
Lojas Quase Dois - Tabela de preços
1 - R$ 1.99
2 - R$ 3.98
...
50 - R$ 99.50
</pre>
 """ 
print('***Emanoel * Bugigangas***')

for i in range(50):
    print(f'O {i+1}º produto custou R$ {(i+1)*1.99:.2f} Reais')
    


#### 12. Um funcionário de uma empresa recebe aumento salarial anualmente: Sabe-se que:
"""<pre>
Esse funcionário foi contratado em 1995, com salário inicial de R$ 1.000,00;
Em 1996 recebeu aumento de 1,015% sobre seu salário inicial;
A partir de 1997 (inclusive), os aumentos salariais sempre correspondem ao dobro do percentual do ano anterior. 
Faça um programa que determine o salário desse funcionário em 2003. 
</pre>
"""

salario = 1000
aumento = 0.015

for i in range(1997, 2004):
    salario *= (1 + aumento)
    aumento *= 2

print('O salario do funcionario em 2003 era de: R$ {:.2f}'.format(salario)) 



""" 13. O cardápio de uma lanchonete é o seguinte:
<pre>
Especificação   Código  Preço
Cachorro Quente 100     R$ 1,20
Bauru Simples   101     R$ 1,30
Bauru com ovo   102     R$ 1,50
Hambúrguer      103     R$ 1,20
Cheeseburguer   104     R$ 1,30
Refrigerante    105     R$ 1,00
Faça um programa que leia o código dos itens pedidos e as quantidades desejadas. 
Calcule e mostre o valor a ser pago por item (preço * quantidade) e o total geral do pedido. 
Considere que o cliente deve informar quando o pedido deve ser encerrado.
</pre>

"""
cachorroquente = 100
total = 0

codigo = input('informe o codigo do produto ou digite "sair": ')

while codigo != 'somar':
    qtdade = int(input('informe a quantidade que deseja comprar: '))
    
    if codigo == '100':
        total += 1.2 * qtdade
    elif codigo == '101':
        total += 1.3 * qtdade
    elif codigo == '102':
        total += 1.5 * qtdade
    elif codigo == '103':
        total += 1.2 * qtdade
    elif codigo == '104':
        total += 1.3 * qtdade
    elif codigo == '105':
        total += 1.2 * qtdade
    else:
        print('O Codigo não existe:')    
    codigo = input('informe o codigo do produto ou digite "somar": ')
print('O valor total dos produtos é de: R$',total)
    