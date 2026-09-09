# Mode: longform

> Modo invocado por `/writing longform [ensaio|capitulo|whitepaper]`.
> Skill mãe: `/writing` (ver `SKILL.md` raiz).

Texto longo onde a estrutura importa tanto quanto cada frase. Diferente de newsletter (semanal, foco em uma ideia) e post (curto, denso). Tamanho típico: 3.000–30.000 palavras.

## Sub-comandos

- `/writing longform ensaio` — peça única, argumento desenvolvido. Ex: ensaio Substack longo, peça pra LinkedIn Pulse, artigo blog.
- `/writing longform capitulo` — capítulo de livro ou parte de obra maior. Tem dependência de capítulos vizinhos.
- `/writing longform whitepaper` — peça técnica/executiva com objetivo declarado. Estrutura formal: problema → análise → recomendação.

## Princípios comuns

- **DNA central** vale com ressalvas: longform pode aceitar parágrafos um pouco mais densos (até 7 frases) onde a ideia exige.
- **Outline antes de prosa.** Em longform, NÃO começar pela prosa. Outline em árvore (3 níveis: seção → subseção → bullet) e iterar até Flavio aprovar.
- **Research é parte do trabalho.** Longform sempre exige fact-check (`/writing fact-check`) e research em fontes primárias antes de bater o draft.
- **Iteração de draft em rodadas:** Draft A (estrutural — testar argumento), Draft B (preencher gaps), Draft C (polish + DNA + humanize).

## Procedimento (ensaio)

1. **Tese central em 1 frase** — sem isso, não começa.
2. **3-5 movimentos do argumento** — cada movimento é uma seção. Cada seção é independentemente defensável.
3. **Outline em árvore** — sub-bullets dentro de cada movimento. Iterar com Flavio até aprovar.
4. **Research por movimento** — fontes primárias. Marcar `[FONTE: ...]` no outline.
5. **Draft A** — prosa estrutural. Foco: o argumento aguenta? Sem polish.
6. **Crítica analítica** (auto-review): forças e fragilidades de cada movimento.
7. **Draft B** — endereçar fragilidades, preencher gaps de research.
8. **Draft C** — polish: DNA pass + humanize pass + revisão didática.
9. **Fact-check final** — toda quote, todo número, toda atribuição.
10. **Publish** — direto via canal apropriado (Substack longo, LinkedIn Pulse, blog).

## Procedimento (capítulo)

Igual ao ensaio, mais:
- **Mapa do livro** — capítulo precisa caber na obra. Antes de outline, revisar capítulos vizinhos para coerência de tese, vocabulário, exemplos.
- **Glossário** — palavras-chave que o livro usa de forma específica. Capítulo respeita.
- **Cross-refs** — apontar para outros capítulos onde apropriado, sem repetir conteúdo.

## Procedimento (whitepaper)

Estrutura formal obrigatória:
1. **Sumário executivo** (1 página máximo).
2. **Contexto / problema** — por que esse paper existe agora.
3. **Análise** — fatos, dados, modelo conceitual.
4. **Opções** — 3 alternativas comparadas.
5. **Recomendação** — qual opção, por quê.
6. **Implementação** — quem faz, quando, como medir.
7. **Anexos** — fontes, dados brutos, casos relacionados.

Tom mais formal que ensaio, mas a voz do Flavio continua valendo (DNA central). Sem jargão consultivo padrão.

## Anti-patterns

- ❌ Começar pela prosa antes do outline aprovado — vira rabbit hole de reescrita.
- ❌ "Vou pesquisar enquanto escrevo" — research e prosa em rodadas separadas. Confunde os dois e a qualidade despenca.
- ❌ Citações sem fact-check — em longform, uma quote falsa derruba o paper inteiro.
- ❌ "Conclusão" genérica que repete o sumário — fechamento de longform é onde o argumento pousa, não onde se resume.
- ❌ Listas longas em prosa corrida — listas operacionais OK, mas longform pede argumentação, não tutorial.

## Output esperado

Estrutura sugerida no vault:
- `Efforts/Writings/Longform/<projeto>/<data>-<slug>.md`
- Versionamento inline (Outline V1 → V2 → V3 aprovado; Draft A → B → C final) seguindo o mesmo padrão de `modes/newsletter.md`.

Frontmatter:
```yaml
---
Date: YYYY-MM-DD
type: ensaio | capitulo | whitepaper
status: outlining | drafting | polishing | ready | published
projeto: <nome do livro/série/projeto>
canal: <substack-longo | linkedin-pulse | blog | livro | pdf>
research: '[[link pra arquivo de research]]'
fact-check: <data do último fact-check>
---
```

## Quando escalar

- Longform com >10.000 palavras → considerar quebrar em ensaios encadeados (newsletter série).
- Whitepaper com decisão executiva pesada → escalar para Birdperson + revisão humana adicional antes de publicar.
- Capítulo de livro → coordenar com editor / revisor humano se houver.
