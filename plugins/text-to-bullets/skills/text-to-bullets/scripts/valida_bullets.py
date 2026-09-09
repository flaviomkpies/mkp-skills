# -*- coding: utf-8 -*-
"""valida_bullets — gate deterministico do /text-to-bullets.

Prova FIDELIDADE AO DOCUMENTO (nao verdade do documento):
  1. citacao do bullet existe na lista de referencias do texto-fonte
  2. numero em bullet EVIDE aparece no texto-fonte E PERTO da fonte citada
     (proximidade: o numero tem de estar na vizinhanca do sobrenome que o bullet atribui)
  3. campo `literal` bate caractere a caractere com o original
  4. AFIRMA/EVIDE tem fonte; DECISAO nao tem fonte externa; ACHADO tem artefato rastreavel

Uso: python3 valida_bullets.py <bullets.jsonl> --fonte <documento.md>
Exit 1 se houver qualquer falha.
"""
import json, re, sys, io, argparse, unicodedata

def norm(s):
    s = unicodedata.normalize("NFKD", (s or "")).encode("ascii", "ignore").decode().lower()
    return re.sub(r"\s+", " ", s)

def janelas_da_fonte(sobrenome, texto, raio=420):
    """Trechos do documento na vizinhanca de cada mencao ao sobrenome citado."""
    js = [texto[max(0, m.start()-raio): m.end()+raio]
          for m in re.finditer(re.escape(norm(sobrenome)), texto)]
    return js

def num_ocorre(n, texto):
    """Confere o numero como TOKEN, nao como substring: '47' nao pode casar dentro de
       '1478088706' nem de '147'. Percentual so casa com forma percentual."""
    pct = n.strip().endswith("%")
    base = n.replace("%", "").strip()
    variantes = {base, base.replace(".", ""), base.replace(",", ""),
                 base.replace(".", ","), base.replace(",", ".")}
    for v in {x for x in variantes if x}:
        e = re.escape(v)
        if pct:
            if re.search(r"(?<![\d.,])" + e + r"\s*(%|por cento|pontos percentuais|p\.p\.)", texto):
                return True
        else:
            if re.search(r"(?<![\d.,])" + e + r"(?![\d.,])", texto):
                return True
    return False

ap = argparse.ArgumentParser()
ap.add_argument("bullets"); ap.add_argument("--fonte", required=True)
ap.add_argument("--quiet", action="store_true")
a = ap.parse_args()

src = io.open(a.fonte, encoding="utf-8").read()
corpo, _, resto = src.partition("# REFERÊNCIAS")
if not resto: corpo, resto = src, src
lista, _, apend = resto.partition("# APÊNDICE")
corpo_n = norm(corpo + " " + apend)

NOME = r"(?:von |van |della |del )?[A-ZÁÉÍÓÚÂÊÔÃÕÇ][A-Za-zÀ-ÿ'’-]+"
PERMITIDAS = set()
for ln in [l.strip() for l in lista.split("\n") if l.strip()]:
    m = re.match(r"^(%s)[,.].*?\((\d{4})[a-z]?\)" % NOME, ln)
    if m: PERMITIDAS.add((norm(m.group(1)), m.group(2)))

falhas, n = [], 0
for linha in io.open(a.bullets, encoding="utf-8"):
    linha = linha.strip()
    if not linha: continue
    b = json.loads(linha); n += 1
    rot = f"[{b.get('secao','?')}] {b.get('texto','')[:58]}"
    tipo, fonte = b.get("tipo", ""), (b.get("fonte") or "").strip()

    if tipo in ("AFIRMA", "EVIDE") and not fonte:
        falhas.append(("sem fonte", rot))
    if tipo == "DECISAO" and fonte and "autor" not in norm(fonte):
        falhas.append(("DECISAO com fonte externa", rot))
    if tipo == "ACHADO":
        if "autor" not in norm(fonte) and "propri" not in norm(fonte):
            falhas.append(("ACHADO deve ser atribuido ao autor/propria pesquisa", rot))
        if not (b.get("local") or "").strip():
            falhas.append(("ACHADO sem artefato rastreavel em `local`", rot))

    if fonte and "autor" not in norm(fonte):
        m = re.match(r"^(%s).*?\(?(\d{4})" % NOME, fonte)
        if not m:
            falhas.append(("fonte sem autor+ano legivel", rot))
        elif (norm(m.group(1)), m.group(2)) not in PERMITIDAS:
            falhas.append((f"citacao fora da lista de referencias: {fonte}", rot))

    if tipo in ("EVIDE", "ACHADO"):
        if tipo == "EVIDE" and not (b.get("local") or "").strip():
            falhas.append(("EVIDE sem localizador", rot))
        sob = None
        if fonte and "autor" not in norm(fonte) and "propri" not in norm(fonte):
            mm = re.match(r"^(%s)" % NOME, fonte)
            sob = mm.group(1) if mm else None
        janelas = janelas_da_fonte(sob, corpo_n) if sob else None
        for num in re.findall(r"\d[\d.,]*%?", b.get("texto", "")):
            if len(num.strip(".,")) < 2: continue
            if not num_ocorre(num, corpo_n):
                falhas.append((f"numero '{num}' nao aparece no texto-fonte", rot))
            elif janelas is not None and not any(num_ocorre(num, j) for j in janelas):
                falhas.append((f"numero '{num}' existe no texto, mas longe de '{sob}' — "
                               f"atribuicao provavelmente trocada", rot))

    lit = (b.get("literal") or "").strip().strip('"“”')
    if lit and norm(lit) not in corpo_n:
        falhas.append(("quote nao confere com o original", rot))

if not a.quiet:
    print(f"bullets: {n} · referencias permitidas: {len(PERMITIDAS)} · falhas: {len(falhas)}")
    for motivo, rot in falhas: print(f"  [X] {motivo}\n      {rot}")
    if not falhas: print("  todos os bullets sao fieis ao documento.")
sys.exit(1 if falhas else 0)
