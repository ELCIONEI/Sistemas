import speech_recognition as sr
import pyttsx3
import winsound
import threading
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- CONFIGURAÇÃO GLOBAL ---
def iniciar_driver():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    
    # 1. Garanta que a janela abra em tamanho Desktop real
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--start-maximized")
    
    # 2. Caminho absoluto para o perfil (evita erros de localização)
    perfil_nome = "perfil_automacao"
    caminho_completo = os.path.join(os.getcwd(), perfil_nome)
    chrome_options.add_argument(f"--user-data-dir={caminho_completo}")
    
    # 3. User-Agent fixo de Desktop (Chrome estável)
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")

    service = Service(ChromeDriverManager().install())
    d = webdriver.Chrome(service=service, options=chrome_options)
    return d

driver = iniciar_driver()

# --- FUNÇÕES DE INTERAÇÃO ---
def falar(texto):
    print(f"IA: {texto}")
    engine = pyttsx3.init()
    # Ajuste de voz para soar mais natural
    voices = engine.getProperty('voices')
    for voice in voices:
        if "brazil" in voice.name.lower():
            engine.setProperty('voice', voice.id)
    engine.setProperty('rate', 185)
    engine.say(texto)
    engine.runAndWait()

def emitir_bip(tipo="inicio"):
    frequencia = 1000 if tipo == "inicio" else 600
    winsound.Beep(frequencia, 200)

def acao_playlist(url):
    try:
        driver.get(url)
        # Tempo para carregar os elementos dinâmicos
        wait = WebDriverWait(driver, 20)
        
        falar("Localizando botão de reprodução...")

        # Lista de possíveis seletores para o botão de Play (abrange as duas imagens)
        seletores = [
            'button[data-testid="play-button"]',        # Versão Completa (Imagem 2)
            'button[aria-label*="Reproduzir"]',         # Versão em PT-BR
            'button[aria-label*="Play"]',               # Versão em Inglês
            '.e-9541-button-main',                      # Classe comum em versões simplificadas
            'button[data-encore-id="buttonPrimary"]'    # Seletor genérico de ação principal
        ]

        botao_clicado = False
        for seletor in seletores:
            try:
                # Tenta encontrar cada seletor por no máximo 3 segundos
                botao = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, seletor)))
                botao.click()
                botao_clicado = True
                falar("Música iniciada!")
                break
            except:
                continue # Tenta o próximo seletor da lista

        if not botao_clicado:
            # Caso os seletores falhem, tentamos o atalho de teclado "Enter" 
            # que muitas vezes aciona o play se a página carregar focada
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ENTER)
            falar("Tentei iniciar pelo teclado.")

    except Exception as e:
        print(f"Erro ao interagir com a lista: {e}")
        falar("Abri a página, mas houve um erro ao clicar no play.")

def acao_busca_geral(termo):
    try:
        url_busca = f"https://www.youtube.com/results?search_query={termo}"
        driver.get(url_busca)
        wait = WebDriverWait(driver, 10)
        # Clica no primeiro vídeo
        primeiro_video = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "ytd-video-renderer #video-title")))
        primeiro_video.click()
    except Exception as e:
        falar("Tive um problema na busca do Youtube.")

# --- LOOP PRINCIPAL ---
def monitorar_voz():
    reconhecedor = sr.Recognizer()
    reconhecedor.dynamic_energy_threshold = True # Ajusta ao ruído do ambiente automaticamente
    
    with sr.Microphone() as source:
        falar("Sistemas prontos.")

        while True:
            try:
                # Escuta a palavra de ativação "Computador"
                audio = reconhecedor.listen(source, timeout=None, phrase_time_limit=3)
                chamada = reconhecedor.recognize_google(audio, language='pt-BR').lower()

                if "computador" in chamada:
                    emitir_bip("inicio")
                    falar("Pois não?")
                    
                    # Pausa estratégica para não ouvir a própria voz
                    time.sleep(0.5) 
                    
                    # Escuta o comando real
                    audio_comando = reconhecedor.listen(source, timeout=5, phrase_time_limit=8)
                    texto = reconhecedor.recognize_google(audio_comando, language='pt-BR').lower()
                    print(f"Comando: {texto}")

                    if "minha playlist" in texto:
                        # Substitua pelo link real da sua playlist
                        link_real = "https://open.spotify.com/playlist/64gzin89TniM1Bv8I8udjz"
                        threading.Thread(target=acao_playlist, args=(link_real,)).start()

                    elif "tocar" in texto:
                        busca = texto.replace("tocar", "").strip()
                        falar(f"Buscando {busca}")
                        threading.Thread(target=acao_busca_geral, args=(busca,)).start()

                    elif any(cmd in texto for cmd in ["pausar", "parar", "continuar", "reproduzir"]):
                        # Envia espaço para o navegador controlar o player
                        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.SPACE)
                        falar("Feito.")

                    elif "sai" in texto or "encerrar" in texto:
                        falar("Encerrando, Até logo!")
                        driver.quit()
                        break

            except (sr.WaitTimeoutError, sr.UnknownValueError):
                continue # Volta a ouvir sem dar erro se não entender
            except Exception as e:
                print(f"Erro: {e}")

if __name__ == "__main__":
    monitorar_voz()