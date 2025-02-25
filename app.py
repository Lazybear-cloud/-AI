from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Flask 서버 실행 중!"

app = Flask(__name__)

# ✅ OpenAI 클라이언트 객체 올바르게 생성
client = openai.Client(api_key="OPEN_API_KEY")

@app.route("/chatbot", methods=["POST"])
def chatbot():
    try:
        data = request.get_json()
        if not data or "message" not in data:
            return jsonify({"error": "잘못된 요청 형식"}), 400  # 400 Bad Request 반환

        user_input = data["message"]

        response = client.chat.completions.create(  # ✅ 최신 OpenAI API 방식
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "당신은 부동산 경매에 대한 전문가입니다. 사용자의 질문에 대해 직접적인 답변을 제공하세요."},  # ✅ 응답을 직접 하도록 유도
                {"role": "user", "content": user_input}
            ]
        )

        return jsonify({"response": response.choices[0].message.content})

    except Exception as e:
        print(f"❌ 서버 오류 발생: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
