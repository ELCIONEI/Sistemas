#o sistema calcula a media do aluno e ja informa toda a situação para o proximo ano letivo.

nota1 = float(input("Informe a nota do 1°_Bimestre: "))
if nota1 > 10:
    print("A nota informada é invalida: ", nota1)
else:
    print('Nota do 1°_Bimestre foi: ', nota1)

nota2 = float(input('Informe a nota do 2°_Bimestre: '))
if nota2 > 10:
    print('A nota informada é invalida: ', nota2)
else:
    print('A nota do 2°Bimestre foi:',nota2)

nota3 = float(input('Informe a nota do 3°_Bimestre: '))
if nota3 > 10:
    print("A nota informada é invalida: ",nota3)
else:
    print('A nota do 3°_Bimestre foi: ', nota3)

nota4 = float(input('Informe a nota do 4°_Bimestre: '))
if nota4 > 10:
    print('A nota informada é invalida:',nota4)
else:
    print('A nota do 4°_Bimestre foi: ', nota4)
    
media = (nota1 + nota2 + nota3 + nota4)/4

if media < 7:
    print('A Media semestral não foi alcançada: ')

    notaRecuperacao = float(input("Informe a nota de recumperação: "))
    if notaRecuperacao < 7:
        print('Aluno reprovado!!')
        print("A nota de recuperação foi: ", notaRecuperacao)
    else:
        print("Aluno Aprovado com Recuperação: ", notaRecuperacao)
        print("A nota de aprovação foi: ",notaRecuperacao)
else:
    print("Aluno aprovado")
    print('A media foi: ', media)



