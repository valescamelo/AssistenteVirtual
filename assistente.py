#etapas do criação do programa assistente virtual 
import speech_recognition as sr
import pyttsx3

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
        
def assistente(): #principal função do assistente virtual
    falar('Olá! Sou sua assistente virtual. No que posso ajudar? ')

    while True:
        informacao = ouvir()
        print(f'Você disse: {informacao}')

        if "sair" in informacao:
            falar('Até logo')
            break
        elif 'Olá' in informacao or "Oi" in informacao:
            falar('Olá! Como posso ajudar você?')
        elif 'Está tudo bem?' in informacao:
            falar('Estou bem, obrigada!')
        else: 
            falar("Desculpe. Ainda não sei resolver isso.")

if __name__ == "__main__": #quando um codigo é executado por si só. 
    assistente()

