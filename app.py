from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app, resources={r"/analyze": {"origins": "https://sunggonggado.com"}})

# OpenAI API 키 설정 (환경 변수에서 가져오기)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["GET"])
def home():
    return "Flask 서버 정상 작동 중!"

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.json
        auction_text = data.get("text", "").strip()

        if not auction_text or len(auction_text) < 10:
            return jsonify({"result": "경매 물건의 위치, 감정가, 근저당 여부 등의 정보를 포함하여 입력해 주세요."})
        
        # OpenAI API 호출
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "당신은 부동산 경매 권리분석 전문가입니다. 사용자가 입력한 부동산 경매 물건을 분석해 주세요."},
                {"role": "user", "content": auction_text}
            ]
        )

        # OpenAI에서 반환된 순수 텍스트
        result = response.choices[0].message.content.strip()
        
        return jsonify({"result": result})  # HTML 없이 텍스트만 반환

    except Exception as e:
        import traceback
        error_message = traceback.format_exc()
        print("🔥 서버 오류 발생:\n", error_message)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
