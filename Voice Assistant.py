import tkinter as tk
from tkinter import ttk
from threading import Thread
import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia

# Initialize the speech recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Function to convert text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to greet the user
def greet():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good morning!")
    elif 12 <= hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak("How can I assist you today?")

# Function to recognize user's speech
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            query = recognizer.recognize_google(audio, language='en-US')
            print("User:", query)
            return query.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't get that. Can you repeat?")
            return listen()
        except sr.RequestError:
            speak("Sorry, I'm currently not available. Please try again later.")
            return ""

# Function to perform tasks based on user input
def perform_task(query):
    if 'wikipedia' in query:
        speak("Searching Wikipedia...")
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        speak(results)
    # Add more tasks here based on user preferences
    else:
        speak("Sorry, I couldn't understand that request.")

# Function to start the voice assistant
def start_assistant():
    greet()
    while True:
        query = listen()
        if 'exit' in query:
            speak("Goodbye!")
            break
        perform_task(query)

# Function to start the assistant in a separate thread
def start_assistant_thread():
    assistant_thread = Thread(target=start_assistant)
    assistant_thread.start()

# Function to stop the assistant
def stop_assistant():
    # Stop any speaking currently in progress
    engine.stop()

# Create a Tkinter window
root = tk.Tk()
root.title("Voice Assistant")

# Create a button to start the assistant
start_button = ttk.Button(root, text="Start Assistant", command=start_assistant_thread)
start_button.pack(pady=10)

# Create a button to stop the assistant
stop_button = ttk.Button(root, text="Stop Assistant", command=stop_assistant)
stop_button.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()