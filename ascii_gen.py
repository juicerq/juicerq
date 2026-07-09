import sys
from PIL import Image

RAMP = " .':;|!i(ljknmwkX%M@@"


def ascii_masked(photo_path, mask_path, cols, rows, gamma):
    alpha_full = Image.open(mask_path).getchannel("A")
    bbox = alpha_full.getbbox()
    gray = Image.open(photo_path).convert("L").crop(bbox).resize((cols, rows))
    alpha = alpha_full.crop(bbox).resize((cols, rows))
    g, a = gray.load(), alpha.load()
    subject = sorted(g[x, y] for y in range(rows) for x in range(cols) if a[x, y] >= 96)
    rank = {}
    for i, v in enumerate(subject):
        rank.setdefault(v, i / (len(subject) - 1))
    out = []
    for y in range(rows):
        line = ""
        for x in range(cols):
            if a[x, y] < 96:
                line += " "
                continue
            v = (1.0 - rank[g[x, y]]) ** gamma
            line += RAMP[max(1, int(v * (len(RAMP) - 1)))]
        out.append(line.rstrip())
    return out


if __name__ == "__main__":
    photo, mask, cols, rows, gamma = sys.argv[1:6]
    for line in ascii_masked(photo, mask, int(cols), int(rows), float(gamma)):
        print(line)
