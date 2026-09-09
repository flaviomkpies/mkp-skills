#!/usr/bin/env python3
"""
Veredas OS — docs_to_epub (CLI)

Purpose:     Junta documentos (markdown e/ou HTML, inclusive cadernos /show-me com prints
             em base64) num EPUB com capa, sumário e um capítulo por arquivo; opcionalmente
             envia ao Kindle e copia ao Drive. É o caminho para "manda isso para o Kindle"
             quando a entrada não é PDF (para PDF: /pdf-to-ebook).
Owner:       CoS
Created:     2026-09-09 (origem: caderno consolidado da metodologia da dissertação)
Lifetime:    durable
Inputs:      arquivos .md/.html na ordem dos capítulos; --title; --author
Outputs:     .epub (pandoc); --send manda via send_to_kindle.py; --drive copia por rclone
Nota:        prints em base64 são extraídos para arquivos JPEG; tamanho final < 49 MB (limite Kindle).
"""
from __future__ import annotations
import argparse, base64, re, subprocess, sys, tempfile, html as H
from pathlib import Path

CSS = """body{font-family:Georgia,serif;line-height:1.4}h1{font-size:1.5em}h2{font-size:1.2em}
img{max-width:100%;height:auto}table{border-collapse:collapse;width:100%;font-size:.85em}
th,td{border-bottom:1px solid #999;padding:4px;vertical-align:top;text-align:left}
.note,.div{font-size:.9em;border-left:3px solid #444;padding-left:.6em}.loc{font-size:.85em;color:#333}sup{font-size:.7em}"""

def md_to_html(p: Path) -> str:
    txt = p.read_text(encoding="utf-8")
    if txt.startswith("---"):                       # frontmatter fora
        i = txt.find("\n---", 3); txt = txt[i + 4:] if i > 0 else txt
    return subprocess.run(["pandoc", "-f", "markdown", "-t", "html"], input=txt, text=True,
                          capture_output=True, check=True).stdout

def html_body(p: Path, work: Path, idx: int) -> str:
    s = p.read_text(encoding="utf-8", errors="ignore")
    s = re.sub(r"<style>.*?</style>|<script>.*?</script>", "", s, flags=re.S)
    if "<body" in s: s = s[s.index(">", s.index("<body")) + 1:]
    if "</body>" in s: s = s[:s.rindex("</body>")]
    n = [0]
    def dump(m):                                     # base64 -> arquivo (pandoc não embute data: grandes)
        n[0] += 1; ext = "jpg" if m.group(1) == "jpeg" else m.group(1)
        f = work / f"img_{idx:02d}_{n[0]:03d}.{ext}"; f.write_bytes(base64.b64decode(m.group(2)))
        return f"<img src='{f}'"
    s = re.sub(r"<img src='data:image/(\w+);base64,([^']+)'", dump, s)
    s = re.sub(r'<img src="data:image/(\w+);base64,([^"]+)"', dump, s)
    s = re.sub(r"<a class='s' href='[^']*'[^>]*>(\d+)</a>", r"<sup>[\1]</sup>", s)   # links sobrescritos dos cadernos
    return s

def chapter_title(p: Path, frag: str) -> str:
    m = re.search(r"<h1[^>]*>(.*?)</h1>", frag, flags=re.S)
    return re.sub(r"<[^>]+>", "", m.group(1)).strip() if m else p.stem.replace("_", " ")

def cover(path: Path, title: str, sub: str) -> None:
    from PIL import Image, ImageDraw, ImageFont
    im = Image.new("RGB", (1200, 1800), "white"); d = ImageDraw.Draw(im)
    fb = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 64)
    fr = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 38)
    d.rectangle([80, 80, 1120, 1720], outline="black", width=6); y = 300
    for line in re.findall(r".{1,26}(?:\s|$)", title): d.text((140, y), line.strip(), fill="black", font=fb); y += 86
    y += 40
    for line in re.findall(r".{1,42}(?:\s|$)", sub): d.text((140, y), line.strip(), fill="black", font=fr); y += 56
    im.save(path)

def main() -> int:
    ap = argparse.ArgumentParser(description="md/html → EPUB (→ Kindle)")
    ap.add_argument("inputs", nargs="+"); ap.add_argument("--out", required=True)
    ap.add_argument("--title", required=True); ap.add_argument("--author", default="Flavio Pies · Veredas OS")
    ap.add_argument("--subtitle", default=""); ap.add_argument("--lang", default="pt-BR")
    ap.add_argument("--send", action="store_true", help="manda ao Kindle (send_to_kindle.py)")
    ap.add_argument("--drive", default="", help="destino rclone, ex.: 'gdrive:40_Acadêmico/.../x.epub'")
    a = ap.parse_args()
    work = Path(tempfile.mkdtemp(prefix="docs_to_epub_")); parts = []
    for i, f in enumerate(map(Path, a.inputs), 1):
        frag = md_to_html(f) if f.suffix.lower() == ".md" else html_body(f, work, i)
        t = chapter_title(f, frag); frag = re.sub(r"<h1[^>]*>.*?</h1>", "", frag, count=1, flags=re.S)
        frag = re.sub(r"<(/?)h([2-5])", lambda m: f"<{m.group(1)}h{int(m.group(2))}", frag)
        parts.append(f"<h1>{H.escape(t)}</h1>\n{frag}")
    (work / "book.html").write_text("<!DOCTYPE html><html><head><meta charset='utf-8'></head><body>" + "\n".join(parts) + "</body></html>", encoding="utf-8")
    (work / "epub.css").write_text(CSS); cover(work / "cover.png", a.title, a.subtitle or a.author)
    out = Path(a.out).resolve()
    subprocess.run(["pandoc", str(work / "book.html"), "-o", str(out), "--toc", "--toc-depth=2", "--split-level=1",
                    "--css", str(work / "epub.css"), "--epub-cover-image", str(work / "cover.png"),
                    "--metadata", f"title={a.title}", "--metadata", f"author={a.author}", "--metadata", f"lang={a.lang}"],
                   check=True, cwd=work)
    mb = out.stat().st_size / 1e6; print(f"OK {out} ({mb:.1f} MB, {len(parts)} capítulos)")
    if mb > 49: print("ACIMA do limite do Kindle (49 MB): reduza os prints", file=sys.stderr); return 2
    if a.send:
        sender = Path(__file__).with_name("send_to_kindle.py")
        if not sender.exists():
            print("--send: envie o EPUB por e-mail ao seu endereço Send to Kindle; não há script de envio nesta instalação."); return 0
        r = subprocess.run([sys.executable, str(sender), str(out)], capture_output=True, text=True)
        print(r.stdout.strip() or r.stderr.strip())
        if r.returncode: return r.returncode
    if a.drive:
        subprocess.run(["rclone", "copyto", str(out), a.drive, "--retries", "5", "--retries-sleep", "40s"], check=True)
        print("Drive:", a.drive)
    return 0

if __name__ == "__main__":
    sys.exit(main())
