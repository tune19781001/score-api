def calculate_score(data):
    score = 0
    category_scores = {
        "market": 0,
        "technical": 0,
        "chart": 0,
        "fundamentals": 0
    }
    comments = []

    # 地合い（最大5点）
    if data.get("spy", 0) > 0:
        category_scores["market"] += 2
        comments.append("SPYが上昇 → 地合い加点")
    if data.get("qqq", 0) > 0:
        category_scores["market"] += 1
        comments.append("QQQが上昇 → テック系加点")
    if data.get("vix", 100) < 15:
        category_scores["market"] += 1
        comments.append("VIX低下 → リスクオン地合い")
    if 145 <= data.get("usd_jpy", 0) <= 155:
        category_scores["market"] += 1
        comments.append("ドル円が安定 → 為替評価良")

    # テクニカル（最大5点）
    if data.get("rsi", 0) < 30:
        category_scores["technical"] += 2
        comments.append("RSI30以下 → 反発候補で加点")
    elif 50 <= data.get("rsi", 0) <= 60:
        category_scores["technical"] += 1
        comments.append("RSI中立帯 → 初動サイン")

    if data.get("volume_ratio", 0) >= 1.2:
        category_scores["technical"] += 1
        comments.append("出来高増 → 注目度加点")

    if data.get("ma_break", False):
        category_scores["technical"] += 2
        comments.append("MAブレイク → トレンド転換加点")

    # チャート需給（最大5点）
    if data.get("volume_ratio", 0) > 1.5 and data.get("rsi", 0) > 50:
        category_scores["chart"] += 3
        comments.append("出来高＋RSI初動 → チャート良好")
    elif data.get("volume_ratio", 0) > 1.2:
        category_scores["chart"] += 2
        comments.append("出来高のみ加点")

    # 財務（最大5点）
    if data.get("roe", 0) > 10:
        category_scores["fundamentals"] += 2
        comments.append("ROE10%以上 → 財務健全")
    if data.get("profit_margin", 0) > 10:
        category_scores["fundamentals"] += 1
        comments.append("利益率10%以上 → 収益力あり")

    total = sum(category_scores.values())

    if total >= 15:
        judgment = "⭕ 波に乗れる"
    elif 12 <= total <= 14:
        judgment = "△ 条件付きGO"
    elif 10 <= total <= 11:
        judgment = "⚠ 様子見"
    else:
        judgment = "❌ 静観"

    return {
        "score": total,
        "judgment": judgment,
        "category_scores": category_scores,
        "comments": comments
    }
