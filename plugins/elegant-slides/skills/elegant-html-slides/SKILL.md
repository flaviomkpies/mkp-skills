---
name: elegant-html-slides
description: "Deck HTML single-file 16:9 na identidade reThink/reMarkable — branco, P&B, serifa nos títulos, régua vertical. Use para 'slides reMarkable', 'deck branco editorial', 'deck sóbrio/e-ink'. Para .pptx use /elegant-html-to-pptx."
---

# elegant-html-slides

Motor de slides HTML de tela fixa 16:9 (fork enxuto do `frontend-slides` de zarazhangrui) **travado no tema editorial Elegant / reMarkable**. O upstream pergunta o estilo e oferece 46 templates; aqui não há escolha de estilo — o design system em `design.md` (papel + serifa + fios, accent único toggleável, modo e-ink P&B) é a única fonte visual. O que se decide é **conteúdo e densidade**, nunca a estética. Tema neutro: sem logo/marca de empresa.

Output: **um arquivo HTML self-contained** (CSS/JS inline), 16:9 em qualquer tela, navegável por teclado/touch, exportável pra PDF.

## ⚠️ Identidade vigente (05/09/2026)

O tema branco/Fraunces das seções abaixo ficou para trás: a Régua de hoje é a dos decks **W1/W2 Acme**
(Literata + Inter, numerais laranja, **fotos em colunas e em fundo full-bleed**, chevrons, diagramas).
Leia **`design.md §Régua W2`** antes de gerar e, se houver deck anterior do tema, **abra o pptx mais
recente e olhe 5–6 páginas**: ele é a fonte, não este arquivo.
Regra do autor: **nunca um slide chato,
o design representa a ideia**; lista numerada só quando a ordem é o conteúdo. Para `.pptx`, o caminho
preferido virou clonar arquétipos (`/elegant-html-to-pptx` §método W2).

**Entrega que ele assina como aluno é a exceção**, e ela suspende a regra acima: chrome da Régua,
repertório gráfico desligado, base de texto pesada — `design.md §Exceção sancionada — entrega acadêmica`.

## Quando NÃO usar
- Documento corrido (`.docx`) → skill de docx.

## Fronteira de entrega (decisão — HTML × PPTX)
**HTML é a entrega final** para: web, leave-behind navegável, apresentação em tela, link/Vercel, e PDF (via `export-pdf.sh`, com modo e-ink P&B pra reMarkable). É o formato canônico desta skill.
**Quem vai EDITAR no PowerPoint → `/elegant-html-to-pptx`** (criada em 22/07/2026, mora no vault). Ela reconstrói o deck **shape a shape em PowerPoint nativo**, com o palco 1920×1080 mapeado 1:1 (6350 EMU/px, 0,5 pt/px): cada texto vira caixa clicável, fio vira retângulo, barra vira shape. Só simbologia complexa (gráfico de linha com dezenas de pontos, glifo desenhado à mão) entra como imagem. Medido no caso IMC 20/08/2026: **99,5/100**, cobertura textual 100%, 322 caixas nativas contra 1 imagem em 15 slides.
> ⚠️ Esta linha dizia, até 20/08/2026, "NÃO converter este HTML→pptx editável (…) perda garantida", e o meio-termo era empacotar screenshots. Ficou **obsoleta** quando a skill irmã nasceu e provou o contrário; o aviso sobrevivente fazia agente parar e refazer o deck do zero. Screenshot 1-por-slide segue existindo como último recurso, não como o caminho.

## Arquivos
| Arquivo | Papel | Quando ler |
|---|---|---|
| `design.md` | Tema Elegant/reMarkable → palco de slide (tokens, fontes web Fraunces/Literata/JetBrains Mono, escala 1920×1080, modo e-ink). Sem marca de empresa. | SEMPRE antes de gerar |
| `LAYOUTS.md` | 10 arquétipos de slide + anti-padrões. Escolher arquétipo por tipo de conteúdo. | Antes de gerar |
| `VOICE.md` | Voz do autor adaptada a slide (DNA de `/writing`). Travessão zerado, sem hipérbole, números concretos. | Antes de redigir texto |
| `snippets.html` | Blocos copy-paste do tema (papel, régua dupla, drop-cap, filete de accent, pull-quote, KPI, divisória). | Geração |
| `scripts/validate.sh` | Checagem determinística (estrutura/marca/a11y) antes de entregar. | Antes de entregar |
| `CHARTS.md` | Receitas de data-viz do tema (grayscale + 1 accent; waterfall, barras, tornado, KPI…) + anti-padrões. | Ao desenhar gráfico |
| `PITFALLS.md` | Armadilhas de engenharia + **QA numérico** (deck data-driven/JS, edição segura de HTML single-line, regra do "sem plug"). | Deck que COMPUTA números ou ao EDITAR um existente |
| `scripts/test-deck-static.py` | **Tier 0 — estático, SEM browser (~50ms):** regras de texto por `<section>` (ponto final, aritmética, travessão, bola), estrutura/navegação (`deck.show` em range, controller, R$ k). Gate rápido. Sai 0/1. | Fase 4.5 — **1º gate, sempre** |
| `scripts/test-deck.py` | **Tier 1 — browser/Playwright (~s):** só o que depende de render — sobreposição (altura dinâmica), título/valor populado por JS, console, variedade de fonte. Sai 0/1. | Fase 4.5 — após o Tier 0 |
| `scripts/slop-audit.py` | **Camada 2 (Haiku):** anti-AI-slop semântico (hedging, clichês, filler, CTA, recomendação em material neutro, action-title=rótulo) + teste "história pelos títulos". Sinaliza, não reprova. | Fase 4.5 — antes de entregar |
| `engine/viewport-base.css` | CSS base do palco fixo 16:9. **Incluir INTEGRAL** em todo deck. | Geração |
| `engine/html-template.md` | Arquitetura HTML + controller JS (scaling, nav, edição inline) | Geração |
| `engine/deck-stage.js` | Implementação completa de scaling+navegação+edição (inline no HTML) | Geração |
| `engine/data-deck.md` + `data-deck-example.html` | **Deck número-pesado:** single source `DATA` + `renderAll` (título/KPI/tabela/gráfico saem de 1 lugar → mata o stale-rework). | Gerar BP/financeiro |
| `scripts/model-to-data.py` | **Excel (aba DECK) → bloco `DATA` do deck** (`--update-deck`). Deck e modelo = 1 fonte, zero transcrição. | Gerar/atualizar deck do modelo |
| `engine/components-example.html` | **Componentes de dado testados** (kpiRow · dataTable · barChart · waterfall) — copie + ligue DATA. Excelência por construção, passa a suíte. | Montar slide analítico |
| `engine/layouts-example.html` | **Layouts narrativos testados** (cardsRow · hubSpokes · staircase · processFlow), portados do catálogo `um catálogo de padrões de marca`. | Montar slide conceitual/diagrama |
| `engine/animation-patterns.md` | Referência de animações CSS/JS | Geração |
| `scripts/extract-pptx.py` | Extrai conteúdo de .pptx | Modo conversão |
| `scripts/export-pdf.sh` | Exporta o HTML pra PDF (Playwright) | Export |

---

### Camada opcional — "Prova revisada"
Deck que pede calor humano/didático (workshop, aula): ver `design.md §Prova revisada` — camada de caneta (ícones rough, sublinhado-GIF, marginália Caveat) por cima da Régua digital. Conceito o autor 21/08/2026.

## Workflow

### Fase 0 — Detectar modo
Deck novo · conversão de `.pptx` · ou edição de HTML existente.

### Fase 1 — Conteúdo + densidade (única pergunta ao usuário)
Pergunte de uma vez: **objetivo**, **nº de slides aprox.**, **conteúdo já pronto ou a redigir**, e **densidade**:

| Densidade | Pra quê | Comportamento |
|---|---|---|
| **Baixa / palco** | talk, keynote, ao vivo | 1 ideia/slide, tipo grande, 1–3 bullets |
| **Alta / leitura** | report, handout, async | slides auto-contidos, grids/tabelas, 4–8 bullets ou 4–6 cards |

Baseline sempre: sem scroll, sem overflow, sem sobreposição.

> **NÃO** pergunte o estilo. O estilo é o tema Elegant/reMarkable (`design.md`), travado. Única escolha estética válida: **modo Elegant (com accent) vs e-ink (P&B)** — defina pelo destino (tela/board → Elegant; impressão/reMarkable → e-ink).

### Fase 2 — ~~Style discovery~~ (REMOVIDA)
Não gerar previews nem oferecer templates. O tema é fixo.

### Fase 2.5 — Narrativa + VOZ (consulting-grade, ANTES de estilizar)
Estruturar o argumento, não só o visual. Um deck bonito sem tese é forma vazia.
**Voz = do autor (`VOICE.md`), não consulting genérico.** Ler `VOICE.md` (adapta o DNA de `/writing` pra slide) antes de escrever qualquer título/texto. Regra dura: **travessão "—" zerado** · sem hipérbole · números concretos com fonte · palavras simples · sem maiúscula após dois-pontos · IA não AI · fechamento sem CTA inspiracional.
1. **Pirâmide:** resposta/conclusão primeiro; dados sustentam, não antecedem.
2. **Action-titles:** cada título de slide é a **conclusão (so-what)**, frase completa — não rótulo. "Conecto estratégia e IA aplicada a serviços profissionais" > "Quem sou".
3. **Lógica horizontal:** ler SÓ os títulos, em sequência, deve contar a história (S→C→R). Se não fecha, reordene/reescreva.
4. **MECE + SCR** dentro de cada slide; 1 ideia por slide.
5. **Arco do deck (so-what → now-what):** abre com **síntese executiva** (a resposta + os pilares de apoio, logo após a capa — não no fim), desenvolve provando cada pilar (MECE), e **fecha com recomendação acionável** (SMART: o quê · quem · quando · quick wins). Parar no insight é meia-pirâmide: tem o "so what", falta o "now what". Arquétipos `Síntese executiva` e `Recomendação` no `LAYOUTS.md`.
6. **Enquadrar o problema** (deck que analisa/decide): a 1ª página de conteúdo declara a **pergunta** (SMART) + critério de sucesso. Sem isso, o leitor não sabe o que está sendo respondido (McKinsey: definição ruim = raiz do projeto ruim).
7. **Destilar e dissentir:** cortar todo slide que não move a tese (DISTILL — se não cabe na storyline, por que está aí?); declarar a **fronteira** no rodapé (o que ficou de fora e por quê — sem corte silencioso); quando o número favorece a tese, incluir a **visão contrária** com lógica e fato (obrigação de dissentir).
Escrever os action-titles dos N slides ANTES de tocar no HTML e conferir que, lidos juntos, formam a narrativa **começando pela resposta e terminando na ação**.
8. **Resultado antes do detalhe (Minto na vertical):** todo bloco analítico abre pela conclusão/número, não pela mecânica. Dado denso (DRE por produto, custos por linha) vira **2 slides**: pág. de resultado (a leitura agregada, gráfico) seguida de pág. de detalhe (a tabela densa). Nunca abrir com a tabela e deixar o leitor garimpar o so-what.

> Origem destes pontos: *McKinsey Approach to Problem Solving* (Staff Paper 66) + *Pyramid Principle* (Minto). Pirâmide = resposta no topo; SCR = Situação·Complicação·Resolução; os 3 testes da pirâmide (pra baixo: gera 1 pergunta? · horizontal: MECE? · pra cima: forma um "so what"?).

### Fase 3 — Gerar

**Escada de reuso — pare no primeiro degrau que serve:**

1. `engine/components-example.html` — `kpiRow` · `dataTable` · `barChart` · `waterfall`. Testados, passam a suíte. Tabela e gráfico de barras NÃO se escrevem à mão.
2. `engine/layouts-example.html` — `cardsRow` · `hubSpokes` · `staircase` · `processFlow`.
3. Deck anterior do mesmo tema — ⚠️ **copiar o gerador de um deck anterior propaga os atalhos dele.** Se aquele deck posicionou tudo em pixel absoluto e escreveu tabela à mão, você vai herdar a classe de defeito junto com o layout. Antes de copiar, cheque se o que você precisa está nos degraus 1-2.
4. Escrever do zero — só quando 1-3 genuinamente não cobrem, e nesse caso o novo componente volta para `engine/` no fim.

> Origem: caso CAPM/Petrobras 21/08/2026. Escrevi `dataTable` e `barChart` do zero duas vezes (HTML e PPTX) com os componentes prontos a um `Read` de distância — porque copiei o gerador do deck anterior, que também os tinha escrito à mão. Custo medido: ~250s de geração mais a classe de sobreposição que componente testado não produz.

Antes de gerar, **leia**: `design.md` (sistema visual) + `engine/viewport-base.css` + `engine/html-template.md` + `engine/deck-stage.js` (+ `animation-patterns.md` se precisar).

**Deck número-pesado (BP, modelo financeiro, número que repete em vários slides):** seguir `engine/data-deck.md` — um `const DATA` único alimenta tabelas, gráficos, KPIs **e os action-titles**; **nenhum literal numérico no output exibido** (tudo via DATA + helper de formato). Mata a varredura de stale ao mudar uma base (muda 1 lugar, propaga).

Regras do palco fixo (**NÃO-NEGOCIÁVEIS**, do motor upstream):
- Canvas 1920×1080 escalado como um todo. 16:9 em toda tela, inclusive celular. Não reflowar conteúdo por dispositivo.
- Escala uniforme só (transform no `.deck-stage`); sem breakpoints que rearranjam.
- Slides com `.active`/`.visible` via `visibility`/`opacity`/`pointer-events` — nunca `display:none`.
- Incluir o conteúdo INTEGRAL de `viewport-base.css` no `<style>`.
- `clamp()` só fora do palco. Nunca negar funções CSS direto; use `calc(-1 * clamp(...))`.
- Incluir suporte a `prefers-reduced-motion`.

Aplicar `design.md`: tokens via CSS vars, tipografia (Fraunces/Literata/JetBrains Mono), ritmo de espaçamento, gramática de fios (régua dupla, filete de accent, hairlines), modo Elegant vs e-ink. Valores fluidos viram coordenadas no palco 1920×1080 (proporções, não regras de reflow vivo).

**Escrita consulting:** título de slide = action-title (afirmação, não rótulo) · estrutura pirâmide (resposta primeiro) · SCR onde couber · bullets MECE. Slide sem action-title é rótulo, não mensagem.

Output: 1 HTML self-contained · CSS/JS inline · fontes web (nunca system font) · comentários `/* === SEÇÃO === */` · edição inline incluída por padrão (controller do `html-template.md`/`deck-stage.js`).

### Fase 4 — Conversão de .pptx
`python3 scripts/extract-pptx.py <in.pptx> <out_dir>` → confirmar títulos/contagem → gerar HTML preservando texto, ordem e imagens (notas como comentários HTML). Sem fase de estilo (tema travado).

### Fase 4.5 — Auto-crítica visual (OBRIGATÓRIA antes de entregar)
Nunca entregar um deck que a skill não OLHOU. Loop:
1. **Suíte de testes em 3 tiers (rápido → caro):**
   - **Tier 0 — estático, ~50ms (1º gate, sempre):** `python3 scripts/test-deck-static.py deck.html [--forbidden "nome1,nome2"]` → **zero FAIL**. Texto por `<section>` (ponto final em título/subt/bullet, aritmética em prosa, travessão, bola), navegação (`deck.show` em range, controller), magnitude k×mil, marcadores de rascunho/pergunta em aberto, "Fonte" em slide sem dado. `--forbidden` = termos do projeto (nomes internos/codinomes).
   - **Tier 1 — browser, ~s (só o que depende de render):** `python3 scripts/test-deck.py deck.html` → **zero FAIL** (sobreposição com altura dinâmica, ancoragem inferior, largura do subtítulo vs título, alinhamento da agenda, título/valor populado por JS, console, variedade de fonte). Mais `bash scripts/validate.sh deck.html` (estrutura/fontes do tema) e `bash scripts/contrast-audit.sh deck.html` (WCAG AA; texto ink/g1 sobre papel passa folgado — o accent bronze é decorativo, não texto-corpo; no modo e-ink o accent some e os fios seguram a hierarquia).
   - **Tier 1b — artefatos gerados (~ms, sem browser):**
     `python3 scripts/check-svg.py *.svg` → todo `<text>` dentro do viewBox, medido pelas
     métricas reais da fonte. Pega o rótulo cortado que o SVG válido não denuncia.
     Se o deck virou `.pptx`: `python3 <lib>/check_pptx.py deck.pptx --fontes "..."` →
     texto sobre texto, tinta fora do palco, `<p:style>` (sombra do tema), conector como fio.
     **Emita `xmlns` nos SVGs**: sem ele o arquivo parseia sem namespace e ferramenta
     externa "não acha" texto nenhum.
   - **Tier 2 — semântico (Haiku):** `python3 scripts/slop-audit.py deck.html` → flags de AI-slop/voz (hedging, clichê, filler, afirmar o óbvio, recomendação em material neutro, action-title=rótulo, subtítulo=paráfrase) + teste "história pelos títulos". **Sinaliza, não reprova.** Usa `ANTHROPIC_API_KEY` (portável) ou, no workspace de origem, `claude -p` (OAuth) automático.
2. `bash scripts/export-pdf.sh deck.html /tmp/qc.pdf` + `pdftoppm -png -r 70 /tmp/qc.pdf /tmp/qc` → **Read cada PNG**.
3. Criticar cada slide contra o checklist (**uma a uma** — o erro nº1 só aparece olhando a página individual, não o contact-sheet):
   - [ ] **sem sobreposição** (erro mais frequente): tabela/chart subindo no título, painéis empilhados, decoração por cima do texto. Padrão de correção: **conteúdo denso/full-height flui do topo** (ancorar embaixo faz a tabela alta subir sobre o título); conteúdo que não preenche a altura, sim, ancora embaixo.
   - [ ] nada estoura o palco (texto cortado, painel fora dos 1920×1080, decoração saindo errado)
   - [ ] elemento decorativo aparece (cuidado: stroke-draw some no screenshot — ver WARN do validate)
   - [ ] contraste do texto legível (tinta/cinza sobre papel; no slide tinta, papel sobre tinta)
   - [ ] área morta grande? slide vazio demais = falta conteúdo ou layout errado
   - [ ] action-title legível e carrega o so-what
   - [ ] arquétipos variam ao longo do deck (não repetir 1 layout)
   - [ ] **lendo só os títulos**: começa pela resposta e termina na ação? a história fecha (S→C→R)?
   - [ ] tem **síntese executiva** no início e **recomendação acionável** no fim (não para no insight)?
   - [ ] todo gráfico/tabela de análise tem **kicker** apontando o so-what + **fonte** no rodapé?
   - [ ] decomposição/ranking declara a **fronteira** (o que ficou de fora)?
4. Corrigir e **re-renderizar** até passar. Só então entregar.

### Fase 4.6 — QA numérico (OBRIGATÓRIA se o deck computa/exibe números) — ler `PITFALLS.md`
O QA visual pega layout; **não pega número errado nem stale**. Se há tabelas, KPIs, gráficos com valor,
ou um motor JS (`prep()`/`render()`):
1. **Meça os números pelo DOM, não pelo olho no PNG** (screenshot escalado engana). `textContent`,
   nunca `innerText` (vazio em slide fora de tela).
2. **Toda ponte/cascata FECHA e cada linha tem origem.** **NUNCA conta-de-chegada/plug** para bater num
   alvo — se o bottom-up não bate, mostre o resíduo nomeado ou diga que o alvo é aproximado/negociado.
3. **Ao mudar uma métrica de base, varra TODAS as referências** (tabelas, KPIs, base de sensibilidade,
   rótulos de gráfico, prosa, títulos): `grep` pelo valor antigo + render-meça os pontos. Valores JS não
   aparecem no grep — confira renderizado.
4. **Um gráfico referencia o dado em vários lugares** (altura da barra, rótulo, escala, título) — troque
   todos. **Funções de desenho são compartilhadas** — cheque todos os consumidores antes de editar.
5. Se há modelo Excel paralelo, **cruze deck↔modelo** (recompute pycel).

### Fase 4.7 — A suíte se testa (rodar quando mexer em QUALQUER gate)

```bash
python3 tests/test_gates.py <deck_bom.html> [deck_bom.pptx]
```

Injeta um defeito conhecido por vez e exige que o gate correspondente pegue, e exige que
nenhum gate morda o artefato bom. **Um gate que para de morder é uma regressão silenciosa:**
o detector de fundo de conteúdo do `test-deck.py` ficou cego por meses porque procurava
`position` no `style` inline enquanto a identidade Régua marca por classe — passou 0 FAIL
em páginas quebradas até 21/08/2026. Nada testava o testador.

Corolário para qualquer gate novo: se o seletor não achar nada, **diga que não achou**.
Três ferramentas diferentes nesta casa já imprimiram sucesso medindo o conjunto vazio.

### Fase 5 — Entrega
Abrir no browser, explicar navegação (setas/espaço/touch, `E` = editar).
**Versionar como apresentação:** nome com prefixo de data + `vN+1` (ex. `20260622_nome_v3.html`), **nunca sobrescrever** a versão anterior, HTML e PDF lado a lado, histórico preservado. Mesma disciplina de `.pptx`.

### Fase 6 — Share/Export (opcional)
- PDF: `bash scripts/export-pdf.sh <arquivo.html>` (1ª vez instala Playwright; use `--compact` pra reduzir). **P&B reMarkable:** setar `--accent:var(--ink)` no `:root` (modo e-ink, ver `design.md`) antes de exportar — o tema já é grayscale-safe.

---

## Crédito
Motor base: [frontend-slides](https://github.com/zarazhangrui/frontend-slides) (zarazhangrui), MIT — `engine/LICENSE-frontend-slides`. Adaptação Elegant/reMarkable: design system editorial travado (papel + serifa + fios, modo e-ink) + escrita consulting + remoção da escolha de estilo.
