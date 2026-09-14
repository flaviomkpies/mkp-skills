#!/usr/bin/env python3
def _chrome():
    """Acha o Chrome/Chromium: $CHROME_BIN, depois PATH, depois caminhos comuns Linux/macOS."""
    import os, shutil as _sh
    if os.environ.get("CHROME_BIN"):
        return os.environ["CHROME_BIN"]
    for n in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser"):
        p = _sh.which(n)
        if p:
            return p
    for p in ("/opt/google/chrome/chrome",
              "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
              "/Applications/Chromium.app/Contents/MacOS/Chromium"):
        if os.path.exists(p):
            return p
    return "google-chrome"

"""
workspace de origem — slop-audit (camada 2: anti-AI-slop semântico via Haiku)

Purpose:     Extrai o texto de cada slide (título + corpo) e pede a um modelo barato
             (Haiku) para flagar padrões de AI-slop e violações de voz que regex não pega:
             travessão, hedging, "não apenas… mas também", filler consulting genérico,
             CTA inspiracional, recomendação em material M&A neutro, action-title que é
             rótulo (não conclusão). Também o teste "história pelos títulos".
Owner:       O autor
Created:     2026-06-24
Last-edited: 2026-06-24 (via skill elegant-html-slides)
Issue:       fast-track
Lifetime:    durable
Inputs:      deck.html (arg) · ANTHROPIC_API_KEY (env) · Chrome headless
Outputs:     relatório stdout (issues por slide) · --json opcional
Cron:        manual (Fase 4.6 do workflow da skill)

Complementa test-deck.py (camada 1 determinística). Haiku porque é julgamento, não
asserção: o objetivo é SINALIZAR pra revisão humana, não reprovar automaticamente.
Uso: python3 slop-audit.py deck.html [--model claude-haiku-4-5] [--json out.json]
"""
import asyncio, sys, os, json, argparse
from playwright.async_api import async_playwright

SYSTEM = """Você é um editor severo de decks editoriais (tema Elegant/reMarkable). Avalia o texto dos slides contra a VOZ do autor (VOICE.md) e contra AI-slop. NÃO reescreve — só FLAGA, citando o trecho.

Regras (cada violação vira um issue):
- travessão "—" em qualquer lugar (a marca zera travessão; usar vírgula/dois-pontos)
- hedging: "potencialmente", "talvez", "pode vir a", "de certa forma", "é importante notar", "vale destacar/ressaltar"
- estruturas-clichê: "não apenas… mas também", "tanto… quanto", "mais do que nunca", "em um mundo onde"
- filler de consultoria genérico / adjetivos vazios ("robusto", "sinérgico", "holístico", "de ponta")
- hipérbole / CTA inspiracional no fechamento
- recomendação ("a empresa deve", "recomendamos", "sugerimos") em material que deve ser NEUTRO (M&A factual)
- action-title que é RÓTULO, não conclusão (so-what). Ex.: "Quem somos" (rótulo) vs "Conecto X a Y" (conclusão). Flag títulos sem verbo de tese.
- afirmar o ÓBVIO/trivial (ex.: "o imposto é variável", "o custo é indexado à receita", "a projeção reage ao cenário") — não agrega, é ruído
- subtítulo que apenas PARAFRASEIA o título (deve qualificar, delimitar escopo, dar método ou dizer como ler o slide — nunca repetir o título)
- sinal aritmético em prosa (=, +, ×, ÷) — unidade (R$/t) e seta de fluxo (→) são OK
- ponto final em título/bullet/subtítulo

Responda SÓ com JSON válido:
{"slides":[{"i":<índice>,"issues":[{"type":"<regra>","quote":"<trecho>","why":"<1 frase>"}]}],
 "storyline":{"verdict":"<ok|fraca>","note":"<lendo só os títulos em sequência: começa pela resposta e termina na ação? a história fecha?>"}}
Slides sem issue: não inclua. Se nada, "slides":[]."""

EXTRACT = r"""()=>{return [...document.querySelectorAll('.slide')].map((s,i)=>{
  if(window.deck&&window.deck.show)window.deck.show(i);
  const t=s.querySelector('.title'); const sub=s.querySelector('.subt');
  const body=[...s.querySelectorAll('p,li,td,.subt,h3,.lead,[id$=-lead]')].map(e=>e.textContent.replace(/\s+/g,' ').trim()).filter(x=>x.length>2);
  return {i, title:(t?t.textContent.replace(/\s+/g,' ').trim():''), sub:(sub?sub.textContent.trim():''), body:[...new Set(body)].slice(0,12)};
}).filter(s=>s.title||s.body.length);}"""

async def extract(path, chrome):
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path=chrome,args=['--no-sandbox','--disable-gpu'])
        pg=await b.new_page(viewport={'width':1920,'height':1080})
        await pg.goto('file://'+os.path.abspath(path)); await pg.wait_for_timeout(800)
        data=await pg.evaluate(EXTRACT); await b.close(); return data

def _parse(txt):
    try: return json.loads(txt[txt.find('{'):txt.rfind('}')+1]), None
    except Exception as e: return None, f"resposta não-parseável: {e}\n{txt[:300]}"

def call_haiku(slides, model):
    payload="\n".join(f"[{s['i']}] TÍTULO: {s['title']}\n  SUBT: {s['sub']}\n  CORPO: {' | '.join(s['body'])}" for s in slides)
    user=f"Audite estes slides:\n\n{payload}"
    # Caminho 1 — API (portável, fora do workspace de origem): exige ANTHROPIC_API_KEY + lib anthropic
    key=os.environ.get('ANTHROPIC_API_KEY')
    if key:
        try:
            import anthropic
            msg=anthropic.Anthropic(api_key=key).messages.create(model=model, max_tokens=4000, system=SYSTEM,
                messages=[{"role":"user","content":user}])
            return _parse(msg.content[0].text)
        except Exception as e:
            return None, f"API anthropic falhou: {e}"
    # Caminho 2 — claude -p (workspace de origem/OAuth). Regra <issue>: euid=0 → rodar como ubuntu.
    import subprocess, shutil
    if not shutil.which('claude'):
        return None, "sem ANTHROPIC_API_KEY e sem CLI `claude` — defina a chave ou rode num ambiente com claude."
    cmd=['claude','-p',SYSTEM+"\n\n"+user,'--model',model.replace('claude-haiku-4-5','haiku'),'--permission-mode','bypassPermissions']
    if hasattr(os,'geteuid') and os.geteuid()==0:
        cmd=['claude']+cmd
    try:
        r=subprocess.run(cmd, capture_output=True, text=True, timeout=240)
        if r.returncode!=0: return None, f"claude -p falhou (rc={r.returncode}): {r.stderr[:200]}"
        return _parse(r.stdout)
    except Exception as e:
        return None, f"claude -p exceção: {e}"

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('deck')
    ap.add_argument('--chrome', default=_chrome())
    ap.add_argument('--model', default='claude-haiku-4-5'); ap.add_argument('--json')
    a=ap.parse_args()
    slides=asyncio.run(extract(a.deck, a.chrome))
    res, err = call_haiku(slides, a.model)
    if a.json: json.dump({'extracted':slides,'audit':res,'error':err}, open(a.json,'w'), ensure_ascii=False, indent=1)
    if err: print("  (slop-audit não rodou:", err, ")"); sys.exit(0)
    n=0
    for s in res.get('slides',[]):
        for iss in s.get('issues',[]):
            n+=1; print(f"  ⚠️  [#{s['i']:>3}] {iss['type']}: \"{iss.get('quote','')[:60]}\" — {iss.get('why','')}")
    st=res.get('storyline',{})
    print(f"\n  storyline: {st.get('verdict','?')} — {st.get('note','')}")
    print(f"  {n} flags de AI-slop/voz (Haiku — revisão humana, não reprova automático)")

if __name__ == '__main__':
    main()
