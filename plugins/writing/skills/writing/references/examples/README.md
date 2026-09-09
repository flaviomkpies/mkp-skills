# Examples — exemplos canônicos de textos do Flavio

Pointers (não cópias) para textos publicados que servem de calibração de voz para os modos da skill `/writing`.

**Por que pointer e não cópia:** se Flavio re-edita um post publicado (typo, atualização), exemplo continua atualizado. Conteúdo canônico vive em `Efforts/Projects/` ou no Linear. Aqui só apontamos.

**Como usar:** antes de escrever prosa em qualquer modo, abrir 2-3 exemplos relevantes. Ler com atenção a cadência de frase, abertura, fechamento, transições. Ver `../primitives/voice-calibration.md` para o procedimento completo.

---

## Substack (newsletter)

Vault path: `Efforts/Projects/Newsletter AI & Negócios/02_Sprint_Active/5_Published/`

| Exemplo | Vault path | O que demonstra |
|---|---|---|
| **Anatomia de um Agente** (06/05/2026) | `2026-05-06-anatomia-do-agente_published.md` | Calibração mais recente. Padrão "fato concreto + número" na abertura. Estrutura "tese → 5 dimensões → fechamento com callback ao gancho". URL Substack: https://flaviomacknightpies.substack.com/p/a-anatomia-de-um-agente |
| **OpenClaw 2 meses** (03/04/2026) | `2026-04-03-openclaw-meu-time-de-agentes_published.md` | Voz primária do Flavio. Honestidade obrigatória sobre limites. Vitórias concretas listadas (cron rotinas). Fechamento em 3 tempos com callback. **Calibração canônica para newsletter.** |
| **3 Fases das Ferramentas de AI** (publicado mar/2026) | `010_As_fases_das_ferramentas_de_AI_2026.md` | Estrutura "fases progressivas". Uso de bullets em descrições operacionais (permitido). Outline detalhado antes da prosa. URL: https://flaviomacknightpies.substack.com/p/tres-fases-das-ferramentas-de-ai |
| **Empresa Já é Digitalizada** (mar/2026) | `003_Empresa_Digitalizada.md` | Tom conversacional puro, sem listas. Argumento que sobrevive em prosa corrida. |
| **Reflexão Executiva China** (24/03/2026) | `2026-03-24_reflexao-executiva-china-renmin.md` | Variante Substack do post China. Cadência mais ensaística. |
| **Over-optimization procrastination** | `over-optimization-procrastination.md` | Honestidade sobre falha pessoal — exemplo de como Flavio admite limite sem virar coach. |

### Substack Notes (formato curto)

| Exemplo | Vault path | O que demonstra |
|---|---|---|
| **Claude Cowork — trabalho real** | `note-claude-cowork-trabalho-real.md` | Note Substack. Densidade alta, ~200 palavras. Hook na primeira linha. |
| **Gemini Live — busca tempo real** | `note-gemini-live-busca-tempo-real.md` | Note. Comparação técnica curta. |
| **Teaser 3 fases** | `note-tres-fases-teaser.md` | Note como teaser de post longo. Convite, não setup. |
| **Teaser over-optimization** | `note-over-optimization-teaser.md` | Note como teaser. |

---

## LinkedIn

Posts LinkedIn não estão consolidados em pasta canônica como o Substack. Disponíveis hoje:

| Exemplo | Origem | O que demonstra |
|---|---|---|
| **Reflexão Executiva China — RENMIN** | [Linear BIZ-84](https://linear.app/veredas/issue/BIZ-84) (description tem texto completo) | Post LinkedIn longo. Estrutura "percepções executivas em bullets". Tom executivo direto. Variante PT-BR mais formal que Substack. |
| **Lições Jack Conte** | [Linear BIZ-133](https://linear.app/veredas/issue/BIZ-133) + arquivo em `Efforts/Projects/Newsletter AI & Negócios/02_Sprint_Active/4_Ready_to_Pub/Jack Conte - post linkedin.md` | Post LinkedIn baseado em palestra. 3-5 lições, sem call-to-action genérico. |
| **Viagem China MBA/GNAM** | [Linear BIZ-91](https://linear.app/veredas/issue/BIZ-91) | Sem texto consolidado no vault — só registro Linear. |

### Lacuna identificada — LinkedIn

A organização de LinkedIn está **incompleta**. Hoje os textos vivem dispersos em:
- Linear issue descriptions (texto inline mas sem link Substack-style)
- `4_Ready_to_Pub/` (drafts pré-publicação)
- Não há `5_Published_LinkedIn/` ou similar

**Recomendação para o próximo Sprint:** criar pasta `Efforts/Posts/LinkedIn/5_Published/` com texto final dos posts e URL LinkedIn no frontmatter, espelhando o padrão da newsletter. Pedir ao Flavio que arquive os 3 posts existentes (BIZ-84, BIZ-91, BIZ-133) nesse formato.

Enquanto isso não é feito, este README aponta para as fontes existentes. **Quando precisar de mais exemplos LinkedIn, pedir ao Flavio diretamente** — ele tem o texto final dos posts na sua conta LinkedIn.

---

## Como cada modo da skill consulta os exemplos

| Modo | Exemplos relevantes |
|------|---------------------|
| `newsletter` | Substack longos (5 itens) — calibração principal. Notes (4 itens) — para teaser/pre-publish. |
| `post linkedin` | LinkedIn (3 itens) — referência única hoje. |
| `post twitter` / `post threads` | Notes do Substack como aproximação. Lacuna explícita: Flavio raramente publica thread Twitter próprio. |
| `longform` | Não há exemplo canônico de longform > 3000 palavras hoje. Quando criar, arquivar aqui. |

---

## Atualização contínua

Este README é vivo. A cada post publicado:
1. O agente (ou Flavio) adiciona linha à tabela.
2. Anota o que de novo o post demonstra (não duplicar "voz primária" — já temos).
3. Mantém ordem cronológica reversa (mais recente em cima) por canal.

**Limite:** ~12 exemplos por canal. Mais que isso, agente entra em "voz média" diluída. Rotacionar — manter os 12 mais representativos, arquivar os antigos.
