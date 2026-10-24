"""Genera los SVG animados del README con la paleta del portafolio.

Uso: python scripts/generate_svgs.py
Las estadísticas (stats.svg) se piden a la API de GitHub con GITHUB_TOKEN / GH_TOKEN
o, si no existen, con `gh auth token`. Sin token se conserva el stats.svg anterior.
"""
import json
import os
import subprocess
import urllib.request
from datetime import datetime
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




# ─── tarjetas (proyectos y webs de estudio) ────────────────────────────────
def wrap(text, width):
    lines, cur = [], ""
    for word in text.split():
        if len(cur) + len(word) + 1 > width:
            lines.append(cur)
            cur = word
        else:
            cur = f"{cur} {word}".strip()
    return lines + [cur]


STATUS_COLOR = {"released": GREEN, "live": CYAN, "in-progress": MUTED}


def card(slug, title, desc, stack, status, delay, folder="projects"):
    w, h = 272, 178
    color = STATUS_COLOR[status]
    lines = wrap(desc, 34)
    assert len(lines) <= 3, f"descripción demasiado larga en {slug}: {lines}"
    b = backdrop(w, h, r=12)
    b += f'\n  <g opacity="0"><set attributeName="opacity" to="1" begin="{delay}s" fill="freeze"/>'
    b += f'\n  <text x="18" y="30" font-size="11" fill="{MUTED}">~/{folder}/</text>'
    b += f"""
  <circle cx="{w - 22}" cy="26" r="4" fill="{color}">
    <animate attributeName="opacity" values="1;0.35;1" dur="1.9s" repeatCount="indefinite"/>
  </circle>
  <text x="{w - 32}" y="30" font-size="10" fill="{color}" text-anchor="end">{status}</text>"""
    b += f'\n  <text x="18" y="56" font-size="16" font-weight="700" fill="{CYAN}">{escape(title)}</text>'
    for i, line in enumerate(lines):
        b += f'\n  <text x="18" y="{84 + i * 17}" font-size="11.5" fill="{TEXT}" opacity="0.85">{escape(line)}</text>'
    b += f'\n  <line x1="18" y1="{h - 38}" x2="{w - 18}" y2="{h - 38}" stroke="{BORDER}"/>'
    b += f'\n  <text x="18" y="{h - 17}" font-size="11" fill="{GREEN}">{escape(" · ".join(stack))}</text>'
    b += "\n  </g>"
    prefix = "project" if folder == "projects" else "teaching"
    (OUT / f"{prefix}-{slug}.svg").write_text(svg(w, h, b, title), encoding="utf-8")


# ─── comunidad ─────────────────────────────────────────────────────────────
def community():
    w, h = 840, 210
    x, y0, lh = 24, 70, 25
    b = backdrop(w, h) + title_bar(w, f"{USER}: ~/community")
    b += typed("c1", x, y0, "cat /etc/group", 0.3)
    rows = [
        ("Director de Sistemas", "Club de Software Libre - UTEC"),
        ("Asistente de cátedra", "Programación II · UTEC"),
        ("Mentor", "Desarrollo Basado en Plataformas · 18 h de asesorías"),
        ("Voluntario", "UTEC Ventures · prototipado con Tech MBA"),
        ("Hackathons", "RIMAC · HACK UTEC 2025-II · TECSUP · DBP 2025"),
    ]
    for i, (role, where) in enumerate(rows):
        b += reveal(x, y0 + lh * (i + 1),
                    f'<tspan fill="{GREEN}">▶</tspan> {escape(role.ljust(21))}<tspan fill="{MUTED}">{escape(where)}</tspan>',
                    1.4 + i * 0.2)
    (OUT / "community.svg").write_text(svg(w, h, b, "joseph@dev:~$ cat /etc/group"), encoding="utf-8")


# ─── estadísticas (API de GitHub) ──────────────────────────────────────────
LOGIN = "JosephAnderson234"
# Lenguajes que inflan el conteo por archivos generados (notebooks, sitios exportados, contenido)
SKIP_LANGS = {"HTML", "Jupyter Notebook", "MDX", "CSS", "Tcl"}
QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      totalCommitContributions totalPullRequestContributions
      totalRepositoriesWithContributedCommits
      contributionCalendar { totalContributions }
    }
    repositories(first: 100, ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC,
                 orderBy: {field: PUSHED_AT, direction: DESC}) {
      totalCount
      nodes {
        name pushedAt stargazerCount
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) { edges { size node { name } } }
      }
    }
  }
}"""


def github_token():
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        return token
    try:
        return subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def fetch_stats():
    token = github_token()
    if not token:
        return None
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": LOGIN}}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as res:
        return json.load(res)["data"]["user"]


def stats():
    try:
        user = fetch_stats()
    except Exception as err:  # sin red o token inválido: se conserva el SVG anterior
        print("stats: no se pudo consultar GitHub:", err)
        return
    if not user:
        print("stats: sin token, se conserva stats.svg")
        return

    cc = user["contributionsCollection"]
    repos = user["repositories"]["nodes"]
    numbers = [
        (cc["contributionCalendar"]["totalContributions"], "contribuciones en el último año"),
        (cc["totalCommitContributions"], "commits"),
        (cc["totalPullRequestContributions"], "pull requests"),
        (cc["totalRepositoriesWithContributedCommits"], "repos con commits"),
        (user["repositories"]["totalCount"], "repos públicos propios"),
        (sum(r["stargazerCount"] for r in repos), "estrellas"),
    ]
    langs = {}
    for r in repos:
        for e in r["languages"]["edges"]:
            name = e["node"]["name"]
            if name not in SKIP_LANGS:
                langs[name] = langs.get(name, 0) + e["size"]
    top = sorted(langs.items(), key=lambda kv: -kv[1])[:6]
    total = sum(langs.values()) or 1
    recent = [r for r in repos if r["name"] != LOGIN][:4]

    w, h = 840, 392
    b = backdrop(w, h) + title_bar(w, f"{USER}: ~ — git log --stats")
    # columna izquierda: números
    b += reveal(24, 70, "actividad", 0.2, size=12, fill=MUTED)
    for i, (n, label) in enumerate(numbers):
        y = 100 + i * 27
        b += reveal(24, y, f'<tspan fill="{CYAN}" font-weight="700">{n:>6,}</tspan>  {escape(label)}', 0.4 + i * 0.15)
    # columna derecha: lenguajes con barras que crecen
    lx, bar_w = 440, 250
    b += reveal(lx, 70, "lenguajes · repos públicos", 0.2, size=12, fill=MUTED)
    for i, (name, size) in enumerate(top):
        y = 100 + i * 27
        pct = size / total
        full = max(bar_w * size / top[0][1], 4)
        color = CYAN if i % 2 == 0 else GREEN
        begin = 0.5 + i * 0.15
        b += reveal(lx, y, escape(name), begin, size=13)
        b += f"""
  <rect x="{lx + 96}" y="{y - 10}" width="{bar_w}" height="10" rx="5" fill="{BORDER}" opacity="0.5"/>
  <rect x="{lx + 96}" y="{y - 10}" width="0" height="10" rx="5" fill="{color}">
    <animate attributeName="width" from="0" to="{full:.1f}" begin="{begin}s" dur="0.8s" fill="freeze"
             calcMode="spline" keyTimes="0;1" keySplines="0.2 0.8 0.2 1"/>
  </rect>"""
        b += reveal(w - 24, y, f"{pct:.0%}", begin + 0.6, size=12, fill=MUTED).replace("<text ", '<text text-anchor="end" ', 1)
    # abajo: últimos repos con push
    b += f'\n  <line x1="24" y1="272" x2="{w - 24}" y2="272" stroke="{BORDER}"/>'
    b += reveal(24, 296, "últimos push", 1.6, size=12, fill=MUTED)
    for i, r in enumerate(recent):
        date = datetime.fromisoformat(r["pushedAt"].replace("Z", "+00:00")).strftime("%Y-%m-%d")
        lang = r["languages"]["edges"][0]["node"]["name"] if r["languages"]["edges"] else ""
        col, row = i % 2, i // 2
        b += reveal(24 + col * 408, 324 + row * 27,
                    f'<tspan fill="{GREEN}">●</tspan> {escape(r["name"])} <tspan fill="{MUTED}">{date} · {escape(lang)}</tspan>',
                    1.8 + i * 0.15)
    (OUT / "stats.svg").write_text(svg(w, h, b, "git log --stats"), encoding="utf-8")
    print("stats: actualizado")


def footer():
    w, h = 840, 44
    b = backdrop(w, h, r=10)
    msg = 'echo "gracias por pasar :)"'
    b += typed("f", 18, 28, msg, 0.2, size=15)
    (OUT / "cmd-exit.svg").write_text(svg(w, h, b, msg), encoding="utf-8")


if __name__ == "__main__":
    whoami()
    section("skills", "skills --list")
    section("projects", "ls ~/projects")
    section("teaching", "ls ~/teaching")
    section("stats", "git log --stats")
    community()
    footer()

    card("food-rutine", "food-rutine",
         "App de rutinas de comida con login de Google, sync entre dispositivos y avisos push.",
         ["Next.js", "NestJS", "Prisma"], "live", 0.2)
    card("naturalsql", "NaturalSQL",
         "Convierte tu esquema SQL en una base vectorial para que un LLM genere SQL preciso.",
         ["TS", "Python", "RAG"], "released", 0.35)
    card("intgen", "intgen",
         "CLI que genera interfaces TypeScript y schemas Zod desde un JSON o una URL. En npm.",
         ["Node.js", "TS", "Zod"], "released", 0.5)
    card("yiujarvis", "Yiujarvis",
         "Asistente personal por consola para Windows: planner, memoria, plugins y tools MCP.",
         ["Python", "LLMs", "MCP"], "in-progress", 0.65)
    card("cs-tutor", "adaptive-cs-tutor",
         "Skill de tutoría de CS con 8 estrategias pedagógicas que enseña con tu propio material.",
         ["Claude Skills", "Python"], "released", 0.8)
    card("portafolio", "my-portafolio",
         "Portafolio interactivo estilo escritorio Linux, con ventanas y terminal propia.",
         ["Next.js", "TS", "Tailwind"], "live", 0.95)

    card("so", "so-utec",
         "Sistemas Operativos · 23 páginas y 9 simuladores: procesos, mutex, semáforos, memoria.",
         ["Astro", "React", "GSAP"], "live", 0.2, folder="teaching")
    card("paralela", "comp-paralela-utec",
         "Computación Paralela · 12 playgrounds: Amdahl, PRAM, simulador MPI, Mandelbrot.",
         ["Astro", "React", "KaTeX"], "live", 0.35, folder="teaching")
    card("ml", "machine-utec",
         "Machine Learning · 32 páginas, 38 simuladores, modo examen y Python en el navegador.",
         ["Astro", "React", "Pyodide"], "live", 0.5, folder="teaching")

    stats()
    print("ok", sorted(p.name for p in OUT.iterdir()))
