from xml.sax.saxutils import escape

WIDTH = 60

DARK = {
    "key": "#ffa657", "value": "#a5d6ff", "add": "#3fb950", "del": "#f85149",
    "cc": "#616e7f", "bg": "#161b22", "fg": "#c9d1d9",
}
LIGHT = {
    "key": "#953800", "value": "#0a3069", "add": "#1a7f37", "del": "#cf222e",
    "cc": "#c2cfde", "bg": "#f6f8fa", "fg": "#24292f",
}


def header(y, name):
    filler = "—" * (WIDTH - len(name) - 5)
    return f'<tspan x="390" y="{y}">{escape(name)}</tspan> -{filler}-—-'


def key_markup(key):
    parts = key.split(".")
    return ".".join(f'<tspan class="key">{escape(p)}</tspan>' for p in parts)


def field(y, key, value, field_id=None):
    prefix_len = 2 + len(key) + 1
    just = WIDTH - prefix_len - 2 - len(value)
    dots = " " + "." * just + " " if just > 2 else {0: "", 1: " ", 2: ". "}[max(just, 0)]
    dots_attr = f' id="{field_id}_dots"' if field_id else ""
    value_attr = f' id="{field_id}"' if field_id else ""
    return (
        f'<tspan x="390" y="{y}" class="cc">. </tspan>{key_markup(key)}:'
        f'<tspan class="cc"{dots_attr}>{dots}</tspan>'
        f'<tspan class="value"{value_attr}>{escape(value)}</tspan>'
    )


def blank(y):
    return f'<tspan x="390" y="{y}" class="cc">. </tspan>'


def stats_rows():
    return [
        '<tspan x="390" y="470" class="cc">. </tspan><tspan class="key">Repos</tspan>:'
        '<tspan class="cc" id="repo_data_dots"> .... </tspan><tspan class="value" id="repo_data">0</tspan>'
        ' {<tspan class="key">Contributed</tspan>: <tspan class="value" id="contrib_data">0</tspan>}'
        ' | <tspan class="key">Stars</tspan>:'
        '<tspan class="cc" id="star_data_dots"> ........... </tspan><tspan class="value" id="star_data">0</tspan>',
        '<tspan x="390" y="490" class="cc">. </tspan><tspan class="key">Commits</tspan>:'
        '<tspan class="cc" id="commit_data_dots"> ................. </tspan><tspan class="value" id="commit_data">0</tspan>'
        ' | <tspan class="key">Followers</tspan>:'
        '<tspan class="cc" id="follower_data_dots"> ....... </tspan><tspan class="value" id="follower_data">0</tspan>',
        '<tspan x="390" y="510" class="cc">. </tspan><tspan class="key">Lines of Code on GitHub</tspan>:'
        '<tspan class="cc" id="loc_data_dots">. </tspan><tspan class="value" id="loc_data">0</tspan>'
        ' ( <tspan class="addColor" id="loc_add">0</tspan><tspan class="addColor">++</tspan>, '
        '<tspan id="loc_del_dots"> </tspan><tspan class="delColor" id="loc_del">0</tspan>'
        '<tspan class="delColor">--</tspan> )',
    ]


def panel():
    return [
        header(30, "juicerq@github"),
        field(50, "OS", "Linux (CachyOS)"),
        field(70, "Uptime", "0 years, 0 months, 0 days", "age_data"),
        field(90, "Host", "Dogama"),
        field(110, "Kernel", "Lead Backend Engineer"),
        field(130, "Shell", "fish"),
        blank(150),
        field(170, "Languages.Programming", "TypeScript, JavaScript, Rust"),
        field(190, "Languages.Computer", "HTML, CSS, SQL, YAML"),
        field(210, "Languages.Real", "Português, English"),
        blank(230),
        field(250, "IDE", "Don't need it anymore"),
        field(270, "Hobbies.Software", "Game Dev (Godot)"),
        header(310, "- Contact"),
        field(330, "Email.Personal", "julio.cerqueiira@gmail.com"),
        field(350, "GitHub", "juicerq"),
        field(370, "Location", "São Paulo, Brasil"),
        field(390, "Born.in", "Salvador - Bahia"),
        header(450, "- GitHub Stats"),
        *stats_rows(),
    ]


def svg(colors, ascii_lines):
    ascii_tspans = "\n".join(
        f'<tspan x="15" y="{30 + i * 20}">{escape(line)}</tspan>'
        for i, line in enumerate(ascii_lines)
    )
    panel_tspans = "\n".join(panel())
    return f"""<?xml version='1.0' encoding='UTF-8'?>
<svg xmlns="http://www.w3.org/2000/svg" xml:space="preserve" font-family="ConsolasFallback,Consolas,monospace" width="985px" height="530px" font-size="16px">
<style>
@font-face {{
src: local('Consolas'), local('Consolas Bold');
font-family: 'ConsolasFallback';
font-display: swap;
-webkit-size-adjust: 109%;
size-adjust: 109%;
}}
.key {{fill: {colors['key']};}}
.value {{fill: {colors['value']};}}
.addColor {{fill: {colors['add']};}}
.delColor {{fill: {colors['del']};}}
.cc {{fill: {colors['cc']};}}
text, tspan {{white-space: pre;}}
</style>
<rect width="985px" height="530px" fill="{colors['bg']}" rx="15"/>
<text x="15" y="30" fill="{colors['fg']}" class="ascii">
{ascii_tspans}
</text>
<text x="390" y="30" fill="{colors['fg']}">
{panel_tspans}
</text>
</svg>"""


if __name__ == "__main__":
    ascii_lines = open("ascii.txt").read().splitlines()
    while len(ascii_lines) < 22:
        ascii_lines.append("")
    open("dark_mode.svg", "w").write(svg(DARK, ascii_lines))
    open("light_mode.svg", "w").write(svg(LIGHT, ascii_lines))
    print("svgs written")
