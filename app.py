from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv
from flask import render_template

# Load environment variables from .env
load_dotenv("ts.env")

app = Flask(__name__)
CORS(app)

# Load Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print(" Gemini API key not found. Running in DEMO MODE.")

# -------------------------------
# Test route (optional but useful)
# -------------------------------
@app.route("/test", methods=["GET"])
def test():
    return jsonify({
        "status": "Flask running",
        "gemini_key_loaded": bool(GEMINI_API_KEY)
    })


@app.route("/")
def home():
    return render_template("index.html")


# -------------------------------
# Main analyze route
# -------------------------------
@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({"error": "No text provided"}), 400

    user_text = data["text"].strip()

    if not user_text:
        return jsonify({"error": "Empty message"}), 400

    if len(user_text) > 2000:
        return jsonify({"error": "Message too long"}), 400

    # DEMO MODE (no API key)
    if not GEMINI_API_KEY:
        return jsonify({
            "result": (
                "Demo mode response:\n\n"
                "The message cannot be analyzed using Gemini because "
                "the API key is not configured. "
                "This placeholder exists for evaluation purposes."
            )
        })

    # Gemini API endpoint
    url = (
    "https://generativelanguage.googleapis.com/v1beta/"
    "models/gemini-pro:generateContent?key=" + GEMINI_API_KEY
)

       

    # Structured prompt (better results)
    prompt = f"""
You are a cybersecurity assistant.

Analyze the following message and classify it as:
- Fraud
- Suspicious
- Safe

Explain the reasons in simple bullet points.

Message:
{user_text}
"""

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    try:
        response = requests.post(url, json=payload, timeout=20)
        response.raise_for_status()

        gemini_output = response.json()
        result_text = gemini_output["candidates"][0]["content"]["parts"][0]["text"]

        return jsonify({"result": result_text})

    except Exception as e:
        return jsonify({
            "result": "Gemini service is currently unavailable. Please try again later.",
            "error": str(e)
        }), 500

print(app.url_map)
print("Gemini key loaded:", bool(os.getenv("GEMINI_API_KEY")))



# -------------------------------
# Run the app
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)
