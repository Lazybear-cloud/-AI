from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app, resources={r"/analyze": {"origins": "https://sunggonggado.com"}})

openai.api_key = os.getenv("OPENAI_API_KEY")  # OpenAI API 키 환경 변수에서 가져오기

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

        # 최신 OpenAI API 방식 적용
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "경매 물건을 분석해줘."},
                {"role": "user", "content": auction_text}
            ]
        )

        result = response.choices[0].message.content
        return jsonify({"result": result})

    except Exception as e:
        import traceback
        error_message = traceback.format_exc()
        print("🔥 서버 오류 발생:\n", error_message)  # Render Logs에서 확인 가능
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
