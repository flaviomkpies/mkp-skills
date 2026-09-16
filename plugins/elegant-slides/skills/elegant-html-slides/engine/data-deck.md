# Deck data-driven — single source de números (decks número-pesados)

Para BP / modelo financeiro / qualquer deck onde **o mesmo número aparece em vários slides**.
Resolve o custo que mais doeu numa sessão real: mudar uma base (um indicador que muitos slides
citam) e ter
que caçar ~10 referências stale uma a uma. Com esta convenção, **muda 1 lugar e propaga**.

> Deck simples (texto estático, sem números repetidos)? **Não use isto** — segue o `html-template.md`.

## Exemplo executável (a referência do PADRÃO de dados)
**`engine/data-deck-example.html`** — 3 slides (capa+KPI, tabela, gráfico) onde título, KPI,
tabela e barras saem todos de um `const DATA`. Provado: 1 edição em DATA propaga para as
superfícies que dependem dela; nenhuma linha passa de ~160 chars (vs 318KB numa linha no deck
que improvisou isso). Roda limpo nos `scripts/test-deck-static.py` + `test-deck.py` (0 FAIL/WARN).

> Copie a **camada de dados** (DATA + funções de render + `window.deck`), não o CSS — que é mínimo
> de propósito. O chrome visual (palco, fontes, cores, componentes) vem de `viewport-base.css` +
> `design.md` como em qualquer deck. Este exemplo isola o padrão, não substitui o design system.

## De onde vem o DATA: o modelo Excel (`scripts/model-to-data.py`)
A fonte única **estende ao modelo** — o `DATA` é gerado do Excel, não transcrito à mão (foi a
transcrição manual que gerou o gap deck↔Excel de ~R$222k/ano numa sessão real). Deck e modelo
viram **uma fonte só**, impossíveis de divergir.

Duas pontas da convenção:
1. **No modelo** — uma aba **`DECK`** tidy: linha 1 = `key | ano1 | ano2 | …` (vira `DATA.years`);
   cada linha `<key> | <v1> | <v2> | …` vira `DATA[key]=[v…]`; 1 valor de texto vira escalar
   (`company`, `fonte`). É o único lugar com número de negócio. Exemplo: `data-deck-example-model.xlsx`.
2. **No deck** — o bloco `DATA` fica entre `/* DATA:START */` e `/* DATA:END */`. O extrator reescreve
   só entre os marcadores; o resto do deck não muda.

```bash
python3 scripts/model-to-data.py modelo.xlsx --update-deck deck.html   # modelo → deck
python3 scripts/model-to-data.py modelo.xlsx                           # só imprime o bloco DATA
```
Mudou o modelo → re-roda → deck atualiza (provado: 1 célula no Excel propaga pra KPI+título+tabela+gráfico).
**Caveat:** salve o modelo com valores calculados (Excel/LibreOffice) — `data_only` lê o cache, não recalcula fórmula.

## Catálogo de componentes testados (`components-example.html`)
Arquétipos prontos e **vetados pela suíte** (0 FAIL/WARN) — gerar um slide vira **escolher + ligar o
DATA**, não desenhar layout e iterar. Excelência por construção: sem overlap, ancoragem certa,
action-title, e altura/rótulo/escala saindo da **mesma** série. Copie a função + o CSS dela pro deck.
- **`kpiRow(alvo, items[{label,value}])`** — linha de N cards de KPI (largura auto).
- **`dataTable(alvo, cols[], rows[{label,values[]}])`** — tabela de séries por ano.
- **`barChart(svg, labels[], values[])`** — barras de uma série.
- **`waterfall(svg, steps[{label,value,type}])`** — ponte/cascata (âncora `abs` cheia + `delta` flutuante; peso).

Layouts narrativos (`layouts-example.html`, portados do catálogo de padrões de layout):
- **`cardsRow(alvo, cards[{n,title,body}])`** — N cards de síntese (3col_cards / payoff).
- **`hubSpokes(svg, hub, spokes[])`** — mapa conceitual: hub central + satélites.
- **`staircase(svg, steps[{label,sub}])`** — trajetória/ambição em degraus ascendentes.
- **`processFlow(alvo, steps[{label,sub}])`** — cadeia de valor / input→processo→output.

Cresce: arquétipo novo, **uma vez vetado contra a suíte**, entra aqui. É ponto de partida, não camisa
de força — slide bespoke continua possível.

## As 3 regras
1. **Um `const DATA = {...}` = a fonte da verdade.** Séries por ano/cenário. É o único lugar com
   números de negócio. Multi-linha, uma chave por linha.
2. **`renderAll()` + funções de componente populam tudo de DATA** — tabelas, gráficos, KPIs **e os
   action-titles** (`el.textContent = "A receita cresce de " + m(DATA.receita[0]) + " a " + m(last)`).
   `<section>`s têm `id` vazios; o JS preenche. Um gráfico tira altura, rótulo, escala e título do
   **mesmo** `DATA.serie` (mata o bug "rótulo 16,2 vs barra 14,7").
3. **Nenhum literal numérico no output exibido.** Título/subtítulo/KPI/prosa/rótulo passam por DATA +
   um helper de formato (`m()`). Se você digitou "R$8,7M" no HTML, errou — vira stale na próxima
   mudança de base.

## Legibilidade (o que destrava a edição barata)
`DATA` e as funções de render são **multi-linha indentadas** — um statement/linha, uma linha de array
por linha. **Nunca concatenar o motor numa linha-monstro.** Assim a ferramenta **Edit** funciona
(diff por linha), `grep` acha o dado, e a suíte de testes lê. (No deck legado que era 1 linha de
318KB, toda edição virava `python3 replace` — caro e propenso a erro.)

## Controller + gate
Use o controller do `html-template.md` (`SlidePresentation`), expondo `window.deck` com `show(i)`
(o exemplo faz isso — necessário para os testes e para `deck.show(N)` de agenda). Antes de entregar,
rode a suíte (Fase 4.5): com DATA single-source, uma mudança de base propaga e os testes **confirmam
a consistência numa passada**, em vez do sweep manual.
