import os
import pygame
import speech_recognition as sr
from langchain_community.llms import Ollama  # Importing from langchain_community
from gtts import gTTS
import datetime
import webbrowser

# Function to ensure the existence of the 'mp3_files' directory
def ensure_directory_exists(directory):
    try:
        os.makedirs(directory, exist_ok=True)
    except OSError as e:
        print(f"Error creating directory {directory}: {e}")

# Ensure 'mp3_files' directory exists
ensure_directory_exists("mp3_files")

# Initialize pygame mixer
pygame.mixer.init()

# Function definitions for playing audio, generating mp3, speaking, and recognizing speech
def play(file_path):
    try:
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    except Exception as e:
        print(f"Error while playing {file_path}: {e}")

def generate_mp3(output_folder, text):
    tts = gTTS(text=text, lang='en-in')
    mp3_file_path = os.path.join(output_folder, f"{text[:20].replace(' ', '_')}.mp3")  # Use a unique identifier based on the text
    try:
        if not os.path.exists(mp3_file_path):
            tts.save(mp3_file_path)
    except PermissionError as e:
        print(f"Permission error: {e}. Trying to save in the user directory.")
        mp3_file_path = os.path.join(os.path.expanduser("~"), "output.mp3")
        if not os.path.exists(mp3_file_path):
            tts.save(mp3_file_path)
    return mp3_file_path

def speak(text):
    output_folder = "mp3_files"
    mp3_file_path = generate_mp3(output_folder, text)
    print(f"Jarvis: {text}")  # Print the text response to console
    play(mp3_file_path)

def recognize_speech():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Microphone accessed successfully.")
            recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
            print("Listening...")
            audio = recognizer.listen(source)
            
            try:
                print("Recognizing...")
                command = recognizer.recognize_google(audio)
                print(f"User said: {command}")
                return command.lower()  # Convert to lowercase for easier comparison
            except sr.UnknownValueError:
                print("Could not understand audio")
                speak("Sorry, I couldn't understand that.")
                return None
            except sr.RequestError:
                print("Could not request results; check your network connection")
                speak("Sorry, there seems to be a network issue.")
                return None
    except Exception as e:
        print(f"Error accessing the microphone: {e}")
        speak("Sorry, I am having trouble accessing the microphone.")
        return None

def ollama_query(query):
    ollama = Ollama(base_url='http://localhost:11434', model='phi3')  # Adjust URL and model as needed
    return ollama(query)

if __name__ == '__main__':
    speak("Hello, my name is Ollama, how can I help you today?")
    while True:
        query = recognize_speech()
        if query:
            query = query.lower()  # Ensure query is lowercase for consistent comparison
            print(f"User query: {query}")

            if 'time' in query:
                current_time = datetime.datetime.now().strftime("%I:%M %p")
                response_text = f"The current time is {current_time}"
                speak(response_text)
            elif 'today date' in query:
                current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
                response_text = f"Today is {current_date}"
                speak(response_text)
            elif 'play music' in query:
                response_text = "Opening YouTube Music for you. Search for your desired song and enjoy!"
                speak(response_text)
                # You can add functionality to open YouTube Music here if needed
            elif 'open gmail' in query:
                webbrowser.open("https://mail.google.com")
                response_text = "Opening Gmail for you."
                speak(response_text)
            elif 'open facebook' in query:
                webbrowser.open("https://www.facebook.com")
                response_text = "Opening Facebook for you."
                speak(response_text)
            elif 'open instagram' in query:
                webbrowser.open("https://www.instagram.com")
                response_text = "Opening Instagram for you."
                speak(response_text)
            elif 'open linkedin' in query:
                webbrowser.open("https://www.linkedin.com")
                response_text = "Opening LinkedIn for you."
                speak(response_text)
            elif 'open google maps' in query:
                webbrowser.open("https://www.google.com/maps")
                response_text = "Opening Google Maps for you."
                speak(response_text)
            elif 'open groww' in query:
                webbrowser.open("https://groww.in")
                response_text = "Opening Groww for you."
                speak(response_text)
            elif 'open whatsapp' in query:
                webbrowser.open("https://web.whatsapp.com")
                response_text = "Opening WhatsApp for you."
                speak(response_text)
            elif 'open messenger' in query:
                webbrowser.open("https://www.messenger.com")
                response_text = "Opening Messenger for you."
                speak(response_text)
            elif 'search google map' in query:
                location = query.replace("search google map", "").strip()
                webbrowser.open(f"https://www.google.com/maps/search/{location}")
                response_text = f"Showing {location} on Google Maps."
                speak(response_text)
            elif any(word in query for word in ['bye', 'exit', 'quit', 'goodbye']):
                response_text = "Goodbye!"
                speak(response_text)
                break
            else:
                ai_response = ollama_query(query)
                if ai_response:
                    speak(ai_response)
                else:
                    response_text = "Sorry, I couldn't understand that."
                    speak(response_text)
