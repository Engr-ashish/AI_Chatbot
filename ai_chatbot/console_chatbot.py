import openai
import pyttsx3
import speech_recognition as sr
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

# Initialize text-to-speech engine
engine = pyttsx3.init()

def get_ai_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}"

def voice_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except Exception as e:
            print("Sorry, I didn't catch that.")
            return None

def chatbot():
    print("Welcome to AI Chatbot! Type 'quit' to exit.")
    
    while True:
        print("\nChoose input method:")
        print("1. Type your message")
        print("2. Speak your message")
        choice = input("Enter choice (1 or 2): ")
        
        if choice == '1':
            user_input = input("\nYou: ")
        elif choice == '2':
            user_input = voice_input()
            if user_input is None:
                continue
        else:
            print("Invalid choice. Please try again.")
            continue
            
        if user_input.lower() == 'quit':
            print("Goodbye!")
            break
            
        print("\nAI is thinking...")
        response = get_ai_response(user_input)
        
        print(f"\nAI: {response}")
        
        engine.say(response)
        engine.runAndWait()

if __name__ == "__main__":
    chatbot()
