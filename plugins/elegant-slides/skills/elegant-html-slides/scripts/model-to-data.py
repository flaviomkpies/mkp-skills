#!/usr/bin/env python3
"""
Veredas OS — model-to-data (Excel → DATA: estende a fonte única ao modelo)

Purpose:     Lê o bloco de saída de um modelo Excel (aba DECK) e emite o objeto
             `const DATA = {...}` do deck data-driven — ou o injeta direto no deck
             entre os marcadores /* DATA:START */ e /* DATA:END */. Mata a transcrição
             manual modelo→deck e o gap deck↔Excel (deck e modelo viram UMA fonte).
Owner:       Flavio
Created:     2026-06-24
Last-edited: 2026-06-24 (via skill elegant-html-slides)
Issue:       fast-track
Lifetime:    durable
Inputs:      modelo.xlsx (aba DECK) · opcional deck.html (--update-deck)
Outputs:     stdout (bloco DATA) OU deck.html atualizado in-place
Cron:        manual (gerar/atualizar deck a partir do modelo)

Convenção da aba DECK (tidy): linha 1 = cabeçalho [key, ano1, ano2, …] (vira DATA.years).
Cada linha seguinte: <key> | <v1> | <v2> | … → array numérico; 1 valor de texto → escalar
(company, fonte). O modelo precisa estar salvo com valores calculados (data_only lê o cache).
Uso: python3 model-to-data.py modelo.xlsx [--sheet DECK] [--update-deck deck.html]
"""
import json, argparse, openpyxl

START = "/* DATA:START"
END = "/* DATA:END */"

def extract(path, sheet):
    wb = openpyxl.load_workbook(path, data_only=True)   # data_only: lê valor calculado, não a fórmula
    ws = wb[sheet] if sheet in wb.sheetnames else wb.active
    rows = [r for r in ws.iter_rows(values_only=True)]
    if not rows:
        raise SystemExit(f"aba '{ws.title}' vazia")
    header = rows[0]
    data = {"years": [str(c) for c in header[1:] if c not in (None, "")]}
    for r in rows[1:]:
        key = r[0]
        if key in (None, ""):
            continue
        key = str(key).strip()
        if key.lower() == "years":          # cabeçalho já definiu years
            continue
        vals = [c for c in r[1:] if c is not None and c != ""]
        if not vals:
            continue
        data[key] = vals[0] if (len(vals) == 1 and isinstance(vals[0], str)) else list(vals)
    return data

def to_js(data):
    body = "\n".join(f"  {k}: {json.dumps(v, ensure_ascii=False)}," for k, v in data.items())
    return "const DATA = {\n" + body + "\n};"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("model")
    ap.add_argument("--sheet", default="DECK")
    ap.add_argument("--update-deck", help="deck.html: substitui o bloco entre os marcadores DATA")
    a = ap.parse_args()
    js = to_js(extract(a.model, a.sheet))
    if not a.update_deck:
        print(js); return
    html = open(a.update_deck, encoding="utf-8").read()
    i, j = html.find(START), html.find(END)
    if i < 0 or j < 0:
        raise SystemExit("marcadores /* DATA:START */ … /* DATA:END */ não encontrados no deck")
    head = "/* DATA:START — gerado por model-to-data.py a partir do modelo; edite o MODELO, não aqui */\n"
    open(a.update_deck, "w", encoding="utf-8").write(html[:i] + head + js + "\n" + html[j:])
    n = len(extract(a.model, a.sheet)) - 1
    print(f"DATA atualizado em {a.update_deck} ({n} séries/escalares + years)")

if __name__ == "__main__":
    main()
