# backend/services/origin.py
# small keyword->origin lookup
ORIGIN_MAP = {
    "blue pottery": "Jaipur, Rajasthan",
    "ajrakh": "Kutch, Gujarat",
    "bandhani": "Rajasthan / Gujarat",
    "banarasi": "Varanasi, Uttar Pradesh",
    "madhubani": "Mithila (Bihar)",
    "pattachitra": "Odisha/West Bengal",
    "dokra": "Chhattisgarh / Odisha",
    "khurja": "Khurja, Uttar Pradesh",
    "channapatna": "Channapatna, Karnataka",
    "pashmina": "Kashmir",
    "teracotta": "West Bengal / Tamil Nadu",
    "bluepottery": "Jaipur, Rajasthan"
}

def guess_origin(vision_caption: str, description: str, keywords: list):
    text = " ".join([vision_caption or "", description or "", " ".join(keywords or [])]).lower()
    for k, v in ORIGIN_MAP.items():
        if k in text:
            return v, k
    return None, None
