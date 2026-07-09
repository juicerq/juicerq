import sys
from PIL import Image, ImageEnhance, ImageOps

RAMP = " .':;|!i(ljknmwkX%M@@"

def to_ascii(path, box, cols, rows, contrast=1.6, invert=False):
    img = Image.open(path).convert("L").crop(box)
    img = ImageOps.autocontrast(img)
    img = ImageEnhance.Contrast(img).enhance(contrast)
    img = img.resize((cols, rows))
    if invert:
        img = ImageOps.invert(img)
    px = img.load()
    lines = []
    for y in range(rows):
        line = ""
        for x in range(cols):
            v = px[x, y]
            line += RAMP[v * (len(RAMP) - 1) // 255]
        lines.append(line.rstrip())
    return lines

if __name__ == "__main__":
    l, t, r, b, cols, rows, contrast, inv = sys.argv[1:9]
    for line in to_ascii(
        "avatar.png",
        (int(l), int(t), int(r), int(b)),
        int(cols),
        int(rows),
        float(contrast),
        inv == "1",
    ):
        print(line)
