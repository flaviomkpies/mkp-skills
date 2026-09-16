---
name: capivara
description: "Background check de pessoa ou empresa para due diligence e qualificação: notícias, redes e fontes públicas, classificação de risco vermelho/amarelo/verde e um relatório com fonte em cada afirmação. Use para 'levanta o background de X', 'roda um capivara', 'due diligence dessa pessoa'."
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, WebSearch, WebFetch, AskUserQuestion
---

# Capivara — background check de pessoa e empresa

> O nome vem da gíria de análise de crédito no Brasil: "puxar a capivara" é puxar o histórico
> de alguém.
>
> **Antes da primeira vez:** leia o `ADAPTAR.md` do plugin — ele define **onde o relatório é
> salvo** no seu sistema. Sem isso a skill grava um markdown na pasta atual, que funciona mas
> não conversa com o lugar onde você guarda gente.

## Princípios (não negociáveis)

1. **Só fonte pública e aberta.** Busca na web, páginas públicas de redes sociais, busca pública
   de tribunais, imprensa. **Nunca** raspar atrás de login, nunca burlar paywall ou CAPTCHA,
   nunca simular consulta a birô pago — se não dá para cobrir, o relatório diz "não coberto".
2. **Não é parecer jurídico nem certidão.** É um raio-x de reputação e exposição para apoiar
   decisão de negócio. Achado vermelho é motivo para aprofundar com advogado ou com uma consulta
   paga, não um veredito.
3. **Proporcionalidade.** Só roda com um **motivo de negócio declarado** — é campo obrigatório
   da entrada. Não é ferramenta de vigilância sobre pessoa privada, e não se usa para checar
   alguém com quem você não tem relação de negócio.
4. **Documento de identidade nunca sai em canal externo.** CPF ou CNPJ, quando informados, ficam
   só no arquivo local; não vão para mensagem, e-mail ou comentário em ferramenta compartilhada.
5. **Toda afirmação cita a fonte.** Sem URL, não entra no relatório — ou entra numa linha
   marcada "não confirmado".

## Entrada

- **Nome completo** (obrigatório)
- **CPF ou CNPJ** (opcional — melhora a busca fiscal e jurídica; sem ele a cobertura cai, e o
  relatório precisa dizer isso)
- **Contexto de uso** (obrigatório — "avaliando aquisição", "cliente novo", "sócio em potencial")

Sem nome, não roda. Sem contexto, pergunte antes: o contexto muda o que é relevante. Uma
aquisição pesa passivo e litígio societário; qualificar um cliente pesa capacidade de pagamento e
reputação.

## Workflow

### 1 · Buscar em quatro frentes, em paralelo

Duas a três consultas por frente — o nome sozinho, o nome com variações ou apelido, e o nome com
a empresa, quando você já sabe qual:

- **Notícias:** `"<nome>" notícia`, `"<nome>" entrevista`, `"<nome>" <empresa>`
- **Redes:** `"<nome>" LinkedIn`, `"<nome>" Twitter OR X`, `"<nome>" Instagram` — pegue só o que
  aparece no resultado da busca (manchete, cargo, bio pública). Não faça login em nada, não siga
  link que peça autenticação.
- **Fiscal e jurídico:** `"<nome>" processo`, `"<nome>" CNPJ`, `"<nome>" falência OR recuperação
  judicial OR execução fiscal`. Fora do Brasil, troque pelos equivalentes locais (registro
  mercantil, court records, companies house).
- **Exposição pública:** `"<nome>" palestra OR podcast OR artigo OR livro`

Abra as duas ou três fontes mais relevantes de cada frente antes de citar: manchete de busca
engana.

### 2 · Classificar o risco

- 🔴 **Vermelho** — processo criminal, falência ou recuperação judicial ativa, notícia negativa
  recorrente e consistente (fraude, disputa societária pública, litígio trabalhista em massa),
  pendência fiscal grave visível.
- 🟡 **Amarelo** — processo cível isolado (comum em qualquer histórico empresarial), notícia
  negativa isolada ou antiga, presença pública escassa demais para o papel que a pessoa diz
  ocupar, dado inconsistente entre fontes.
- 🟢 **Verde** — nada relevante encontrado, presença pública consistente com o perfil declarado.

**Ausência de achado não é verde quando a cobertura foi fraca.** Sem documento, ou com nome muito
comum, o risco é 🟡 com a nota "cobertura insuficiente para concluir". Confundir duas pessoas com
o mesmo nome é o erro mais caro desta skill — confirme sobrenome, empresa ou cidade antes de
consolidar qualquer achado numa pessoa.

### 3 · Montar o relatório

```markdown
## Capivara — <Nome> (<data>)

**Contexto:** <motivo de negócio declarado>
**Risco geral:** 🔴/🟡/🟢 <um parágrafo de motivo>

### Identidade confirmada
<cargo, empresa, formação, histórico — só o que tem fonte>

### Presença digital
- LinkedIn / X / Instagram: <achado, ou "não localizado">

### Notícias e exposição pública
<cada achado com data e fonte>

### Fiscal e jurídico
<achados, cada um com fonte>
**Cobertura:** <"com documento" ou "só por nome — cobertura reduzida">

### O que isso significa para a decisão
<3 a 5 linhas, no contexto declarado>

### Fontes
<todas as URLs citadas>

---
*Levantamento por fontes públicas. Não substitui parecer jurídico nem consulta a birô de crédito.*
```

### 4 · Salvar — onde o seu perfil disser

`references/perfil-local.md` responde três coisas: **onde** o relatório vai, **como** o arquivo
se chama e **o que** vai no cabeçalho dele.

Sem perfil, o padrão é um markdown em `./capivara/<nome-em-minúsculas>-<AAAA-MM-DD>.md`, e a
skill avisa que está usando o padrão.

Duas regras valem em qualquer destino:

- **Rodada nova acrescenta, não sobrescreve.** Se já existe registro dessa pessoa, a seção
  datada entra no fim. O histórico de como a leitura mudou vale mais que a foto de hoje.
- **O documento de identidade fica no arquivo, nunca no resumo** que você manda por mensagem.

### 5 · Entregar

O caminho do arquivo e um resumo de 3 a 5 linhas. **Se o risco é 🔴, isso é a primeira linha** —
nunca enterrado no meio do relatório.

## Limitações (diga sempre, não esconda)

- Sem acesso a birô de crédito pago, nem a lista oficial de pessoa politicamente exposta.
- Busca pública de tribunal tem cobertura parcial: nem todo processo é indexado, e segredo de
  justiça não aparece.
- Nome comum sem documento é risco real de confundir duas pessoas — o relatório sinaliza.
- Não serve a compliance regulatório (KYC bancário, prevenção à lavagem). É apoio de decisão
  informal.
