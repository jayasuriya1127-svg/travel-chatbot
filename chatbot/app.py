import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai
from google.genai import types

from chatbot_config import TRAVEL_MATE_SYSTEM_PROMPT

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")

if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not configured in the .env file.")

client = genai.Client(api_key=API_KEY)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()

    if not message:
        return jsonify({"error": "Please enter a message."}), 400

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=message,
            config=types.GenerateContentConfig(
                system_instruction=TRAVEL_MATE_SYSTEM_PROMPT,
                temperature=0.4,
                max_output_tokens=800,
            ),
        )

        answer = response.text.strip() if response.text else "I couldn't generate a response."
        return jsonify({"reply": answer})

    except Exception:
        return jsonify({
            "error": "I'm having trouble connecting right now. Please try again."
        }), 500


if __name__ == "__main__":
    app.run()
