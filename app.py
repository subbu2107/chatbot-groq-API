from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Groq Client
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# Store Chat Memory
chat_history = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():

    user_message = request.json.get("message")

    try:

        messages = [
            {
                "role": "system",
                "content": "You are Victor AI, a smart AI assistant."
            }
        ]

        # Add previous chat memory
        for item in chat_history[-8:]:
            messages.append(item)

        # Current user message
        messages.append({
            "role": "user",
            "content": user_message
        })

        # AI Response
        response = client.chat.completions.create(

            model="qwen/qwen3-32b",

            messages=messages,

            temperature=0.7,

            max_tokens=500
        )

        reply = response.choices[0].message.content

        # Save Memory
        chat_history.append({
            "role": "user",
            "content": user_message
        })

        chat_history.append({
            "role": "assistant",
            "content": reply
        })

        return jsonify({
            "reply": reply,
            "time": datetime.now().strftime("%I:%M %p")
        })

    except Exception as e:

        return jsonify({
            "reply": str(e)
        })

if __name__ == "__main__":
    app.run(debug=True)