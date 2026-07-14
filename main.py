import speech_recognition as sr
import webbrowser
import pyttsx3
import time
import pyautogui
import random
import google.generativeai as genai

pyautogui.FAILSAFE = True      # Enabled by default, keep this True!
pyautogui.PAUSE = 0.1     # Short pause after each PyAutoGUI call to prevent overwhelming the system

genai.configure(api_key="Your_Gemini_API_Key_Here")
ai_model = genai.GenerativeModel('gemini-1.5-flash')

def ask_gemini_brain(user_query):
    """Sends the voice command to Gemini with a system prompt to stay in character."""
    try:
        system_instruction = (
            "You are Shanky, a personal assistant to help me in my work related to studies and coding. "
            "Keep your answers brief (1-2 sentences maximum)." #You can edit it and make it according to your own needs.
        )
        
        full_prompt = f"{system_instruction}\n\nUser says: {user_query}"
        
        response = ai_model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        print(f"!!! Gemini API Brain Error: {e}")
        return "Brain server encountered an error."

def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 175)
    engine.say(text)
    engine.runAndWait()
    engine.stop()
    del engine

def Task(command, r):
    command_clean = command.lower()
    if "open youtube" in command_clean:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
    elif "open google" in command_clean:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
    elif "open facebook" in command_clean:
        speak("Opening Facebook")
        webbrowser.open("https://www.facebook.com")
    elif "open twitter" in command_clean:
        speak("Opening Twitter")
        webbrowser.open("https://www.twitter.com")
    elif "how are you" in command_clean or "how r u" in command_clean:
        speak("As great as you designed me!")
    elif "open instagram" in command_clean:
        speak("Opening Instagram")
        webbrowser.open("https://www.instagram.com")
    elif "open whatsapp" in command_clean:
        speak("Opening WhatsApp")
        webbrowser.open("https://web.whatsapp.com")
    elif "open spotify" in command_clean:
        speak("Opening Spotify")
        webbrowser.open("https://www.spotify.com")
    elif "play music" in command_clean:
        speak("Playing music on Spotify")
        webbrowser.open("https://open.spotify.com")
        time.sleep(5)  # Wait for the page to load
        pyautogui.press('space')  # Press the spacebar to start playing
    elif "pause it" in command_clean or "stop it" in command_clean:
        pyautogui.press('playpause')  # Press the play/pause button
        speak("Done")
    elif "play it" in command_clean or "resume it" in command_clean:
        pyautogui.press('playpause')  # Press the play/pause button
        speak("Done")
    elif "bye-bye" in command_clean or "goodbye" in command_clean:
        speak("Goodbye sir, have a nice day!")
        exit()
    elif "should i do it" in command_clean: #Just a fun feature, you can remove it if you want.
        random_number = random.randint(0, 1)
        if random_number == 0:
            speak("No, I don't think you should do it.")
        else:
            speak("Yes, I think you should do it.")
    elif "open mail" in command_clean:
        speak ("Opening Gmail")
        webbrowser.open("https://mail.google.com")
    elif "open ai" in command_clean:
        speak("Opening Gemini Pro")
        webbrowser.open("https://gemini.google.dev/pro")
    elif "nothing" in command_clean:
        speak("Okay sir, let me know if you need anything.")
    elif "open message" in command_clean:
        speak("Opening Messages")
        webbrowser.open("https://messages.google.com/web/authentication")
    else:
        print("[Consulting Gemini Brain...]")
        ai_reply = ask_gemini_brain(command)
        speak(ai_reply)    
  

if __name__ == "__main__":

    r = sr.Recognizer()
    mic = sr.Microphone()
    

    while True:

        try:
            with mic as source:
                print("Listening.....")
                audio = r.listen(source, timeout=10)
                print("Recognizing.....")
            word = r.recognize_google(audio)
            print(word)
            
            if word.lower() == "Your Inital Wake Up Call" or word.lower() == "Similar Sounding Wake Up Call" or word.lower() == "Similar Sounding Wake Up Call": #Please add the initial wake up call here but if you want to use the main wake up call only then you can remove it.
                speak("Hello sir, how can I help you?")
                print("'Your Assistant Name' is ready!")
                break

        except Exception as e:
            print("Couldn't Understand {0}".format(e))

WAKE_WORD = "Wake Up Call" #Please add your wake up call here, you can change it to whatever you want.

while True:
    wake_phrase = ""
    try:
        with mic as source:
            r.adjust_for_ambient_noise(source, duration=0.4)
            r.energy_threshold = 600
            print("\n[Waiting for Wake Word]...")
            audio = r.listen(source, phrase_time_limit=3)
                    
        # Processing the audio happens outside the context manager
        wake_phrase = r.recognize_google(audio).lower().lower()
        print(f"Heard locally: '{wake_phrase}'")
                    
    except sr.UnknownValueError:
        continue
    except Exception as e:
        print(f"Wake word listening error: {e}")
        continue

    # 2. If the wake word matches, open a brand new microphone block for the command
    if any(word in wake_phrase for word in WAKE_WORD):
        speak("Ya")
                    
        try:
            with mic as source:
                print("[Listening for Command]...")
                audio_command = r.listen(source, timeout=5, phrase_time_limit=7)
                        
            print("[Recognizing...]")
            command = r.recognize_google(audio_command)
            print(f"User Command: {command}")
                        
            Task(command, r)
                        
        except sr.UnknownValueError:
            speak("I didn't quite catch that.")
        except Exception as e:
            print(f"Command listening error: {e}")