from PIL import Image, ImageDraw, ImageFont
import os

OUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'docs')
os.makedirs(OUT_DIR, exist_ok=True)
OUT_PATH = os.path.join(OUT_DIR, 'demo.gif')

W, H = 640, 360
BG_COLORS = [(30,144,255), (34,139,34), (255,140,0), (128,0,128)]
TEXTS = [
    "Agentic Pay Demo",
    "POST /agent/authorize-agent",
    "Carbon Impact Demo",
    "POST /carbon/enrich-transaction",
]

frames = []
try:
    font = ImageFont.truetype("DejaVuSans-Bold.ttf", 28)
except Exception:
    from PIL import ImageFont
    font = ImageFont.load_default()

for i, txt in enumerate(TEXTS):
    img = Image.new('RGB', (W, H), color=BG_COLORS[i % len(BG_COLORS)])
    d = ImageDraw.Draw(img)
    # measure text using textbbox for compatibility
    bbox = d.textbbox((0,0), txt, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    d.text(((W-w)/2, (H-h)/2), txt, font=font, fill=(255,255,255))
    # add small subtitle
    subtitle = "Open Finance Prototypes"
    sbbox = d.textbbox((0,0), subtitle, font=font)
    sw, sh = sbbox[2] - sbbox[0], sbbox[3] - sbbox[1]
    d.text(((W-sw)/2, (H-h)/2 + 50), subtitle, font=font, fill=(255,255,255))
    frames.append(img)

# save animated GIF
frames[0].save(OUT_PATH, format='GIF', append_images=frames[1:], save_all=True, duration=1200, loop=0)
print(f"Wrote demo GIF to {OUT_PATH}")
