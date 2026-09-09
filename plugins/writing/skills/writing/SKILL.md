---
name: writing
description: "Skill mãe para escrita: newsletter Substack, posts curtos (LinkedIn/Twitter/Threads), longform (ensaio/capítulo/whitepaper), humanizer de texto, fact-check de afirmações, e edição do DNA de voz. Use para qualquer tarefa de escrita que não seja resumir artigo (use /summarize-article) ou publicar (use /substack)."
category: conteudo-editorial
argument-hint: "[newsletter|post|longform|fact-check|humanize|dna] [sub-args]"
allowed-tools: Read Glob Grep Edit Write Bash WebFetch WebSearch Agent AskUserQuestion
---

# Writing — skill mãe para tarefas de escrita

Roteia para sub-modos especializados. Cada modo tem seu próprio arquivo em `modes/` e pode invocar `primitives/` compartilhadas (humanizer patterns, fact-check protocol, DNA checklist, voice calibration).

## Princípio central

**Flavio escreve, AI assiste.** A voz é do Flavio. O papel da AI é organizar, pesquisar, checar, cortar, comprimir e aplicar DNA — nunca substituir o autor.

> "Writing generates ideas, not just communicates them." — Paul Graham

## Modos disponíveis

Use `/writing <modo> [sub-args]`. Sem args, este help é exibido.

| Modo | Quando usar | Sub-comandos |
|------|-------------|--------------|
| `newsletter` | "Newsletter do Flavio: IA na prática" (Substack). Artigo novo → skill `/newsletter-post`; este modo = acervo de voz (DNA/spines/gate) + fluxo manual legado | `outline` · `draft` · `polish` · `publish` · `suggest` |
| `post` | Posts curtos (LinkedIn / Twitter / Threads) | `linkedin` · `twitter` · `threads` |
| `longform` | Texto longo (ensaio, capítulo, whitepaper) | `ensaio` · `capitulo` · `whitepaper` |
| `fact-check` | Verificar afirmações / quotes antes de publicar (single-claim) ou documento inteiro multi-round (`iterative`) | `<claim>` · `iterative <arquivo>` |
| `humanize` | Remover marcas de AI de texto qualquer | `<arquivo>` |
| `dna` | Mostrar ou editar DNA de voz | `show` · `edit` |

**Não está aqui (skills irmãs):**
- `/summarize-article` — converter artigo em PDF reMarkable de 7 páginas
- `/substack` — publicação via browser automation no Substack
- `/typst-pdf` — geração de PDF (infraestrutura, chamada por outras skills)

Detalhes em `references/related-skills.md`.

## Roteamento

Ao receber `/writing <modo> [args]`, ler o arquivo correspondente em `modes/<modo>.md` e seguir o procedimento descrito.

- `/writing` (sem args) → mostra esta lista de modos.
- `/writing newsletter [sub]` → `modes/newsletter.md`. Sub-comandos resolvidos lá dentro.
- `/writing post [sub]` → `modes/post.md`.
- `/writing longform [sub]` → `modes/longform.md`.
- `/writing fact-check <claim>` → `modes/fact-check.md`.
- `/writing humanize <arquivo>` → `modes/humanize.md`.
- `/writing dna [show|edit]` → `modes/dna.md`.

## DNA de voz

A voz do Flavio é única e inviolável. O `DNA.md` raiz desta skill é a fonte canônica para todo modo. Cada modo pode ter ajustes específicos (ex: vocabulário proibido da newsletter, tom mais informal de Twitter), mas o núcleo da voz vem do DNA central.

Ler `DNA.md` antes de qualquer prosa. Os modos chamam DNA + checklist + humanizer pass na ordem prescrita.

## CORRECOES.md — o log de calibração

`CORRECOES.md` (raiz desta skill) guarda os **anti-patterns colhidos comparando o texto que o
agente entregou com o que o Flavio de fato enviou**. O DNA é a voz canônica e recebe a regra
promovida; o CORRECOES guarda a ocorrência literal (antes→depois, data, caso), que é o que faz a
regra ser aplicável. Ler as famílias A (postura comercial) e C (estrutura executiva) **antes** de
escrever qualquer documento que sai com o nome do Flavio para terceiros. Alimentado por
`/desdobrar §5-bis`; promoção ao DNA quando um padrão chega a 3 rodadas.

## Primitives compartilhadas

Os modos usam blocos compartilhados em `primitives/`:
- `humanizer-patterns.md` — 39 padrões AI a remover (24 Wikipedia + tells 2026 + sync blader v2.11 em 05/09/2026)
- `../scripts/tells_pt.py` — **gate determinístico** de frase de coach (fragmento · "não é X, é Y" · kicker · tricolon · aforismo · travessão); roda antes do humanizer pass, exit 1 acima do teto
- `fact-check-protocol.md` — template canônico para spawn Haiku + WebFetch
- `dna-checklist.md` — checklist aplicável após cada draft
- `voice-calibration.md` — como ler posts publicados para calibrar voz

## Como esta skill se relaciona com agentes

- **Birdperson (researcher)** — owner de research e conteúdo de longform / newsletter / fact-check.
- **Meeseeks (executor)** — chamado quando há pipeline Sprint Ops (PM→PO→Meeseeks→QA) para um post específico.
- **Janitor (Obsidian)** — handoff: valida frontmatter e tags depois que um post vira published.

A skill é a ferramenta. O agente decide quando e como usar.
