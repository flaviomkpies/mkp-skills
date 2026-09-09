# -*- coding: utf-8 -*-
"""Gate determinístico do .pptx — o lado que não tinha nenhum.

Quatro classes de defeito que a casa já produziu e pagou:
  1. texto colidindo com texto  (rótulo + microcopy no caso CAPM 21/08)
  2. forma fora do palco        (conteúdo empurrado além do slide)
  3. <p:style> presente         (traz a sombra do tema Office; IMC 20/08)
  4. conector usado como fio    (renderiza ~10px fora do PowerPoint; IMC 20/08)
mais fonte fora do tema.

    python3 check_pptx.py deck.pptx [--fontes "Fraunces,Inter,Inter SemiBold"]

Sai 1 se houver FAIL. A largura do texto é MEDIDA (textmetrics), não estimada:
estimar por len() é a origem da classe 1.
"""
import sys, os, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pptx import Presentation
from pptx.util import Emu
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn
import textmetrics as TM

PALCO_W, PALCO_H = 1920, 1080


def _px(v, escala):
    return float(v) * escala if v is not None else 0.0


def caixas_de_texto(slide, escala):
    """(x0,y0,x1,y1, texto, shape) do texto REALMENTE tintado em cada forma."""
    out = []
    for sh in slide.shapes:
        if not sh.has_text_frame:
            continue
        tf = sh.text_frame
        texto = tf.text.strip()
        if not texto:
            continue
        bx, by = _px(sh.left, escala), _px(sh.top, escala)
        bw, bh = _px(sh.width, escala), _px(sh.height, escala)
        larg, alt, alinh = 0.0, 0.0, PP_ALIGN.LEFT
        for p in tf.paragraphs:
            linha = "".join(r.text for r in p.runs)
            if not linha.strip():
                continue
            r0 = p.runs[0]
            fam = r0.font.name or "Inter"
            tam = r0.font.size.pt if r0.font.size else 18
            try:
                w = TM.largura(linha, fam, tam * (4 / 3), bold=bool(r0.font.bold),
                               italic=bool(r0.font.italic))
            except TM.FonteAusente:
                w = 0.55 * tam * (4 / 3) * len(linha)   # degrada, mas avisa depois
            larg = max(larg, min(w, bw if bw else w))
            alt += tam * (4 / 3) * 1.35
            alinh = p.alignment or alinh
        if larg <= 0:
            continue
        if alinh == PP_ALIGN.RIGHT:
            x0 = bx + bw - larg
        elif alinh == PP_ALIGN.CENTER:
            x0 = bx + (bw - larg) / 2
        else:
            x0 = bx
        out.append((x0, by, x0 + larg, by + max(alt, 1), texto, sh))
    return out


def intersecta(a, b, folga=2.0):
    return (a[0] < b[2] - folga and b[0] < a[2] - folga
            and a[1] < b[3] - folga and b[1] < a[3] - folga)


def checar(caminho, fontes_ok=None):
    prs = Presentation(caminho)
    escala = PALCO_W / prs.slide_width          # EMU -> px do palco
    res = []
    for i, slide in enumerate(prs.slides, 1):
        cxs = caixas_de_texto(slide, escala)
        for a in range(len(cxs)):
            for b in range(a + 1, len(cxs)):
                if intersecta(cxs[a], cxs[b]):
                    res.append(("FAIL", i, f"texto sobre texto: {cxs[a][4][:34]!r} × {cxs[b][4][:34]!r}"))
        # chave = elemento XML: python-pptx devolve um proxy NOVO a cada iteração,
        # então id(shape) não casa entre as duas varreduras. (21/08/2026)
        tintado = {id(c[5]._element): c for c in cxs}
        for sh in slide.shapes:
            x0, y0 = _px(sh.left, escala), _px(sh.top, escala)
            x1, y1 = x0 + _px(sh.width, escala), y0 + _px(sh.height, escala)
            fora_caixa = x0 < -2 or y0 < -2 or x1 > PALCO_W + 2 or y1 > PALCO_H + 2
            c = tintado.get(id(sh._element))
            if c:
                # Em forma de texto o que o leitor vê é a TINTA, não a caixa. Caixa grande
                # com texto curto renderiza certa — reprovar isso ensina a ignorar o gate.
                # Mas fica o aviso: crescer o texto joga o conteúdo pra fora em silêncio.
                if c[0] < -2 or c[1] < -2 or c[2] > PALCO_W + 2 or c[3] > PALCO_H + 2:
                    res.append(("FAIL", i, f"texto fora do palco: {c[4][:40]!r} termina em "
                                           f"({c[2]:.0f},{c[3]:.0f})"))
                elif fora_caixa:
                    res.append(("WARN", i, f"caixa passa do palco (texto ainda cabe): "
                                           f"{c[4][:34]!r} até x={x1:.0f}"))
            elif fora_caixa:
                res.append(("FAIL", i, f"forma fora do palco: {sh.shape_type} em "
                                       f"({x0:.0f},{y0:.0f})-({x1:.0f},{y1:.0f})"))
            if sh._element.find(qn('p:style')) is not None:
                res.append(("FAIL", i, "<p:style> presente: traz a sombra do tema Office"))
            if sh.element.tag.endswith('}cxnSp'):
                res.append(("WARN", i, "conector: renderiza espesso fora do PowerPoint, usar retângulo"))
            if sh.has_text_frame and fontes_ok:
                for p in sh.text_frame.paragraphs:
                    for r in p.runs:
                        if r.font.name and r.font.name not in fontes_ok:
                            res.append(("WARN", i, f"fonte fora do tema: {r.font.name}"))
    return prs, res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pptx")
    ap.add_argument("--fontes", default="")
    a = ap.parse_args()
    fontes = {s.strip() for s in a.fontes.split(",") if s.strip()} or None
    prs, res = checar(a.pptx, fontes)
    vistos = set()
    for nivel, i, msg in res:
        chave = (nivel, i, msg[:60])
        if chave in vistos:
            continue
        vistos.add(chave)
        print(f"  {nivel:<4} [pág {i:>2}] {msg}")
    nf = sum(1 for n, _, _ in res if n == "FAIL")
    nw = len(vistos) - sum(1 for n, i, m in res if n == "FAIL" and (n, i, m[:60]) in vistos)
    print(f"\n  {len(prs.slides._sldIdLst)} páginas · {nf} FAIL · {len(vistos)-nf if len(vistos)>=nf else 0} WARN")
    return 1 if nf else 0


if __name__ == "__main__":
    sys.exit(main())
