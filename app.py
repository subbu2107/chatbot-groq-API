from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
import os

# Load .env
load_dotenv()

app = Flask(__name__)

# Groq Client
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# Memory
chat_history = []

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    user_message = data.get("message")

    try:

        messages = [
            {
                "role": "system",
                "content": "You are Victor AI, a powerful AI assistant."
            }
        ]

        # Previous memory
        for item in chat_history[-8:]:
            messages.append(item)

        # Current message
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


# IMPORTANT FOR VERCEL
app = app
