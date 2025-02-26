from flask import Flask, request, jsonify
import openai
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 워드프레스에서 요청 가능하도록 CORS 활성화

openai.api_key = "YOUR_OPENAI_API_KEY"  # OpenAI API 키 설정

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    auction_text = data.get("text", "")

    # OpenAI API 호출
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "경매 물건을 분석해줘."},
                  {"role": "user", "content": auction_text}]
    )

    result = response["choices"][0]["message"]["content"]
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(debug=True)
