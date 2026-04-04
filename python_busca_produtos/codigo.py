#Instalar as bibliotecas - pip install pandas openpyxl nbformat ipykernel plotly numpy o

#passo 1: Importar a base de dados
import pandas as pd

tabela = pd.read_csv("cancelamentos_sample.csv")

print(tabela)



