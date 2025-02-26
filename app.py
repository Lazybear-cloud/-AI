from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app, resources={r"/analyze": {"origins": "*"}})  # 운영 시 "https://sunggonggado.com"으로 제한

# OpenAI API 키 설정 (환경 변수에서 가져오기)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["GET"])
def home():
    return "Flask 서버 정상 작동 중! 프롬프트 입력123"

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.json
        auction_text = data.get("text", "").strip()

        if not auction_text or len(auction_text) < 10:
            return jsonify({"result": "경매 물건의 위치, 감정가, 근저당 여부 등의 정보를 포함하여 입력해 주세요."})

        # OpenAI 프롬프트 생성
        prompt = f"""
        # 📌 부동산 경매 권리분석 리포트

        다음 **경매 물건**의 **권리분석**을 진행해주세요.  
        주어진 정보만 분석하며, 추가적인 추측은 하지 마세요.

        ## **1️⃣ 물건 개요**
        주어진 경매 물건 정보를 기반으로 **소재지, 감정가, 최저가, 면적** 등을 정리해주세요.

        ## **2️⃣ 등기부등본 분석**
        | 구분 | 등기권자 | 채권금액 | 소멸 여부 |
        |------|--------|---------|----------|
        | 말소기준권리 | - | - | - |
        | 후순위 근저당 | - | - | - |
        | 가압류 | - | - | - |

        ✅ **결론:**  
        - 말소기준권리 확인 후 소멸 여부 정리  
        - 낙찰 시 깨끗한 상태로 인수 가능한지 분석  

        ## **3️⃣ 임차인 분석**
        | 임차인 | 점유 | 전입일 | 확정일 | 보증금 | 인수 여부 |
        |--------|------|------|------|------|------|
        | - | - | - | - | - | - |

        ✅ **결론:**  
        - 대항력 있는 임차인의 존재 여부  
        - 낙찰 후 추가 보증금 부담 여부  

        ## **4️⃣ 추가 리스크 분석**
        - 건물 노후화, 지하층 여부, 명도 난이도 등 확인  

        ## **5️⃣ 입찰 전략 및 예상 낙찰가**
        - 과거 매각 사례 비교 후 예상 낙찰가 분석  

        ## **🔍 최종 결론**
        - 낙찰 추천 여부 및 주요 유의사항 정리  

        📍 **입찰 전략:** (추천 입찰가 제공)  
        📍 **리스크:** (추가 확인이 필요한 사항)  

        ## **📌 경매 물건 정보**
        {auction_text}
        """

        # OpenAI API 호출
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "당신은 부동산 경매 권리분석 전문가입니다. 사용자가 입력한 부동산 경매 물건을 분석해 주세요."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=3000
        )

        result = response["choices"][0]["message"]["content"]
        return jsonify({"result": result})

    except Exception as e:
        import traceback
        error_message = traceback.format_exc()
        print("🔥 서버 오류 발생:\n", error_message)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
