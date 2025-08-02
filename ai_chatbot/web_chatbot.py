from flask import Flask, render_template, request, jsonify
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/')
def home():
    return render_template('chat.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        ai_message = response.choices[0].message.content
        return jsonify({'message': ai_message})
    except Exception as e:
        return jsonify({'message': f"Sorry, I encountered an error: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)
