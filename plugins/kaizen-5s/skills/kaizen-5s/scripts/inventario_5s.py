#!/usr/bin/env python3
"""
kaizen-5s — inventário (só leitura) de uma pasta para a fase Seiri.
Uso: python3 inventario_5s.py <pasta> [--md]
Lista: .md sem frontmatter · sem proveniência · sem tag de eixo (class/ wf/) · com hard wrap ·
stubs sem link · famílias _vN · prefixo ERRADO · caches e temporários · pastas sem cabeça.
Não escreve nada. Ignora pastas com ponto. ponytail: heurísticas simples, o veredito é da leitura.
"""
import os, re, sys, json, statistics
raiz = sys.argv[1]; md = "--md" in sys.argv
FM = re.compile(r"^---\n(.*?)\n---", re.S)
EIXO = re.compile(r"\b(class|wf)/[\w-]+")
LINK = re.compile(r"\[\[[^\]]+\]\]")
rel = {k: [] for k in ("sem_frontmatter", "sem_provenance", "sem_eixo", "hard_wrap", "stub_sem_link", "familia_vN", "errado", "cache_tmp", "pasta_sem_cabeca", "duplicata_md5", "solto_na_raiz")}
import hashlib
hashes = {}
recebidos = {}   # alvo de wikilink -> contagem (mede função)
notas = []
for d, subs, files in os.walk(raiz):
    subs[:] = [s for s in subs if not s.startswith(".")]
    nomes = set(files)
    if files and not any(f == "_LEIA-ME.md" or (f.startswith("_") and f.endswith(".md")) for f in files):
        rel["pasta_sem_cabeca"].append(os.path.relpath(d, raiz) or ".")
    for f in files:
        p = os.path.join(d, f); r = os.path.relpath(p, raiz)
        low = f.lower()
        if d == raiz and low.endswith((".md", ".pdf", ".html", ".docx", ".txt")) and not f.startswith("_") and not f.startswith("00_"): rel["solto_na_raiz"].append(r)
        try:
            if os.path.getsize(p) > 512:
                h = hashlib.md5(open(p, "rb").read()).hexdigest(); hashes.setdefault(h, []).append(r)
        except Exception: pass
        if low.startswith("errado"): rel["errado"].append(r)
        if re.search(r"idx_cache.*\.json$|\.tmp$|^~\$|\.bak$|\.orig$", low): rel["cache_tmp"].append(r)
        m = re.match(r"^(.*)_v(\d+)(\.\w+)$", f)
        if m: rel["familia_vN"].append((os.path.join(os.path.relpath(d, raiz), m.group(1) + m.group(3)), int(m.group(2)), r))
        if low.endswith(".md"):
            try: t = open(p, encoding="utf-8", errors="replace").read()
            except Exception: continue
            fm = FM.match(t); corpo = t[fm.end():] if fm else t
            for l in LINK.findall(t): recebidos[l.strip("[]").split("|")[0].split("#")[0]] = recebidos.get(l.strip("[]").split("|")[0].split("#")[0], 0) + 1
            if not fm: rel["sem_frontmatter"].append(r); continue
            head = fm.group(1)
            if not re.search(r"^provenance:", head, re.M): rel["sem_provenance"].append(r)
            if not EIXO.search(head): rel["sem_eixo"].append(r)
            prosa = re.sub(r"```.*?```", "", corpo, flags=re.S)
            linhas = [l for l in prosa.split("\n") if len(l.strip()) > 40 and not l.lstrip().startswith(("|", "#", "-", ">", "*"))]
            if len(linhas) >= 8 and statistics.median(len(l) for l in linhas) <= 100 and sum(1 for l in linhas if 60 <= len(l) <= 100) / len(linhas) > 0.7:
                rel["hard_wrap"].append(r)
            notas.append((r, os.path.splitext(f)[0], len(re.sub(r"\s+", " ", prosa).strip())))
for r, nome, n in notas:
    if n < 300 and recebidos.get(nome, 0) < 2: rel["stub_sem_link"].append(r)
rel["duplicata_md5"] = [sorted(v) for v in hashes.values() if len(v) > 1]
fam = {}
for base, v, r in rel["familia_vN"]: fam.setdefault(base, []).append((v, r))
rel["familia_vN"] = [{"base": b, "versoes": sorted(vs)} for b, vs in fam.items() if len(vs) > 1]
if md:
    print(f"# Inventário 5S — {raiz}\n")
    for k, v in rel.items():
        print(f"## {k} ({len(v)})")
        for x in v[:40]: print(f"- {x}")
        if len(v) > 40: print(f"- … +{len(v)-40}")
        print()
else:
    print(json.dumps({k: (v if len(v) <= 200 else v[:200] + [f"+{len(v)-200}"]) for k, v in rel.items()}, ensure_ascii=False, indent=1))
