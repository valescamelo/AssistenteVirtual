#etapas do criação do programa assistente virtual 
import tkinter as tk
from tkinter import scrolledtext
import speech_recognition as sr
import pyttsx3
import webbrowser
from datetime import datetime
import requests


def falar(texto): #transforma texto em fala
    enige = pyttsx3.init() #pyttsx3 sintetiza voz 
    enige.say(texto) #metodo
    enige.runAndWait()

def ouvir(): #verifica ou audio do microfone e converte em texto
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        saida_texto.insert(tk.END, "Assistente: Estou ouvindo..\n")
        janela.update()
        try:
            audio = recognizer.listen(source, timeout=5)
            informacao = recognizer.recognize_google(audio, language='pt-BR')
            return informacao.lower()
        except sr.UnknownValueError:
            return "Não compreendi o que você disse."
        except sr.RequestError:
            return "Erro no serviço de reconhecimento de voz."
        except sr.WaitTimeoutError:
            return "Você não informou nada. Tempo egostado!"

def consultar_hr(): #função para consultar hora no assistente virtual
    agora = datetime.now()
    hora_atual = agora.strftime("%H:%M") #strftime personalisa horas e datas 
    return (f"Informações de hora: {hora_atual}")

def pesquisar_google(termo): #função para abrir uma pesquisa no navegador
    url = (f"https://www.google.com/search?q={termo}")
    webbrowser.open(url)
    return (f"Pesquisa encontrada conforme solicitado: {termo}.")

def previsao_tempo(cidade): #função para obter previsão do tempo usando a API OpenWeatherMap
    url = f"https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid=40463302f72fed69d87c015b3b6f2ff4&lang=pt_br&units=metric"
    try:
        resposta = requests.get(url)
        dados = resposta.json() #json formato que apresenta informações, transfere dados entre servidor e cliente
        if resposta.status_code == 200:
            temperatura = dados['main']['temp']
            descricao = dados['weather'][0]['description'] #descrição de clima no primeiro elemento da lista associada a chave clima.
            return (f"A previsão do tempo para a {cidade} é de {descricao}, com temperatura de {temperatura}C°.")
        else:
            return "Não encontrei a previsão para a cidade solicitada"
    except Exception as e: #tratamento de exceções que ocorre durante a execução de codigo usando try.
        return "Houve um problema ao verificar a previsão do tempo."

def noticias(): #últimas noticias utilizando a API NewsAPI
    url=("https://newsapi.org/v2/top-headlines?q=br&apiKey=d9b07398b5c84077bf9e5103bb05197c")
    try:
        resposta = requests.get(url)
        resposta.raise_for_status() #gera o erro caso o codigo não for 200
        dados = resposta.json()
        
        if "articles" in dados and len(dados['articles']) > 0:
            art = dados["articles"][:5] #seleciona as 5 principais noticias
            ret_noticias = [f"{i+1}. {artigo['title']}" for i, artigo in enumerate(art)]
            return  "As principais notícias do momento são:\n" + "\n".join(ret_noticias)
        else:
            return "Não consegui encontrar notícias agora."
    
    except Exception as e:
        return "Houve um erro ao tentar acessar as notícias."
    

def assistente(informacao): #principal função do assistente virtual
    if "sair" in informacao:
        falar('Até logo')
        janela.quit()
    elif "olá" in informacao or "oi" in informacao:
        resposta = 'Olá! Como posso ajudar você?'
    elif "está tudo bem?" in informacao:
        resposta = 'Estou bem, obrigada!'
    elif "me informe a hora" in informacao:
        resposta = consultar_hr
    elif "pesquisar" in informacao:
        falar("Qual é a pesquisa de hoje?")
        pesquisa = ouvir()
        resposta = pesquisar_google(pesquisa)
    elif "previsão do tempo" in informacao:
        falar("Para qual cidade deseja saber a previsão?")
        cidade = ouvir()
        resposta = previsao_tempo(cidade)
    #elif "notícias" in informacao:
            #pesq_noticias = noticias()
            #falar(pesq_noticias)
    else: 
        resposta = "Desculpe. Ainda não sei resolver isso."
    saida_texto.insert(tk.END, f'Você: {informacao}\nAssistente: {resposta} ')
    falar(resposta)

def executar_assistente():
    informcao = ouvir()
    if informcao:
        assistente(informcao)
    else: 
        saida_texto.insert(tk.END, "Assistente: Não entendi. Tente novamente.\n")


#Interface gráfica com Tkinter
janela = tk.Tk()
janela.title("Assistente Virtual Pessoal")

#Configurações dos elementos da interface gráfica 

saida_texto=scrolledtext.ScrolledText(janela, wrap=tk.WORD, width=50, height=20, font=("Arial", 12))
saida_texto.pack(pady=10)

botao_ouvir = tk.Button(janela, text="Falar com a Assistente", command=executar_assistente, bg="#4CAF50", fg="white", font=("Arial", 12))
botao_ouvir.pack(pady=10)

texto_manual = tk.Entry(janela, width=50, font=("Arial", 12))
texto_manual.pack(pady=5)

def informacao_manual():
    informacao = texto_manual.get()
    texto_manual.delete(0, tk.END)
    executar_assistente(informacao)

botao_enviar = tk.Button(janela, text="Enviar Comando", command=informacao_manual, bg="#008CBA", fg="white", font=("Arial", 12))
botao_enviar.pack(pady=5)


#Executar a interface
falar("Assistente iniciada com sucesso")
janela.mainloop()
    
#if __name__ == "__main__": #executando a principal função do código
    #assistente()

