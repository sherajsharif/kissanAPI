from flask import Flask, request, jsonify
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
import asyncio
import httpx

# Load environment variables from .env
load_dotenv()
api_key = os.getenv("DHENU_API_KEY")

# Initialize AsyncOpenAI client with Dhenu API
client = AsyncOpenAI(
    base_url="https://api.dhenu.ai/v1",
    api_key=api_key,
    timeout=60,  # Increase timeout as Dhenu API may be slow
)

app = Flask(__name__)

@app.route("/", methods=["GET"])
def root():
    return jsonify({
        "name": "Kissan AI",
        "made_by": "Rishiswar Industry Private Limited",
        "message": "Namaste! Main Kissan AI hoon, Rishiswar Industry Private Limited dwara viksit ek prasangik kisaan sahayak API. Yeh API aapko kisaan sambandhit sawalon ke liye sahi uttar pradan karta hai."
    }), 200

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "name": "Kissan AI",
        "made_by": "Rishiswar Industry Private Limited"
    }), 200

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    if not data or "query" not in data or not data["query"].strip():
        return jsonify({"error": "Please provide a valid 'query' field in JSON."}), 400
    query = data["query"].strip()

    async def get_response():
        try:
            response_text = ""
            stream = await client.chat.completions.create(
                model="dhenu2-in-8b-preview",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are Kissan AI, an agricultural assistant developed by Rishiswar Industry Private Limited. "
                            "Always introduce yourself as Kissan AI and never mention Dhenu or any other provider. "
                            "Answer all questions in a helpful, friendly, and professional manner, focusing on Indian agriculture."
                        )
                    },
                    {"role": "user", "content": query}
                ],
                stream=True,
                stream_options={"include_usage": True}
            )
            async for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    response_text += chunk.choices[0].delta.content
            return {"response": response_text}
        except httpx.TimeoutException:
            return {"error": "Request to Dhenu API timed out."}
        except Exception as e:
            return {"error": f"Error: {str(e)}"}

    result = asyncio.run(get_response())
    status_code = 200 if "response" in result else 500
    return jsonify(result), status_code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
