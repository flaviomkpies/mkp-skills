#!/usr/bin/env python3
"""Olha a maquina de quem instalou e devolve um rascunho de perfil, em markdown.

So leitura: lista, nunca escreve nem move nada. O que ele nao descobrir sozinho vira uma
pergunta no fim do relatorio, para quem esta adaptando responder.

Uso:
    python3 detectar_ambiente.py            # varre o HOME
    python3 detectar_ambiente.py ~/work     # varre outra raiz
"""
import json
import os
import pathlib
import platform
import shutil
import subprocess
import sys

IGNORAR = {".git", "node_modules", ".venv", "venv", "__pycache__", ".cache", "Library",
           ".Trash", ".local", ".npm", ".cargo", "AppData", ".rustup", "site-packages"}
FUNDO = 4  # profundidade maxima da varredura: mais que isso demora e nao acrescenta


def caminhar(raiz, fundo=FUNDO):
    raiz = pathlib.Path(raiz).expanduser()
    base = len(raiz.parts)
    for dirpath, dirnames, filenames in os.walk(raiz, topdown=True):
        p = pathlib.Path(dirpath)
        if len(p.parts) - base >= fundo:
            dirnames[:] = []
        dirnames[:] = [d for d in dirnames if d not in IGNORAR and not d.startswith(".")
                       or d in (".obsidian", ".claude")]
        yield p, dirnames, filenames


def achar(raiz):
    repos, vaults, claude, notas = [], [], [], []
    for p, dirs, files in caminhar(raiz):
        if ".git" in dirs or (p / ".git").exists():
            repos.append(p)
            dirs[:] = [d for d in dirs if d != ".git"]
        if ".obsidian" in dirs:
            vaults.append(p)
        if ".claude" in dirs and p != pathlib.Path.home():
            claude.append(p / ".claude")
        if p.name.lower() in ("notes", "notas", "zettelkasten", "second brain", "wiki"):
            notas.append(p)
    return repos, vaults, claude, notas


def contar_md(d, teto=4000):
    n = 0
    for _, _, files in os.walk(d):
        n += sum(1 for f in files if f.endswith(".md"))
        if n > teto:
            return f"{teto}+"
    return n


def ferramentas():
    out = {}
    for t in ("git", "gh", "python3", "pandoc", "rclone", "rg", "jq", "code", "obsidian",
              "pdfinfo", "tesseract", "libreoffice", "soffice"):
        c = shutil.which(t)
        if c:
            out[t] = c
    return out


def harness():
    """O que ja existe na config do Claude Code de quem instalou."""
    h = pathlib.Path.home() / ".claude"
    info = {"dir": str(h) if h.exists() else None}
    if not h.exists():
        return info
    info["CLAUDE.md"] = (h / "CLAUDE.md").exists()
    info["skills"] = sorted(d.name for d in (h / "skills").glob("*") if d.is_dir()) if (h / "skills").is_dir() else []
    info["commands"] = len(list((h / "commands").glob("*.md"))) if (h / "commands").is_dir() else 0
    st = h / "settings.json"
    if st.exists():
        try:
            d = json.loads(st.read_text(encoding="utf-8"))
            info["hooks"] = sorted(d.get("hooks", {}).keys())
        except (json.JSONDecodeError, OSError):
            info["hooks"] = "settings.json ilegivel"
    return info


def git_id(repo):
    def g(*a):
        try:
            return subprocess.run(["git", "-C", str(repo), *a], capture_output=True,
                                  text=True, timeout=10).stdout.strip()
        except (subprocess.SubprocessError, OSError):
            return ""
    return g("config", "--get", "remote.origin.url"), g("rev-parse", "--abbrev-ref", "HEAD")


def main():
    raiz = sys.argv[1] if len(sys.argv) > 1 else str(pathlib.Path.home())
    repos, vaults, claude, notas = achar(raiz)

    print(f"# Rascunho de perfil — {platform.system()} {platform.release()}")
    print(f"\nVarrido: `{raiz}` (profundidade {FUNDO})\n")

    print("## Repositorios git\n")
    if repos:
        for r in sorted(repos)[:12]:
            url, br = git_id(r)
            print(f"- `{r}` — branch `{br or '?'}`{('  ·  ' + url) if url else ''}")
        if len(repos) > 12:
            print(f"- … e mais {len(repos) - 12}")
    else:
        print("- nenhum encontrado")

    print("\n## Vaults Obsidian\n")
    for v in sorted(vaults) or []:
        print(f"- `{v}` — {contar_md(v)} notas .md")
    if not vaults:
        print("- nenhum encontrado")
        if notas:
            print("\n  Pastas que parecem ser de notas, sem Obsidian:")
            for n in sorted(notas)[:5]:
                print(f"  - `{n}` — {contar_md(n)} .md")

    print("\n## Claude Code\n")
    h = harness()
    if not h["dir"]:
        print("- `~/.claude` nao existe")
    else:
        print(f"- config em `{h['dir']}`")
        print(f"- CLAUDE.md proprio: {'sim' if h.get('CLAUDE.md') else 'nao'}")
        print(f"- skills instaladas: {', '.join(h['skills']) if h.get('skills') else 'nenhuma'}")
        print(f"- slash commands: {h.get('commands', 0)}")
        print(f"- hooks configurados: {', '.join(h['hooks']) if h.get('hooks') else 'nenhum'}")
    if claude:
        print(f"- configs por projeto: {', '.join(str(c) for c in sorted(claude)[:6])}")

    print("\n## Ferramentas no PATH\n")
    f = ferramentas()
    print("- " + ", ".join(f"`{k}`" for k in f) if f else "- nenhuma das procuradas")

    print("""
## O que a maquina nao conta — responda antes de escrever o perfil

1. **Onde mora o registro de uma sessao de trabalho?** (pasta por data, issue, nada ainda)
2. **Onde mora uma regra que vale para sempre?** (CLAUDE.md, doc do repo, nada ainda)
3. **Onde mora um aprendizado pontual?** (memoria do Claude, arquivo de notas, nada)
4. **Qual e o seu gerenciador de trabalho?** (Linear, Jira, GitHub Issues, Todoist, nenhum)
5. **O que nunca pode ser feito sem voce aprovar?** (fechar tarefa, mandar e-mail, commitar, publicar)
6. **Como se escreve no seu vault com seguranca?** (app aberto, arquivo direto, sync que atrapalha)
7. **Entregavel versionado: sobrescreve ou vira _vN+1?**
8. **Quem mais mexe nos mesmos arquivos?** (so voce, um time, outros agentes)
""")
    return 0


if __name__ == "__main__":
    sys.exit(main())
