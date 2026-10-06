#!/usr/bin/env python3
"""Generate a brand's Claude Code mod: spinner, HTML preview, GIFs and README.

Part of the brand-mod skill (cofoundy/brand-skills). Standard library only; Python 3.10+.

    python3 brand-mod.py brand/mod.json                  # mod + preview.html into brand/mod/
    python3 brand-mod.py brand/mod.json --media          # + README GIFs (needs agent-browser + ffmpeg)
    python3 brand-mod.py brand/mod.json --check          # + claude plugin validate / test

mod.json (paths relative to it; name/slug/url fall back to the package's brand.yaml):
    {
      "primary": "#2885AE",                    # or "stops": 8 colors, shadow → white
      "desktop_word": "#2984AD",               # optional: word color in the desktop app (default: primary)
      "logo_svg": "assets/logo.svg",           # color logo: desktop app, light theme
      "logo_light_svg": "assets/logo-light.svg",  # optional: light logo: terminal + desktop dark theme
      "words": { "thinking": [...], "tool-use": [...], "tool-input": [...], "responding": [...], "requesting": [...] },
      "done": ["Shipped", "Cooked"],           # end of turn: «<word> for 12s»
      "name": "Cofoundy", "slug": "cofoundy", "url": "cofoundy.dev", "owner": "Cofoundy SAC"
    }

Output: <out>/<slug>-spinner/ (default <out> = the mod.json folder + /mod): the installable plugin,
which is also its own marketplace, preview.html, README.md with images first, and media/ (--media).
"""

from __future__ import annotations

import argparse
import base64
import json
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
TEMPLATE = SKILL / "template"
MODES = ["thinking", "tool-use", "tool-input", "responding", "requesting"]
HEX = re.compile(r"^#[0-9A-Fa-f]{6}$")


def die(msg: str) -> None:
    print(f"✘ {msg}", file=sys.stderr)
    sys.exit(1)


# ── Colors ───────────────────────────────────────────────────────────────────────────────────
def rgb(h: str) -> tuple[int, int, int]:
    return int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16)


def mix(a: str, b: str, t: float) -> str:
    """t=0 → a, t=1 → b."""
    ra, rb = rgb(a), rgb(b)
    return "#" + "".join(f"{round(x + (y - x) * t):02X}" for x, y in zip(ra, rb))


def derive_stops(primary: str) -> list[str]:
    """8 tones from shadow to light with the primary at [3]; the glint runs [3] → [7]."""
    return [
        mix(primary, "#000000", 0.78),
        mix(primary, "#000000", 0.6),
        mix(primary, "#000000", 0.35),
        primary.upper(),
        mix(primary, "#FFFFFF", 0.22),
        mix(primary, "#FFFFFF", 0.5),
        mix(primary, "#FFFFFF", 0.8),
        "#FFFFFF",
    ]


# ── Logos ────────────────────────────────────────────────────────────────────────────────────
def _split(svg: str) -> tuple[str, str, str]:
    """(opening <svg …>, content, viewBox) of an SVG."""
    svg = re.sub(r"<\?xml[^>]*\?>|<!--.*?-->", "", svg, flags=re.S).strip()
    m = re.match(r"(<svg\b[^>]*>)(.*)</svg>\s*$", svg, flags=re.S)
    if not m:
        die("the logo is not an <svg>…</svg>")
    head, inner = m.group(1), m.group(2)
    vb = re.search(r'viewBox="([^"]+)"', head)
    if vb:
        box = vb.group(1).replace(",", " ")
    else:
        w = re.search(r'width="([\d.]+)', head)
        h = re.search(r'height="([\d.]+)', head)
        box = f"0 0 {w.group(1) if w else 100} {h.group(1) if h else 100}"
    return head, inner, box


def sweep_svg(svg: str, light: str | None = None) -> str:
    """The logo with a soft white sweep (SMIL) every 3.2 s, for the desktop app.

    Works for any logo: a white copy of the drawing, masked by a gradient that crosses it
    diagonally. With a light version, the SVG shows it when the OS is in dark mode
    (prefers-color-scheme inside the SVG). The app draws it as an image; without SMIL it stays still.
    """
    head, inner, box = _split(svg)
    x, y, w, h = box.split()
    white = re.sub(r'\s(id)="[^"]*"', "", inner)
    white = re.sub(r'(fill|stroke)="(?!none)[^"]*"', r'\1="#FFFFFF"', white)
    white = re.sub(r"(fill|stroke)\s*:\s*(?!none)[^;\"]+", r"\1:#FFFFFF", white)
    logos = f'<g class="bm-color">{inner}</g>'
    style = ""
    if light:
        _, l_inner, l_box = _split(light)
        logos += f'<svg class="bm-light" x="{x}" y="{y}" width="{w}" height="{h}" viewBox="{l_box}">{l_inner}</svg>'
        style = (
            "<style>.bm-light{display:none}@media (prefers-color-scheme: dark)"
            "{.bm-light{display:inline}.bm-color{display:none}}</style>"
        )
    overlay = (
        '<defs><linearGradient id="bm-sweep" x1="0" y1="0" x2="1" y2="0.45">'
        '<stop offset="0.3" stop-color="#fff" stop-opacity="0"/>'
        '<stop offset="0.5" stop-color="#fff" stop-opacity="1"/>'
        '<stop offset="0.7" stop-color="#fff" stop-opacity="0"/>'
        '<animateTransform attributeName="gradientTransform" type="translate" '
        'values="-1.2 0;-1.2 0;1.2 0;1.2 0" keyTimes="0;0.15;0.65;1" dur="3.2s" repeatCount="indefinite"/>'
        f'</linearGradient><mask id="bm-mask" maskUnits="userSpaceOnUse" x="{x}" y="{y}" width="{w}" height="{h}">'
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#bm-sweep)"/></mask></defs>'
        f'<g mask="url(#bm-mask)" opacity="0.45">{white}</g>'
    )
    return f"{head}{style}{logos}{overlay}</svg>"


def png_b64(svg_path: Path) -> str:
    if not shutil.which("rsvg-convert"):
        print(
            "⚠ no rsvg-convert: the terminal gets no logo (brew install librsvg / apt install librsvg2-bin)"
        )
        return ""
    out = subprocess.run(
        ["rsvg-convert", "-a", "-w", "64", "-h", "64", str(svg_path)],
        capture_output=True,
        check=True,
    ).stdout
    return base64.b64encode(out).decode()


# ── Input ────────────────────────────────────────────────────────────────────────────────────
def from_brand_yaml(folder: Path) -> dict:
    """name / slug / links.domain from the package's brand.yaml (no YAML library needed)."""
    f = folder / "brand.yaml"
    if not f.exists():
        return {}
    text = f.read_text()

    def scalar(key: str) -> str:
        m = re.search(rf"^\s*{key}:\s*(.+?)\s*(?:#.*)?$", text, flags=re.M)
        return m.group(1).strip().strip("\"'") if m else ""

    return {
        k: v
        for k, v in {
            "name": scalar("name"),
            "slug": scalar("slug"),
            "url": scalar("domain"),
        }.items()
        if v
    }


def load(path: Path) -> dict:
    b = {**from_brand_yaml(path.parent), **json.loads(path.read_text())}
    for k in ("name", "slug", "logo_svg"):
        if not b.get(k):
            die(f"mod.json: missing «{k}» (name/slug can come from brand.yaml)")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", b["slug"]):
        die("slug: lowercase letters, digits and hyphens only (kebab-case)")
    stops = b.get("stops") or (derive_stops(b["primary"]) if b.get("primary") else None)
    if not stops or len(stops) != 8 or not all(HEX.match(s) for s in stops):
        die("mod.json: «primary» (#RRGGBB) or «stops» (8 colors #RRGGBB)")
    b["stops"] = [s.upper() for s in stops]
    b["desktop_word"] = (b.get("desktop_word") or b["stops"][3]).upper()
    words = b.get("words") or {}
    fallback = words.get("responding") or ["Working"]
    b["words"] = {
        m: [w for w in words.get(m, fallback) if w] or fallback for m in MODES
    }
    b["done"] = b.get("done") or ["Done"]
    base = path.parent
    b["logo_svg_path"] = (base / b["logo_svg"]).resolve()
    b["logo_light_path"] = (base / b.get("logo_light_svg", b["logo_svg"])).resolve()
    for p in (b["logo_svg_path"], b["logo_light_path"]):
        if not p.exists():
            die(f"not found: {p}")
    return b


def ts(v) -> str:
    return json.dumps(v, ensure_ascii=False)


# ── The mod ──────────────────────────────────────────────────────────────────────────────────
def write_mod(b: dict, dest: Path) -> dict:
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(
        TEMPLATE,
        dest,
        ignore=shutil.ignore_patterns("preview.html.tmpl", "README.md.tmpl"),
    )
    # The test ships as .tmpl so a repo-wide test runner doesn't collect it without the mod loaded.
    (dest / "hooks" / "spinner.test.tsx.tmpl").rename(
        dest / "hooks" / "spinner.test.tsx"
    )
    slug, name = b["slug"], b["name"]
    light = (
        b["logo_light_path"].read_text()
        if b["logo_light_path"] != b["logo_svg_path"]
        else None
    )
    svg = sweep_svg(b["logo_svg_path"].read_text(), light)
    png = png_b64(b["logo_light_path"])
    brand = {
        "name": name,
        "slug": slug,
        "url": b.get("url", ""),
        "command": f"{slug}-spinner",
    }
    (dest / "hooks" / "brand.ts").write_text(
        "// GENERATED by skills/brand-mod/scripts/brand-mod.py from mod.json: do not edit by hand.\n"
        f"export const BRAND = {ts(brand)}\n\n"
        "// Brand scale, shadow to light: [0..2] darks, [3] primary, [4..6] lights, [7] white.\n"
        f"export const STOPS = {ts(b['stops'])}\n\n"
        "// Word color in the desktop app: one color, readable on light and dark themes.\n"
        f"export const DESKTOP_WORD = {ts(b['desktop_word'])}\n\n"
        "// One word per turn phase (Spinner.props.mode).\n"
        f"export const WORDS: Record<string, string[]> = {ts(b['words'])}\n\n"
        "// End of turn: the engine draws «<word> for 12s».\n"
        f"export const DONE = {ts(b['done'])}\n\n"
        "// Desktop app logo (SVG with an SMIL sweep) and terminal logo (64 px PNG, base64).\n"
        f"export const LOGO_SVG = {ts(svg)}\n"
        f"export const LOGO_PNG = {ts(png)}\n"
    )
    owner = b.get("owner") or name
    plugin = {
        "name": f"{slug}-spinner",
        "version": "1.0.0",
        "description": f"{name} brand spinner for Claude Code (terminal and desktop app)",
        "author": {"name": owner},
    }
    (dest / ".claude-plugin" / "plugin.json").write_text(
        json.dumps(plugin, ensure_ascii=False, indent=2) + "\n"
    )
    market = {
        "name": slug,
        "owner": {"name": owner},
        "plugins": [
            {
                "name": f"{slug}-spinner",
                "source": "./",
                "description": plugin["description"],
            }
        ],
    }
    (dest / ".claude-plugin" / "marketplace.json").write_text(
        json.dumps(market, ensure_ascii=False, indent=2) + "\n"
    )
    return {"svg": svg, "png": png}


def write_preview(b: dict, assets: dict, dest: Path) -> Path:
    t = (TEMPLATE / "preview.html.tmpl").read_text()
    words = [w for m in ("tool-use", "responding", "thinking") for w in b["words"][m]]
    small = re.sub(
        r'(<svg\b[^>]*?)\s(width|height)="[^"]*"', r"\1", assets["svg"], count=2
    )
    small = small.replace("<svg", '<svg width="16" height="16"', 1)
    for k, v in {
        "__NAME__": b["name"],
        "__SLUG__": b["slug"],
        "__FIRSTWORD__": words[0],
        "__DESKTOP_WORD__": b["desktop_word"],
        "__STOPS__": ts(b["stops"]),
        "__WORDS__": ts(list(dict.fromkeys(words))),
        "__PNG_URI__": f"data:image/png;base64,{assets['png']}"
        if assets["png"]
        else "",
        "__SVG__": small,
    }.items():
        t = t.replace(k, v)
    out = dest / "preview.html"
    out.write_text(t)
    return out


# ── README media ─────────────────────────────────────────────────────────────────────────────
def ab(session: str, *args: str) -> str:
    return subprocess.run(
        ["agent-browser", "--session", session, *args], capture_output=True, text=True
    ).stdout


def capture(preview: Path, media: Path) -> list[str]:
    """Record each preview window (#terminal, #desktop-light, #desktop-dark) and crop it to a GIF.

    agent-browser records the whole viewport (1280 px wide, whatever `viewport` says), so the
    window rectangle is measured with `eval` and ffmpeg crops it with a margin.
    """
    for tool in ("agent-browser", "ffmpeg"):
        if not shutil.which(tool):
            print(f"⚠ no {tool}: the README ships without GIFs")
            return []
    media.mkdir(exist_ok=True)
    session = f"brand-mod-{int(time.time())}"
    made = []
    pad = 22
    probe = "JSON.stringify({r: document.querySelector('figure:not(.off) .win').getBoundingClientRect()})"
    with tempfile.TemporaryDirectory() as tmp:
        for shot in ("terminal", "desktop-light", "desktop-dark"):
            # A different query per shot forces a reload: a hash-only change keeps the old page.
            ab(session, "open", f"file://{preview}?shot={shot}#{shot}")
            ab(session, "wait", "700")
            raw = ab(session, "eval", probe).strip()
            try:
                info = json.loads(raw)
                r = (json.loads(info) if isinstance(info, str) else info)["r"]
            except (ValueError, KeyError, TypeError):
                print(f"⚠ could not measure the {shot} window: {raw[:120]}")
                continue
            video = Path(tmp) / f"{shot}.webm"
            ab(session, "record", "start", str(video))
            ab(session, "wait", "3400")
            ab(session, "record", "stop")
            x, y = max(0, int(r["left"] - pad)), max(0, int(r["top"] - pad))
            w, h = int(r["width"] + 2 * pad), int(r["height"] + 2 * pad)
            gif = media / f"{shot}.gif"
            vf = (
                f"crop={w - w % 2}:{h - h % 2}:{x}:{y},fps=12,scale=760:-1:flags=lanczos,"
                "split[a][b];[a]palettegen=max_colors=96[p];[b][p]paletteuse=dither=bayer"
            )
            subprocess.run(
                ["ffmpeg", "-v", "error", "-y", "-i", str(video), "-vf", vf, str(gif)],
                check=True,
            )
            made.append(gif.name)
        ab(session, "close")
    return made


def write_readme(b: dict, dest: Path, media: list[str]) -> None:
    t = (TEMPLATE / "README.md.tmpl").read_text()
    name = b["name"]
    if "terminal.gif" in media:
        hero = f'<p align="center"><img src="media/terminal.gif" alt="{name} spinner in the terminal" width="760"></p>'
        desk = (
            '<p align="center">\n'
            '  <img src="media/desktop-light.gif" alt="Desktop app, light theme" width="49%">\n'
            '  <img src="media/desktop-dark.gif" alt="Desktop app, dark theme" width="49%">\n</p>'
        )
    else:
        hero = "> Open `preview.html` to see it moving (the README images come from `--media`)."
        desk = ""
    words = ", ".join(
        f"«{w}»"
        for w in list(dict.fromkeys(w for m in MODES for w in b["words"][m]))[:8]
    )
    for k, v in {
        "{{HERO}}": hero,
        "{{DESKTOP}}": desk,
        "{{WORDS}}": words,
        "{{DONE}}": ", ".join(f"«{w}»" for w in b["done"][:5]),
        "{{name}}": name,
        "{{slug}}": b["slug"],
    }.items():
        t = t.replace(k, v)
    (dest / "README.md").write_text(t)


def check(dest: Path) -> bool:
    if not shutil.which("claude"):
        print("⚠ no claude CLI: the mod was not validated")
        return True
    ok = True
    for cmd in (
        ["claude", "plugin", "validate", str(dest)],
        ["claude", "plugin", "test", str(dest)],
    ):
        r = subprocess.run(cmd, capture_output=True, text=True)
        print(("✔ " if r.returncode == 0 else "✘ ") + " ".join(cmd[1:3]))
        if r.returncode != 0:
            print(r.stdout[-2000:] + r.stderr[-2000:])
            ok = False
    return ok


def main() -> None:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("config", type=Path, help="mod.json (inside the brand package)")
    ap.add_argument(
        "--out", type=Path, help="output folder (default: <mod.json folder>/mod)"
    )
    ap.add_argument(
        "--media",
        action="store_true",
        help="record the README GIFs (agent-browser + ffmpeg)",
    )
    ap.add_argument(
        "--check", action="store_true", help="run claude plugin validate and test"
    )
    a = ap.parse_args()

    config = a.config.resolve()
    b = load(config)
    out = (a.out or config.parent / "mod").resolve()
    dest = out / f"{b['slug']}-spinner"
    assets = write_mod(b, dest)
    preview = write_preview(b, assets, dest)
    media = capture(preview, dest / "media") if a.media else []
    write_readme(b, dest, media)
    ok = check(dest) if a.check else True
    print(
        json.dumps(
            {"mod": str(dest), "preview": str(preview), "media": media, "ok": ok},
            ensure_ascii=False,
        )
    )
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
