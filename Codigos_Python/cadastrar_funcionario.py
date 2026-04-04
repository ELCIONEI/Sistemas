"""
O sistema permitira cadastrar, retornará a lista de cadastro e realizar busca de um funcionario se cadastrado.
"""
def menu():# Aqui é onde voce encontra o Menu com as opçoes de acesso ao sistema
    sistema = SistemaCadastro()

    while True:
        print("===*** Sistema de Cadastro de Funcionários ***===")
        print("1. Cadastrar Funcionário")
        print("2. Listar Funcionários")
        print("3. Buscar Funcionário")
        print("4. Sair")
        
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            sistema.adicionar_funcionario()
        elif escolha == '2':
            sistema.listar_funcionarios()
        elif escolha == '3':
            sistema.buscar_funcionario()
        elif escolha == '4':
            print("*Saindo do Sistema!*")
            break
        else:
            print("Opção inválida! Tente novamente.\n")

class Funcionario: #criando a classe funcionario
    def __init__(self, nome, idade, cargo, salario):# o _init_para iniciar objetos
        self.nome = nome # o self para que seja acessada a variavel que pertence a classe
        self.idade = idade
        self.cargo = cargo
        self.salario = salario

    def __str__(self):#A função _str_que me retornará strings nos objetos da classe
        return f"Nome: {self.nome}, Idade: {self.idade}, Cargo: {self.cargo}, Salário: R${self.salario:.2f}"
        #retornando os objetos da classe
class SistemaCadastro: #Criando a classe cadastro
    def __init__(self):
        self.funcionarios = []

    def adicionar_funcionario(self):#criando a função adicionar funcionario que poderá ser chamada de qualquer parte do codigo
#Aqui é onde o fucnionario será cadastrado com as informações necessarias       
        nome = input("Digite o nome do funcionário: ")
        idade = int(input("Digite a idade do funcionário: "))
        cargo = input("Digite o cargo do funcionário: ")
        salario = float(input("Digite o salário do funcionário: "))
        funcionario = Funcionario(nome, idade, cargo, salario)
        self.funcionarios.append(funcionario)
        print("Funcionário cadastrado com sucesso!\n")

    def listar_funcionarios(self):#Aqui listará os funcionarios cadastrados
        if not self.funcionarios:
            print("Não há funcionários cadastrados.\n")
        else:#Retornará a lista de funcionarios se ja houver.
            print("Lista de Funcionários:")
            for f in self.funcionarios:
                print(f)
            print()

    def buscar_funcionario(self):#aqui buscará un fucnionario pelo nome
        nome = input("Digite o nome do funcionário que deseja buscar: ")
        encontrado = False
        for f in self.funcionarios:
            if f.nome.lower() == nome.lower():
                print(f"\nFuncionário encontrado: {f}\n")
                encontrado = True
                break            #retornará encontrado ou não encontrado
        if not encontrado:
            print("Funcionário não encontrado.\n")

if __name__ == "__main__":#permite que o codigo seja executado quando o programa python é executado como principal
    menu()
