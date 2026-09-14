#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
score_conversion — nota de consistência da conversão HTML->PPTX em dimensões.
Objetivo: um número auditável + quebra por dimensão. Reusável (recebe o pptx,
o markdown-fonte do texto e a pasta de PNGs do HTML pra o diff visual).
"""
import sys, os, re, unicodedata, glob
from pptx import Presentation
from PIL import Image

def norm(s):
    s=unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()
    s=re.sub(r'[^a-z0-9 ]',' ',s); return re.sub(r'\s+',' ',s).strip()

def source_lines(md):
    out=[]; cap=False
    for ln in open(md,encoding='utf-8'):
        t=ln.rstrip('\n')
        if t.startswith('### '): cap=True; continue
        if t.startswith('#') or t.startswith('>'): cap=False; continue
        if cap and t.strip() and not t.startswith('*('):
            out.append(t.strip())
    return out

def pptx_text(pptx):
    prs=Presentation(pptx); runs=[]; native=0; pics=0
    for sl in prs.slides:
        for sh in sl.shapes:
            if sh.shape_type==13: pics+=1
            if sh.has_text_frame:
                for p in sh.text_frame.paragraphs:
                    for r in p.runs:
                        if r.text.strip(): runs.append(r)
                if sh.text_frame.text.strip(): native+=1
    return prs, runs, native, pics

PALETTE={'141414','4A4A4A','6E6E6E','DADAD6','BFBFBA','FCFCFC','FFFFFF'}
FONTS_OK={'Literata Light','Literata','Inter','Inter SemiBold'}

def visual_sim(pptx_pngs, html_pngs):
    sims=[]
    for a,b in zip(sorted(pptx_pngs),sorted(html_pngs)):
        ia=Image.open(a).convert('L').resize((256,144))
        ib=Image.open(b).convert('L').resize((256,144))
        pa,pb=ia.load(),ib.load()
        diff=sum(abs(pa[x,y]-pb[x,y]) for y in range(144) for x in range(256))
        sims.append(1-diff/(256*144*255))
    return sims

def run(pptx, md, html_glob, pptx_glob, n_slides=None, n_faces=None,
        fonts_ok=None, palette=None):
    # Os limiares eram fixos no deck de um projeto (10 slides, 6 faces, tema Literata):
    # qualquer outro deck perdia 20 pontos por não ser aquele. Agora default = o próprio
    # deck (n_slides) e o conjunto de faces que ele de fato usa. (21/08/2026)
    FONTS_OK_ = fonts_ok or FONTS_OK
    PALETTE_ = palette or PALETTE
    prs,runs,native,pics=pptx_text(pptx)
    # 1. estrutura
    nsl=len(prs.slides._sldIdLst)
    # 2. cobertura textual
    src=source_lines(md); blob=norm(' '.join(r.text for r in runs))
    hit=sum(1 for l in src if norm(l)[:60] in blob or (len(norm(l))>15 and norm(l)[:40] in blob))
    cov=hit/len(src) if src else 0
    # 3. paleta
    badc=set()
    for r in runs:
        try:
            c=r.font.color.rgb
            if c is not None and str(c).upper() not in PALETTE_: badc.add(str(c))
        except: pass
    palette_ok = len(badc)==0
    # 4. fontes
    badf=set(r.font.name for r in runs if r.font.name and r.font.name not in FONTS_OK_)
    # embed
    import zipfile
    nfont=sum(1 for n in zipfile.ZipFile(pptx).namelist() if n.endswith('.fntdata'))
    # 5. editabilidade
    edit_ratio = native/(native+pics) if (native+pics) else 0
    # 6. visual
    sims=visual_sim(sorted(glob.glob(pptx_glob)), sorted(glob.glob(html_glob)))
    vis=sum(sims)/len(sims) if sims else 0

    dims=[
        (f"Estrutura ({n_slides or nsl} slides)", 10,
         10 if (n_slides is None or nsl==n_slides) else max(0,10-abs(nsl-n_slides)*3)),
        ("Cobertura textual", 25, round(cov*25,1)),
        ("Editabilidade (texto nativo)", 15, round(edit_ratio*15,1)),
        ("Paleta P&B do tema", 10, 10 if palette_ok else 4),
        ("Tipografia (fontes do tema)", 15, 15 if not badf else 6),
        ("Fontes embutidas", 10, 10 if nfont>=(n_faces or 6) else 0),
        ("Fidelidade visual de layout", 15, round(vis*15,1)),
    ]
    total=round(sum(d[2] for d in dims),1)
    print("="*60); print("NOTA DE CONSISTÊNCIA DA CONVERSÃO HTML → PPTX"); print("="*60)
    for name,w,sc in dims:
        print(f"  {name:<34} {sc:>5} / {w}")
    print("-"*60); print(f"  {'TOTAL':<34} {total:>5} / 100")
    print("="*60)
    print(f"detalhes: slides={nsl} · cobertura={cov:.0%} ({hit}/{len(src)}) · "
          f"nativos={native} imgs={pics} · fontes_fora={badf or '—'} · "
          f"cores_fora={badc or '—'} · faces_embed={nfont} · visual={vis:.0%}")
    if sims: print("  visual por slide: "+" ".join(f"{s:.0%}" for s in sims))
    return total

if __name__=="__main__":
    B=os.path.dirname(__file__); RP=os.path.join(B,"..","..")
    run(os.path.join(B,"deck_final.pptx"),
        os.path.join(RP,"deck_texto.md"),
        os.path.join(RP,"qc8-*.png"),
        os.path.join(B,"cmp-*.png"))
