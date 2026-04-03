#Estrutura de repetição
# Faça um programa que leia um nome de usuário e a sua senha 
# e não aceite a senha igual ao nome do usuário, 
# mostrando uma mensagem de erro e voltando a pedir as informações.


repete = 's'

while repete == 's':
	login = input('Informe o nome de usuario! ')
	senha = input('Informe a senha! ')
	
	while login == senha:
		print('O login e a senha não podem ser iguais:')
		login = input('Informe o nome de usuario! ')
		senha = input('Informe a senha! ')
	while len (senha) < 6:
		print('A senha deve conter no minimo 6 caracteres! ')
		senha = input('Informe a senha! ')
	if senha  > 6:
		print('Usuario cadastrado com sucesso')
	repete = input('Digite "s" para repetir a operação ou ENTER para sair! ')

	

    