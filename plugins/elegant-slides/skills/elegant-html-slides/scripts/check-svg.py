#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gate de SVG: todo <text> tem que caber dentro do viewBox.

A classe de defeito: rótulo ancorado perto da borda com texto mais largo do que o
espaço — o SVG continua válido, o navegador desenha, e o texto sai cortado sem
nenhum erro. Aconteceu no caso CAPM (21/08): "β realavancado a 34,4%" virou
"ealavancado a 34,4%" e só apareceu ao olhar o PNG.

Mede pelas métricas reais da fonte (textmetrics), não por len(texto).

    python3 check-svg.py grafico.svg [outro.svg ...]

Sai 1 se algum texto vazar.
"""
import sys, os, pathlib
from lxml import etree

import pathlib as _pl; sys.path.insert(0, str(_pl.Path(__file__).resolve().parents[2] / "elegant-html-to-pptx" / "lib"))
try:
    import textmetrics as TM
except ImportError:
    # Sem o medidor não há verificação possível. Sair alto: gate que não mede
    # e devolve 0 é pior que gate nenhum, porque fabrica confiança.
    sys.exit("check-svg: textmetrics não encontrado (mount do vault caiu?). "
             "NÃO verifiquei nada — não trate isto como aprovação.")

SVG_NS = "{http://www.w3.org/2000/svg}"
TOL = 1.0


def _textos(raiz):
    """<text> com ou sem namespace. SVG gerado à mão costuma sair sem xmlns: parseado
    como XML os elementos ficam sem namespace, o iter namespaced casa com ZERO e o gate
    imprime 'ok' sem ter olhado nada. Encontrado em 21/08/2026."""
    achados = list(raiz.iter(f"{SVG_NS}text")) + list(raiz.iter("text"))
    vistos, out = set(), []
    for t in achados:
        if id(t) not in vistos:
            vistos.add(id(t)); out.append(t)
    return out


def _fam(nome):
    """'Inter, system-ui, sans-serif' -> 'Inter'."""
    return (nome or "Inter").split(",")[0].strip().strip("'\"")


def checar(caminho):
    raiz = etree.parse(str(caminho)).getroot()
    vb = (raiz.get("viewBox") or "").split()
    if len(vb) != 4:
        return [("FAIL", f"{caminho}: sem viewBox, impossível verificar")]
    x0, y0, w, h = map(float, vb)
    x1, y1 = x0 + w, y0 + h
    out = []
    textos = _textos(raiz)
    if not textos:
        return [("FAIL", f"{caminho}: nenhum <text> encontrado — o gate não verificou nada. "
                         f"Verifique o parse antes de confiar no 'ok'.")]
    for t in textos:
        txt = "".join(t.itertext()).strip()
        if not txt:
            continue
        if t.get("transform"):
            continue                       # rotacionado/transladado: fora do escopo simples
        try:
            x = float(t.get("x", 0)); y = float(t.get("y", 0))
            tam = float(t.get("font-size", 16))
        except ValueError:
            continue
        peso = (t.get("font-weight") or "").strip()
        bold = peso in ("bold", "600", "700", "800", "900")
        try:
            larg = TM.largura(txt, _fam(t.get("font-family")), tam, bold=bold)
        except TM.FonteAusente:
            continue
        anc = t.get("text-anchor", "start")
        ini = x - larg if anc == "end" else (x - larg / 2 if anc == "middle" else x)
        fim = ini + larg
        if ini < x0 - TOL:
            out.append(("FAIL", f"corta à esquerda ({ini:.0f} < {x0:.0f}): {txt[:42]!r}"))
        elif fim > x1 + TOL:
            out.append(("FAIL", f"corta à direita ({fim:.0f} > {x1:.0f}): {txt[:42]!r}"))
        elif y < y0 - TOL or y > y1 + tam + TOL:
            out.append(("FAIL", f"fora na vertical (y={y:.0f}): {txt[:42]!r}"))
    return out


def main(args):
    total = 0
    for a in args:
        res = checar(a)
        nome = pathlib.Path(a).name
        for nivel, msg in res:
            print(f"  {nivel}  [{nome}] {msg}")
        total += len(res)
        if not res:
            print(f"  ok    [{nome}] todos os textos dentro do viewBox")
    print(f"\n  {total} FAIL")
    return 1 if total else 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(2)
    sys.exit(main(sys.argv[1:]))
