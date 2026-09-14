#!/usr/bin/env python3
"""tells_pt — contador determinístico de "frase de coach" em prosa PT-BR.

O DNA já proíbe (tom de coach, fecho de efeito, staccato); o que faltava era medir.
Conta, por parágrafo: fragmento (≤4 palavras) · contraste negado ("não é X, é Y" /
"X, não Y" / "X e não Y") · kicker (parágrafo fecha com frase ≤8 palavras) · tricolon
(3+ frases curtas seguidas) · aforismo ("X é o Y de Z", "X é Y. Y é Z.") · travessão.

Uso: python3 tells_pt.py texto.md [--max N] [--perfil newsletter|academico]
     → exit 1 se total > N (default 3).

Perfil: os limiares nasceram calibrados para newsletter, onde a frase publicada do autor
tem 8 palavras ou menos. Em prosa academica a frase media passa de 20, e os MESMOS tells
aparecem em construcoes longas — o gate passava limpo num texto cheio deles (medido em
11/09/2026, Introducao da dissertacao: 2 tells, ambos falso-positivo de citacao). O perfil
academico sobe a fronteira de "frase curta" para 14 palavras e liga os tres detectores que
so aparecem em texto longo: paralelismo negativo com dois-pontos, regra de tres e setup.
Régua: post de ~1.000 palavras publicado pelo autor fica em 0–3. Um tell isolado é voz;
a densidade é o problema (blader/humanizer §31, Wikipedia "Signs of AI writing").
"""
import re, sys, io

path = sys.argv[1]
mx = int(sys.argv[sys.argv.index('--max') + 1]) if '--max' in sys.argv else 3
perfil = sys.argv[sys.argv.index('--perfil') + 1] if '--perfil' in sys.argv else 'newsletter'
CURTA = 14 if perfil == 'academico' else 8
src = io.open(path, encoding='utf-8').read()
src = re.sub(r'^---\n.*?\n---\n', '', src, flags=re.S)           # frontmatter fora
paras = [p.strip() for p in re.split(r'\n\s*\n', src) if p.strip() and not p.startswith('#')]
# citação entre parênteses é atribuição, não prosa: sai antes de medir (senão "Bick, Blandin
# e Deming" conta como regra de três e o gate vira ruído).
paras = [re.sub(r'\s*\([^()]*\)', '', p) for p in paras]
# citação NARRATIVA ("Tranfield, Denyer e Smart (2003)") deixa os sobrenomes no texto corrido;
# depois que o parêntese sai, "A, B e C" vira falso tricolon. Atribuição não é prosa: sai antes
# de medir. (Bug irmão do de 11/09, medido em 12/09 na dissertação: 20 dos 54 tells eram nomes.)
AUTORES = re.compile(
    r'\b[A-ZÁÉÍÓÚÂÊÔÃÕÇ][\wÀ-ÿ\'\u2019]+'
    r'(?:,\s*[A-ZÁÉÍÓÚÂÊÔÃÕÇ][\wÀ-ÿ\'\u2019]+)+'
    r'\s+e\s+[A-ZÁÉÍÓÚÂÊÔÃÕÇ][\wÀ-ÿ\'\u2019]+')
paras = [AUTORES.sub('FONTE', p) for p in paras]

SENT = re.compile(r'(?<=[.!?:;])\s+(?=[A-ZÁÉÍÓÚÂÊÔÃÕÇ"“(])')
NEG = re.compile(r'\b[nN]ão (?:é|era|foi|são|está)\b[^.;:]{2,80}?[,;.:] ?(?:[Éé]|era|foi|são|está)\b'
                 r'|\b(?:não|nunca|raramente|jamais) [^.;:]{2,80}?: [a-zé]'
                 r'|\bnão [^.;:]{2,60}?, mas\b'
                 r'|\bnão (?:para|fica|se limita) (?:em|n[oa]|por)[^.;:]{0,40}?: '
                 r'|\b(?:e|,) não (?:d[eo]|a|o|na|no|pelo|sobre|por)\b[^.]{0,40}\.'
                 r'|\bnão [^.]{0,40}, (?:e sim|mas sim)\b'
                 r'|\b\w+ é \w+, não \w+[.:;]')                        # "Pergunta é dúvida, não confirmação"
AFOR = re.compile(r'^\w+ é [oa] \w+ d[eoa]s? \w+\.$|\b(?:tem nome|a linguagem d[ao]|a moeda d[ao])\b')  # só frase curta inteira

THROAT = re.compile(r'\b(?:[Hh]á (?:uma|um) (?:razão|motivo)|[Vv]ale (?:notar|dizer|lembrar)|'
                    r'[ÉéEe] importante (?:notar|dizer|lembrar)|[Oo] (?:ponto|fato) é que|'
                    r'[Oo] que (?:chama|salta)|[Oo] (?:primeiro|segundo|terceiro|último) '
                    r'(?:traço|ponto|elemento|aspecto)|[Vv]ai mais longe|[Nn]ão para por aí)\b')
JUIZO  = re.compile(r'\b[oa] mais (?:incômod[oa]|interessante|curios[oa]|impressionante|'
                    r'surpreendente|grave|inquietante)\b|\b(?:notável|impressionante|'
                    r'justamente|precisamente) \w+')
TRES   = re.compile(r'(?<![,;])\b(\w[\w\sáéíóúâêôãõç]{2,40}), (\w[\w\sáéíóúâêôãõç]{2,40}) e '
                    r'(\w[\w\sáéíóúâêôãõç]{2,40})[.;,]')

def words(s): return len(re.findall(r"\w+(?:['-]\w+)?", s))

total, rows = 0, []
for i, p in enumerate(paras, 1):
    sents = [s.strip() for s in SENT.split(p) if s.strip()]
    hits = []
    frags = [s for s in sents if words(s) <= 4]
    if frags: hits.append(f'fragmento×{len(frags)}: ' + ' | '.join(frags))
    if len(sents) >= 2 and words(sents[-1]) <= CURTA: hits.append(f'kicker: "{sents[-1]}"')
    run = 0
    for s in sents:
        run = run + 1 if words(s) <= CURTA else 0
        if run == 3: hits.append('tricolon de frases curtas'); break
    for m in NEG.finditer(p): hits.append(f'contraste negado: "{m.group(0).strip()}"')
    for s_ in sents:
        if words(s_) <= CURTA + 1 and AFOR.search(s_): hits.append(f'aforismo: "{s_}"')
    for m in THROAT.finditer(p): hits.append(f'setup: "{m.group(0).strip()}"')
    for m in JUIZO.finditer(p):  hits.append(f'juízo do autor: "{m.group(0).strip()}"')
    tres = TRES.findall(p)
    if tres: hits.append(f'regra de três×{len(tres)}: ' + ' | '.join(', '.join(t)[:60] for t in tres[:2]))
    if '—' in p or ' – ' in p: hits.append('travessão')
    total += len(hits)
    for h in hits: rows.append(f'§{i:02d}  {h}')

print('\n'.join(rows) or '(nenhum tell)')
print(f'\n{total} tells em {len(paras)} parágrafos · {sum(words(p) for p in paras)} palavras · teto {mx}')
sys.exit(1 if total > mx else 0)
