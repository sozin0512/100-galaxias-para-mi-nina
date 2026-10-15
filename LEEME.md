# 💫 100 Galaxias — búsqueda del tesoro + "¿Quieres ser mi novia?"

Cada QR abre `index.html?id=N`. Cada número genera una galaxia distinta (forma, colores, movimiento, cámara, estrellas fugaces).
La galaxia N muestra una **pista** para encontrar la N+1. La **#100** hace la pregunta con Sí / No (el "No" se escapa 😜).

## Qué editar (todo está en `CONFIG`, al inicio de `index.html`)
- `nombre`: el nombre de ella (o en el link: `?name=Ana`). `titulo` (o `?msg=...`), `frases`, `cartas`, `fotos`.
- `pistas`: escribe tus pistas en orden. `pistas[0]` sale en la galaxia #1 y dice dónde está la #2, etc. Las que no escribas se rellenan con pistas genéricas.
- `total`: cantidad de galaxias (100). Si lo cambias, cambia también `TOTAL` en `generar_qr.py`.
- `ordenEstricto`: si ella abre una galaxia salteada, le dice "Primero encuentra la galaxia #X". Para probar tú sin que se bloquee: agrega `&prueba=1` al link. Para borrar el progreso: `&reiniciar=1`.
- `playlist`: canciones de YouTube (`titulo`, `artista`, `youtubeId`). Cada galaxia empieza en la canción `id % cantidad`, con botones ⏮ ⏭, pausa y silencio. Antes de sonar pide permiso con "Toca para escuchar música 🎵".
- `whatsapp`: opcional, tu número para que ella te avise cuando diga que sí.
- La canción con `final: true` (KESI de Camilo) suena siempre en la galaxia #100; las galaxias 1-99 rotan entre las demás.
- Demo: `index.html?demo=1` = galaxia final con KESI.

## Publicarla gratis (necesario para que suene la música de YouTube)
Abierto con doble clic (file://) la galaxia funciona, pero YouTube no reproduce videos ahí (error 153). Súbela a internet:
1. **Netlify Drop**: entra a https://app.netlify.com/drop y arrastra esta carpeta. Te da un link tipo `https://algo.netlify.app`.
2. O **GitHub Pages**: sube la carpeta a un repositorio y activa Pages.

## Regenerar los QR con tu link real (un comando)
```
pip install qrcode pillow reportlab
python generar_qr.py https://TU-LINK.netlify.app
```
Crea `qr/galaxia_001.png` … `qr/galaxia_100.png`, `qr_links.csv` y `qr_hojas.pdf` (20 por hoja, listos para imprimir y recortar).
⚠️ Los QR incluidos ahora apuntan a `https://TU-SITIO.netlify.app` (de ejemplo): regénéralos antes de imprimir.
