# Tela de loguin com os capmos usuario e senha.
import tkinter as tk     #importa as bibliotecas para construção de telas
from tkinter import messagebox
from tkinter import PhotoImage

# Função de loguin
def login():
    usuario = entrada_usuario.get()
    senha = entrada_senha.get()
    if usuario == "admin" and senha == "1234":  # Exemplo de validação simples
        messagebox.showinfo("Login", "Login realizado com sucesso!")
    else:
        messagebox.showwarning("Erro", "Usuário ou senha incorretos!")

def sair():
    janela.destroy()

# Janela principal
janela = tk.Tk()
janela.title("Tela de Login")
janela.geometry("400x300")  # Define tamanho da janela
janela.resizable(False, False)  # Desabilita redimensionamento
# Define cor de fundo da janela



tk.Label(janela, text="Usuário:").pack(pady=10)
entrada_usuario = tk.Entry(janela)
entrada_usuario.pack()

tk.Label(janela, text="Senha:").pack(pady=10)
entrada_senha = tk.Entry(janela, show="*")
entrada_senha.pack()

tk.Button(janela, text="Acessar", command=login).pack(pady=12)
tk.Button(janela, text="CANCELAR", command=sair).pack()

# Chamada da janela
janela.mainloop()

