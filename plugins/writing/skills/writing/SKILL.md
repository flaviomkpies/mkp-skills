---
name: writing
description: "Skill mae para escrita: newsletter, posts curtos (LinkedIn/X/Threads), longform (ensaio/capitulo/whitepaper), humanizer de texto, fact-check de afirmacoes e edicao do DNA de voz. Use para qualquer tarefa de escrita autoral."
argument-hint: "[newsletter|post|longform|fact-check|humanize|dna] [sub-args]"
allowed-tools: Read, Glob, Grep, Edit, Write, Bash, WebFetch, WebSearch, AskUserQuestion
---

# Writing — skill mãe para tarefas de escrita

Roteia para sub-modos especializados. Cada modo tem seu próprio arquivo em `modes/` e pode invocar `primitives/` compartilhadas (humanizer patterns, fact-check protocol, DNA checklist, voice calibration).

## Princípio central

**Você escreve, a AI assiste.** A voz é sua. O papel da AI é organizar, pesquisar, checar, cortar, comprimir e aplicar DNA — nunca substituir o autor.

> "Writing generates ideas, not just communicates them." — Paul Graham

## Modos disponíveis

Use `/writing <modo> [sub-args]`. Sem args, este help é exibido.

| Modo | Quando usar | Sub-comandos |
|------|-------------|--------------|
| `newsletter` | Artigo de newsletter | `outline` - `draft` - `polish` |
| `post` | Posts curtos (LinkedIn / Twitter / Threads) | `linkedin` · `twitter` · `threads` |
| `longform` | Texto longo (ensaio, capítulo, whitepaper) | `ensaio` · `capitulo` · `whitepaper` |
| `fact-check` | Verificar afirmações / quotes antes de publicar (single-claim) ou documento inteiro multi-round (`iterative`) | `<claim>` · `iterative <arquivo>` |
| `humanize` | Remover marcas de AI de texto qualquer | `<arquivo>` |
| `dna` | Mostrar ou editar DNA de voz | `show` · `edit` |

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

A voz do autor é única e inviolável. O `DNA.md` raiz desta skill é a fonte canônica para todo modo. Cada modo pode ter ajustes específicos (ex: vocabulário proibido da newsletter, tom mais informal de Twitter), mas o núcleo da voz vem do DNA central.

Ler `DNA.md` antes de qualquer prosa. Os modos chamam DNA + checklist + humanizer pass na ordem prescrita.

## CORRECOES.md — o log de calibração

`CORRECOES.md` (raiz desta skill) guarda os **anti-patterns colhidos comparando o texto que o
agente entregou com o que o autor de fato enviou**. O DNA é a voz canônica e recebe a regra
promovida; o CORRECOES guarda a ocorrência literal (antes→depois, data, caso), que é o que faz a
regra ser aplicável. Ler as famílias A (postura comercial) e C (estrutura executiva) **antes** de
escrever qualquer documento que sai com o nome do autor para terceiros. Alimentado por
uma rotina de after-action; promoção ao DNA quando um padrão chega a 3 rodadas.

## Primitives compartilhadas

Os modos usam blocos compartilhados em `primitives/`:
- `humanizer-patterns.md` — 39 padrões AI a remover (24 Wikipedia + tells 2026 + sync blader v2.11 em 05/09/2026)
- `../scripts/tells_pt.py` — **gate determinístico** de frase de coach (fragmento · "não é X, é Y" · kicker · tricolon · aforismo · travessão); roda antes do humanizer pass, exit 1 acima do teto
- `fact-check-protocol.md` — template canônico para spawn Haiku + WebFetch
- `dna-checklist.md` — checklist aplicável após cada draft
- `voice-calibration.md` — como ler posts publicados para calibrar voz

