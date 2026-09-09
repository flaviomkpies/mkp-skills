# Mode: newsletter

> Modo invocado por `/writing newsletter [outline|draft|polish|publish|suggest]`.
> Skill mãe: `/writing` (ver `SKILL.md` raiz). Para outros tipos de texto, ver `modes/post.md` (curtos) ou `modes/longform.md` (ensaio/capítulo/whitepaper).

Modo newsletter da "Newsletter do Flavio: IA na prática" (Substack — rebrand 2026-07; ex-"AI & Negócios").

## ⚠️ Pipeline canônico mudou (2026-07)

**Artigo novo = skill `/newsletter-post`** (átomo em `_Atomos/`, verificador, focus group, pacote SEO, Notes candidatas). Publicação = `/substack` · Notes = `/newsletter-note` · comentários em publicações alheias = `/newsletter-comments` · arte = `/newsletter-art` (identidade v4 minimal editorial).

**Este modo permanece como acervo vivo de VOZ:** as seções "DNA de Escrita", "Narrative spines", "Calibração" e "Gate de Decisão" abaixo são fonte canônica (o /newsletter-post as consome). O workflow de etapas 0A-6 abaixo é o fluxo manual LEGADO — usar só se o Flavio pedir explicitamente.

## Contexto da newsletter

Norte (memória `project_newsletter_north_star`, ditado 2026-07-05): PRIMÁRIO = estruturar pensamento / estudar IA aplicada a negócios e trabalho do conhecimento; SECUNDÁRIO = popularizar com método. Nunca distorcer pauta/voz por alcance.

**Voz:** ver `../DNA.md` (skill raiz). Vocabulário proibido e narrative spines específicos de newsletter ficam neste arquivo (seções abaixo).

## Paths atuais

```
LAR ATUAL (desde 30/08/2026, ENG-278 T04): Efforts/Writing/Newsletter/<YYYY-MM-DD-slug>/
├── post.md, fontes.md, feedback-Flavio.md, imagens, deck…   ← uma pasta por post, sem subpasta de estágio
└── estágio no frontmatter: status (rascunho|revisao|publicado) · provenance (human|ai-assisted) · canal · publicado_em
    (lido pela Base Atlas/Bases/Escrita.base; regra em Efforts/Writing/Artigos/_LEIA.md)

LEGADO (não criar nada novo aqui): Efforts/Projects/Newsletter AI & Negócios/ — _Atomos/, 00_Backlog, 01_Backlog,
01_Research, 02_Sprint_Active (publicados antigos em 5_Published/). Em 05/09/2026 o CoS salvou um post no lugar
errado por seguir este bloco; a fonte é o vault (`ls Efforts/Writing/Newsletter`).
```

---

## Comandos

### `/newsletter write` — Fluxo principal (brain dump → post)

Ponto de entrada **0A**. Flavio já tem material bruto — áudio transcrito, texto livre,
rascunho solto, ou research file existente. AI parte desse material e executa etapas 1-4.

### `/newsletter write-interview` — Fluxo guiado (entrevista → post)

Ponto de entrada **0B**. Flavio tem a ideia mas pouco tempo. AI faz perguntas de múltipla
escolha via AskUserQuestion para extrair o conteúdo, depois executa etapas 1-4.

### `/newsletter polish <arquivo>` — Polir draft existente

Aplica DNA de escrita a um texto já escrito. Etapa 4 isolada (DNA checklist + humanizer pass).

### `/newsletter humanize <arquivo>` — Só o passe humanizer

Roda apenas a sub-etapa 4b: remove marcas de AI (em-dash, vocabulário inflado, rule of three, promotional, etc.). Útil quando o draft já passou pelo DNA e só falta desumanizar. Carrega os patterns dos patterns em `../primitives/humanizer-patterns.md` (`../primitives/humanizer-patterns.md`) antes de atuar.

### `/newsletter publish <arquivo>` — Publicar rascunho no Substack

Etapa 6. Dispara o script browser automation da skill `/substack` para criar rascunho no Substack a partir do `.md` aprovado. Pré-requisito: cookies válidos (ver fallback manual abaixo). Move o arquivo para `5_Published/` após confirmação.

### `/newsletter suggest` — Sugerir pautas

Cruza backlog, research, posts publicados e contexto atual. Apresenta 3 sugestões
com ângulo, gancho e público.

---

## Estrutura do arquivo de post (versionamento inline)

Cada post vive num único arquivo `.md` que acumula todas as versões. NUNCA apagar
versões anteriores — cada iteração é registro do processo criativo.

```markdown
---
(frontmatter)
---

# [Título do Post]

## Entrevista
(resumo das respostas de Flavio — etapa 0A ou 0B)

---

# Outlines

## Outline V1
(primeira versão)

## Outline V2
(revisão após feedback)

## Outline V3 ← APROVADO
(versão final aprovada — marcar com ← APROVADO)

---

# Prosa

## Draft A
(primeira versão de prosa)

## Draft B
(revisão após feedback)

## Draft C — FINAL
(versão final — marcar com — FINAL)

---

## DNA checklist
(checklist de revisão aplicada na última versão)
```

**Regras:**
- Nunca sobrescrever versão anterior. Criar nova seção H2 (V1, V2, V3...)
- Marcar versão aprovada com `← APROVADO` ou `— FINAL`
- Se Flavio pede mudança no outline após aprovação: criar V(N+1), não editar o aprovado
- Mesma lógica para prosa: Draft A, B, C...
- O arquivo cresce, mas o histórico é valioso para calibração futura do DNA

---

## As Etapas

### Etapa 0A — Brain Dump (ponto de entrada principal)

**Input:** Flavio fornece material bruto. Pode ser:
- Transcrição de áudio (Flavio grava falando livremente)
- Texto livre digitado
- Research file já existente em `01_Research/`
- Combinação dos acima

**O que AI faz:**
1. Ler o material integralmente
2. Identificar: tese central, blocos de argumento, exemplos, dados, tom
3. NÃO reescrever — apenas registrar o que encontrou
4. Perguntar (1 pergunta, curta): "Entendi que a ideia central é [X]. Falta algo ou quero mudar o foco?"
5. Seguir para Etapa 1

### Etapa 0B — Entrevista Guiada (alternativa)

**Quando usar:** Flavio tem pouco tempo ou a ideia ainda não está articulada.

**Formato:** AskUserQuestion, uma pergunta por vez, múltipla escolha quando possível.
Preview curta (máx 2 linhas).

Sequência:
1. "Sobre o que é esse post?" (resposta aberta)
2. "Qual é o tipo?" (A) experiência pessoal, B) framework, C) análise de tendência, D) opinião)
3. "O que motivou agora?" (A-D com opções derivadas da resposta 1)
4. "Quais pontos não podem faltar?" (resposta aberta — keywords)
5. "Tem algo que NÃO deve entrar?" (resposta aberta)

Se já existe research file: ler ANTES e adaptar as perguntas ao material.

**Output:** compilação das respostas como material bruto → seguir para Etapa 1.

### Etapa 1 — Outline (extrair estrutura do material)

**Objetivo:** organizar o que Flavio disse/escreveu numa estrutura indentada.
NÃO é prosa. NÃO inventar conteúdo. Apenas reorganizar o que já existe.

**O que AI faz:**
1. Extrair a estrutura implícita do material bruto
2. Montar outline indentado:

```markdown
## OUTLINE

- **Gancho**
  - [frase ou conceito do Flavio que funciona como abertura]

- **Bloco 1 — [nome extraído do material]**
  - [ideia principal — palavras de Flavio]
    - [evidência/exemplo que ele mencionou]

- **Bloco 2 — [nome]**
  - [ideia principal]
    - [evidência/exemplo]

- (quantos blocos forem necessários)

- **Fechamento**
  - [tom e direção que Flavio indicou]
```

3. Apresentar a Flavio: "Esse outline captura o que você quer dizer? Quer mudar ordem, tirar, adicionar?"
4. Se Flavio pedir research antes de aprovar → Etapa 2 primeiro, depois volta ao outline
5. **Só avança com aprovação explícita**

**Regra Graham:** o outline é leve, não detalhado. Cada bullet = 1 ideia. O objetivo é dar
direção, não travar. Ideias novas podem surgir na prosa — e devem ser incorporadas.

### Etapa 2 — Research (sob demanda)

**Quando:** Flavio pede, ou o outline tem afirmações que precisam de verificação.
NÃO é etapa obrigatória — só quando necessário.

**O que AI faz:**
- Buscar no vault: `01_Research/`, posts publicados, backlog
- WebSearch para dados, referências, estatísticas se necessário
- Checar fatos mencionados por Flavio no brain dump
- Surfar conexões com posts anteriores ou referências do vault

**Output:** briefing curto (máx 10 bullets) com:
- Fatos verificados que sustentam o post
- Dados concretos encontrados
- Conexões com material existente
- `[DADO PENDENTE: descrição]` para o que não encontrou

**Regra absoluta:** nada inventado. Se não encontrou, marca como pendente.

### Etapa 3 — Prosa (tighten, não reescrever)

**Objetivo:** transformar o outline aprovado em prosa corrida, preservando a voz de Flavio.

**O que AI faz:**
1. Ler últimos 3-4 posts em `5_Published/` para calibrar voz
2. Escrever prosa bloco a bloco, usando as palavras e expressões de Flavio do brain dump
3. Onde Flavio já escreveu frases boas no material bruto: manter intactas
4. Onde há gaps entre blocos: escrever transições mínimas e naturais
5. Aplicar DNA de escrita (ver seção abaixo)
6. Marcar `[FLAVIO: completar — contexto X]` onde falta informação
7. Salvar em `2_Drafting/` com data no nome

**Regras de temperatura zero:**
- Escrever APENAS a partir do que está no outline, brain dump, research ou entrevista
- NÃO inventar exemplos, perguntas retóricas, estatísticas, citações
- NÃO fabricar interações ("o que me perguntam...", "pessoas dizem...")
- NÃO adicionar frases que soam bem mas não dizem nada
- Cada frase deve ser rastreável ao material de Flavio

**Regra Graham — ideias novas são bem-vindas:**
Se durante a escrita surgir uma conexão genuína (entre blocos do próprio Flavio,
ou com research verificado), pode incluir — mas marcar como `[SUGESTÃO AI]` para
Flavio decidir se mantém.

### Etapa 4 — Polimento (cortar, comprimir, checar)

**Objetivo:** aplicar DNA de escrita + humanizer pass como checklist de revisão.

Subdividida em **4a (DNA)** e **4b (Humanizer)**. Sempre nessa ordem — DNA corrige voz, humanizer tira resíduo de AI.

#### 4a — DNA pass

1. **Ler em voz alta (mentalmente):** cada frase soa como Flavio falando? Marcar as que não
2. **Cortar:** remover cada palavra que não adiciona significado (Paul Graham: "se é chato, corte")
3. **Comprimir:** cada ideia-chave cabe em uma frase? Se não, a ideia não está clara (Naval)
4. **Checar fatos:** toda afirmação tem base no material ou research?
5. **DNA checklist:** passar item por item (ver seção "DNA de Escrita" abaixo)

#### 4b — Humanizer pass

**Gate determinístico primeiro (05/09/2026):** `python3 ../scripts/tells_pt.py <arquivo>` → exit 0 (≤3 tells em ~1.000 palavras). Conta fragmento, "não é X, é Y", kicker de parágrafo, tricolon, aforismo e travessão. Nasceu do post da sabatina: a v1 passou por DNA + humanizer e saiu com 9 tells; o Flavio leu e disse "frase de coach". A lista de padrões só funciona quando algo conta.


Aplicado **depois** do DNA pass, como segunda camada de defesa contra resíduo de AI.

Carregar os patterns canônicos antes de atuar:
```
cat "../primitives/humanizer-patterns.md"
```

Ou invocar `/writing humanize <arquivo>` que lê e aplica os patterns automaticamente.

Scan obrigatório (patterns de maior impacto, em ordem):
- **Anti-atribuição AI** (aprendizado 2026-04-21) → toda expressão que o AI inventou entra marcada `[SUGESTÃO AI]` com justificativa, NUNCA corre na prosa como se fosse voz do Flavio. Exemplo real: "engenharia com quinas" foi sugerida pelo AI, Flavio precisou perguntar "sua ou minha?". Se detectar expressão sem origem rastreável no brain dump / entrevista / fontes, marcar imediatamente
- **Em-dash vs hyphen consistency** → verificar section headers. Frequente: corpo usa "—" mas headers usam "-". Padronizar
- **Fragments sem verbo principal** → em parágrafos de transição, detectar frases que não têm sujeito+verbo conjugado. Corrigir para sentença completa. Exemplo real do post 2026-04-21: "Atualmente, uma entrega grande em andamento..." não tem verbo, precisou virar "Hoje tenho uma entrega grande em andamento"
- **Concordância em orações compostas** → "Pega tasks... e trabalham" (singular→plural). Revisar cada oração coordenada
- **Aspas que abrem e não fecham** → varredura de `"..."` garantindo pareamento
- **"ok" minúsculo em contexto formal** → trocar para "OK" ou "aprovação"
- **Em-dash overuse** (—) → substituir por vírgula/ponto quando não for pausa dramática real
- **Rule of three forçado** ("innovation, inspiration, and insights") → quebrar ou reduzir
- **Negative parallelisms** ("não é só X, é Y") → afirmar diretamente
- **Vocabulário AI**: delve, crucial, landscape (abstrato), tapestry, underscore, pivotal, testament, foster, align, intricate — cortar ou trocar
- **Promotional**: vibrant, seamless, robust, groundbreaking, profound — cortar
- **Copula avoidance**: "serves as", "stands as", "represents a" → usar `é`, `tem`, `faz`
- **-ing endings superficiais**: "..., highlighting X, reflecting Y" → ponto final antes
- **Elegant variation**: sinônimos ciclados desnecessariamente → repetir o termo
- **Título case em headings** → sentence case
- **Boldface mecânico** em listas → remover
- **Hedging excessivo**: "pode potencialmente...", "talvez possivelmente" → afirmar ou cortar

Output do humanizer pass: diff com motivo por linha alterada.

#### 4c — Apresentar resultado

Mostrar a Flavio: diff DNA + diff Humanizer, separados, com justificativa. Edits cirúrgicos — nunca reescrever parágrafos inteiros. Se um parágrafo pede reescrita completa, voltar à Etapa 1.

Salvar em `3_Polishing/`.

### Etapa 5 — Aprovação

Apresentar versão final a Flavio. Se aprovado → mover para `4_Ready_to_Pub/`.

### Etapa 6 — Publicação no Substack

Dispara quando Flavio pede `/newsletter publish <arquivo>` ou confirma publicação após aprovação.

**Publicação automática no Substack:** só existe na máquina de origem (perfil de browser e scripts próprios). Fora dela, publique pelo site do Substack, colando o texto final.
