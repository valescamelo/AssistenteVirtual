#etapas do criação do programa assistente virtual 
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
        print('Aguardando...')
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
    url=("https://newsapi.org/v2/top-headlines?country=br&apiKey=d9b07398b5c84077bf9e5103bb05197c")
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

def assistente(): #principal função do assistente virtual
    falar('Olá! Sou sua assistente virtual. No que posso ajudar?')

    while True:
        informacao = ouvir()
        print(f'Você disse: {informacao}')

        if "sair" in informacao:
            falar('Até logo')
            break
        elif "olá" in informacao or "oi" in informacao:
            falar('Olá! Como posso ajudar você?')
        elif "está tudo bem?" in informacao:
            falar('Estou bem, obrigada!')
        elif "me informe a hora" in informacao:
            hora = consultar_hr
            falar(hora)
        elif "pesquisar" in informacao:
            falar("Qual é a pesquisa de hoje?")
            termo = ouvir()
            if termo != "Não entendi o que você disse":
                resultado = pesquisar_google(termo)
                falar(resultado)
            else:
                falar("Não entendi o que você quer pesquisar")
        elif "previsão do tempo" in informacao:
            falar("Para qual cidade deseja saber a previsão?")
            cidade = ouvir()
            if cidade != "Não compreendi o que você disse.":
                previsao = previsao_tempo(cidade)
                falar(previsao)
            else:
                falar("Não consegui entender a cidade informada.")
        elif "notícias" in informacao:
            pesq_noticias = noticias()
            falar(pesq_noticias)
        else: 
            falar("Desculpe. Ainda não sei resolver isso.")

if __name__ == "__main__": #executando a principal função do código
    assistente()

