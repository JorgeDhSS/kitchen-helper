import threading, mutagen, time, queue, json
from tkinter import *
from tkinter import ttk
import pygame as pygame 
import tkinter as tk
from tkmacosx import Button
import speech_recognition as sr
from gtts import gTTS
from PIL import ImageTk, Image

#TODO implementar click a botón de ingredientes
def speak(textToSpeak):
    Speak.config(bg="#2D7A00")
    instructions.config(text=textToSpeak)
    tts = gTTS(textToSpeak, lang="es-ES")
    tts.save('audio.mp3')
    pygame.mixer.init()
    pygame.mixer.music.load("audio.mp3")
    # Extraer la duración del archivo de audio en minutos y segundos
    min, seg = divmod(mutagen.File(f'audio.mp3').info.length, 60)
    # Sumar todos los segundos
    ts = (round(min)*60)+round(seg, 1)
    pygame.mixer.music.play()
    # IMPORTANTE: si no se define este timer de espera
    # no habrá tiempo para que se reproduzca el audio
    time.sleep(ts)

def microphone(rec, source, q: queue.Queue):
    Micro.config(bg="#2D7A00")
    #guardar la entrada por micrófono en una variable 
    audio = rec.listen(source)
    try:
        aud_text = rec.recognize_google(audio,language = 'es-ES')#convertir audio a texto 
    except Exception as inst:
        aud_text = "EXCEPTION"
    q.put_nowait(aud_text)

def instructionsF(fileJson, nameUser, rec, source, q):
    data = json.load(fileJson)
    title.config(text=data['titulo'])
    for i in data['pasos']:
        ilustrationImg = ImageTk.PhotoImage(Image.open(i["img"]))
        ilustration.config(image=ilustrationImg, width=80)
        stepT = threading.Thread(name="stepT", target=speak(i["instruction"]))
        stepT.start()
        stepT.join()
        if not stepT.is_alive():
            Speak.config(bg="#8B8B8C")
            isReady = False
            while(not isReady):
                microphone(rec, source, q)
                aud_text = q.get_nowait()
                print(aud_text)
                if aud_text == "listo":
                    isReady = True
            Micro.config(bg="#8B8B8C")
    # Closing file
    fileJson.close()
    finishT = threading.Thread(name="finishT", target=speak("Receta concluida, favor de decir 'Otra' si se quiere seguir otra receta o 'salir' para cerrar la aplicación"))
    finishT.start()
    finishT.join()
    if not finishT.is_alive():
        Speak.config(bg="#8B8B8C")
        finishListener = threading.Thread(name="finishListener", target=microphone(rec, source, q))
        finishListener.start()
        finishListener.join()
        if not finishListener.is_alive():
            Micro.config(bg="#8B8B8C")
            aud_text = q.get_nowait()
            #TODO añadir caso de salir
            if aud_text == "Otra":
                mainMenuT = threading.Thread(name="mainMenuT", target=mainMenu(nameUser, rec, source, q))
                mainMenuT.start()

def otherOptions(rec, source, q, nameUser):
    otherOptionsMessages = threading.Thread(name="otherOptionsMessage", target=speak("1. Tostadas de tinga de setas  \n 2. Regresar"))
    otherOptionsMessages.start()
    otherOptionsMessages.join()
    if not otherOptionsMessages.is_alive():
        Speak.config(bg="#8B8B8C")
        listeningOtherOptions = threading.Thread(name="listeningOtherOptions", target=microphone(rec, source, q))
        listeningOtherOptions.start()
        listeningOtherOptions.join()
        if not listeningOtherOptions.is_alive():
            Micro.config(bg="#8B8B8C")
            aud_text = q.get_nowait()
            if aud_text == "EXCEPTION":
                messageException = threading.Thread(name="exceptionMessage", target=speak("Lo sentimos {}, ocurrió un error, vuelve a intentarlo".format(nameUser)))
                messageException.start()
                messageException.join()
                if not messageException.is_alive():
                    Speak.config(bg="#8B8B8C")
                    tOtherOptions = threading.Thread(name="otherOptions", target=otherOptions(rec, source, q, nameUser))
                    tOtherOptions.start()
            else:
                match aud_text:
                    case "uno" | 1 | "1":
                        fileJson = open('receta_3.json')
                        instructionsT = threading.Thread(name="instructionsF", target=instructionsF(fileJson, nameUser, rec, source, q))
                        instructionsT.start()
                    case "dos" | 2 | "2":
                        tVoice = threading.Thread(name="mainMenu", target=mainMenu(nameUser, rec, source, q))
                        tVoice.start()
                    case default:
                        notFoundOption = threading.Thread(name="notFoundOption", target=speak("Lo sentimos {}, la opción elegida no se encuentra en el menú, por favor, intente de nuevo".format(nameUser)))
                        notFoundOption.start()
                        notFoundOption.join()
                        if not notFoundOption.is_alive():
                            Speak.config(bg="#8B8B8C")
                            tOtherOptions = threading.Thread(name="otherOptions", target=otherOptions(rec, source, q, nameUser))
                            tOtherOptions.start()
def mainMenu(nameUser, rec, source, q):
    newThread = threading.Thread(name="firstMessage", target=speak("Hola {}, di el número de la receta que quieres cocinar: \n 1.Sopa de fideo \n 2. Espagueti rojo  \n 3. Otras".format(nameUser)))
    newThread.start()
    newThread.join()
    if not newThread.is_alive():
        Speak.config(bg="#8B8B8C")
        listening = threading.Thread(name="listening", target=microphone(rec, source, q))
        listening.start()
        listening.join()
        if not listening.is_alive():
            Micro.config(bg="#8B8B8C")
            aud_text = q.get_nowait()
            print(aud_text)
            if aud_text == "EXCEPTION":
                messageException = threading.Thread(name="exceptionMessage", target=speak("Lo sentimos {}, ocurrió un error, vuelve a intnetarlo".format(nameUser)))
                messageException.start()
                messageException.join()
                if not newThread.is_alive():
                    Speak.config(bg="#8B8B8C")
                    mainMenuT = threading.Thread(name="mainMenuT", target=mainMenu(nameUser, rec, source, q))
                    mainMenuT.start()
            elif aud_text == "tres" or aud_text == "3" or aud_text == 3:
                tOtherOptions = threading.Thread(name="otherOptions", target=otherOptions(rec, source, q, nameUser))
                tOtherOptions.start()
            else:
                match aud_text:
                    case "uno" | 1 | "1":
                        fileJson = open('receta_1.json')
                        instructionsT = threading.Thread(name="instructionsF", target=instructionsF(fileJson, nameUser, rec, source, q))
                        instructionsT.start()
                    case "dos" | 2 | "2":
                        fileJson = open('receta_2.json')
                        instructionsT = threading.Thread(name="instructionsF", target=instructionsF(fileJson, nameUser, rec, source, q))
                        instructionsT.start()
                    case default:
                        notFoundOption = threading.Thread(name="notFoundOption", target=speak("Lo sentimos {}, la opción elegida no se encuentra en el menú, por favor, intente de nuevo".format(nameUser)))
                        notFoundOption.start()
                        notFoundOption.join()
                        if not notFoundOption.is_alive():
                            Speak.config(bg="#8B8B8C")
                            mainMenuT = threading.Thread(name="mainMenuT", target=mainMenu(nameUser, rec, source, q))
                            mainMenuT.start()


def voiceInterface():
    newThread = threading.Thread(name="welcomeMessage", target=speak("Bienvenido usuario, ¿Cómo te llamas?"))
    newThread.start()
    newThread.join()
    if not newThread.is_alive():
        Speak.config(bg="#8B8B8C")
    #Declarar recnoconedor de voz
    rec = sr.Recognizer()
    #activar el micrófono como recurso que estará permanentemente en escucha 
    with sr.Microphone() as source:
        q = queue.Queue()
        rec.adjust_for_ambient_noise(source)
        listeningName = threading.Thread(name="listeningName", target=microphone(rec, source, q))
        listeningName.start()
        listeningName.join()
        if not listeningName.is_alive():
            Micro.config(bg="#8B8B8C")
            nameUser = q.get_nowait()
            if nameUser == "EXCEPTION":
                voiceInterfaceT = threading.Thread(name="voiceInterfaceT", target=voiceInterface)
                voiceInterfaceT.start()
                voiceInterfaceT.join()
                if not voiceInterfaceT.is_alive():
                    return 0
            else:
                mainThread = threading.Thread(name="mainThread", target=mainMenu(nameUser, rec, source, q))
                mainThread.start()
                mainThread.join()
                if not mainThread.is_alive():
                    return 0
            
#elemento raíz de la GUI
root = Tk()
#frame donde se meterán los objetos, es de tipo GRID
frm = ttk.Frame(root, padding=10)
frm.grid()
#Label título
title = Label(frm, text="Bienvenido usuario", font=('Arial bold', 25))
title.grid(padx=10, pady=10, column=0, row=0, sticky = W)
#Button (ingredientes)
btnIngredientes = Button(frm, borderless=1, bg='#2D7A00', fg="#ffffff", highlightbackground='#2D7A00', text="🍎Ingredientes", command=print("Botón presionado"))
btnIngredientes.grid(column=2, row=0)
ttk.Label(frm, text="Instrucciones", font=('Arial bold', 18), anchor="w", justify= LEFT).grid(padx=10, pady=5, sticky = W, column=0, row=1)
#Instructions field (Label)
instructions = Label(frm, wraplength=390, text="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserun", font=('Arial', 18), anchor="nw", justify= LEFT)
instructions.grid(sticky="nw", padx=10, pady=5, row=2, column=0, columnspan=2, rowspan=2)
# Cargar imagen del disco.
imageMicro = tk.PhotoImage(file="micro.png")
imageSpeaker= tk.PhotoImage(file="Speaker.png")
# Insertarla en una etiqueta.
Micro = Label(frm, image=imageMicro, bg="#8B8B8C", width=80)
Micro.grid(padx=10, pady=5, row=2, column=2, rowspan=1)
Speak = Label(frm, image=imageSpeaker, bg="#8B8B8C", width=80)
Speak.grid(padx=10, pady=5, row=3, column=2, rowspan=1)
ttk.Label(frm, text="Ilustración", font=('Arial bold', 18), anchor="w", justify= LEFT).grid(padx=10, pady=5, sticky = W, column=0, row=4)
ilustrationImg = ImageTk.PhotoImage(Image.open("micro.png"))
ilustration = Label(frm, image=imageMicro, width=80)
ilustration.grid(padx=5, pady=5, row=5, column=0)
t2 = threading.Thread(name="voiceInterface", target=voiceInterface)
t2.start()
root.mainloop()
