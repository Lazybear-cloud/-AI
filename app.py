from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app, resources={r"/analyze": {"origins": "https://sunggonggado.com"}})

# OpenAI API 키 설정
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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

        # 프롬프트 수정 (번호 중복 제거)
        auction_prompt = f"""
        사용자가 입력한 부동산 경매 물건 정보를 분석하세요.

        📌 분석 시 **볼드체(굵은 글씨)를 사용하지 말고**, 적절한 이모티콘(예: 🏠, 💰, ⚠️ 등)을 활용하여 가독성을 높여주세요.

        입력된 정보:
        {auction_text}

        📊 분석 내용
        1️⃣ 기본 정보: 물건의 위치, 감정가, 최저 입찰가
        2️⃣ 권리관계 분석: 근저당, 압류, 가처분, 가등기 등과 말소기준권리
        3️⃣ 법률적 위험 요소: 인수해야 할 채무, 소송 위험 ⚠️
        4️⃣ 명도 난이도 : 명도 난이도와 가능성
        5️⃣ 수익성 평가: 예상 매각 가격, 임대 수익 가능성 💰
        6️⃣ 추천 여부: 투자 관점에서 추천 여부 및 추가 확인해야 할 사항 🤔
        """

        # OpenAI API 호출
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": """당신은 대한민국 부동산 경매 권리분석 전문가입니다. 
                사용자가 입력한 경매 물건 정보를 분석하고, 문제점을 파악하며, 투자 적합성을 평가하는 역할을 합니다. 
                해당 물건의 권리관계, 채무 부담, 입찰 시 주의사항, 수익성 분석을 고려하여 답변하세요. 법률적 위험 요소와 추가 확인해야 할 점도 포함해 주세요."""},
                {"role": "user", "content": auction_prompt}
            ]
        )

        # OpenAI 응답 처리 (최신 버전 대응)
        result = response.choices[0].message['content'].strip()
        
        return jsonify({"result": result})  

    except Exception as e:
        import traceback
        error_message = traceback.format_exc()
        print("🔥 서버 오류 발생:\n", error_message)
        return jsonify({"error": "서버 오류가 발생했습니다. 다시 시도해 주세요."}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
