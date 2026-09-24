"""Genera los SVG animados del README con la paleta del portafolio."""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)

BG = "#07090d"
TEXT = "#e6f5ff"
MUTED = "#93a8bd"
CYAN = "#76f7f7"
GREEN = "#92ff9f"
BORDER = "rgba(176,232,255,0.22)"
FONT = "'JetBrains Mono','Fira Code',ui-monospace,SFMono-Regular,Consolas,'Liberation Mono',monospace"
CW = 0.6  # ancho aprox. de un caracter monoespaciado relativo al font-size

USER = "joseph@dev"


def backdrop(w, h, r=14):
    return f"""
  <defs>
    <radialGradient id="g1" cx="105%" cy="-10%" r="90%">
      <stop offset="0" stop-color="{CYAN}" stop-opacity="0.16"/>
      <stop offset="1" stop-color="{CYAN}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="g2" cx="-5%" cy="110%" r="80%">
      <stop offset="0" stop-color="{GREEN}" stop-opacity="0.12"/>
      <stop offset="1" stop-color="{GREEN}" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="{r}" fill="{BG}"/>
  <rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="{r}" fill="url(#g1)"/>
  <rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="{r}" fill="url(#g2)"/>
  <rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="{r}" fill="none" stroke="{BORDER}"/>"""


def prompt_tspans(cmd=""):
    return (f'<tspan fill="{GREEN}">{USER}</tspan><tspan fill="{MUTED}">:</tspan>'
            f'<tspan fill="{CYAN}">~</tspan><tspan fill="{MUTED}">$ </tspan>'
            f'<tspan fill="{TEXT}">{escape(cmd)}</tspan>')


def typed(uid, x, y, cmd, begin, size=14, speed=0.055):
    """Prompt que aparece y luego 'teclea' el comando caracter por caracter."""
    pw = len(f"{USER}:~$ ") * size * CW
    n = len(cmd)
    values = ";".join(f"{pw + i * size * CW:.1f}" for i in range(n + 1)) + ";2000"
    key_times = ";".join(f"{i / (n + 1):.4f}" for i in range(n + 2))
    dur = max(n * speed, 0.1)
    return f"""
  <clipPath id="c{uid}"><rect x="{x}" y="{y - size - 4}" width="0" height="{size + 10}">
    <set attributeName="width" to="{pw:.1f}" begin="{begin}s" fill="freeze"/>
    <animate attributeName="width" values="{values}" keyTimes="{key_times}" calcMode="discrete"
             begin="{begin + 0.35:.2f}s" dur="{dur:.2f}s" fill="freeze"/>
  </rect></clipPath>
  <text x="{x}" y="{y}" font-size="{size}" clip-path="url(#c{uid})" xml:space="preserve">{prompt_tspans(cmd)}</text>"""


def reveal(x, y, content, begin, size=14, weight=400, fill=TEXT):
    return f"""
  <text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" opacity="0" xml:space="preserve">{content}<set attributeName="opacity" to="1" begin="{begin}s" fill="freeze"/></text>"""


def cursor(x, y, begin, size=14):
    return f"""
  <rect x="{x}" y="{y - size + 2}" width="{size * CW:.1f}" height="{size + 2}" fill="{CYAN}" opacity="0">
    <animate attributeName="opacity" values="1;0" dur="1s" calcMode="discrete" begin="{begin}s" repeatCount="indefinite"/>
  </rect>"""


def svg(w, h, body, label):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(label, {'"': '&quot;'})}" font-family="{FONT}">
  <title>{escape(label)}</title>{body}
</svg>
"""


def title_bar(w, title):
    return f"""
  <line x1="1" y1="38" x2="{w - 1}" y2="38" stroke="{BORDER}"/>
  <circle cx="22" cy="19" r="5" fill="{CYAN}" opacity="0.85"/>
  <circle cx="40" cy="19" r="5" fill="{GREEN}" opacity="0.6"/>
  <circle cx="58" cy="19" r="5" fill="{MUTED}" opacity="0.4"/>
  <text x="{w / 2}" y="24" font-size="12" fill="{MUTED}" text-anchor="middle">{escape(title)}</text>
  <text x="{w - 20}" y="24" font-size="12" fill="{MUTED}" text-anchor="end" opacity="0.7">zsh</text>"""


# ─── whoami ────────────────────────────────────────────────────────────────
def whoami():
    w, h = 840, 300
    x, y0, lh = 24, 70, 25
    b = backdrop(w, h) + title_bar(w, f"{USER}: ~")
    b += typed("w1", x, y0, "whoami", 0.3)
    b += reveal(x, y0 + lh, "Joseph Anderson Cose Rojas", 1.1, size=17, weight=700, fill=CYAN)
    b += reveal(x, y0 + lh * 2, "Full Stack Developer · Ciencias de la Computación @ UTEC · Lima, Perú", 1.3, fill=TEXT)
    b += typed("w2", x, y0 + lh * 3.6, "cat now.txt", 1.8)
    b += reveal(x, y0 + lh * 4.6, f'<tspan fill="{GREEN}">▶</tspan> Fullstack Developer <tspan fill="{MUTED}">@</tspan> Mekánico', 2.8)
    b += reveal(x, y0 + lh * 5.6, f'<tspan fill="{GREEN}">▶</tspan> Director de Sistemas <tspan fill="{MUTED}">@</tspan> Club de Software Libre - UTEC', 3.0)
    b += reveal(x, y0 + lh * 6.6, f'<tspan fill="{MUTED}">· antes: Cognitia · BioActiva · Maftech · Asistente de cátedra Programación II</tspan>', 3.2)
    b += typed("w3", x, y0 + lh * 8.2, "", 3.7)
    b += cursor(x + len(f"{USER}:~$ ") * 14 * CW, y0 + lh * 8.2, 3.8)
    (OUT / "whoami.svg").write_text(svg(w, h, b, "joseph@dev:~$ whoami"), encoding="utf-8")


# ─── separadores de sección ────────────────────────────────────────────────
def section(name, cmd):
    w, h = 840, 44
    b = backdrop(w, h, r=10)
    b += typed("s", 18, 28, cmd, 0.2, size=15)
    (OUT / f"cmd-{name}.svg").write_text(svg(w, h, b, f"{USER}:~$ {cmd}"), encoding="utf-8")


# ─── tarjetas de proyecto ──────────────────────────────────────────────────
def wrap(text, width):
    lines, cur = [], ""
    for word in text.split():
        if len(cur) + len(word) + 1 > width:
            lines.append(cur)
            cur = word
        else:
            cur = f"{cur} {word}".strip()
    return lines + [cur]


def card(slug, title, desc, stack, status, delay):
    w, h = 272, 178
    color = GREEN if status == "released" else CYAN
    b = backdrop(w, h, r=12)
    b += f'\n  <g opacity="0"><set attributeName="opacity" to="1" begin="{delay}s" fill="freeze"/>'
    b += f'\n  <text x="18" y="30" font-size="11" fill="{MUTED}">~/projects/</text>'
    b += f"""
  <circle cx="{w - 22}" cy="26" r="4" fill="{color}">
    <animate attributeName="opacity" values="1;0.35;1" dur="1.9s" repeatCount="indefinite"/>
  </circle>
  <text x="{w - 32}" y="30" font-size="10" fill="{color}" text-anchor="end">{status}</text>"""
    b += f'\n  <text x="18" y="56" font-size="16" font-weight="700" fill="{CYAN}">{escape(title)}</text>'
    for i, line in enumerate(wrap(desc, 34)):
        b += f'\n  <text x="18" y="{84 + i * 17}" font-size="11.5" fill="{TEXT}" opacity="0.85">{escape(line)}</text>'
    b += f'\n  <line x1="18" y1="{h - 38}" x2="{w - 18}" y2="{h - 38}" stroke="{BORDER}"/>'
    b += f'\n  <text x="18" y="{h - 17}" font-size="11" fill="{GREEN}">{escape(" · ".join(stack))}</text>'
    b += "\n  </g>"
    (OUT / f"project-{slug}.svg").write_text(svg(w, h, b, title), encoding="utf-8")


def footer():
    w, h = 840, 44
    b = backdrop(w, h, r=10)
    msg = 'echo "gracias por pasar :)"'
    b += typed("f", 18, 28, msg, 0.2, size=15)
    (OUT / "cmd-exit.svg").write_text(svg(w, h, b, msg), encoding="utf-8")


whoami()
section("skills", "skills --list")
section("projects", "ls ~/projects")
section("stats", "git log --stats")
footer()
card("portafolio", "my-portafolio",
     "Portafolio interactivo estilo escritorio Linux, con ventanas y terminal propia.",
     ["Next.js", "TS", "Tailwind"], "live", 0.2)
card("naturalsql", "NaturalSQL",
     "Experimento de RAG para generar SQL a partir de lenguaje natural. Publicado en PyPI.",
     ["Python", "RAG", "LLMs"], "released", 0.4)
card("cc-discord", "cc-discord-presence",
     "Discord Rich Presence que muestra tu sesión de Claude Code en tu perfil.",
     ["Go", "Discord RPC"], "released", 0.6)
print("ok", sorted(p.name for p in OUT.iterdir()))
