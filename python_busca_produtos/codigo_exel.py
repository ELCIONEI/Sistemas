#instale no terminal o pyautogui-"pip install pyutogui"
#Instale o pandas - "pip install pandas openpyxl", o openpyxl dará outras funcionalidades ao pandas.
#Importe o pyautogui
import pyautogui
import time
pyautogui.PAUSE = 3 #Aguardará 3 segundos entre um comando e outro.
#time.sleep() # se desejar aumentar o tempo de execução em ponto especifico do codigo.

#1° passo - acessar a planilha em que os dados serão gravados

#pressione a tecla windows
pyautogui.press("win")
#escreva libre
pyautogui.write("libre")#Abrirá a planilha libreoffice
#pressione enter
pyautogui.press("enter")
#clic nesta posição - Abrirá a tabela
pyautogui.click(x=303, y=244)#clic para abrir a planilha
#clic nesta possição - Será a posição da primeira celula da planilha, na coluna codigo.
pyautogui.click(x=61, y=203)

#2° - Passo construir o laço para gravar sem que indicamos os dados, será feito automaticamente.

#Agora que ja estamos acessando a planilha, iniciaremos a gravação dos dados que desejamos.
#Importar a base de dados
import pandas # O pandas é para acessar a base de dados
#crie a variavel para armazenar as informações da base de dados(dei o nome de tabela)
tabela = pandas.read_csv("automacao\produtos.csv")

#3° Passo - Gravar os produtos na tabela

for linha in tabela.index:
    
    #Gravar o codigo
    codigo = tabela.loc[linha, 'codigo']
    pyautogui.write(str(codigo))
    pyautogui.press('tab')
    
    #Gravar a marca
    marca = tabela.loc[linha, 'marca']
    pyautogui.write(str(marca))
    pyautogui.press("tab")
    
    #gravar o tipo
    tipo = tabela.loc[linha, 'tipo']
    pyautogui.write(str(tipo))
    pyautogui.press("tab")
    
    #gravar a categoria
    categoria = tabela.loc[linha, 'categoria']
    pyautogui.write(str(categoria))
    pyautogui.press("tab")
    
    #gravar o preço
    preco_unitario = tabela.loc[linha, 'preco_unitario']
    pyautogui.write(str(preco_unitario))
    pyautogui.press("tab")
    
    #gravar o custo 
    custo = tabela.loc[linha, 'custo']
    pyautogui.write(str(custo))
    pyautogui.press('tab')
    
    #gravar Observação(obs)
    obs = str(tabela.loc[linha, 'obs'])
    if obs != 'nan':
        pyautogui.write(str(obs))
    pyautogui.press("enter")
    pyautogui.press("home")
#O sistema foi desenvolvido usando o libreoffice para gravar na planilha.
#Pega as informações desejadas da base de dados e monta uma planilha, a planilha fica a sua escolha.
# O codigo auxilia eu usei para capturar a posição do mouser em determinado ponto onde eu queria que o clic automatico ocorrece.
# O tempo pyautogui.PAUSE = 3 , foi porque o meu computador é muito lento.