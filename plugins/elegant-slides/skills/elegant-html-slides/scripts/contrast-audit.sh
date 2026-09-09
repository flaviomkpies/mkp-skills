#!/bin/bash
# Veredas OS — elegant-html-slides contrast-audit
# Purpose:     Auditoria WCAG de contraste real (DOM via Playwright) de um deck Elegant/reMarkable
# Owner:       Flavio
# Created:     2026-06-19
# Last-edited: 2026-06-19 (CoS via fast-track)
# Issue:       fast-track
# Lifetime:    durable
# Inputs:      <deck.html>
# Outputs:     relatório stdout · exit 0 (sem falhas) / 1 (falhas WCAG AA) / 2 (uso)
# Cron:        manual
set -u
F="${1:-}"
[ -f "$F" ] || { echo "uso: bash scripts/contrast-audit.sh <deck.html>"; exit 2; }
ABS=$(readlink -f "$F")
TEMP_DIR=$(mktemp -d)
trap 'rm -rf "$TEMP_DIR"' EXIT

cat > "$TEMP_DIR/audit.mjs" << 'JS'
import { chromium } from 'playwright';
const file = process.env.DECK;
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
await page.goto('file://' + file, { waitUntil: 'networkidle' });
await page.evaluate(() => document.fonts.ready);
await page.addStyleTag({ content: '*{transition:none!important;animation:none!important;}' });

const results = await page.evaluate(() => {
  const lum = (r,g,b) => { const a=[r,g,b].map(v=>{v/=255;return v<=0.03928?v/12.92:Math.pow((v+0.055)/1.055,2.4);}); return 0.2126*a[0]+0.7152*a[1]+0.0722*a[2]; };
  const ratio = (c1,c2) => { const L1=lum(...c1),L2=lum(...c2); return (Math.max(L1,L2)+0.05)/(Math.min(L1,L2)+0.05); };
  const parse = s => { const m=s.match(/rgba?\(([^)]+)\)/); if(!m) return null; const p=m[1].split(',').map(x=>parseFloat(x)); if(p.length>=4 && p[3]===0) return null; return [p[0],p[1],p[2]]; };
  const compose = (top, bot, a) => top.map((c,i)=>Math.round(c*a + bot[i]*(1-a)));
  const effBg = el => { // compõe as camadas de fundo (com alpha) de el até a raiz sobre branco
    let e=el; const layers=[];
    while(e){ const st=getComputedStyle(e); if(st.backgroundImage && st.backgroundImage!=='none') return 'IMG';
      const m=st.backgroundColor.match(/rgba?\(([^)]+)\)/);
      if(m){ const p=m[1].split(',').map(parseFloat); const a=p.length>=4?p[3]:1; if(a>0) layers.push([[p[0],p[1],p[2]],a]); }
      e=e.parentElement; }
    let base=[255,255,255];
    for(let i=layers.length-1;i>=0;i--){ base=compose(layers[i][0], base, layers[i][1]); }
    return base;
  };
  const out=[];
  const slides=[...document.querySelectorAll('.slide')];
  slides.forEach((slide,si)=>{
    slides.forEach(s=>s.classList.remove('active','visible'));
    slide.classList.add('active','visible');
    [...slide.querySelectorAll('*')].forEach(el=>{
      const hasText=[...el.childNodes].some(n=>n.nodeType===3 && n.textContent.trim().length>1);
      if(!hasText) return;
      const st=getComputedStyle(el);
      if(st.visibility==='hidden'||st.opacity==='0'||st.display==='none') return;
      const fg=parse(st.color); if(!fg) return;
      const bg=effBg(el);
      if(bg==='IMG') return; // foto duotone tem overlay próprio — pular
      const fs=parseFloat(st.fontSize), fw=parseInt(st.fontWeight)||400;
      const large = fs>=24 || (fs>=18.66 && fw>=700);
      const need = large?3.0:4.5;
      const r=ratio(fg,bg);
      if(r < need){
        out.push({slide:si+1, txt:el.textContent.trim().slice(0,42), ratio:+r.toFixed(2), need, fs:Math.round(fs), fw, fg, bg});
      }
    });
  });
  return out;
});
await browser.close();

if(results.length===0){ console.log('  \x1b[32mOK\x1b[0m   sem falhas de contraste (WCAG AA)'); process.exit(0); }
console.log('  \x1b[31m'+results.length+' falha(s) de contraste WCAG AA:\x1b[0m');
for(const r of results){
  console.log(`  slide ${r.slide} · ratio ${r.ratio} (precisa ${r.need}) · ${r.fs}px/${r.fw} · rgb(${r.fg}) sobre rgb(${r.bg}) · "${r.txt}"`);
}
process.exit(1);
JS

cd "$TEMP_DIR"
echo '{ "name":"contrast-audit","private":true,"type":"module" }' > package.json
echo "instalando Playwright (1ª vez demora)..." >&2
npm install playwright &>/dev/null || { echo "falha ao instalar playwright"; exit 1; }
npx playwright install chromium &>/dev/null || { echo "falha ao instalar chromium"; exit 1; }

echo "contrast-audit: $F"
DECK="$ABS" node "$TEMP_DIR/audit.mjs"
