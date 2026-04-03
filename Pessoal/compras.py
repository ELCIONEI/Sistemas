#SISTEMA DE COMPRAS ONLINE 

class Produto:         #Criando a classe produto e seus atributos
    def __init__(self, nome, preco, quantidade):
        self.nome = nome
        self.preco = preco
        self.quantidade = quantidade

    def __str__(self):
        return f"Nome: {self.nome} Valor: R$ {self.preco:.2f}  (Estoque: {self.quantidade})"


class Loja:        #Criando a classe loja com os atributos produtos  e carrinho. 
    def __init__(self):
        self.produtos = []
        self.carrinho = []
    #Função para adicionar os produtos
    def adicionar_produto(self, produto):
        self.produtos.append(produto)
    #Função para listar os produtos em estoque
    def listar_produtos(self):
        print("\nProdutos disponíveis:")
        for i, produto in enumerate(self.produtos):
            print(f"{i + 1}. {produto}")
    #Função para adicionar os prdutos escolhidos ao carrinho
    def adicionar_ao_carrinho(self, indice, quantidade):
        if 0 <= indice < len(self.produtos):
            produto = self.produtos[indice]
            if produto.quantidade >= quantidade:
                self.carrinho.append((produto, quantidade))
                produto.quantidade -= quantidade
                print(f"\n{quantidade} unidade(s) de {produto.nome} adicionada(s) ao carrinho.")
            else:
                print("\nQuantidade insuficiente no estoque!")
        else:
            print("\nProduto inválido!")
    #Função para verificar os produtos do carrinho
    def visualizar_carrinho(self):
        print("\n* Carrinho de compras: *")
        if not self.carrinho:
            print("Seu carrinho está vazio.")
        else:
            total = 0
            for produto, quantidade in self.carrinho:
                subtotal = produto.preco * quantidade
                print(f"{produto.nome} - {quantidade} unidade(s) - Subtotal: R$ {subtotal:.2f}")
                total += subtotal
            print(f"\nTotal: R$ {total:.2f}")
    #Função para finalizar as compras
    def finalizar_compra(self):
        if not self.carrinho:
            print("\nO carrinho está vazio.!")
        else:
            self.visualizar_carrinho()
            print("\nCompra finalizada! Volte Sempre.")
            self.carrinho = []  # Esvazia o carrinho


# Simulação da loja
loja = Loja()

# Adicionando produtos na loja
loja.adicionar_produto(Produto("Camiseta", 50.00, 10))
loja.adicionar_produto(Produto("Calça Jeans", 120.00, 5))
loja.adicionar_produto(Produto("Tênis", 200.00, 8))
loja.adicionar_produto(Produto("Boné", 30.00, 20))

# Menu de acesso ao sistema
while True:
    print("\n---*** NEY MAGAZINE ***---")
    print("1. Listar produtos")
    print("2. Adicionar produto ao carrinho")
    print("3. Visualizar carrinho")
    print("4. Finalizar compra")
    print("5. Sair")

    opcao = input("\nDigite a opcão Desejada: ")

    if opcao == "1":
        print("---*** Listando Produtos ***---")
        loja.listar_produtos()
    elif opcao == "2":
        print("---*** Visualizando o Estoque ***---")
        loja.listar_produtos()
        try:
            indice = int(input("\nDigite o nome do produto que deseja comprar: ")) - 1
            quantidade = int(input("Digite a quantidade: "))
            loja.adicionar_ao_carrinho(indice, quantidade)
        except ValueError:
            print("\nEntrada inválida. Tente novamente.")
    elif opcao == "3":
        print("---*** Visualizando o Carrinho ***---")
        loja.visualizar_carrinho()
    elif opcao == "4":
        loja.finalizar_compra()
    elif opcao == "5":
        print("\nSAINDO ! Obrigado por comprar conosco: !")
        break
    else:
        print("\nOpção inválida. Tente novamente.")
print('*E.F.F*')
