"""Gera camadas de trabalho (sem tocar nos originais):
public/images/cenaN.webp      cópia de trabalho
public/layers/cenaN_fg.png    Camilo recortado (alpha)
public/layers/cenaN_bg.jpg    fundo com o personagem removido por inpainting
"""
import sys, cv2, numpy as np
from pathlib import Path
from PIL import Image
from rembg import remove, new_session

root = Path(__file__).resolve().parents[1]
src = root / "assets-originais" / "imagens"
sess = new_session("birefnet-general")
only = sys.argv[1:]  # ex.: 2 3 (vazio = todos)
for p in sorted(src.glob("*.webp")):
    if only and p.stem not in only:
        continue
    n = p.stem
    img = Image.open(p).convert("RGB")
    img.save(root / "public/images" / f"cena{n}.webp", quality=95)
    cut = remove(img, session=sess, post_process_mask=True)
    cut.save(root / "public/layers" / f"cena{n}_fg.png")
    a = np.array(cut)[:, :, 3]
    m = (a > 20).astype(np.uint8) * 255
    m = cv2.dilate(m, np.ones((25, 25), np.uint8))
    bgr = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    small = cv2.resize(bgr, None, fx=0.5, fy=0.5); ms = cv2.resize(m, None, fx=0.5, fy=0.5)
    inp = cv2.inpaint(small, ms, 12, cv2.INPAINT_TELEA)
    inp = cv2.resize(inp, (bgr.shape[1], bgr.shape[0]))
    out = np.where(m[..., None] > 0, inp, bgr)
    cv2.imwrite(str(root / "public/layers" / f"cena{n}_bg.jpg"), out, [cv2.IMWRITE_JPEG_QUALITY, 92])
    cov = (a > 20).mean()
    print(n, f"cobertura do personagem: {cov:.0%}")
