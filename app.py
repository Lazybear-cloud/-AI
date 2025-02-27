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

        auction_prompt = f"""
        사용자가 입력한 부동산 경매 물건 정보를 분석하세요.
        
        📌 분석 시 **볼드체(굵은 글씨)를 사용하지 말고**, 적절한 이모티콘(예: 🏠, 💰, ⚠️ 등)을 활용하여 가독성을 높여주세요.
        
        입력된 정보:
        {auction_text}
        
        📊 분석 내용
        1️⃣ 기본 정보: 물건의 위치, 감정가, 최저 입찰가
        2️⃣ 권리관계 분석: 근저당, 압류, 가처분, 가등기 등
        3️⃣ 권리분석 위험 요소: 인수해야 할 채무, 인수해야하는 권리, 소송 위험 ⚠️
        4️⃣ 명도 난이도 : 명도 대상, 명도 가능성과 전략을 간단히
        5️⃣ 수익성 평가: 예상 매각 가격, 임대 수익 가능성 💰
        6️⃣ 추천 여부: 투자 관점에서 추천 여부 및 추가 확인해야 할 사항 🤔
        ⚠️ 유의할 점 : 선순위 임차인, 말소되지 않고 인수되는 권리, 손해 가능성, 대위변제 가능성 등
        """

        
        # OpenAI API 호출
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "당신은 부동산 경매 권리분석 전문가입니다. 사용자가 입력한 부동산 경매 물건을 분석해 주세요. 경매 물건을 철저히 분석하고, 투자 적합성을 평가하며, 법률적 위험 요소를 식별하는 역할을 합니다."},
                {"role": "user", "content": auction_prompt}
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
