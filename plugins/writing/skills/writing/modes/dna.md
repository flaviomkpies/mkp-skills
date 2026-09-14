# Mode: dna

> Modo invocado por `/writing dna [show|edit]`.
> Skill mãe: `/writing` (ver `SKILL.md` raiz).

Edita explicitamente o DNA de voz. Em vez de mudar `DNA.md` na mão (e arriscar inconsistência), use este modo: ele garante que o DNA seja modificado com justificativa rastreável e, quando aplicável, propaga ajustes para os modos.

## Sub-comandos

- `/writing dna show` — mostra o DNA atual com origem de cada regra (quando entrou, por quê).
- `/writing dna edit` — modo guiado de adição, modificação ou remoção de regra.

## Procedimento (show)

1. Ler `../DNA.md` raiz.
2. Ler também `modes/newsletter.md` para regras específicas de newsletter (vocabulário proibido, narrative spines).
3. Apresentar de forma organizada:
   - Voz / Estrutura / Linguagem / Proibições absolutas / Referências de estilo (DNA central).
   - Vocabulário proibido / Narrative spines (newsletter-específico).
4. Ao lado de cada regra inviolável recente, mostrar a fonte (ex: "deployed 2026-04-21, <issue>").

## Procedimento (edit)

1. **AskUserQuestion** sobre tipo de mudança:
   - **Adicionar nova regra** — o autor descreve. Perguntar: o que motivou (incidente, padrão recorrente, leitura externa)? É genérica (DNA central) ou específica de um modo (ex: só newsletter)?
   - **Modificar regra existente** — o autor aponta qual. Perguntar: o que mudou de contexto? A regra antiga continua válida em outro escopo?
   - **Remover regra** — o autor aponta qual. Perguntar: por quê? Há registro do motivo original?
2. **Aplicar a mudança** com ressalvas:
   - Adicionar **comentário de origem** (quando entrou, por quê) próximo à regra. Não mexer nas regras vizinhas sem motivo.
   - Se a mudança afeta múltiplos modos, atualizar todos consistentemente.
3. **Sumário da mudança** — produzir um diff curto da edição para o autor aprovar antes de salvar.
4. **Salvar.** Atualizar `DNA.md` (ou modo específico) com timestamp.
5. **Memory:** se a mudança veio de incidente recorrente (3+ correções iguais), salvar em memory persistente do agente para referência futura.

## Critérios de promoção (quando uma correção vira regra)

Hoje, regras entram no DNA quando:
- Padrão de correção do autor repete **3 vezes** em posts diferentes.
- Incidente único MAS de impacto editorial alto (atribuição errada, fact-check furado).
- Aprendizado externo (livro, post de Paul Graham/Naval/Mollick) que o autor quer adotar.

Critério rigoroso. DNA com 100 regras = ninguém lê. DNA com 30 regras testadas = funciona.

## Anti-patterns

- ❌ Adicionar regra "porque parece boa ideia" sem incidente concreto.
- ❌ Especificar regra de modo num arquivo errado (ex: regra newsletter no DNA central).
- ❌ Remover regra sem registrar motivo (perde-se a história).
- ❌ Sobrescrever regra existente sem comparar contexto antigo vs novo.

## Output esperado

Para `show`: relatório formatado, no chat, com regras agrupadas por categoria + origem.

Para `edit`: arquivo `DNA.md` (ou mode específico) atualizado, diff visível em commit/Obsidian, log da mudança em memory persistente se aplicável.
