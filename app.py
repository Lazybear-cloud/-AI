from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, resources={r"/analyze-auction": {"origins": "*"}}, supports_credentials=True)

@app.route("/analyze-auction", methods=["POST"])
def analyze_auction():
    try:
        data = request.get_json()
        if not data or "auction_info" not in data:
            return jsonify({"error": "잘못된 요청 형식"}), 400

        auction_info = data["auction_info"]
        analysis_result = f"경매 분석 결과: '{auction_info}'에 대한 평가 완료."

        return jsonify({"analysis_result": analysis_result}), 200

    except Exception as e:
        print(f"❌ 서버 오류 발생: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # ✅ Render에서 자동으로 포트 설정
    app.run(host="0.0.0.0", port=port, debug=True)
