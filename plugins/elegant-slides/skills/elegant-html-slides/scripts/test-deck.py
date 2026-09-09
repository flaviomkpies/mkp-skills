#!/usr/bin/env python3
"""
Veredas OS — test-deck (suíte de testes determinística de deck HTML)

Purpose:     Roda asserts contra o DOM renderizado de um deck elegant-html-slides
             (sobreposição/posição, pontuação, sinais aritméticos, controller, console).
Owner:       Flavio
Created:     2026-06-24
Last-edited: 2026-06-24 (via skill elegant-html-slides)
Issue:       fast-track
Lifetime:    durable
Inputs:      deck.html (arg) · Chrome headless (--chrome)
Outputs:     relatório stdout (FAIL/WARN) · exit 0/1 · --json opcional
Cron:        manual (Fase 4.5/4.6 do workflow da skill)

Camada 1 (esta): checagens OBJETIVAS via Playwright/DOM. Camada 2 (anti-AI-slop
semântico) = slop-audit.py (Haiku). Cada erro pego na prática virou teste (ver PITFALLS.md).
Uso: python3 test-deck.py deck.html [--chrome ...] [--json out.json]
"""
import asyncio, sys, re, json, argparse, os
from playwright.async_api import async_playwright

STAGE_W, STAGE_H = 1920, 1080

DOM_PROBE = r"""
(idx) => {
  if (window.deck && typeof window.deck.show === 'function') window.deck.show(idx);
  const s = document.querySelectorAll('.slide')[idx];
  if (!s) return {missing:true};
  const stage = document.querySelector('.deck-stage'); if (stage) stage.style.transform = 'none';
  const r = el => { if(!el) return null; const b = el.getBoundingClientRect();
    return {top:Math.round(b.top),bottom:Math.round(b.bottom),left:Math.round(b.left),right:Math.round(b.right),h:Math.round(b.height)}; };
  const title = s.querySelector('.title'), subt = s.querySelector('.subt'), foot = s.querySelector('.foot');
  // Fundo do conteúdo = folha mais baixa que carrega texto/mídia, fora do chrome.
  // NÃO usar div[style*="absolute"]: pega só quem declara position no style inline, e
  // deck que marca por classe (.cb da Régua) devolvia cont=null — asserção de rodapé
  // ficava cega em 6 de 9 páginas. Medido em 21/08/2026, caso CAPM/Petrobras.
  const CHROME = '.foot,.topnav,.pager,.rulev,.title,.subt,.hd';
  let cont = null, contB = 0;
  s.querySelectorAll('*').forEach(el=>{
    if (el.matches(CHROME) || el.closest(CHROME)) return;
    if (el.children.length) return;                                   // só folhas
    const midia = el.tagName==='IMG' || el.tagName==='SVG' || el.tagName==='IMAGE';
    if (!midia && !el.textContent.trim()) return;
    const b = el.getBoundingClientRect();
    const fullBleed = b.left<60 && b.right>1860 && b.top<60;          // atmosfera de fundo, não é conteúdo
    if (!fullBleed && b.height>0 && b.bottom>contB && b.bottom<=1200){contB=b.bottom;cont=el;}
  });
  const txt = el => el ? el.textContent.replace(/\s+/g,' ').trim() : null;
  const sizes = new Set();
  s.querySelectorAll('.cont *, div[style*="absolute"] *').forEach(el=>{
    if (el.children.length===0 && el.textContent.trim().length>1) sizes.add(getComputedStyle(el).fontSize); });
  return {
    title: r(title), subt: r(subt), foot: r(foot), cont: r(cont),
    titleTxt: txt(title), subtTxt: txt(subt),
    fontSizes: [...sizes], slideDisplayNone: getComputedStyle(s).display === 'none',
    overflow: [...s.querySelectorAll('*')].some(el=>{const b=el.getBoundingClientRect();
      return b.left<-2 || b.top<-2 || b.right>1922 || b.bottom>1082;}),
  };
}
"""

def check_text_rules(slide_i, kind, txt, results):
    if not txt: return
    t = txt.rstrip()
    if t.endswith('.') and not t.endswith('...') and not t.endswith('…'):
        results.append(('FAIL', slide_i, f'{kind}: termina com ponto final → "…{t[-32:]}"'))
    if kind == 'título' and '—' in t:
        results.append(('WARN', slide_i, f'{kind}: travessão "—" (VOICE pede zerar) → "{t[:50]}…"'))
    for sign in [' = ', '×', '÷', '≈']:
        if sign in t:
            results.append(('WARN', slide_i, f'{kind}: sinal aritmético "{sign.strip()}" em prosa → "{t[:50]}…"')); break
    if '·' in t:
        results.append(('WARN', slide_i, f'{kind}: bola "·" no texto (OK só em eyebrow/footer) → "{t[:50]}…"'))

async def run(path, chrome, font_var_threshold=6):
    results = []
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=chrome, args=['--no-sandbox','--disable-gpu','--force-color-profile=srgb'])
        pg = await b.new_page(viewport={'width':STAGE_W,'height':STAGE_H}, device_scale_factor=1)
        console_errs = []
        pg.on('console', lambda m: console_errs.append(f'{m.type}: {m.text}') if m.type=='error' else None)
        pg.on('pageerror', lambda e: console_errs.append(f'pageerror: {e}'))
        await pg.goto('file://'+os.path.abspath(path)); await pg.wait_for_timeout(800)

        if (await pg.evaluate("typeof window.deck")) != 'object':
            results.append(('FAIL','-','window.deck não inicializou (controller — preâmbulo dropado?)'))
        for e in console_errs[:10]:
            results.append(('FAIL','-',f'console/page: {e}'))
        n_slides = await pg.evaluate("document.querySelectorAll('.slide').length")
        src = open(path, encoding='utf-8', errors='ignore').read()
        for m in set(int(x) for x in re.findall(r'deck\.show\((\d+)\)', src)):
            if m >= n_slides:
                results.append(('FAIL','-',f'deck.show({m}) fora de range (deck tem {n_slides}) — navegação quebrada'))

        for i in range(n_slides):
            d = await pg.evaluate(DOM_PROBE, i)
            if not d or d.get('missing'): continue
            if d['slideDisplayNone']:
                results.append(('FAIL', i, 'slide com display:none (motor exige visibility/opacity)'))
            if d['overflow']:
                results.append(('WARN', i, 'elemento estoura o palco 1920×1080'))
            sub_b = (d['subt'] or d['title'] or {}).get('bottom')
            if d['cont'] and sub_b and d['cont']['top'] < sub_b - 2:
                results.append(('FAIL', i, f'conteúdo sobe sobre título/subtítulo (cont.top {d["cont"]["top"]} < {sub_b})'))
            if d['cont'] and d['foot'] and d['cont']['bottom'] > d['foot']['top'] + 1:
                results.append(('FAIL', i, f'conteúdo sobrepõe rodapé (cont.bottom {d["cont"]["bottom"]} > foot.top {d["foot"]["top"]})'))
            elif d['cont'] and d['foot'] and 0 < d['foot']['top'] - d['cont']['bottom'] < 8:
                results.append(('WARN', i, f'conteúdo a {d["foot"]["top"]-d["cont"]["bottom"]}px do rodapé (apertado <8px)'))
            # C1 — conteúdo flutuando no topo (deveria ancorar inferior)
            ref_b = (d['subt'] or d['title'] or {}).get('bottom')
            if d['cont'] and d['foot'] and ref_b:
                gap_below = d['foot']['top'] - d['cont']['bottom']; gap_above = d['cont']['top'] - ref_b
                if gap_below > 200 and gap_above < 70:
                    results.append(('WARN', i, f'conteúdo flutua no topo (gap {gap_below}px abaixo · {gap_above}px acima) — ancorar inferior'))
            # C2 — subtítulo multi-linha mais estreito que o título (quebra antes da largura)
            if d['subt'] and d['title'] and d['subtTxt'] and d['subt']['h']>40 and d['subt']['right'] < d['title']['right']-40:
                results.append(('WARN', i, 'subtítulo quebra antes da largura do título (alinhar à largura do título)'))
            check_text_rules(i, 'título', d['titleTxt'], results)
            check_text_rules(i, 'subtítulo', d['subtTxt'], results)
            if len(d['fontSizes']) > font_var_threshold:
                results.append(('WARN', i, f'{len(d["fontSizes"])} tamanhos de fonte no conteúdo (>{font_var_threshold})'))

        bullets = await pg.evaluate(r"""()=>{let o=[];document.querySelectorAll('li').forEach(li=>{
          let t=li.textContent.replace(/\s+/g,' ').trim(); if(t.endsWith('.')&&!t.endsWith('...')&&!t.endsWith('…')) o.push(t.slice(-40));});return o;}""")
        for t in bullets:
            results.append(('FAIL','-',f'bullet (li) com ponto final → "…{t}"'))
        # C4 — agenda/mini-agenda (item com onclick=deck.show): número e título top-alinhados
        # (diferença RELATIVA num↔texto no mesmo item — invariante à posição/escala do slide)
        agenda = await pg.evaluate(r"""()=>{const st=document.querySelector('.deck-stage');if(st)st.style.transform='none';
          let out=[],seen=new Set();
          document.querySelectorAll('.slide').forEach((s,si)=>{
            s.querySelectorAll('[onclick^="deck.show"]').forEach(it=>{
              if(it.children.length<2||seen.has(si))return;
              const num=it.children[0], tb=it.children[1]; const tt=tb.children.length?tb.children[0]:tb;
              if(!/^\d{1,3}$/.test((num.textContent||'').trim()))return;  // item de agenda = 1º filho é número (evita FP em outros onclick=deck.show)
              const dn=num.getBoundingClientRect().top, dt=tt.getBoundingClientRect().top;
              if(Math.abs(dn-dt)>8){out.push({s:si,d:Math.round(dn-dt),l:(tt.textContent||'').trim().slice(0,18)});seen.add(si);}
            });});return out;}""")
        for ag in agenda:
            results.append(('WARN', ag['s'], f'agenda: número e título desalinhados no topo (Δ{ag["d"]}px) — "{ag["l"]}"'))
        await b.close()
    return results

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('deck'); ap.add_argument('--chrome', default='/opt/google/chrome/chrome')
    ap.add_argument('--json'); ap.add_argument('--font-var', type=int, default=6)
    a = ap.parse_args()
    res = asyncio.run(run(a.deck, a.chrome, a.font_var))
    fails = [r for r in res if r[0]=='FAIL']; warns = [r for r in res if r[0]=='WARN']
    for sev, i, msg in sorted(res, key=lambda r:(r[0]!='FAIL', str(r[1]))):
        loc = f'#{i}' if i!='-' else 'deck'
        print(f'  {"FAIL" if sev=="FAIL" else "warn"} [{loc:>5}] {msg}')
    print(f'\n  {len(fails)} FAIL · {len(warns)} WARN')
    if a.json: json.dump([{'sev':s,'slide':i,'msg':m} for s,i,m in res], open(a.json,'w'), ensure_ascii=False, indent=1)
    sys.exit(1 if fails else 0)

if __name__ == '__main__':
    main()
