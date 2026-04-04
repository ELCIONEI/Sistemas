"""
Controle de estoque.
O sistema permitirá cadastrar,listar cadastros existententes,atualizar e remover produtos ja cadastrados do estoque
"""

#A parte principal do codigo, menu de opções de acesso.
def menu():
    controle = ControleEstoque
    while True:
        print('\n---*** Controle de Estoque ***---')
        
        print('1. Cadastro de Produto')
        print('2. Consultar Produto')
        print('3. Cadastrar  no Estoque')
        print('4. Excluir Produto')
        print('5. Sair do Sistema')
        opcao = input('Digite a opção Desejada: ')

        if opcao == '1':
            codigo = input('Informe o codigo do produto: ')
            nome = input('Informe o nome do produto: ')
            qtde = int(input('Informe a quantidade a ser cadastrada: '))
            preco = float(input('Informe o valor do produto: '))
        elif opcao == '2':
            controle.consultar_produtos()
        elif opcao == '3':
            codigo = int(input('Informe o codigo do produto: '))
            qtde = int(input('Informe a quantidade que deseja cadastrar: '))
        elif opcao == '4':
            codigo = int(input('Informe o codigo do Produto: '))
            controle.remover_produto(codigo)
        elif opcao == '5':
            print('***SAINDO DO SISTEMA***')
            break
        else:
            print('A sua Opcão é invalida.')

class Produto:#criando a classe do produto com os atributos
    def __init__(self, codigo, nome, qtde, preco):#o _init_ para niciar o objeto na estancia local
        self.codigo = codigo
        self.nome = nome        #self refere-se ao objeto atual da classe, permitindo acessar atributos e métodos dentro de uma instância específica.
        self.qtde = qtde
        self.preco = preco

    def __str__(self):  #O _str_ usado para retornar uma representação de string de um objeto.
        return f"[{self.codigo}] {self.nome} - qtde: {self.qtde}, Preço: R${self.preco:.2f}"
    
class ControleEstoque: #criando a classe do estoque
    def __init__(self):
        self.produtos = {}
    
    def cadastrar_produto(self, codigo, nome, qtde, preco):#função para cadastrar o produto
        if codigo in self.produtos:
            print('Codigo ja existente')
        else:
            self.produtos[codigo] = Produto(codigo, nome, qtde, preco )
            print(f"O produto '{nome}' foi cadastrado com sucesso!")
    
    def consultar_produto(self, nome, codigo):#função para consultar o estoque
        if not self.produtos: # caso o produto consultado não exista
            print('Nenhum produto cadastrado!')
        else:
            for produto in self.produtos.values():
                print(f'O produto {produto} foi localizado')
    
    def atualizar_estoque(self, codigo, qtde):#função para cadastrar o produto no estoque
        if codigo in self.produtos:
            self.produtos[codigo].qtde += qtde
            print(f"O produto '{self.produtos[codigo].nome}'foi atualizado no estoque ")
        else:
            print('Produto não cadastrado!')
    
    def remover_produto(self, codigo):
        if codigo in self.produtos:
            removido = self.produtos.pop(codigo)
            print(f"O Produto '{removido.nome}' foi removido do estoque! ")
        else:
            print('Produto não localizado para remoção:!')

if __name__ == "__main__":#permite que o codigo seja executado quando o programa python é executado como principal
    menu()
