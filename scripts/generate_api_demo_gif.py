from PIL import Image, ImageDraw, ImageFont
import os, textwrap

OUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'docs')
os.makedirs(OUT_DIR, exist_ok=True)
OUT_PATH = os.path.join(OUT_DIR, 'demo_api.gif')

W, H = 900, 480
BG = (18,18,18)
CARD_BG = (30,30,30)
ACCENT = (0,150,136)
TEXT_COLOR = (230,230,230)
FONT_SIZE_TITLE = 28
FONT_SIZE_BODY = 16

try:
    font_title = ImageFont.truetype("DejaVuSans-Bold.ttf", FONT_SIZE_TITLE)
    font_body = ImageFont.truetype("DejaVuSans.ttf", FONT_SIZE_BODY)
except Exception:
    from PIL import ImageFont
    font_title = ImageFont.load_default()
    font_body = ImageFont.load_default()

frames = []

steps = [
    {
        "title": "Agentic Pay — Authorize Agent (GOOD)",
        "request": {
            "agent_id": "agent_demo",
            "spending_limit": 100,
            "currency": "USD",
            "merchant_category": "restaurants"
        },
        "response": {
            "status": "Authorized",
            "consent_id": "consent_tkn_demo_001",
            "merchant_constraints": "restaurants"
        }
    },
    {
        "title": "Agentic Pay — Authorize Agent (BAD)",
        "request": {
            "agent_id": "agent_demo_bad",
            "spending_limit": 600,
            "currency": "USD",
            "merchant_category": "casino"
        },
        "response": {
            "status": "Denied",
            "reason": "Limit Exceeded or Prohibited Category (casino)"
        }
    },
    {
        "title": "Carbon Impact — Enrich Transaction (LOW)",
        "request": {
            "mcc": "5411",
            "amount": 50.00,
            "description": "Weekly groceries"
        },
        "response": {
            "original_transaction": "Weekly groceries",
            "merchant_category": "Grocery Stores",
            "carbon_footprint_kg": 6.0,
            "insight": {"text": "Low carbon impact — consider this option frequently", "good": True}
        }
    },
    {
        "title": "Carbon Impact — Enrich Transaction (HIGH)",
        "request": {
            "mcc": "5541",
            "amount": 50.00,
            "description": "Fuel purchase"
        },
        "response": {
            "original_transaction": "Fuel purchase",
            "merchant_category": "Gas Stations",
            "carbon_footprint_kg": 105.0,
            "insight": {"text": "High carbon impact — consider alternatives or offsets", "good": False}
        }
    }
]

def render_card(draw, x, y, w, h, title, body_lines, font_title, font_body):
    padding = 12
    # background
    draw.rectangle([x, y, x+w, y+h], fill=CARD_BG, outline=(60,60,60))
    # title
    draw.text((x+padding, y+padding), title, font=font_title, fill=ACCENT)
    # body (supports either plain strings or (text, color) tuples)
    oy = y+padding+40
    for item in body_lines:
        if isinstance(item, tuple):
            line, color = item
        else:
            line, color = item, TEXT_COLOR
        draw.text((x+padding, oy), line, font=font_body, fill=color)
        oy += 22

for step in steps:
    # title frame
    img = Image.new('RGB', (W, H), color=BG)
    d = ImageDraw.Draw(img)
    # header
    d.text((20,16), step['title'], font=font_title, fill=TEXT_COLOR)
    d.text((20,54), 'Request → Response', font=font_body, fill=(180,180,180))
    # request card
    req_text = []
    import json
    req_json = json.dumps(step['request'], indent=2)
    for line in req_json.splitlines():
        req_text += textwrap.wrap(line, width=40) or ['']
    render_card(d, 20, 100, 420, 320, 'Request', req_text, font_title, font_body)
    # response card
    res_text = []
    # render response fields except 'insight'
    resp_fields = {k: v for k, v in step['response'].items() if k != 'insight'}
    res_json = json.dumps(resp_fields, indent=2)
    for line in res_json.splitlines():
        res_text += textwrap.wrap(line, width=40) or ['']
    # append insight if present (colored)
    insight = step['response'].get('insight')
    if insight:
        color = (50,205,50) if insight.get('good') else (255,69,0)
        res_text.append('')
        res_text.append((f"INSIGHT: {insight.get('text')}", color))
    render_card(d, 460, 100, 420, 320, 'Response', res_text, font_title, font_body)
    frames.append(img)

# Add a closing summary frame
img = Image.new('RGB', (W, H), color=BG)
d = ImageDraw.Draw(img)
d.text((20,120), 'Demo complete — explore the API at /docs', font=font_title, fill=TEXT_COLOR)
frames.append(img)

frames[0].save(OUT_PATH, format='GIF', append_images=frames[1:], save_all=True, duration=1200, loop=0)
print('Wrote demo GIF to', OUT_PATH)
