"""Genera los QR de todas las galaxias, un CSV y un PDF imprimible.

Uso (un solo comando):
    python generar_qr.py https://TU-SITIO.netlify.app
Sin argumento usa BASE_URL de abajo. TOTAL debe coincidir con CONFIG.total en index.html.
Requisitos: pip install qrcode pillow reportlab
"""
import sys, csv, os
import qrcode
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm

BASE_URL = "https://TU-SITIO.netlify.app"   # ✏️ cámbialo por tu link real (o pásalo como argumento)
TOTAL = 100

base = (sys.argv[1] if len(sys.argv) > 1 else BASE_URL).rstrip("/")
aqui = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(aqui, "qr"), exist_ok=True)
filas = []
for i in range(1, TOTAL + 1):
    url = f"{base}/?id={i}"
    q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=12, border=3)
    q.add_data(url); q.make(fit=True)
    ruta = os.path.join(aqui, "qr", f"galaxia_{i:03d}.png")
    q.make_image(fill_color="black", back_color="white").save(ruta)
    filas.append((i, url, ruta))
with open(os.path.join(aqui, "qr_links.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["id", "url"]); [w.writerow([i, u]) for i, u, _ in filas]
# PDF: 4 x 5 por hoja carta, con número
c = canvas.Canvas(os.path.join(aqui, "qr_hojas.pdf"), pagesize=letter)
W, H = letter; cols, rows = 4, 5; m = 1.2 * cm
cw, ch = (W - 2 * m) / cols, (H - 2 * m) / rows; lado = min(cw, ch) - 1.0 * cm
for k, (i, url, ruta) in enumerate(filas):
    if k and k % (cols * rows) == 0: c.showPage()
    j = k % (cols * rows); x = m + (j % cols) * cw; y = H - m - (j // cols + 1) * ch
    c.setDash(2, 3); c.setLineWidth(0.3); c.rect(x + 2, y + 2, cw - 4, ch - 4); c.setDash()
    c.drawImage(ruta, x + (cw - lado) / 2, y + 0.8 * cm, lado, lado)
    c.setFont("Helvetica-Bold", 12); c.drawCentredString(x + cw / 2, y + 0.3 * cm, f"Galaxia #{i}" + (" (final)" if i == TOTAL else ""))
c.save()
print(f"Listo: {TOTAL} QR en qr/, qr_links.csv y qr_hojas.pdf apuntando a {base}/?id=N")
