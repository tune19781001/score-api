# app.py

from flask import Flask, request, jsonify

app = Flask(__name__)

# スコア評価関数（簡易版）
def score_evaluation(inputs):
    total = 0
    comments = []

    # 地合い評価
    if inputs["spy"] > 0 and inputs["qqq"] > 0:
        total += 2
        comments.append("SPY/QQQが上昇 → 地合い良好")
    if inputs["vix"] < 20:
        total += 1
        comments.append("VIX低下 → リスク低め")
    if 145 <= inputs["usd_jpy"] <= 155:
        total += 1
        comments.append("為替安定ゾーン")

    # テクニカル評価
    if inputs["rsi"] < 30:
        total += 2
        comments.append("RSI30以下 → 売られすぎで反発期待")
    if inputs["volume_ratio"] > 1.5:
        total += 1
        comments.append("出来高急増 → 注目度高")
    if inputs["ma_break"]:
        total += 1
        comments.append("移動平均線上抜け")

    # 財務評価
    if inputs["roe"] > 10:
        total += 1
        comments.append("ROE > 10% → 経営効率◎")
    if inputs["profit_margin"] > 15:
        total += 1
        comments.append("利益率高い → 収益性あり")

    return total, comments

# ルートエンドポイント（確認用）
@app.route("/")
def index():
    return "スコア評価BotのAPIが起動しています！"

# 評価用のPOSTエンドポイント
@app.route("/score", methods=["POST"])
def score():
    data = request.json
    score, comments = score_evaluation(data)
    result = {
        "score": score,
        "comments": comments,
        "judgment": judge(score)
    }
    return jsonify(result)

# 判定ロジック
def judge(score):
    if score >= 15:
        return "🟢 強気判断（条件が整っている）"
    elif score >= 12:
        return "🟡 条件付きGO（不安要素あり）"
    elif score >= 10:
        return "🟠 保留（様子見）"
    else:
        return "🔴 弱気（見送り推奨）"

if __name__ == "__main__":
    app.run(port=8000)
