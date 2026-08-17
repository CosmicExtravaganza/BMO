import speech_recognition as sr
import os 
import ollama
import pyaudio
from piper import PiperVoice

#os.system('spd-say "Hello, I am ready."')

command_prefix = "spd-say "
command_endfix = "Respond as BMO would from Adventure time"


r = sr.Recognizer()


p = pyaudio.PyAudio()
for i in range(p.get_device_count()):
    dev = p.get_device_info_by_index(i)
    if dev['maxInputChannels'] > 0:
        print(f"Device Index {i}: {dev['name']}")

while True:
    try:
        with sr.Microphone(device_index=0) as source:
            print("Listening...")
            print(source)
            r.adjust_for_ambient_noise(source, duration=0.2)
            audio = r.listen(source, 10, 15)
            text = r.recognize_google(audio)
            text = text.lower()
            result = ollama.generate(model="llama3", prompt=text + command_endfix)
            print(result['response']) 
            response = '"' + result['response'] + '"'
            os.system(command_prefix + response)  
            print(command_prefix + text)
            print("You said:", text)
            if "exit" in text:
                print("Exiting program...")
                break

    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

    except sr.UnknownValueError:
        print("Could not understand audio")

    except KeyboardInterrupt:
        print("Program terminated by user")
        break

    except sr.WaitTimeoutError:
         os.system(command_prefix + "Would you like to exit?...")
         audio = r.listen(source, 10, 15)
         text = r.recognize_google(audio)
         if (text == "exit"):
             break
         else: 
             pass