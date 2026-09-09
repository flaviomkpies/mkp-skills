# Mode: post

> Modo invocado por `/writing post [linkedin|twitter|threads]`.
> Skill mãe: `/writing` (ver `SKILL.md` raiz).

Posts curtos para redes sociais. Diferente de newsletter (longo, narrativo) e longform (ensaio). Tamanho típico: 100-1500 caracteres por unidade. Foco em densidade de ideia.

## Sub-comandos

- `/writing post linkedin` — post longo de LinkedIn (até ~1300 caracteres + carrossel opcional).
- `/writing post twitter` — thread de tweets (cada tweet ≤ 280 caracteres, encadeado).
- `/writing post threads` — post Threads (semelhante a Twitter, mas com tom Meta).

## Princípios comuns (todos os sub-comandos)

- **DNA central** vale (ler `../DNA.md` antes).
- **Sem hashtags forçadas.** Só se for vocabulário relevante.
- **Sem emojis no corpo** — exceção: 1 emoji estrutural máximo (separador visual), nunca decorativo.
- **Hook na primeira linha.** Em redes sociais, primeira linha é praticamente o post inteiro pra muito leitor.
- **Sem "Pensei sobre X..."** ou abertura genérica. Vai direto ao ponto.
- **Cita posts próprios anteriores** quando faz sentido — building public coerente.

## Procedimento (LinkedIn)

1. **Brain dump:** Flavio passa material bruto ou ideia.
2. **Hook:** sugerir 2-3 versões da primeira frase. Flavio escolhe.
3. **Corpo:** 3-5 parágrafos curtos. Densidade > completude.
4. **Fechamento:** sem call-to-action genérico ("o que vocês acham?"). Pode ter pergunta específica conectada ao tema, ou simplesmente parar quando o ponto foi feito.
5. **Polish:** humanize pass + remover tudo que parece consultoria de LinkedIn padrão.

## Procedimento (Twitter / Threads)

1. **Tese central em 1 frase** — esse é o tweet 1 da thread.
2. **Quebra em sub-pontos** — cada sub-ponto = 1 tweet. Máximo 7 tweets numa thread (mais que isso vira post longo, vai pra LinkedIn ou newsletter).
3. **Numeração explícita** (1/7, 2/7, ...) opcional — uso depende do tom.
4. **Tweet final = punchline ou link** para post completo (newsletter / blog).
5. **Polish individual:** cada tweet precisa fazer sentido isolado (alguém vai retweetar só um, sem contexto).

## Anti-patterns específicos de redes sociais

- ❌ "Aprendi 5 coisas...":  rule of three / five forçado.
- ❌ "Aqui vai um insight..." — fake hook, não diz nada.
- ❌ "Concordas?", "O que pensam?" — pergunta vazia no fim.
- ❌ Citação de quote alheia sem contexto — cite mas comente em 1 frase.
- ❌ Listas com bullet de 1 palavra cada ("Foco. Disciplina. Coragem.") — vazio.

## Cross-posting

Se o post vai pro LinkedIn E Twitter:
- LinkedIn versão: completa, narrativa.
- Twitter versão: comprimida, thread se necessário.
- **Não publicar idêntico nos dois.** Plataformas têm tom diferente.


## Ciclo de revisão (Flavio escreve, IA assiste)

Padrão validado em 2026-05-07 (caso PUC-MG):

1. **v1 (IA):** primeiro draft com base no material lido (Granola, etc).
2. **v2 (IA refino):** ajustes a partir de feedback do Flavio sem ele ter escrito ainda.
3. **v3 (Flavio):** Flavio escreve a versão dele, geralmente é a virada qualitativa do post.
4. **v4 (IA ajustes mínimos):** IA revisa formulação, fluxo, regência, redundância — **NÃO** corta conteúdo que o humano adicionou. Ver `feedback_human_adds_context_ai_respects.md`.
5. **vf (Flavio publica):** Flavio aplica últimos ajustes (espaçamento, links encurtados, anexos visuais) e publica.

## Versionamento dentro do arquivo

Todas as versões ficam no **mesmo arquivo .md**, em seções H1 (`# v1`, `# v2`, ...). Nunca sobrescrever — cada iteração preserva histórico. Convenção:

- `# v1`, `# v2`, ... — drafts iterativos
- `# v3 - Flavio` — versão escrita pelo humano (marcar autoria)
- `# vf - publicada` — versão final que foi publicada (marca o release)
- `**Feedback:**` em itálico abaixo de versão descartada — registra crítica recebida

Ver memory `feedback_versioning_h1_inline.md` para regra completa.

## Output esperado

Arquivo `.md` na pasta apropriada do vault (perguntar a Flavio se não óbvio):
- vinculado à newsletter → derivar do átomo `Efforts/Projects/Newsletter AI & Negócios/_Atomos/artigo-<slug>.md` (pipeline /newsletter-post); salvar o post curto em `Efforts/Posts/<canal>/`.
- `Efforts/Posts/<canal>/<data>-<slug>.md` se for standalone.

Frontmatter mínimo:
```yaml
---
Date: YYYY-MM-DD
canal:
  - linkedin | twitter | threads
status: drafting | ready | published
url_publicado: <preencher após publicar>
---
```
