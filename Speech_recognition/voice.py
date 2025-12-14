#pip install pyaudio
#pip install SpeechRecognition

import speech_recognition as sr
def speech_txt():
    r=sr.Recognizer()     #init
    while True:
        with sr.Microphone() as source:       #source=sr.Microphone()
             
            print("Speak Now........")
            audio=r.listen(source)
        
        try:
            text=r.recognize_google(audio)
            print("You said",text)
        except:
            print("Didn't hear anything")
speech_txt
    
        