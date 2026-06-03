from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

# Groq Client
client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():

    user_message = request.json.get("message")

    try:

        response = client.chat.completions.create(

            model="qwen/qwen3-32b",

            messages=[
                {
                    "role": "user",
                    "content": user_message
                }
            ],

            temperature=0.7,

            max_tokens=300
        )

        reply = response.choices[0].message.content

        return jsonify({
            "reply": reply
        })

    except Exception as e:

        return jsonify({
            "reply": str(e)
        })

# IMPORTANT FOR VERCEL
app = app
