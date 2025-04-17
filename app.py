from flask import Flask, request, jsonify, send_from_directory
import os
from memory_bot import (
    save_judgment,
    search_similar,
    update_conversation,
    get_conversation_history,
    get_response  # 会話補助追加分
)

app = Flask(__name__)

# スコア評価関数（簡易版）
def score_evaluation(inputs):
    total = 0
    comments = []

    if inputs["spy"] > 0 and inputs["qqq"] > 0:
        total += 2
        comments.append("SPY/QQQが上昇 → 地合い良好")
    if inputs["vix"] < 20:
        total += 1
        comments.append("VIX低下 → リスク低め")
    if 145 <= inputs["usd_jpy"] <= 155:
        total += 1
        comments.append("為替安定ゾーン")

    if inputs["rsi"] < 30:
        total += 2
        comments.append("RSI30以下 → 売られすぎで反発期待")
    if inputs["volume_ratio"] > 1.5:
        total += 1
        comments.append("出来高急増 → 注目度高")
    if inputs["ma_break"]:
        total += 1
        comments.append("移動平均線上抜け")

    if inputs["roe"] > 10:
        total += 1
        comments.append("ROE > 10% → 経営効率◎")
    if inputs["profit_margin"] > 15:
        total += 1
        comments.append("利益率高い → 収益性あり")

    return total, comments

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

@app.route("/")
def index():
    return "スコア評価BotのAPIが起動しています！"

# ✅ スコア評価API（保存・会話メモリ付き）
@app.route("/score", methods=["POST"])
def score():
    data = request.json
    score_val, comments = score_evaluation(data)
    judgment = judge(score_val)

    result = {
        "score": score_val,
        "comments": comments,
        "judgment": judgment,
        "saved": True
    }

    update_conversation(str(data), str(result))
    save_judgment(str(data), judgment)

    return jsonify(result)

# ✅ 判断記録API
@app.route("/save_judgment", methods=["POST"])
def save():
    data = request.json
    input_text = data.get("input")
    result = data.get("result")

    if not input_text or not result:
        return jsonify({"error": "input and result are required"}), 400

    save_judgment(input_text, result)
    return jsonify({"status": "記録しました！"})

# ✅ 類似判断検索API（整形済みで返す）
@app.route("/search_similar", methods=["POST"])
def search():
    data = request.json
    input_text = data.get("input")

    if not input_text:
        return jsonify({"error": "input is required"}), 400

    raw = search_similar(input_text)
    history_text = raw.get("history", "")
    lines = history_text.strip().split("\n")
    pairs = [{"input": lines[i][7:], "output": lines[i + 1][8:]} for i in range(0, len(lines)-1, 2)]
    return jsonify({"results": pairs})

# ✅ 会話履歴API（最新3件のみ返す）
@app.route("/conversation_history", methods=["GET"])
def history():
    history_text = get_conversation_history(limit=3)
    return jsonify({"history": history_text})

# ✅ UptimeRobot 対応用の memory API（GET + 会話応答付きPOST）
@app.route("/memory", methods=["GET", "POST"])
def memory_check():
    if request.method == "GET":
        return "Memory bot is alive!"

    try:
        input_text = request.json.get("input", "")
        response = get_response(input_text)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# GPT用ファイル配信（.well-known）
@app.route('/.well-known/<path:filename>')
def well_known_static(filename):
    return send_from_directory('.well-known', filename)

@app.route('/.well-known/openapi.yaml')
def serve_openapi_yaml():
    return send_from_directory(
        '.well-known',
        'openapi.yaml',
        mimetype='application/yaml'
    )

# Flask起動（Render用）
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)