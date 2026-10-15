"""Genera los QR en forma de corazón de todas las galaxias, un CSV y un PDF imprimible.

Uso (un solo comando):
    python generar_qr.py https://TU-SITIO/        (sin argumento usa BASE_URL)
Requisitos: pip install qrcode pillow reportlab   (opcional para verificar: opencv-python-headless)
"""
import sys, csv, os, math
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm

BASE_URL = "https://sozin0512.github.io/100-galaxias-para-mi-nina/"
TOTAL = 100
base = (sys.argv[1] if len(sys.argv) > 1 else BASE_URL).rstrip("/")
aqui = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(aqui, "qr"), exist_ok=True)
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
if not os.path.exists(FONT): FONT = None

def heart_poly(cx, cy, k, n=400):
    pts = []
    for i in range(n):
        t = i / n * 2 * math.pi
        x = 16 * math.sin(t) ** 3
        y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        pts.append((cx + x * k, cy - y * k))
    return pts

def tarjeta(i, url):
    S = 1200
    img = Image.new("RGB", (S, S), "white")
    # brillo suave detrás del corazón
    glow = Image.new("L", (S, S), 0); ImageDraw.Draw(glow).polygon(heart_poly(S / 2, S * 0.47, 37.5), fill=255)
    glow = glow.filter(ImageFilter.GaussianBlur(28))
    img.paste(Image.new("RGB", (S, S), (255, 182, 207)), (0, 0), glow)
    # corazón con degradado rosa → rojo
    mask = Image.new("L", (S, S), 0); ImageDraw.Draw(mask).polygon(heart_poly(S / 2, S * 0.47, 36), fill=255)
    grad = Image.new("RGB", (S, S)); gd = ImageDraw.Draw(grad)
    for y in range(S):
        k = y / S; gd.line([(0, y), (S, y)], fill=(int(255 - 40 * k), int(105 - 85 * k), int(160 - 110 * k)))
    img.paste(grad, (0, 0), mask)
    d = ImageDraw.Draw(img)
    d.line(heart_poly(S / 2, S * 0.47, 36) + [heart_poly(S / 2, S * 0.47, 36)[0]], fill=(255, 235, 242), width=6)
    # QR (corrección H) con módulos redondeados rojo oscuro, sobre recuadro blanco con zona silenciosa
    q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=14, border=3)
    q.add_data(url); q.make(fit=True)
    qi = q.make_image(image_factory=StyledPilImage, module_drawer=RoundedModuleDrawer(radius_ratio=0.5),
                      color_mask=SolidFillColorMask(back_color=(255, 255, 255), front_color=(120, 0, 40))).convert("RGB")
    L = 620; qi = qi.resize((L, L), Image.LANCZOS)
    # corazoncito en el centro (≈7% del área; la corrección H lo tolera)
    qd = ImageDraw.Draw(qi); c = L / 2; r = L * 0.065
    qd.rounded_rectangle([c - r * 1.35, c - r * 1.35, c + r * 1.35, c + r * 1.35], radius=14, fill="white")
    qd.polygon(heart_poly(c, c - r * 0.08, r / 15.5), fill=(230, 30, 90))
    x0, y0 = int(S / 2 - L / 2), int(S * 0.42 - L / 2)
    d.rounded_rectangle([x0 - 16, y0 - 16, x0 + L + 16, y0 + L + 16], radius=36, fill="white")
    img.paste(qi, (x0, y0))
    # número
    f = ImageFont.truetype(FONT, 64) if FONT else ImageFont.load_default()
    txt = f"Galaxia #{i}"
    w = d.textlength(txt, font=f); d.text((S / 2 - w / 2 + 3, y0 + L + 30 + 3), txt, font=f, fill=(120, 0, 40))
    d.text((S / 2 - w / 2, y0 + L + 30), txt, font=f, fill="white")
    return img

filas = []
for i in range(1, TOTAL + 1):
    url = f"{base}/?id={i}"
    ruta = os.path.join(aqui, "qr", f"galaxia_{i:03d}.png")
    tarjeta(i, url).save(ruta, optimize=True)
    filas.append((i, url, ruta))
with open(os.path.join(aqui, "qr_links.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh); w.writerow(["id", "url"]); [w.writerow([i, u]) for i, u, _ in filas]
c = canvas.Canvas(os.path.join(aqui, "qr_hojas.pdf"), pagesize=letter)
W, H = letter; cols, rows = 3, 4; m = 1.0 * cm
cw, ch = (W - 2 * m) / cols, (H - 2 * m) / rows; lado = min(cw, ch) - 0.3 * cm
for k, (i, url, ruta) in enumerate(filas):
    if k and k % (cols * rows) == 0: c.showPage()
    j = k % (cols * rows); x = m + (j % cols) * cw; y = H - m - (j // cols + 1) * ch
    c.setDash(2, 3); c.setLineWidth(0.3); c.setStrokeGray(0.6); c.rect(x + 2, y + 2, cw - 4, ch - 4); c.setDash()
    c.drawImage(ruta, x + (cw - lado) / 2, y + (ch - lado) / 2, lado, lado)
c.save()
print(f"Listo: {TOTAL} QR de corazón en qr/, qr_links.csv y qr_hojas.pdf apuntando a {base}/?id=N")

if "--verificar" in sys.argv or True:
    try:
        import cv2
        det = cv2.QRCodeDetector(); ok = 0; malos = []
        for i, url, ruta in filas:
            im = cv2.imread(ruta)
            val, _, _ = det.detectAndDecode(im)
            if val != url:  # segundo intento a menor tamaño (como lo vería un celular de lejos)
                val, _, _ = det.detectAndDecode(cv2.resize(im, (400, 400), interpolation=cv2.INTER_AREA))
            ok += val == url
            if val != url: malos.append(i)
        print(f"Verificación: {ok}/{len(filas)} QR se leen con el link correcto" + (f" — fallan: {malos}" if malos else ""))
    except ImportError:
        print("(instala opencv-python-headless para verificar automáticamente)")
