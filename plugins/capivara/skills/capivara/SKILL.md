---
name: capivara
description: "Background check de pessoa ou empresa para due diligence e qualificação: notícias, redes e fontes públicas, risco vermelho/amarelo/verde, perfil salvo no CRM do vault. Use para 'levanta o background de X', 'roda um capivara', 'due diligence dessa pessoa'."
category: pesquisa-conhecimento
---

# Capivara — background check de pessoas

> Origem: ENG-307 (pedido por voz Flavio, 2026-07-18). Nome = gíria de análise de crédito
> ("puxar a capivara" = puxar o CPF/histórico, achado em nota do vault sobre reunião Serasa).
> Uso: M&A (Okena/Lúcio), qualificação de cliente novo, due diligence de parceiro/sócio.

## Princípios (não negociáveis)

1. **Só fontes públicas/abertas.** Web search, páginas públicas de LinkedIn/Twitter/Instagram,
   busca pública do JusBrasil/tribunais, imprensa. **Nunca** login-wall scraping, nunca burlar
   paywall/CAPTCHA, nunca Serasa pago (é serviço pago — sinalizar como "não coberto", não simular).
2. **Não é parecer jurídico nem certidão.** É um raio-x de reputação/exposição pra apoiar decisão
   de negócio. Achado "vermelho" = motivo pra aprofundar com advogado/Serasa pago, não veredito.
3. **Proporcionalidade.** Rodar só com motivo de negócio declarado (M&A, cliente novo, parceiro) —
   é o campo "Contexto de uso" do input, obrigatório. Não é ferramenta de vigilância genérica.
4. **CPF/CNPJ nunca aparece em canal externo** (comment Linear, email, Telegram) — fica só no
   frontmatter da nota do vault (dado do CRM interno do Flavio, não segredo de sistema, mas
   também não precisa circular).
5. **Toda afirmação cita a fonte** (URL). Sem fonte = não entra no relatório, ou entra em
   "não confirmado" explícito.

## Input

- **Nome completo** (obrigatório)
- **CPF ou CNPJ** (opcional — melhora precisão da busca fiscal/jurídica, mas a falta dele não
  bloqueia o levantamento; sem CPF a cobertura fiscal/jurídica fica mais fraca, sinalizar isso)
- **Contexto de uso** (obrigatório — ex: "M&A target Okena", "cliente novo Mondoré", "parceiro")

Se faltar nome → não roda, pede o nome. Se faltar contexto → pergunta rápido antes de rodar
(o contexto muda o que é relevante: due diligence de M&A pesa mais passivo/litígio societário,
qualificação de cliente pesa mais capacidade de pagamento e reputação).

## Workflow

### 1. Buscas (WebSearch, 4 frentes em paralelo)

Rodar cada frente com 2-3 queries (nome sozinho + nome com variações/apelidos + nome com
empresa/contexto conhecido, se houver):

- **Notícias:** `"<nome>" notícia`, `"<nome>" entrevista`, `"<nome>" <empresa conhecida>`
- **Redes sociais:** `"<nome>" LinkedIn`, `"<nome>" Twitter OR X`, `"<nome>" Instagram` —
  pegar só o que aparece no resultado de busca (headline, bio pública, cargo). Não logar em
  nada, não seguir link de perfil pedindo login.
- **Fiscal/jurídico:** `"<nome>" jusbrasil`, `"<nome>" processo`, `"<nome>" CNPJ` (se CNPJ
  informado: `<CNPJ> CNPJ` direto), `"<nome>" falência OR recuperação judicial OR execução fiscal`
- **Exposição pública:** `"<nome>" palestra OR podcast OR artigo OR livro`

Usar `WebFetch` nas 2-3 fontes mais relevantes de cada frente pra confirmar o conteúdo antes
de citar (headline de busca pode enganar).

### 2. Classificar risco

- 🔴 **Vermelho** — processo criminal, falência/recuperação judicial ativa, notícia negativa
  recorrente e consistente (fraude, disputa societária pública, litígio trabalhista em massa),
  CNPJ com pendência fiscal grave visível.
- 🟡 **Amarelo** — processo cível isolado (comum em qualquer histórico empresarial BR), notícia
  negativa isolada/antiga, presença digital muito escassa pra alguém no papel esperado (red flag
  fraco de identidade), dado inconsistente entre fontes.
- 🟢 **Verde** — nada de relevante encontrado, presença pública consistente com o perfil
  declarado, sem achado fiscal/jurídico.
- **Sem achado ≠ verde automático se a cobertura foi fraca** (ex: sem CPF, nome muito comum) —
  nesse caso o risco vira 🟡 com nota "cobertura insuficiente pra concluir".

### 3. Montar o relatório

Estrutura fixa (markdown):

```markdown
## Capivara — Background Check <Nome> (<data>)

**Contexto do levantamento:** <contexto de uso>
**Risco geral:** 🔴/🟡/🟢 <um parágrafo de motivo>

### Identidade confirmada
<cargo/empresa atual, formação, histórico profissional resumido — só o que tem fonte>

### Presença digital
- LinkedIn: <achado ou "não localizado">
- Twitter/X: <achado ou "não localizado">
- Instagram: <achado ou "não localizado">

### Notícias e exposição pública
<lista de achados relevantes, cada um com data + fonte>

### Fiscal/jurídico
<achados de JusBrasil/tribunais/CNPJ — cada um com fonte>
**Cobertura:** <"com CPF/CNPJ" ou "sem CPF/CNPJ — busca só por nome, cobertura reduzida">

### Resumo executivo — oportunidade e risco
<3-5 linhas: o que isso significa pra decisão de negócio no contexto declarado>

### Fontes
<lista de URLs citadas>

---
*Gerado por /capivara em <data>. Não substitui parecer jurídico/Serasa pago. Fontes públicas via web search.*
```

### 4. Salvar no vault (CRM)

Reusa a convenção do CRM existente (`Atlas/Notes/Index/People/`, ver
`project_crm_people_notes` na memória) em vez de criar taxonomia paralela:

1. Procurar nota existente com esse nome em `Atlas/Notes/Index/People/`.
2. **Se existe:** anexar a seção "## Capivara — Background Check..." ao final do corpo
   (preserva histórico de rodadas anteriores — não sobrescreve) + atualizar frontmatter
   (chaves abaixo).
3. **Se não existe:** criar nota nova nesse mesmo diretório usando o template
   `Atlas/Utilities/Templates/People Note.md` como base + a seção Capivara.

Frontmatter — chaves adicionadas pela skill (não mexer nas chaves geridas pelo `crm_sync.py`:
`email, phone, LastConversation, LastMeeting, LastWhatsApp, NextMeeting, ContactChannels,
Interactions90d, crm_synced`):

```yaml
tags:
  - class/people
  - wf/agents
cpf: "<só se informado>"
cnpj: "<só se informado>"
capivara_last_check: <data ISO>
capivara_risk: vermelho|amarelo|verde
```

### 5. Entregar

Link da nota + resumo de 3-5 linhas na resposta pro Flavio. Se o risco for 🔴, dizer isso
explícito logo na primeira linha (não enterrar no meio do relatório).

## Limitações (dizer sempre, não esconder)

- Sem acesso a Serasa/SPC pago, birôs de crédito, PEP (pessoa politicamente exposta) oficial —
  só o que aparece em busca pública.
- JusBrasil/tribunais via busca pública tem cobertura parcial (nem todo processo é indexado,
  segredo de justiça não aparece).
- Nome comum sem CPF = risco real de confundir duas pessoas — o relatório sinaliza isso.
- Não é ferramenta de compliance regulatório (KYC bancário, PLD) — é apoio de decisão informal.
