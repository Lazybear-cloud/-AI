from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# ✅ 환경 변수에서 OpenAI API Key 가져오기 (Render에서 자동으로 설정됨)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def home():
    return "Flask 챗봇 서버가 실행 중입니다! 🚀"

@app.route("/chatbot", methods=["POST"])
def chatbot():
    try:
        data = request.get_json()
        if not data or "message" not in data:
            return jsonify({"error": "잘못된 요청 형식"}), 400  # 400 Bad Request

        user_input = data["message"]

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": user_input}]
        )

        return jsonify({"response": response["choices"][0]["message"]["content"]})

    except Exception as e:
        print(f"❌ 서버 오류 발생: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # ✅ Render에서 자동으로 포트 설정
    app.run(host="0.0.0.0", port=port, debug=True)
