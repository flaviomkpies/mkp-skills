# LAYOUTS.md — Arquétipos de slide reThink / reMarkable

> O gerador NÃO repete um template. Escolhe o arquétipo pelo **tipo de conteúdo**.
> Identidade (autoritativa em `design.md`): **branco**, **Fraunces no título + Inter no corpo**, **régua vertical à esquerda + barra no título**, **nav de seções no topo**, monocromático (cor só em link), **conteúdo flui do topo**. Nunca cor chapada, gradiente ou sombra.
> ⚠️ Menções antigas a "régua dupla / drop-cap / bronze / papel quente / ancorar à base" abaixo são da variante Elegant — para a identidade reThink, vale o `design.md`.
> Snippets prontos em `snippets.html`.

Regra de ouro: **1 slide ≠ 1 layout fixo**. Num deck de 5+ slides, use ≥3 arquétipos diferentes. Repetir o mesmo layout 5x = "sem graça".

| # | Arquétipo | Quando usar | Decoração-chave |
|---|---|---|---|
| A | **Capa / hero** | abertura | slide tinta (`--ink`) + headline Fraunces grande + monograma marca-d'água ~5% + eyebrow mono; filete fino sangrando de uma borda |
| B | **Statement + régua** | "quem sou", tese, 1 ideia + parágrafo | parágrafo Inter 300 + **régua dupla** sob o título; opcional drop-cap |
| C | **Divisória de seção** | trocar de tema | slide tinta full-bleed: numeral Fraunces gigante a ~6% atrás de eyebrow+título; fio horizontal curto embaixo |
| D | **Big-statement** | frase de impacto curta | Fraunces 300 grande (não bold), uma palavra em itálico ou `--ink`; muito espaço |
| E | **Diagrama de fios** | relação entre 2–4 atores/itens | hairlines `--hair-strong` como conectores, rótulo Inter pendurado em cada nó |
| F | **Tríade / interseção** | 3 forças que se cruzam | 3 círculos stroke fino (grayscale) + 1 em `--ink` + ponto no centro |
| G | **Timeline de fases** | metodologia, roadmap | 3–4 colunas separadas por fio vertical; numeral Fraunces no topo de cada; sem barra colorida |
| H | **Stat / número** | 1 KPI grande | numeral Fraunces 300 (120–140px) + label mono + fonte |
| I | **Split 2 colunas** | texto Inter (esq) × detalhe mono/dado (dir) | filete vertical `--hair-strong` divisor |
| J | **Síntese executiva** | **logo após a capa** — a resposta primeiro (governing thought) + 3 pilares MECE de apoio | bloco-resposta com **filete de accent** à esquerda no topo + 3 blocos-pilar abaixo (só fios); eyebrow "síntese" |
| K | **Recomendação / próximos passos** | **fecho de deck analítico** — ações SMART (o quê · quem · quando), quick wins destacados | 2 colunas "feito × a fazer" OU lista numerada (Fraunces) com owner/prazo; destaque em `--ink` |
| Z | **Fechamento** | contato / 1 frase final | igual à capa, invertida (monograma grande + 1 linha + dados de contato em mono) |

## Estruturas de conteúdo (onde vão título e conteúdo — VARIAR sempre)
O arquétipo (A–Z) diz o *tipo*; a estrutura diz a *disposição*. Num deck, alternar estruturas evita monotonia. Flavio pediu explicitamente mais variação (2026-06-19).

| Estrutura | Disposição | Bom para |
|---|---|---|
| **S1 · Título topo** | eyebrow+título no topo, conteúdo full-width abaixo | default; diagrama/funil/colunas largas |
| **S2 · Split 1/3 · 2/3** | eyebrow+título+lead fixos na **coluna esquerda (1/3)**; conteúdo (bullets/cards/chart/foto) nos **2/3 da direita** | a maioria dos slides de conteúdo — é o mais versátil e "consulting" |
| **S3 · Split 2/3 · 1/3** | conteúdo principal à esquerda, painel de apoio/legenda/numeral à direita | gráfico + leitura, mapa + notas |
| **S4 · Duas colunas de texto** | abertura Inter (esq) × detalhe/notas em mono (dir) | narrativa densa |
| **S5 · Centralizado** | título + objeto único centralizados | Venn, alvo, 1 número (H), citação |
| **S6 · Foto-metade** | foto duotone ocupa metade (esq ou dir), texto na outra | depoimento, contexto humano |
| **S7 · Full-bleed foto** | foto duotone cobre tudo, título sobreposto (overlay) | divisória de seção (S7+duotone = usar com frequência) |

**Split 1/3·2/3 (S2) — gabarito:** coluna esquerda `width:560px` (de 1656 úteis) com eyebrow+título+lead alinhados ao topo; filete vertical opcional (`--hair-strong`, 1px) na divisa; conteúdo à direita a partir de `x≈760`. Título quebra em 2-3 linhas (Fraunces ~48-56px, peso 400). É o layout-cavalo-de-batalha — usar na maioria dos slides de conteúdo.

## Movimento (regra Flavio)
**Animação é EXCEÇÃO — quase nunca usar.** Default = estático. Se houver, máximo fade sutil único (~120ms, sem movimento/translate, sem stagger). Nada de "surgir debaixo", nada escalonado. Slide estático bem composto > slide animado.

## Princípios de composição
- **Legenda de gráfico = topo-direito do CONTEÚDO, abaixo do título, alinhada à direita, HORIZONTAL (regra Flavio).** As entradas ficam lado a lado (caixa-rótulo · caixa-rótulo), nunca empilhadas. Posição: dentro da área de conteúdo, canto superior-direito, logo abaixo do subtítulo. NUNCA empilhar verticalmente nem jogar no rodapé. (Registrado 2026-06-22.)
- **Rótulo de dado em TODAS as séries.** Num gráfico com 2+ séries (ex.: empilhado existente+novo), cada série leva seu próprio rótulo de valor — não só o total. O callout de leitura (o "olhe aqui") fica **ao lado da série que ele descreve**, com **linha-guia (leader)** apontando para ela; não solto num canto.
- **⚓ Alinhamento vertical = INFERIOR — REGRA CANÔNICA INVIOLÁVEL (Flavio, recorrente; reincidente 2026-06-22 e 2026-06-23).** O cabeçalho (eyebrow+título+lead) fica no topo; o **container de conteúdo** (da metade do slide para baixo) **ancora SEMPRE na base**, logo acima do `.foot`. Gabarito ÚNICO do container: `<div style="position:absolute;left:120px;right:120px;bottom:104px;">` com `align-items:end` nos grids internos. Se o conteúdo não preenche a altura, o respiro fica ENTRE o subtítulo e o conteúdo — o conteúdo assenta na baseline, nunca flutua no topo deixando vazio embaixo.
  - **PROIBIDO no bloco de conteúdo:** `margin-top:`, `top:<n>px`, `align-items:start`/`flex-start`. Qualquer um desses ancora no topo e deixa vazio embaixo = o erro recorrente.
  - **Se o conteúdo é alto e colide com o subtítulo estando ancorado na base:** a saída é **comprimir o conteúdo** (reduzir font-size/padding/densidade da tabela) OU encurtar o subtítulo. **NUNCA** trocar a ancoragem para `margin-top`/`top:`. A base é fixa; o que cede é a densidade. (Foi exatamente aqui que escorreguei na página de CMV — mudei p/ `margin-top` ao ver overlap, em vez de comprimir.)
  - **Checagem de finalização (todo slide, obrigatória):** `grep` o markup do slide por `margin-top` e `top:` dentro do container de conteúdo. Achou → está errado, troca por `bottom:`. A base do conteúdo deve cair na MESMA linha horizontal em todos os slides do deck.
- **Headline = Fraunces (peso 400)** para tom editorial; ênfase = itálico (Fraunces/Inter) ou uma palavra em `--ink`. **Nunca** caixa-alta pesada — elegância é peso baixo + tamanho + espaço.
- **Eyebrow** JetBrains Mono caixa-alta `--g2` em quase todo slide (âncora de seção).
- **Fios sempre têm função** (régua de título, divisor, filete de ênfase) — nunca enfeite solto. Régua dupla só no header; filete de accent no máx 1 por slide.
- **Profundidade = fio + espaço, nunca sombra.** Blocos com `border:1px solid var(--hair)` + fundo `--surface`; monograma marca-d'água a ~5%. PROIBIDO `box-shadow`/gradiente.
- **Densidade:** máx 1 diagrama OU 1 bloco de texto por slide. Se passar, quebra em 2 slides (arquétipo E/G escalam melhor que bullets empilhados).
- **Cor:** dominante grayscale (papel/tinta); **um** accent (bronze) para 1 destaque por slide. Modo e-ink remove o accent — o design não pode depender dele.

## Anti-padrões (= "sem graça")
- ❌ Mesmo layout (eyebrow+headline+body) em todo slide.
- ❌ Sombra/gradiente/glow em qualquer elemento (proibido no tema).
- ❌ Fio de enfeite no canto sem função.
- ❌ Bullets empilhados quando um diagrama (E/F/G) comunicaria melhor.
- ❌ Sans genérica Arial/Helvetica/Roboto, ou serifa no corpo — na identidade reThink o corpo é Inter (sans) e a serifa Fraunces fica só no título.
- ❌ Mais de um hue, ou depender do accent para a hierarquia (tem que ler em P&B).
- ❌ Bloco de conteúdo top-aligned/centralizado quando não preenche a altura (regra: ancorar na base — ver Princípios).
- ❌ Slide que só faz sentido com o apresentador narrando. Cada slide é **autoexplicativo (Minto)**: action-title afirma a resposta; o número total vem antes da composição; quem vê pela 1ª vez entende sem locutor.
