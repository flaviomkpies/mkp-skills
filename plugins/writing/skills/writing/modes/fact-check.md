# Mode: fact-check

> Modo invocado por `/writing fact-check <claim>` (single-claim), `/writing fact-check` (interativo), ou `/writing fact-check iterative <arquivo>` (multi-round em documento inteiro).
> Skill mãe: `/writing` (ver `SKILL.md` raiz).

Verifica afirmações antes de virarem texto público. **Dois sub-modos:**
- **Single-claim** (default): uma afirmação por vez, Haiku + WebFetch — uso original.
- **Iterative** (`iterative <arquivo>`): documento inteiro com ≥10 claims factuais, **Workflow multi-round com agentes paralelos**. Validado em entregas acadêmicas MPA (<issue> Supply Chain Di Serio, <issue> ESG).

## Quando usar (obrigatório)

- Antes de citar quote em post público — qualquer pessoa, qualquer fonte.
- Antes de afirmar fato que tem timestamp / data / atribuição.
- Antes de mencionar URL específica como referência.
- Antes de Draft B em qualquer modo de `/writing`.
- **Entrega acadêmica MPA — modo iterative obrigatório**: dissertação, ensaio individual, paper final de disciplina. Não-negociável (USER.md). Cf. `feedback_factcheck_multiround`.

**Regra inviolável:** se a afirmação está num post Substack ou LinkedIn, ela passa por fact-check antes de publish. Sem exceção.

## Procedimento

Carregar `../primitives/fact-check-protocol.md` para template canônico.

Pipeline:

1. **Receber claim(s)** — uma ou mais afirmações em texto livre, ou apontar arquivo com claims marcadas.
2. **Spawnar Haiku** com prompt do protocol (não inventar prompt — usar template).
3. **Haiku usa WebSearch + WebFetch** para verificar.
4. **Receber output estruturado:**
   - `[FATO]` + URL + trecho verbatim, OU
   - `[CORREÇÃO SUGERIDA]` + dado correto + fonte, OU
   - `[NÃO VERIFICÁVEL]` + razão (paywall, fonte primária inexistente, alucinação prévia).
5. **Reportar ao autor** com 3 níveis:
   - ✅ Verificado — pode usar literal.
   - ⚠️ Parcialmente verificado — usar com cuidado, ou reformular.
   - ❌ Não verificado — não publicar essa afirmação. Buscar alternativa ou tirar.

## Regras críticas

- **Não confiar em URL fabricada.** Se o agente não conseguiu fazer WebFetch real do conteúdo da página, é alucinação. Marcar `[NÃO VERIFICÁVEL]`.
- **Quote no blog ≠ quote em artigo de terceiros.** Se a frase aparece num artigo Medium, é o jornalista falando. Atribuir corretamente. Caso real: <issue>, frase atribuída ao Steinberger no início → era do artigo Global Times Singapore.
- **Confirmar a página existe E contém a frase.** WebSearch que retorna URL plausível não basta — precisa WebFetch + verificar trecho.
- **Limitar tokens do Haiku.** Spawn pequeno — máximo 250 palavras de resposta esperada. Se precisar de pesquisa ampla, escalar para Sonnet com um modelo mais capaz.

## Output canônico (formato esperado do Haiku)

```
[STATUS] — Verificado / Parcialmente / Não verificável

URL: <url se aplicável>
Trecho verbatim: "<5-10 linhas de contexto>"
Atribuição correta: <quem realmente disse — pessoa, jornalista, descrição editorial>
Data / evento: <quando, onde>

Notas: <ressalvas, alternativas, fontes adicionais>
```

## Exemplos de uso

```
/writing fact-check "Jensen Huang chamou OpenClaw de 'projeto open-source mais bem-sucedido da história' no GTC 2026"
```

```
/writing fact-check "Karpathy é founding member da OpenAI e ex-Director of AI da Tesla"
```

```
/writing fact-check arquivo.md  # extrai claims marcadas e verifica todas
```

## Quando NÃO usar

- Fatos amplamente conhecidos sem atribuição específica ("a Anthropic é uma empresa de AI").
- Opiniões pessoais do autor (não são fatos).
- Conteúdo que claramente não vai pra publicação pública.


---

## Sub-modo `iterative` — fact-check multi-round em documento inteiro

Invocado por `/writing fact-check iterative <arquivo.docx|.md>`. Para entregas com ≥10 claims factuais — entrega final MPA, ensaio individual, longform com numerosas atribuições. Validado em <issue> (Supply Chain Di Serio, v1→v10, 6 rounds, 22+ agentes verificadores, zero erros críticos confirmados na entrega).

### Princípio

**Fact-check é iterativo em camadas, não 1 round.** Rounds diferentes pegam coisas diferentes; erros diminuem em gravidade entre rounds; parar quando round N retorna READY (não buscar zero POLISH). Memory: `feedback_factcheck_multiround`.

### Pipeline de 5 camadas

| # | Verificador | Modelo | Foco | Pega |
|---|---|---|---|---|
| 1 | **Fontes primárias** | Opus | claim vs PDF/web primário | erros factuais grossos, atribuições erradas, números invertidos |
| 2 | **Minhas correções vs fonte** | Opus | as correções aplicadas batem? | reescritas que não corrigem completamente |
| 3 | **Sanity textual** | Sonnet | phrasing, conectivos, ambiguidade | "dos quais", absolutos sem suporte, implicações não-intencionais |
| 4 | **Consistência interna** | Sonnet | duplicação, contradições, refs | duplicação literal entre seções, headings inconsistentes |
| 5 | **Revisor estrito final** | Opus | CRITICAL vs POLISH | gate de submissão (READY/NOT_READY) |

### Padrão de implementação (Workflow tool)

```javascript
// Round 1 — fontes primárias, agentes paralelos por área temática
const checagens = await parallel(
  AREAS.map(area => () => agent(
    `Verifique APENAS claims sobre ${area.nome}. PDFs: ${area.fontes.join(', ')}.
     Use pdftotext via Bash. Para cada claim: {claim, verdict, evidence (com página), correction}.`,
    { label: `verify-${area.key}`, model: 'opus', schema: SCHEMA_VERIFY }
  ))
)

// Rounds 2-5 — Sonnet com evidências canônicas como contexto
// (não re-extrair PDFs — economia ~60% de tokens)
const round2 = await agent(
  `EVIDÊNCIAS CANÔNICAS já validadas (não releia PDFs):\n${evidencias_round1}\n\nV2:\n${v2_content}\n\n
   Para cada correção aplicada na V2, verifique se bate com as evidências acima.`,
  { model: 'sonnet', schema: SCHEMA_VERIFY }
)
```

### Critério de parada

- Último round retorna `status: READY` (zero CRITICAL — apenas POLISH).
- **Não buscar zero POLISH** — round N+1 sempre encontra coisas marginais e pode introduzir novos problemas (whack-a-mole).
- Se round 5 ainda tem CRITICAL → continuar; senão → submeter.

### Regras críticas (anti-padrões observados em <issue>)

- ⚠️ **Validar evidência citada por verificador antes de aplicar correção** — verificadores genéricos podem alucinar atribuição pelo título do paper (Sölvell caso). Memory: `feedback_verificador_aluca_por_titulo`.
- ⚠️ **Ao reescrever um parágrafo, releia parágrafos correlacionados** — corrigir sem cross-check vizinho cria duplicação literal entre seções.
- ⚠️ **Round 1 e 2 com Opus, rounds 3-5 com Sonnet** — economia ~60% de tokens passando evidências canônicas como contexto em vez de re-extrair PDFs.

### Exemplos de uso

```
/writing fact-check iterative trabalho-final-supply.docx
# Roda 5 rounds em sequência, gera relatório por round, propõe correções para review
```

```
/writing fact-check iterative ensaio-esg.md --round 3
# Roda só round 3 (sanity textual) — útil em iteração final após o autor aprovar conteúdo
```

### Quando NÃO usar iterative

- Documento curto (<10 claims factuais) → usar single-claim
- Draft inicial / exploratório → fact-check único após decisões de conteúdo, não antes
- Tarefa onde a "fonte primária" é o próprio o autor (memória, opinião) — não tem como verificar contra documento externo
