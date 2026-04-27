import os
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# This client will look for the OPENAI_API_KEY env var we set in EKS
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route('/')
def home():
    return "OpenAI Flask App is Running on EKS!"

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    prompt = data.get("prompt", "Hello, Gemini!")
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return jsonify({"response": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
