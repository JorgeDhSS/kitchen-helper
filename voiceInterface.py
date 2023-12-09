import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import pygame as pygame 

def main():
    title.config(text="Bienvenido usuario'")
    pygame.mixer.init()
    pygame.mixer.music.load("bienvenida.mp3")
    pygame.mixer.music.play()
    #Declarar recnoconedor de voz
    rec = sr.Recognizer()
    #activar el micrófono como recurso que estará permanentemente en escucha 
    with sr.Microphone() as source:
        print('Identifícate, por favor...')
        rec.adjust_for_ambient_noise(source)
        #guardar la entrada por micrófono en una variable 
        audio = rec.listen(source)
        try:
            aud_text = rec.recognize_google(audio,language = 'es-ES')#convertir audio a texto 
            if aud_text == 'Jorge':
                print('Bienvenido usuario')
                print('¿Cuál es la operación que quieres realizar? SUMA, RESTA, MULTIPLICACIÓN O DIVISIÓN')
                #convertir texto a audio 
                tts = gTTS('Bienvenido usuario, ¿Cuál es la operación que quieres realizar? SUMA, RESTA, MULTIPLICACIÓN O DIVISIÓN', lang="es-ES")
                tts.save('bienvenida.mp3')
                playsound('bienvenida.mp3')

                #generar nuevo audio 
                audio2 = rec.listen(source)
                operacion = rec.recognize_google(audio2,language = 'es-ES')#convertir audio a texto 
                print("La operación seleccionada fue :{}".format(operacion))
                print("Ahora diga el primer número a operar")
                tts2 = gTTS("La operación seleccionada fue :{} Ahora diga el primer número a operar".format(operacion), lang="es-ES")
                tts2.save('primerMensaje.mp3')
                playsound('primerMensaje.mp3')

                #generar nuevo audio 
                audio3 = rec.listen(source)
                numberOne = rec.recognize_google(audio3,language = 'es-ES')
                if numberOne == "uno":
                    numberOne = 1
                else:
                    numberOne = int(numberOne)
                print("Ahora diga el segundo número a operar")
                tts3 = gTTS("Ahora diga el segundo número a operar", lang="es-ES")
                tts3.save('segundoMensaje.mp3')
                playsound('segundoMensaje.mp3')

                #generar nuevo audio 
                audio4 = rec.listen(source)
                numberTwo =  rec.recognize_google(audio4,language = 'es-ES')
                if numberTwo == "uno":
                    numberTwo = 1
                else:
                    numberTwo = int(numberTwo)
                resultado = 0
                match operacion:
                    case "suma":
                        resultado = numberOne + numberTwo
                    case "resta":
                        resultado = numberOne - numberTwo
                    case "multiplicacion":
                        resultado = numberOne * numberTwo
                    case "division":
                        resultado = numberOne / numberTwo
    ##
                print("El resultado de la operación es :{}".format(resultado))
                tts4 = gTTS("El resultado de la operación es :{}".format(resultado), lang="es-ES")
                tts4.save('resultado.mp3')
                playsound('resultado.mp3')
            else:
                print('Acceso denegado')
        except Exception as inst:
            print(inst)
