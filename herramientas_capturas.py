"""Genera capturas de varias galaxias y una hoja de muestras (muestras.png).
Uso: python herramientas_capturas.py  (con un servidor local: python -m http.server 8765 en esta carpeta)"""
import sys, json, asyncio
from playwright.async_api import async_playwright
from PIL import Image, ImageDraw, ImageFont
IDS = [int(x) for x in sys.argv[1:]] or [1, 7, 25, 50, 77, 100]
BASE = "http://localhost:8765/index.html"
async def main():
    infos, errores = [], {}
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--use-gl=angle","--use-angle=swiftshader","--enable-unsafe-swiftshader","--ignore-gpu-blocklist","--autoplay-policy=no-user-gesture-required"])
        for i in IDS:
            pg = await b.new_page(viewport={"width": 640, "height": 480})
            errs = []
            pg.on("console", lambda m, errs=errs: errs.append(m.text) if m.type == "error" else None)
            pg.on("pageerror", lambda e, errs=errs: errs.append("PAGEERROR " + str(e)))
            await pg.goto(f"{BASE}?id={i}&prueba=1", wait_until="networkidle")
            await pg.click("#btnMusica", force=True)
            await pg.wait_for_timeout(9000 if i != 100 else 6000)
            if i == 100:
                await pg.wait_for_timeout(1500)
                await pg.click("#btnPreguntar", force=True); await pg.wait_for_timeout(1200)
                await pg.screenshot(path=f"/tmp/g{i}_pregunta.png")
                await pg.dispatch_event("#btnNo", "pointerenter"); await pg.wait_for_timeout(500)
                await pg.screenshot(path=f"/tmp/g{i}_no.png")
                await pg.click("#btnSi", force=True); await pg.wait_for_timeout(5500)
                await pg.screenshot(path=f"/tmp/g{i}_si.png")
            await pg.screenshot(path=f"/tmp/g{i}.png")
            info = await pg.evaluate("window.__galaxia"); info["cancion"] = await pg.inner_text("#cancion")
            infos.append(info); errores[i] = errs
            await pg.close()
        await b.close()
    W, H = 640, 480; cols = 3; rows = (len(IDS) + cols - 1) // cols
    sheet = Image.new("RGB", (W * cols, (H + 40) * rows), "black"); d = ImageDraw.Draw(sheet)
    f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
    for k, (i, info) in enumerate(zip(IDS, infos)):
        x, y = (k % cols) * W, (k // cols) * (H + 40)
        sheet.paste(Image.open(f"/tmp/g{i}.png").convert("RGB"), (x, y))
        d.text((x + 8, y + H + 8), f"#{i} {info['forma']} · {info['paleta']} · {info['movimiento']} · cam {info['camara']}", fill="white", font=f)
    sheet.save("muestras.png")
    print(json.dumps(infos, ensure_ascii=False, indent=1)); print("ERRORES:", json.dumps(errores, ensure_ascii=False, indent=1))
asyncio.run(main())
