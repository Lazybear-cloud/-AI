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
                {"role": "system", "content": "당신은 대한민국 부동산 경매 권리분석 전문가입니다. 사용자가 입력한 경매 물건 정보를 분석하고, 문제점을 파악하며, 투자 적합성을 평가하는 역할을 합니다. 해당 물건의 권리관계, 채무 부담, 입찰 시 주의사항, 수익성 분석을 고려하여 답변하세요. 법률적 위험 요소와 추가 확인해야 할 점도 포함해 주세요."},
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
