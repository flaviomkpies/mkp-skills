# Related skills — skills irmãs de `/writing`

Skills que fazem parte da família "produção de conteúdo" mas estão fora de `/writing` por design.

## `/summarize-article`

**O que faz:** converte qualquer artigo (URL, PDF local, texto) em PDF de 7 páginas no formato reMarkable. Fan-out 3 canais: Email + Obsidian + reMarkable.

**Por que está fora de `/writing`:** o output é summary determinístico de input externo, não criação editorial do Flavio. Workflow distinto.

**Quando usar:** Flavio salvou artigo no Reader / recebeu PDF longo / quer ler em deepwork mode.

## `/substack`

**O que faz:** publicação browser automation no Substack a partir de um `.md` aprovado. Cria rascunho ou publica direto. Cookies salvos em `secrets/substack_cookies.json`.

**Por que está fora de `/writing`:** publicação é canal/delivery, não writing. Receber input já pronto e empurrar para o Substack é uma operação mecânica.

**Quando usar:** depois de `/writing newsletter publish` aprovar o draft. `/writing newsletter publish` chama `/substack` por baixo (no procedimento de etapa 6 do `modes/newsletter.md`).

## `/typst-pdf`

**O que faz:** geração de PDF para reMarkable usando Typst. P&B, A4, fonte DejaVu Sans. Usado por outras skills que precisam gerar PDF (relatórios, briefings, deepwork).

**Por que está fora de `/writing`:** infraestrutura, não writing. É chamado por `/summarize-article`, `/sprint-ops`, `/system-report` etc.

**Quando usar:** quando outra skill precisa gerar PDF. Raramente invocado direto pelo Flavio.

## `/remarkable`

**O que faz:** envia PDF para o reMarkable 2 do Flavio via rmapi. Fallback: copy via OneDrive.

**Por que está fora de `/writing`:** delivery, não writing. Empurra arquivo pronto.

**Quando usar:** depois que `/typst-pdf` gerou o PDF. Geralmente encadeada (skill A gera PDF → `/typst-pdf` → `/remarkable`).

## Diagrama de relação

```
Writing (criar texto)              Publishing (entregar)
─────────────────────              ──────────────────────
/writing newsletter ──────────►    /substack
/writing post                      (LinkedIn / Twitter manual)
/writing longform                  (canal varia)

Sumarização                        Infraestrutura (suporte)
────────────                       ────────────
/summarize-article ──────────►     /typst-pdf
                                   /remarkable
```

## Quando promover de "writing" para "publishing"

Em `modes/newsletter.md`, a etapa 6 (publish) chama `/substack`. Esse é o ponto de transição: o `.md` deixa de ser objeto editável e vira artefato a ser publicado.

Princípio: `/writing` para de mexer no texto na hora de publicar. `/substack` (ou outro canal) opera com texto fechado.

## Skills DELETADAS (histórico de migração ENG-216)

- ❌ `/newsletter` — conteúdo migrado para `modes/newsletter.md`. 
- ❌ `/humanizer` — conteúdo migrado para `modes/humanize.md` + `primitives/humanizer-patterns.md`. 

Backup das skills antigas em `/tmp/skills_backup_<timestamp>/` (transitório). Ver issue ENG-216 para histórico completo.
