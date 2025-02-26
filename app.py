from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app, resources={r"/analyze": {"origins": "https://sunggonggado.com"}})

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["GET"])
def home():
    return "Flask 서버 정상 작동 중!"

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.json
        auction_text = data.get("text", "")

        if not auction_text:
            return jsonify({"error": "No text provided"}), 400

        # OpenAI API 최신 버전 코드 적용
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "경매 물건을 분석해줘."},
                {"role": "user", "content": auction_text}
            ]
        )

        result = response.choices[0].message.content
        return jsonify({"result": result})

    except Exception as e:
        print("🔥 서버 오류 발생:", str(e))  # 오류 로그 출력
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
