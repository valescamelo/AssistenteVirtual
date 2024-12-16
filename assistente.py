#etapas do criação do programa assistente virtual 
import speech_recognition as sr
import pyttsx3
import webbrowser
from datetime import datetime

def falar(texto): #transforma texto em fala
    enige = pyttsx3.init() #pyttsx3 sintetiza voz 
    enige.say(texto) #metodo say para dizer
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
        else: 
            falar("Desculpe. Ainda não sei resolver isso.")

if __name__ == "__main__": #quando um codigo é executado por si só. 
    assistente()

