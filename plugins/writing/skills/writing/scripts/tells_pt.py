#!/usr/bin/env python3
"""tells_pt — contador determinístico de "frase de coach" em prosa PT-BR.

O DNA já proíbe (tom de coach, fecho de efeito, staccato); o que faltava era medir.
Conta, por parágrafo: fragmento (≤4 palavras) · contraste negado ("não é X, é Y" /
"X, não Y" / "X e não Y") · kicker (parágrafo fecha com frase ≤8 palavras) · tricolon
(3+ frases curtas seguidas) · aforismo ("X é o Y de Z", "X é Y. Y é Z.") · travessão.

Uso: python3 tells_pt.py texto.md [--max N]   → exit 1 se total > N (default 3).
Régua: post de ~1.000 palavras publicado pelo Flavio fica em 0–3. Um tell isolado é voz;
a densidade é o problema (blader/humanizer §31, Wikipedia "Signs of AI writing").
"""
import re, sys, io

path = sys.argv[1]
mx = int(sys.argv[sys.argv.index('--max') + 1]) if '--max' in sys.argv else 3
src = io.open(path, encoding='utf-8').read()
src = re.sub(r'^---\n.*?\n---\n', '', src, flags=re.S)           # frontmatter fora
paras = [p.strip() for p in re.split(r'\n\s*\n', src) if p.strip() and not p.startswith('#')]

SENT = re.compile(r'(?<=[.!?:;])\s+(?=[A-ZÁÉÍÓÚÂÊÔÃÕÇ"“(])')
NEG = re.compile(r'\b[nN]ão (?:é|era|foi|são|está)\b[^.;]{2,60}?[,;.] (?:[Éé]|era|foi|são|está)\b'
                 r'|\b(?:e|,) não (?:d[eo]|a|o|na|no|pelo|sobre|por)\b[^.]{0,40}\.'
                 r'|\bnão [^.]{0,40}, (?:e sim|mas sim)\b'
                 r'|\b\w+ é \w+, não \w+[.:;]')                        # "Pergunta é dúvida, não confirmação"
AFOR = re.compile(r'^\w+ é [oa] \w+ d[eoa]s? \w+\.$|\b(?:tem nome|a linguagem d[ao]|a moeda d[ao])\b')  # só frase curta inteira

def words(s): return len(re.findall(r"\w+(?:['-]\w+)?", s))

total, rows = 0, []
for i, p in enumerate(paras, 1):
    sents = [s.strip() for s in SENT.split(p) if s.strip()]
    hits = []
    frags = [s for s in sents if words(s) <= 4]
    if frags: hits.append(f'fragmento×{len(frags)}: ' + ' | '.join(frags))
    if len(sents) >= 2 and words(sents[-1]) <= 8: hits.append(f'kicker: "{sents[-1]}"')
    run = 0
    for s in sents:
        run = run + 1 if words(s) <= 8 else 0
        if run == 3: hits.append('tricolon de frases curtas'); break
    for m in NEG.finditer(p): hits.append(f'contraste negado: "{m.group(0).strip()}"')
    for s_ in sents:
        if words(s_) <= 9 and AFOR.search(s_): hits.append(f'aforismo: "{s_}"')
    if '—' in p or ' – ' in p: hits.append('travessão')
    total += len(hits)
    for h in hits: rows.append(f'§{i:02d}  {h}')

print('\n'.join(rows) or '(nenhum tell)')
print(f'\n{total} tells em {len(paras)} parágrafos · {sum(words(p) for p in paras)} palavras · teto {mx}')
sys.exit(1 if total > mx else 0)
