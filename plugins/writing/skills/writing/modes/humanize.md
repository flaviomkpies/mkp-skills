# Mode: humanize

> Modo invocado por `/writing humanize <arquivo>`.
> Skill mãe: `/writing` (ver `SKILL.md` raiz).

Remove sinais de "AI writing" de um texto qualquer, fazendo soar mais natural e humano. Usa os 24 patterns canônicos em `../primitives/humanizer-patterns.md`.

## Quando usar

- Você tem um texto pronto (qualquer tipo) e suspeita que tem marcas de AI.
- Você acabou de escrever um draft com ajuda de LLM e quer um pass de revisão.
- Você está revisando texto de terceiros que parece artificial.

Para newsletter, usar via `/writing newsletter polish` (que chama humanize internamente como etapa 4b). Para outros casos, este modo standalone.

## Procedimento

1. **Ler o arquivo de input.**
2. **Carregar os 24 patterns canônicos** de `../primitives/humanizer-patterns.md`.
3. **Scan obrigatório (ordem de impacto):**
   - Anti-atribuição AI (ver DNA central): toda expressão sem origem rastreável → `[SUGESTÃO AI]`.
   - Em-dash overuse (—) → manter só onde é pausa dramática real.
   - Fragments sem verbo principal → corrigir.
   - Concordância em orações compostas.
   - Aspas que abrem e não fecham.
   - Em-dash overuse, rule of three, negative parallelisms.
   - AI vocabulary (delve, crucial, landscape, tapestry, underscore, pivotal, testament, foster, intricate).
   - Promotional (vibrant, seamless, robust, groundbreaking, profound).
   - Copula avoidance (serves as, stands as, represents).
   - -ing endings superficiais.
   - Elegant variation (sinônimos ciclados sem motivo).
   - Hedging excessivo.
4. **Adicionar voz** — não apenas remover patterns, mas injetar opinião e personalidade onde for natural. Ver seção "PERSONALITY AND SOUL" em `../primitives/humanizer-patterns.md`.
5. **Output** — diff explicado com motivo por linha alterada. Edits cirúrgicos, nunca reescrever parágrafo inteiro. Se um parágrafo pede reescrita completa, sinalizar — não reescrever sem aprovação.

## Regras invioláveis

- Preservar significado central.
- Manter tom intencional do autor (formal / casual / técnico).
- Não inflar com novo conteúdo — humanizer corta e ajusta, não adiciona ideias.
- Não remover voz do autor confundindo com pattern AI. Quando houver dúvida, marcar como sugestão e perguntar.

## Output esperado

Arquivo editado (ou diff) + nota explicativa por classe de mudança:
- "X em-dashes removidos (mantidos Y como pausa dramática)"
- "Z palavras de AI vocabulary substituídas"
- "W frases reescritas para incluir verbo principal"
- "Concordâncias corrigidas"

Sem inventar — só os patterns que de fato encontrou.
