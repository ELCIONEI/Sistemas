# Aqui são as bibliotecas do python, para a aplicação poder rodar
import customtkinter as ctk
import pyttsx3
import threading
import pandas as pd
import os
import pygame
import json
from datetime import datetime
import tkinter.messagebox as messagebox
from tkinter import filedialog
import tempfile
from screeninfo import get_monitors 
import pythoncom
import pygame._sdl2.audio as sdl2_audio

# ---A pasta PainelJson deve está na maquina da TV e compartilhada pela rede ---

def obter_caminho_json(setor=None):
    # Pasta base onde os arquivos ficarão
    diretorio_base = r"\\PC-01253243\PainelJson"
    
    # Se não existir a pasta, você pode decidir criar ou usar o padrão
    if not os.path.exists(diretorio_base):
        diretorio_base = tempfile.gettempdir() # Fallback para pasta temporária se rede falhar

    if setor:
        # Cria um nome de arquivo limpo (ex: dados_painel_RADIOLOGIA.json)
        nome_arquivo = f"dados_painel_{setor.replace(' ', '_')}.json"
        return os.path.join(diretorio_base, nome_arquivo)
    
    return os.path.join(diretorio_base, "dados_painel_geral.json")

class AppChamada(ctk.CTk):
    def __init__(self):
        super().__init__()
        #Dimensões da tela
        self.title("Chamada de Pacientes                               Suporte: elcioneifernandes@gmail.com")
        largura, altura = 600, 850
        self.centralizar_janela(largura, altura)
        
        pygame.mixer.init() 

        # --- VARIÁVEIS DE CONTROLE ---
        self.arquivo_setor_especifico = ""
        self.setor_atual = ""
        self.medico_atual = ""
        self.sala_atual = ""
        self.especialidade = ""
        self.genero_medico = "o"
        self.atendimentos = []
        self.lista_espera = []
        self.contador_senha = 1
        self.painel_janela = None
        self.zoom_manual = 1.0
        self.hist_slots = [] 

        self.main_frame = ctk.CTkFrame(self, fg_color="#dcdcec")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.tela_setup()

    def centralizar_janela(self, largura, altura):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (largura // 2)
        y = (screen_height // 2) - (altura // 2)
        self.geometry(f"{largura}x{altura}+{x}+{y}")

    def tela_setup(self):
        for widget in self.main_frame.winfo_children(): 
            widget.destroy()

        ctk.CTkLabel(self.main_frame, text="* Informações Obrigatórias*", font=("Roboto", 24, "bold"), text_color="#fa0808").pack(pady=30)
        
        ctk.CTkLabel(self.main_frame, text="Informe o Setor Corretamente:", font=("Roboto", 18, "bold")).pack()
        self.cb_setor = ctk.CTkComboBox(self.main_frame, values=["Setor Atual","PS-CG", "PNEUMOLOGIA","OFTALMOLOGIA","QUEIMADOS","RADIOLOGIA","BARIATRICA", "PRONTO-SOCORRO","CLASSIFICAÇÃO", "TRIAGEM", "AMBULATÓRIO","RECEPÇÃO","RECEPÇÃO 1","MARCAÇÃO","CENTRO-CIRURGICO",], width=350, font=("Roboto", 18))
        self.cb_setor.pack(pady=10)

        self.ent_medico = ctk.CTkEntry(self.main_frame, placeholder_text="Nome do Médico (a)", width=350, font=("Roboto", 20))
        self.ent_medico.pack(pady=10)

        self.ent_especialidade = ctk.CTkEntry(self.main_frame, placeholder_text="Especialidade (Ex: Psicologia)", width=350, font=("Roboto", 20))
        self.ent_especialidade.pack(pady=10)

        self.ent_sala = ctk.CTkEntry(self.main_frame, placeholder_text="Ex: Consultório 8 ou Sala", width=350, font=("Roboto", 20))
        self.ent_sala.pack(pady=10)
        
        ctk.CTkLabel(self.main_frame, text="Informe se é Doutor ou Doutora:", font=("Roboto", 18, "bold")).pack(pady=30)
        self.var_genero = ctk.StringVar(value="") 
        frame_genero = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        frame_genero.pack(pady=15)
        
        ctk.CTkRadioButton(frame_genero, text="Doutor (Dr.)", variable=self.var_genero, value="o", font=("Roboto", 18, "bold"), text_color="#0834fa").pack(side="left", padx=10)
        ctk.CTkRadioButton(frame_genero, text="Doutora (Dra.)", variable=self.var_genero, value="a", font=("Roboto", 18, "bold"), text_color="#fa08e6").pack(side="left", padx=10)
        
        ctk.CTkButton(self.main_frame, text="ACESSAR", command=self.confirmar_setup, font=("Roboto", 16, "bold"), height=45).pack(pady=30)

    def confirmar_setup(self):
        self.setor_atual = self.cb_setor.get()
        self.medico_atual = self.ent_medico.get().strip()
        self.especialidade = self.ent_especialidade.get().strip()
        self.sala_atual = self.ent_sala.get().strip()
        self.genero_medico = self.var_genero.get()
        self.arquivo_setor_especifico = obter_caminho_json(self.setor_atual)
        
        if self.setor_atual == "Setor Atual" or not self.setor_atual:
            messagebox.showwarning("Setor Inválido", "POR FAVOR!, INFORME O SETOR ATUAL.")
            return
        
        if not self.medico_atual or not self.sala_atual or self.genero_medico == "":
            messagebox.showwarning("Aviso", "Preencha todos os campos e selecione Dr./Dra.")
            return

        self.tela_atendimento()

    def tela_atendimento(self):
        for widget in self.main_frame.winfo_children(): 
            widget.destroy()
        
        prefixo = "Dr." if self.genero_medico == "o" else "Dra."
        espec_texto = f" ({self.especialidade})" if self.especialidade else ""
        cabecalho = f"{self.setor_atual}\n{prefixo} {self.medico_atual}{espec_texto}\n{self.sala_atual}"
        ctk.CTkLabel(self.main_frame, text=cabecalho, font=("Roboto", 18, "bold"), text_color="#fa0808").pack(pady=10)

        ctk.CTkLabel(self.main_frame, text="Pacientes em Espera", font=("Roboto", 16, "bold"), text_color="#121312").pack(anchor="w", padx=40)
        self.txt_lista_espera = ctk.CTkTextbox(self.main_frame, width=520, height=180)
        self.txt_lista_espera.pack(pady=5)
        self.txt_lista_espera.bind("<ButtonRelease-1>", self.carregar_paciente_clique)
        self.txt_lista_espera.tag_config("chamado", foreground="gray")

        frame_import = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        frame_import.pack(pady=5)
        ctk.CTkButton(frame_import, text="📂 Lista de Pacientes", command=self.importar_lista, width=100, fg_color="#fb8500").pack(side="left", padx=5)
        ctk.CTkButton(frame_import, text="🔢 Gera Senhas", command=self.gerar_senhas_lista, width=100).pack(side="left", padx=5)
        ctk.CTkButton(frame_import, text="🖨️ Imprimir Senhas", command=self.imprimir_etiqueta, width=100, fg_color="#fb8500").pack(side="left", padx=5)

        ctk.CTkLabel(self.main_frame, text="Ajuste de Zoom da TV", font=("Roboto", 10)).pack()
        self.slider_zoom = ctk.CTkSlider(self.main_frame, from_=0.5, to=2.0, command=self.ajustar_zoom_painel)
        self.slider_zoom.set(self.zoom_manual)
        self.slider_zoom.pack(pady=2)

        ctk.CTkLabel(self.main_frame, text="Em Atendimento", font=("Roboto", 16, "bold"), text_color="#121312").pack(anchor="w", padx=40)
        self.entry_paciente = ctk.CTkEntry(self.main_frame, placeholder_text="Nome do Paciente...", width=400, height=45, font=("Roboto", 18))
        self.entry_paciente.pack(pady=5)

        self.btn_chamar = ctk.CTkButton(self.main_frame, text="🔊 CHAMAR NO PAINEL", command=self.acao_chamar, height=50, font=("Roboto", 20, "bold"), fg_color="#189c5a")
        self.btn_chamar.pack(pady=5)

        frame_status = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        frame_status.pack(pady=10)
        self.btn_confirmar = ctk.CTkButton(frame_status, text="Confirmar Atendimento", command=lambda: self.registrar_status("Atendido"), state="disabled", fg_color="#321fdd", width=180, font=("Roboto", 14, "bold"))
        self.btn_confirmar.pack(side="left", padx=5)
        self.btn_falta = ctk.CTkButton(frame_status, text="Paciente Faltou", command=lambda: self.registrar_status("Faltou"), state="disabled", fg_color="#f51111", width=180)
        self.btn_falta.pack(side="left", padx=5)

        self.txt_historico = ctk.CTkTextbox(self.main_frame, width=520, height=120)
        self.txt_historico.pack(pady=5)

        frame_rodape = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        frame_rodape.pack(fill="x", side="bottom", pady=5)
        ctk.CTkButton(frame_rodape, text="📑 Relatório", width=80, command=self.gerar_excel, fg_color="#5a5a5a").pack(side="left")
        self.label_relogio = ctk.CTkLabel(frame_rodape, text="00:00:00", font=("Roboto", 22, "bold"), text_color="#2fa572")
        self.label_relogio.pack(side="left", expand=True)
        ctk.CTkButton(frame_rodape, text="Sair", width=80, fg_color="#a83232", command=self.quit).pack(side="right")

        self.atualizar_relogio()
        self.atualizar_listas_visual()

    # --- LÓGICA DE CHAMADA ---
    def acao_chamar(self):
        nome = self.entry_paciente.get().strip().upper()
        if not nome: return
        
        senha = next((p["senha"] for p in self.lista_espera if p["nome"] == nome), f"S-{self.contador_senha:03d}")
        
        if not self.salvar_chamada_global(senha, nome):
            return 

        if "S-" in senha and senha == f"S-{self.contador_senha:03d}": 
            self.contador_senha += 1
        
        # --- LINHA ATIVADA ABAIXO ---
        self.abrir_painel_tv()
        
        # Thread para áudio não travar a interface
        threading.Thread(target=self.tocar_sinal_e_anunciar, args=(senha, nome), daemon=True).start()
        
        if not any(at["Senha"] == senha for at in self.atendimentos):
            self.atendimentos.insert(0, {
                "Data": datetime.now().strftime("%d/%m/%Y"), "Hora": datetime.now().strftime("%H:%M:%S"),
                "Senha": senha, "Paciente": nome, "Status": "CHAMADO", "Médico": self.medico_atual
            })
        self.atualizar_listas_visual()
        self.btn_confirmar.configure(state="normal")
        self.btn_falta.configure(state="normal")

    # --- LÓGICA DO PAINEL (TV) ---
    def abrir_painel_tv(self):
        if self.painel_janela is None or not self.painel_janela.winfo_exists():
            self.painel_janela = ctk.CTkToplevel(self)
            self.painel_janela.title(f"Painel - {self.setor_atual}")
            
            monitores = get_monitors()
            if len(monitores) > 1:
                tv = monitores[1] 
                self.painel_janela.geometry(f"{tv.width}x{tv.height}+{tv.x}+{tv.y}")
            else:
                self.painel_janela.geometry("1024x768")

            self.painel_janela.after(200, lambda: self.painel_janela.state('zoomed'))
            self.painel_janela.configure(fg_color="black")
                           
            self.lbl_relogio_tv = ctk.CTkLabel(self.painel_janela, text="", text_color="white")
            self.lbl_relogio_tv.pack(pady=(20, 0))
            
            self.lbl_destaque_senha = ctk.CTkLabel(self.painel_janela, text="---", text_color="yellow")
            self.lbl_destaque_senha.pack(expand=True)

            self.lbl_destaque_sala = ctk.CTkLabel(self.painel_janela, text="", text_color="white")
            self.lbl_destaque_sala.pack(expand=True)
            
            self.lbl_destaque_nome = ctk.CTkLabel(self.painel_janela, text="AGUARDANDO", text_color="#edf109")
            self.lbl_destaque_nome.pack(expand=True)
            
            self.frame_hist_container = ctk.CTkFrame(self.painel_janela, fg_color="#121212", height=150)
            self.frame_hist_container.pack(fill="x", padx=50, pady=20)
            ctk.CTkLabel(self.frame_hist_container, text="SENHAS CHAMADAS:", font=("Roboto", 20), text_color="#FFFFFF").pack()
            
            self.grid_hist = ctk.CTkFrame(self.frame_hist_container, fg_color="transparent")
            self.grid_hist.pack(fill="both", expand=True, padx=10, pady=5)
            self.grid_hist.columnconfigure((0, 1, 2), weight=1)

            self.hist_slots = []
            for i in range(3):
                f = ctk.CTkFrame(self.grid_hist, fg_color="transparent")
                f.grid(row=0, column=i, sticky="nsew")
                lbl_n = ctk.CTkLabel(f, text="", text_color="#0808f5", wraplength=400)
                lbl_n.pack()
                lbl_s = ctk.CTkLabel(f, text="", text_color="#FFFFFF")
                lbl_s.pack()
                self.hist_slots.append({"nome": lbl_n, "sala": lbl_s})

            self.lbl_rodape_tv = ctk.CTkLabel(self.painel_janela, text_color="#FC0404")
            self.lbl_rodape_tv.pack(side="bottom", pady=40)
            
            self.atualizar_relogio_painel() 
            self.atualizar_dados_painel()
            self.redimensionar_fontes_painel()
        else:
            self.painel_janela.focus_force()

    def salvar_chamada_global(self, senha, nome):
        dados_globais = {}
        caminho = self.arquivo_setor_especifico
        if os.path.exists(caminho):
            try:
                with open(caminho, "r", encoding='utf-8') as f:
                    dados_globais = json.load(f)
            except: pass

        nova = {
            "senha": senha, 
            "nome": nome, 
            "sala": self.sala_atual, 
            "medico": f"{'Dr.' if self.genero_medico == 'o' else 'Dra.'} {self.medico_atual}", 
            "especialidade": self.especialidade
        }

        if self.setor_atual not in dados_globais:
            dados_globais[self.setor_atual] = {"historico_painel": [], "ultima_chamada_geral": {}}

        hist = dados_globais[self.setor_atual].get("historico_painel", [])
        hist.insert(0, nova)
        dados_globais[self.setor_atual]["historico_painel"] = hist[:3]
        dados_globais[self.setor_atual]["ultima_chamada_geral"] = nova

        try:
            with open(caminho, "w", encoding='utf-8') as f:
                json.dump(dados_globais, f, indent=4)
            return True
        except IOError:
            return False

    def atualizar_dados_painel(self):
        if not self.painel_janela or not self.painel_janela.winfo_exists(): return
        try:
            if os.path.exists(self.arquivo_setor_especifico):
                with open(self.arquivo_setor_especifico, "r", encoding='utf-8') as f:
                    dados_globais = json.load(f)
                
                dados_setor = dados_globais.get(self.setor_atual, {})
                ch = dados_setor.get("ultima_chamada_geral", {})
                
                if ch:
                    self.lbl_destaque_senha.configure(text=ch.get("senha", "---"))
                    self.lbl_destaque_nome.configure(text=ch.get("nome", ""))
                    self.lbl_destaque_sala.configure(text=ch.get("sala", ""))
                    self.lbl_rodape_tv.configure(text=f"{ch.get('medico')} ({ch.get('especialidade')})")
                
                hist = dados_setor.get("historico_painel", [])
                for i in range(3):
                    if i < len(hist):
                        self.hist_slots[i]["nome"].configure(text=f"{hist[i]['senha']} - {hist[i]['nome']}")
                        self.hist_slots[i]["sala"].configure(text=hist[i]['sala'])
                    else:
                        self.hist_slots[i]["nome"].configure(text="")
                        self.hist_slots[i]["sala"].configure(text="")
        except: pass
        self.painel_janela.after(1000, self.atualizar_dados_painel)

    def tocar_sinal_e_anunciar(self, senha, nome):
        try:
            if os.path.exists("alerta.wav"):
                pygame.mixer.music.load("alerta.wav")
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy(): continue
            pref = "Doutor" if self.genero_medico == "o" else "Doutora"
            msg = f"Senha {senha}. Paciente {nome}. Comparecer ao {self.sala_atual} com {pref} {self.medico_atual}"
            engine = pyttsx3.init()
            engine.say(msg)
            engine.runAndWait()
        except: pass

    # --- FUNÇÕES DE INTERFACE ---
    def registrar_status(self, novo_status):
        nome_atual = self.entry_paciente.get().strip().upper()
        if not nome_atual: return
        for atendimento in self.atendimentos:
            if atendimento["Paciente"] == nome_atual and atendimento["Status"] == "CHAMADO":
                atendimento["Status"] = novo_status
                break
        self.entry_paciente.delete(0, 'end')
        self.btn_confirmar.configure(state="disabled")
        self.btn_falta.configure(state="disabled")
        self.atualizar_listas_visual()

    def gerar_excel(self):
        if not self.atendimentos: return
        try:
            path = os.path.join(os.path.expanduser("~"), "Downloads", f"Relatorio_{self.setor_atual}_{datetime.now().strftime('%d%m%H%M')}.xlsx")
            pd.DataFrame(self.atendimentos).to_excel(path, index=False)
            messagebox.showinfo("Sucesso", "Relatório salvo em Downloads")
        except Exception as e: messagebox.showerror("Erro", str(e))

    def imprimir_etiqueta(self):
        if not self.lista_espera: return
        try:
            path = os.path.join(tempfile.gettempdir(), "etiquetas.rtf")
            with open(path, "w") as f:
                f.write(r"{\rtf1\ansi\deff0 {\fonttbl {\f0 Arial;}} \viewkind4\uc1 \pard\f0\fs28 ")
                for p in self.lista_espera:
                    f.write(fr"\b SENHA: {p['senha']} \b0  - {p['nome']} \par \line ")
                f.write(r"}")
            os.startfile(path)
        except Exception as e: messagebox.showerror("Erro", str(e))

    def importar_lista(self):
        path = filedialog.askopenfilename(filetypes=[("Excel/CSV", "*.xlsx *.xls *.csv")])
        if path:
            try:
                df = pd.read_csv(path) if path.endswith('.csv') else pd.read_excel(path)
                self.lista_espera = [{"nome": str(n).upper(), "senha": None} for n in df[df.columns[0]].dropna()]
                self.atualizar_listas_visual()
            except Exception as e: messagebox.showerror("Erro", str(e))

    def gerar_senhas_lista(self):
        for p in self.lista_espera:
            if not p["senha"]: 
                p["senha"] = f"S-{self.contador_senha:03d}"
                self.contador_senha += 1
        self.atualizar_listas_visual()

    def atualizar_listas_visual(self):
        self.txt_lista_espera.configure(state="normal")
        self.txt_lista_espera.delete("1.0", "end")
        senhas_chamadas = [at["Senha"] for at in self.atendimentos]
        for p in self.lista_espera:
            texto_linha = f"{p['senha'] or '---'} | {p['nome']}\n"
            tag = "chamado" if p['senha'] in senhas_chamadas else None
            self.txt_lista_espera.insert("end", texto_linha, tag)
        self.txt_lista_espera.configure(state="disabled")

        self.txt_historico.configure(state="normal")
        self.txt_historico.delete("1.0", "end")
        for at in self.atendimentos:
            self.txt_historico.insert("end", f"{at['Hora']} | {at['Senha']} | {at['Paciente'][:15]} | {at['Status']}\n")
        self.txt_historico.configure(state="disabled")

    def carregar_paciente_clique(self, event):
        try:
            sel = self.txt_lista_espera.get("insert linestart", "insert lineend")
            if "|" in sel:
                self.entry_paciente.delete(0, 'end')
                self.entry_paciente.insert(0, sel.split("|")[1].strip())
        except: pass

    def atualizar_relogio(self):
        self.label_relogio.configure(text=datetime.now().strftime("%H:%M:%S"))
        self.after(1000, self.atualizar_relogio)

    def atualizar_relogio_painel(self):
        if self.painel_janela and self.painel_janela.winfo_exists():
            self.lbl_relogio_tv.configure(text=datetime.now().strftime("%H:%M:%S"))
            self.painel_janela.after(1000, self.atualizar_relogio_painel)

    def ajustar_zoom_painel(self, valor):
        self.zoom_manual = float(valor)
        self.redimensionar_fontes_painel()

    def redimensionar_fontes_painel(self, event=None):
        if not self.painel_janela or not self.painel_janela.winfo_exists(): return
        w = self.painel_janela.winfo_width()
        if w < 100: w = 1024
        z = self.zoom_manual
        self.lbl_relogio_tv.configure(font=("Roboto", int(w * 0.03 * z), "bold"))
        self.lbl_destaque_senha.configure(font=("Roboto", int(w * 0.15 * z), "bold"))
        self.lbl_destaque_sala.configure(font=("Roboto", int(w * 0.08 * z), "bold"))
        self.lbl_destaque_nome.configure(font=("Roboto", int(w * 0.06 * z), "bold"))
        self.lbl_rodape_tv.configure(font=("Roboto", int(w * 0.035 * z), "bold"))
        for slot in self.hist_slots:
            slot["nome"].configure(font=("Roboto", int(w * 0.022 * z), "bold"))
            slot["sala"].configure(font=("Roboto", int(w * 0.018 * z)))

if __name__ == "__main__":
    app = AppChamada()
    app.mainloop()