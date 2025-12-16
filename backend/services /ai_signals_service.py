import json
from backend.services.ai_client import get_ai_client
from backend.services.ai_prompts import ai_signal_prompt

def _safe_json_load(text: str):
    """
    يحاول يخرج JSON حتى لو الموديل رجّع نص فيه زيادة.
    """
    text = (text or "").strip()

    # حاول direct
    try:
        return json.loads(text)
    except Exception:
        pass

    # حاول تلقى أول { وآخر }
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        chunk = text[start:end+1]
        try:
            return json.loads(chunk)
        except Exception:
            pass

    return None


def generate_signal(asset: str, timeframe: str, market: str, halal_strict: bool = True):
    """
    يرجّع Signal في شكل dict:
    {
      "action": "BUY/SELL/HOLD",
      "entry": 0,
      "stop_loss": 0,
      "take_profit": [..],
      "confidence": 0-100,
      "notes": "..."
    }
    """
    client = get_ai_client()

    prompt = ai_signal_prompt(asset, timeframe, market)
    # إضافة شرط الحلال بوضوح
    if market == "stock" and halal_strict:
        prompt += "\n\nمهم: السهم لازم يكون حلال، إذا فيه شبهة قل HOLD وفسّر."

    # مهم: نخلي الموديل يرجّع JSON فقط
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "أنت محلل تداول محترف. أرجع JSON فقط."},
            {"role": "user", "content": prompt}
        ],
        # إذا مكتبتك تدعمها، تخلي المخرجات JSON مضبوط
        response_format={"type": "json_object"}
    )

    raw = resp.choices[0].message.content
    data = _safe_json_load(raw)

    if not data:
        raise RuntimeError("AI did not return valid JSON")

    # تطبيع حقول أساسية
    action = str(data.get("action", "HOLD")).upper()
    entry = float(data.get("entry", 0) or 0)
    stop_loss = float(data.get("stop_loss", 0) or 0)

    tp = data.get("take_profit", data.get("take_profits", []))
    if isinstance(tp, (int, float, str)):
        tps = [float(tp)]
    elif isinstance(tp, list):
        tps = [float(x) for x in tp if x is not None]
    else:
        tps = []

    confidence = data.get("confidence", 0)
    try:
        confidence = int(confidence)
    except Exception:
        confidence = 0

    return {
        "action": action,
        "entry": entry,
        "stop_loss": stop_loss,
        "take_profit": tps,
        "confidence": confidence,
        "notes": data.get("notes", "")
    }
