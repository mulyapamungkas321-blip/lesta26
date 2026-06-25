import qrcode
from PIL import Image, ImageDraw, ImageFilter
import math

def create_heart_mask(size):
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    cx, cy = size // 2, size // 2
    scale = size * 0.92
    pts = []
    for t in range(0, 360, 2):
        r = math.radians(t)
        x = 16 * (math.sin(r) ** 3)
        y = 13 * math.cos(r) - 5 * math.cos(2*r) - 2 * math.cos(3*r) - math.cos(4*r)
        px = cx + int(x * scale / 16)
        py = cy + int(y * scale / 16 * 0.90)
        pts.append((px, py))
    draw.polygon(pts, fill=255)
    return mask

def create_cake_mask(size):
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    m = size * 0.02
    cx, cy = size // 2, size // 2
    draw.rectangle([m, cy + size*0.05, size - m, size - m], fill=255)
    draw.rectangle([m + size*0.05, m + size*0.10, size - m - size*0.05, cy + size*0.10], fill=255)
    for dx in [-size*0.30, 0, size*0.30]:
        cs = size * 0.016
        draw.ellipse([cx + dx - cs, m + size*0.03, cx + dx + cs, m + size*0.10], fill=255)
    return mask

def make_qr(data, shape="heart", fg="black", bg="white", output="qr.png"):
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fg, back_color=bg).convert("RGB")
    s = img.size[0]

    if shape in ("heart", "cake"):
        mk = {"heart": create_heart_mask, "cake": create_cake_mask}[shape](s)
        out = Image.new("RGB", img.size, bg)
        out.paste(img, mask=mk)
        glow = mk.filter(ImageFilter.GaussianBlur(6))
        tint = Image.new("RGB", img.size, bg)
        out = Image.composite(out, tint, glow)
        out.paste(img, mask=mk)
    else:
        out = img

    out.save(output)
    print(f"QR code saved to {output}")

if __name__ == "__main__":
    import sys
    link = sys.argv[1] if len(sys.argv) > 1 else "https://example.com"
    shape = sys.argv[2] if len(sys.argv) > 2 else "heart"
    fname = sys.argv[3] if len(sys.argv) > 3 else f"qr_{shape}.png"
    fg = sys.argv[4] if len(sys.argv) > 4 else "black"
    bg = sys.argv[5] if len(sys.argv) > 5 else "white"
    make_qr(link, shape=shape, fg=fg, bg=bg, output=fname)
