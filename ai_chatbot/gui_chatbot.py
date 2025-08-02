import openai
import tkinter as tk
from tkinter import scrolledtext, ttk
import threading
import pyttsx3
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

class ChatbotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Chatbot")
        self.root.geometry("600x500")
        
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TButton', font=('Arial', 10), padding=5)
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        
        self.create_widgets()
        self.engine = pyttsx3.init()
        
    def create_widgets(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.chat_display = scrolledtext.ScrolledText(
            main_frame, wrap=tk.WORD, width=60, height=20,
            font=('Arial', 10), state='disabled'
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X)
        
        self.user_input = tk.Text(
            input_frame, height=3, wrap=tk.WORD, font=('Arial', 10)
        )
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.user_input.bind("<Return>", self.send_message_event)
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        send_button = ttk.Button(
            button_frame, text="Send", command=self.send_message
        )
        send_button.pack(side=tk.LEFT, padx=(0, 5))
        
        clear_button = ttk.Button(
            button_frame, text="Clear", command=self.clear_chat
        )
        clear_button.pack(side=tk.LEFT)
        
        self.status = ttk.Label(
            main_frame, text="Ready", relief=tk.SUNKEN, anchor=tk.W
        )
        self.status.pack(fill=tk.X, pady=(5, 0))
        
    def send_message_event(self, event):
        self.send_message()
        return "break"
        
    def send_message(self):
        message = self.user_input.get("1.0", tk.END).strip()
        if not message:
            return
            
        self.update_chat("You", message)
        self.user_input.delete("1.0", tk.END)
        self.user_input.config(state=tk.DISABLED)
        self.status.config(text="AI is thinking...")
        
        threading.Thread(
            target=self.get_ai_response,
            args=(message,),
            daemon=True
        ).start()
        
    def get_ai_response(self, prompt):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            ai_message = response.choices[0].message.content
            
            self.root.after(0, lambda: self.update_chat("AI", ai_message))
            self.root.after(0, self.speak_response, ai_message)
            
        except Exception as e:
            error_msg = f"Sorry, I encountered an error: {str(e)}"
            self.root.after(0, lambda: self.update_chat("AI", error_msg))
            
        finally:
            self.root.after(0, self.enable_input)
            
    def update_chat(self, sender, message):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"{sender}: {message}\n\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
        
    def speak_response(self, text):
        self.engine.say(text)
        self.engine.runAndWait()
        
    def enable_input(self):
        self.user_input.config(state=tk.NORMAL)
        self.status.config(text="Ready")
        
    def clear_chat(self):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete("1.0", tk.END)
        self.chat_display.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatbotGUI(root)
    root.mainloop()
