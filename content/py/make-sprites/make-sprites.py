#!/usr/bin/env python3
"""Build a single SVG sprite from a directory of icon files.

Usage:
    python3 build_sprite.py ICON_DIR OUTPUT_FILE

Each ``*.svg`` file in ICON_DIR becomes one ``<symbol id="...">`` in the
combined sprite.  The id is derived from the filename (``us.svg`` -> ``us``),
the viewBox is carried over from the source file, and everything inside the
root <svg> tag — including <title>/<desc> accessibility text — is kept,
except editor cruft (Inkscape's <metadata> RDF block, <sodipodi:namedview>,
empty <defs/> placeholders), which is stripped, along with namespace
declarations nothing uses anymore.

As an interim measure, ``*.png`` files in ICON_DIR are also picked up:
each is embedded as a base64 data-URI ``<image>`` inside its own symbol
(viewBox from the PNG's pixel dimensions).  Drop in a real ``.svg`` with
the same filename later: it supersedes the PNG automatically and the
symbol id stays stable.

Run before ``pelican`` whenever icons change.
"""

import base64
import re
import struct
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

# Sprite root: hidden with the width-0 trick, NOT display:none
# (display:none breaks <use> resolution in some engines).
ROOT = (
    '<svg xmlns="http://www.w3.org/2000/svg" '
    'style="position:absolute;width:0;height:0;overflow:hidden">\n'
)

ID_OK = re.compile(r"[^a-z0-9-]+")

# Prefixed namespace declarations (xmlns:xlink="...", xmlns:inkscape="...", ...).
NS_DECL = re.compile(r'xmlns:([\w.-]+)\s*=\s*"([^"]+)"')


def slugify(stem: str) -> str:
    """Turn a filename stem into a safe symbol id."""
    return ID_OK.sub("-", stem.strip().lower()).strip("-") or "icon"


def strip_element(text: str, tag: str) -> str:
    """Remove <tag ...>...</tag> blocks (and self-closing <tag .../>)."""
    tag = re.escape(tag)
    return re.sub(rf"<{tag}\b[^>]*/>|<{tag}\b[^>]*>.*?</{tag}\s*>",
                  "", text, flags=re.DOTALL)


def extract_icon(path: Path) -> tuple[str, str, str, str]:
    """Return (id, viewBox_attribute, namespace_attribute, inner_content)."""
    text = path.read_text(encoding="utf-8")

    m = re.search(r"<svg\b[^>]*>", text)
    if m is None:
        raise ValueError(f"{path.name}: no <svg> root tag found")
    root = m.group(0)
    if root.endswith("/>"):
        raise ValueError(f"{path.name}: empty <svg/> root (nothing to sprite)")

    vb = re.search(r'viewBox\s*=\s*"([^"]+)"', root)
    if not vb:
        print(f"  warning: {path.name} has no viewBox on its root; "
              f"sprites need one or the icon will collapse")

    inner_start = m.end()
    inner_end = text.rfind("</svg>")
    if inner_end < inner_start:
        raise ValueError(f"{path.name}: unbalanced <svg> tags")
    inner = text[inner_start:inner_end].strip()

    # Drop editor cruft that adds nothing inside a sprite symbol:
    # Inkscape's <metadata> RDF block, (old files) <sodipodi:namedview>,
    # and empty <defs/> placeholders.  A <defs> WITH content stays:
    # it may hold gradients/filters the icon references via url(#id).
    inner = strip_element(strip_element(inner, "metadata"),
                          "sodipodi:namedview")
    inner = re.sub(r"<defs\b[^>]*/>|<defs\b[^>]*>\s*</defs\s*>", "", inner)
    inner = re.sub(r"\n\s*\n+", "\n", inner).strip()
    if not inner:
        raise ValueError(f"{path.name}: no content between <svg> tags")

    # Accessibility TODO list: note icons missing <title>/<desc>.
    for tag in ("title", "desc"):
        if not re.search(rf"<{tag}\b", inner):
            print(f"  note: {path.name}: no <{tag}> element")

    vb_attr = f' viewBox="{vb.group(1)}"' if vb else ""

    # Re-declare prefixed namespaces from the source root on the symbol,
    # keeping only ones the surviving content still uses (after cruft
    # stripping, dc:/cc:/rdf:/sodipodi: are usually dead weight).
    used = set(re.findall(r"(?<![/\w.-])([A-Za-z][\w.-]*):[A-Za-z]", inner))
    ns_parts = [f'xmlns:{m.group(1)}="{m.group(2)}"'
                for m in NS_DECL.finditer(root)
                if m.group(1) != "xml"   # xml: prefix is predeclared
                and m.group(1) in used]
    ns_attr = (" " + " ".join(ns_parts)) if ns_parts else ""

    return slugify(path.stem), vb_attr, ns_attr, inner


def extract_png(path: Path) -> tuple[str, str, str, str]:
    """Return (id, viewBox_attribute, ns_attr, inner) for a PNG stopgap.

    Embeds the PNG as a base64 data-URI <image> inside its own symbol,
    sized to the PNG's pixel dimensions.  Interim support: the symbol is
    a raster in vector clothing — it cannot be tinted via currentColor.
    """
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise ValueError(f"{path.name}: not a valid PNG file")
    width, height = struct.unpack(">II", data[16:24])

    if len(data) > 10 * 1024:
        print(f"  note: {path.name}: {len(data) // 1024} KB raster "
              f"will bloat the sprite; consider a real SVG")

    b64 = base64.b64encode(data).decode("ascii")
    vb_attr = f' viewBox="0 0 {width} {height}"'
    inner = (f'<image x="0" y="0" width="{width}" height="{height}" '
             f'href="data:image/png;base64,{b64}"/>')
    return slugify(path.stem), vb_attr, "", inner


def main(icon_dir: str, out_file: str) -> int:
    src = Path(icon_dir)
    out = Path(out_file)

    # Never ingest our own output, even when it lands in the icons dir.
    # PNGs ride along as stopgap symbols until real SVGs replace them;
    # a real SVG supersedes a same-named PNG stopgap.
    by_stem: dict[str, Path] = {}
    for f in sorted([*src.glob("*.svg"), *src.glob("*.png")]):
        if f.resolve() == out.resolve():
            continue
        if f.suffix.lower() == ".svg":
            if f.stem in by_stem:
                print(f"  note: {f.name} supersedes the "
                      f"{by_stem[f.stem].name} stopgap")
            by_stem[f.stem] = f
        elif f.stem not in by_stem:
            by_stem[f.stem] = f
    files = sorted(by_stem.values())
    if not files:
        print(f"no .svg/.png files found in {src}")
        return 1

    symbols = []
    seen: set[str] = set()
    for f in files:
        try:
            if f.suffix.lower() == ".png":
                sid, vb_attr, ns_attr, inner = extract_png(f)
            else:
                sid, vb_attr, ns_attr, inner = extract_icon(f)
        except ValueError as e:
            print(f"  warning: skipping {e}")
            continue
        if sid in seen:
            print(f"  warning: duplicate id '{sid}' (from {f.name}); skipped")
            continue
        seen.add(sid)
        symbols.append(
            f'  \n<symbol id="{sid}"{vb_attr}{ns_attr}>\n{inner}\n  </symbol>')
        print(f"  {sid}  <- {f.name}")

    if not symbols:
        print(f"nothing to build from {src}")
        return 1

    sprite = ROOT + "\n".join(symbols) + "\n</svg>\n"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(sprite, encoding="utf-8")

    # Self-check: the combined file must still be well-formed XML.
    try:
        ET.fromstring(sprite)
    except ET.ParseError as e:
        print(f"ERROR: generated sprite is not well-formed XML: {e}")
        return 1

    print(f"{len(symbols)} icons -> {out}")
    return 0

if __name__ == "__main__":
    # if len(sys.argv) != 3:
    #     sys.exit(__doc__)
    # sys.exit(main(sys.argv[1], sys.argv[2]))
    icon_dir = "/home/systemuser/Documents/code/web_resume/tailcd13e6.ts.net/content/py/make-sprites/src/"
    out_file = "/home/systemuser/Documents/code/web_resume/tailcd13e6.ts.net/content/py/make-sprites/dst/sprites.svg"
    main(icon_dir, out_file)
"""

.. |us| raw:: html

   <svg class="icon" style="height:1em" aria-hidden="true"><use href="/static/svg/sprite.svg#us"/></svg>


.. |github| raw:: html

   <a href="https://github.com/kingrpaul" aria-label="GitHub"><svg class="icon" style="height:1em" aria-hidden="true"><use href="/static/svg/sprite.svg#github"/></svg></a>


One line of CSS in custom.css:
.icon { display: inline-block; vertical-align: middle; }

====================



Using python pelican w/RST, can I create an image whose content is specified by an svg file but using a hashtag ID to point to an image within that file?

<svg xmlns="http://www.w3.org/2000/svg"
     style="position:absolute;width:0;height:0;overflow:hidden">
  <symbol id="moon" viewBox="0 0 32 32">
    <path d="M20 4a12 12 0 1 0 8 22A14 14 0 0 1 20 4z" fill="currentColor"/>
  </symbol>
  <symbol id="dash" viewBox="0 0 64 8">
    <rect x="0" y="1" width="64" height="6" rx="3" fill="currentColor"/>
  </symbol>
  <view id="moonview" viewBox="0 0 32 32"/>
</svg>


<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>sprite test</title></head>
<body>
<p>1. Paved road — inline use:</p>
<svg style="height:1.5em;color:#333" aria-hidden="true"><use href="/static/svg/sprite.svg#moon"/></svg>
<svg style="height:1.5em;color:#333" aria-hidden="true"><use href="/static/svg/sprite.svg#dash"/></svg>

<p>2. Dragon corner — fragment crop via img:</p>
<img src="/static/svg/sprite.svg#moonview" style="height:1.5em" alt="">

<p>3. Dragon corner — fragment crop via object (what docutils emits):</p>
<object data="/static/svg/sprite.svg#moonview" type="image/svg+xml"
        style="height:1.5em">fallback</object>
</body></html>


<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"> <title>Pressmark for EP Dutton and Company</title> <a href="https://commons.wikimedia.org/wiki/File:Logo_EP_Dutton_and_Company.png" target="_top"> <path d="..."/> </a> </svg>


.. |moon| raw:: html <svg style="height:1.5em" aria-hidden="true"><use href="/static/svg/sprite.svg#moon"/></svg>

.. |moon| raw:: html <a href="https://commons.wikimedia.org/wiki/File:Whatever" aria-label="EP Dutton pressmark on Wikimedia Commons"> <svg style="height:1.5em" aria-hidden="true"> <use href="/static/svg/sprite.svg#moon"/> </svg> </a>

"""
