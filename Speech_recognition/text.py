#pip install pyttsx3
import pyttsx3
#class ==>init()
txt_sp=pyttsx3.init()
#text=input("Enter the text: ")
#txt_sp.say(text)
#txt_sp.runAndWait()

#Female voice
voice=txt_sp.getProperty('voices')
txt_sp.setProperty('voice',voice[1].id)
txt_sp.setProperty('volume',0.9)
text=input("Enter the text: ")
txt_sp.say(text)
txt_sp.runAndWait()
