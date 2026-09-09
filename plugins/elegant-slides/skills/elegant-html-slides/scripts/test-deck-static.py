#!/usr/bin/env python3
"""
Veredas OS — test-deck-static (Tier 0: testes determinísticos SEM browser)

Purpose:     Análise estática do HTML por <section> (1 por slide): regras de texto
             (ponto final, sinal aritmético, travessão, bola), estrutura e navegação
             (deck.show em range, controller presente, título presente). Roda em
             milissegundos — gate rápido ANTES do tier browser (test-deck.py), que só
             precisa entrar para o que depende de render (sobreposição c/ altura
             dinâmica, valor populado por JS, console).
Owner:       Flavio
Created:     2026-06-24
Last-edited: 2026-06-24 (via skill elegant-html-slides)
Issue:       fast-track
Lifetime:    durable
Inputs:      deck.html (arg)
Outputs:     relatório stdout (FAIL/WARN) · exit 0/1 · --json opcional
Cron:        manual (Fase 4.5 — primeiro gate, antes do browser)

Uso: python3 test-deck-static.py deck.html [--json out.json]
Limite honesto: títulos/valores populados por JS aparecem VAZIOS aqui (id sem texto no
HTML) — viram INFO "dinâmico, conferir no tier browser". Sobreposição com altura de
tabela/texto NÃO é estática (depende de render) → fica no test-deck.py.
"""
import sys, re, json, argparse

def strip_tags(s): return re.sub(r'\s+',' ', re.sub(r'<[^>]+>',' ', s)).strip()

# Marcadores de rascunho/pergunta em aberto — GENÉRICOS (não específicos a projeto/conteúdo).
# Nomes de projeto/pessoa entram via --forbidden, não aqui.
DRAFT_MARKERS = ['a confirmar','a definir','a validar','a separar com','\\bfup\\b','\\btbd\\b',
                 'placeholder','lorem ipsum','\\brascunho\\b','\\[\\?\\]','\\?\\?\\?']
# (sem "TODO": colide com "todo" em PT. Marcadores de código raros num deck — não valem o falso-positivo.)

def text_rules(i, kind, txt, out):
    if not txt: return
    t = txt.rstrip()
    if t.endswith('.') and not t.endswith(('...','…')):
        out.append(('FAIL', i, f'{kind}: ponto final → "…{t[-30:]}"'))
    if kind == 'título' and '—' in t:
        out.append(('WARN', i, f'{kind}: travessão "—" (VOICE pede zerar) → "{t[:48]}…"'))
    for sign in [' = ', '×', '÷', '≈']:
        if sign in t:
            out.append(('WARN', i, f'{kind}: sinal aritmético "{sign.strip()}" em prosa → "{t[:48]}…"')); break
    if '·' in t:
        out.append(('WARN', i, f'{kind}: bola "·" no texto (OK só em eyebrow/footer) → "{t[:48]}…"'))

def run(path, forbidden=None):
    h = open(path, encoding='utf-8', errors='ignore').read()
    out = []
    secs = re.split(r'(?=<section\b)', h)
    secs = [s for s in secs if s.lstrip().startswith('<section')]
    n = len(secs)
    forbidden = [t.strip() for t in (forbidden or []) if t.strip()]

    # Estrutura/navegação (global, estático)
    if 'SlidePresentation' not in h and 'deck-stage' not in h and 'window.deck' not in h:
        out.append(('FAIL', '-', 'controller ausente (sem SlidePresentation/deck-stage) — deck não navega'))
    for m in set(int(x) for x in re.findall(r'deck\.show\((\d+)\)', h)):
        if m >= n:
            out.append(('FAIL', '-', f'deck.show({m}) fora de range (deck tem {n} <section>) — navegação quebrada'))
    # B1 — notação de magnitude misturada (k vs mil), genérico
    vis_all = ' '.join(strip_tags(s) for s in secs)
    if re.search(r'\b\d[\d.,]*\s*k\b', vis_all) and re.search(r'\bmil\b', vis_all):
        out.append(('WARN', '-', 'notação de magnitude misturada no deck ("k" e "mil") — padronizar'))

    for i, s in enumerate(secs):
        vis = strip_tags(s)
        mt = re.search(r'<h2[^>]*class="title"[^>]*>(.*?)</h2>', s, re.S)
        ms = re.search(r'<div[^>]*class="subt"[^>]*>(.*?)</div>', s, re.S)
        title = strip_tags(mt.group(1)) if mt else None
        subt = strip_tags(ms.group(1)) if ms else None
        if mt is not None and not title:
            out.append(('INFO', i, 'título dinâmico (populado por JS) — conferir regras no tier browser'))
        text_rules(i, 'título', title, out)
        text_rules(i, 'subtítulo', subt, out)
        # B2/B4 — marcadores de rascunho / pergunta em aberto (genérico) + termos do projeto (--forbidden)
        for pat in DRAFT_MARKERS:
            m = re.search(r'(?<![\w])('+pat+r')(?![\w])', vis, re.I)
            if m: out.append(('WARN', i, f'marcador de rascunho/pergunta em aberto: "{m.group(1)}" → "{vis[max(0,m.start()-20):m.start()+25]}…"')); break
        for term in forbidden:
            if re.search(r'(?<![\w])'+re.escape(term)+r'(?![\w])', vis, re.I):
                out.append(('WARN', i, f'termo proibido do projeto presente no material: "{term}"')); break
        # B3 — slide SEM dado (sem tabela/svg) com rodapé "Fonte" (fonte espúria)
        mf = re.search(r'<div[^>]*class="foot"[^>]*>(.*?)</div>', s, re.S)
        foot = strip_tags(mf.group(1)) if mf else ''
        if re.search(r'\bfonte\b', foot, re.I) and '<table' not in s and '<svg' not in s:
            out.append(('WARN', i, 'rodapé "Fonte" em slide sem dado (sem tabela/gráfico) — fonte espúria'))
    return out, n

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('deck'); ap.add_argument('--json')
    ap.add_argument('--forbidden', default='', help='termos do projeto a banir (vírgula): nomes internos, codinomes…')
    a = ap.parse_args()
    res, n = run(a.deck, a.forbidden.split(','))
    order = {'FAIL':0,'WARN':1,'INFO':2}
    for sev, i, msg in sorted(res, key=lambda r:(order[r[0]], str(r[1]))):
        loc = f'#{i}' if i!='-' else 'deck'
        tag = {'FAIL':'FAIL','WARN':'warn','INFO':'info'}[sev]
        print(f'  {tag} [{loc:>5}] {msg}')
    f = sum(1 for r in res if r[0]=='FAIL'); w = sum(1 for r in res if r[0]=='WARN'); inf = sum(1 for r in res if r[0]=='INFO')
    print(f'\n  {n} slides · {f} FAIL · {w} WARN · {inf} INFO (estático, sem browser)')
    if a.json: json.dump([{'sev':s,'slide':i,'msg':m} for s,i,m in res], open(a.json,'w'), ensure_ascii=False, indent=1)
    sys.exit(1 if f else 0)

if __name__ == '__main__':
    main()
