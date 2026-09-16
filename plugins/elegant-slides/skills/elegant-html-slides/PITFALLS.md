# PITFALLS.md — Armadilhas de engenharia e QA numérico

> Destilado de uma sessão longa editando um deck **data-driven** (motor JS: `prep()` recomputa o
> modelo, `bars()` desenha gráficos, tabelas e KPIs populados em runtime, slides reativos a cenário).
> O `SKILL.md`/Fase 4.5 cobre bem o **QA visual** (olhar o pixel). Este arquivo cobre o que faltou e
> onde eu mais errei: **QA numérico**, **decks orientados a JS/dados**, e **edição segura de HTML
> single-line**. Ler quando o deck COMPUTA números (não só texto estático) ou ao EDITAR um deck existente.

---

## 1. QA numérico — complementa o visual, não substitui

O QA visual (Read dos PNGs) pega layout. **Não pega número errado nem stale.** São dois modos distintos:

- **NÃO confie em ler número de PNG renderizado/escalado.** Já li um número por outro num PNG escalado — o screenshot reduzido engana. Para CONFERIR VALOR, leia o DOM:
  ```js
  // medir o valor real renderizado, não o olho no PNG
  [...document.getElementById('cf-body').querySelectorAll('tr')].map(tr=>
    [...tr.querySelectorAll('td')].map(c=>c.textContent.trim()))
  ```
- **`textContent`, nunca `innerText`.** Slide fora de tela (`.active`/`.visible` desligados) retorna
  `innerText === ''` — o innerText respeita visibilidade. `textContent` ignora. Toda extração de valor
  de slide não-ativo usa `textContent`.
- **Confira o índice da coluna.** Li `c[3]` (EBITDAprof) achando que era `c[4]` (LL). Antes de afirmar
  um valor, dumpe a linha inteira e confirme o mapeamento de colunas.
- **Toda ponte/cascata/derivado tem que FECHAR (foot) e cada linha tem que ter origem.** Ver §4.
- **Se há deck + modelo (Excel), cruze os dois.** Recompute o Excel (pycel) e compare linha a linha.
  Achei um gap pré-existente de LL deck↔Excel só porque cruzei.

Regra de entrega: **renderize E meça** os números-chave (DOM), não só "olhei e parece ok".

### Por que NÃO há teste automático de consistência numérica entre slides
Tentamos e provamos inviável genericamente (junho/2026): um check que extrai os valores e
flaga "mesmo rótulo, valores diferentes" falha dos dois jeitos — **(a)** table-aware dá
falso-positivo em tabela com mais de uma coluna de rótulo (ex.: "Produto + Frente" — "Ác.
Nítrico" Coleta vs Venda viram o mesmo rótulo), e quantas colunas são rótulo NÃO é genérico
(71 FP num deck limpo); **(b)** só-prosa cross-slide dá 0 FP mas **perde o stale real**,
porque em prosa a métrica vem antes OU depois do valor ("<valor> de EBITDA" vs "EBITDA de <valor>") e capturar os dois lados reintroduz o FP. **Baixo-FP e eficaz são incompatíveis sem
config por-deck** (declarar quais rótulos são a mesma métrica) — o que fere a genericidade.
Logo: consistência numérica fica **manual** (medir os números-chave pelo DOM, acima). Não
re-implemente como check genérico — um teste que não pega o bug que promete é falsa segurança.

---

## 2. Decks data-driven (JS) — a camada de dados é a fonte da verdade

Quando o deck computa em runtime (uma `prep()`/`render()` alimenta tabelas/gráficos/KPIs), o HTML
estático **mente** — só mostra os esqueletos vazios.

- **Não confie em extração estática.** Títulos/valores podem ser preenchidos por JS (`id` vazio no
  HTML). Quase adicionei títulos DUPLICADOS em slides que já tinham título via JS (`id="rc-title"`
  vazio no fonte, populado no `renderAll`). **Renderize** para ver o conteúdo real antes de mexer.
- **Funções de desenho são COMPARTILHADAS.** A `bars()` desenhava o gráfico de receita E o de EBITDA;
  uma edição mexeu nos dois. Antes de editar uma função, `grep` por todas as chamadas e saiba todos os
  consumidores.
- **Um gráfico tem MÚLTIPLAS referências ao mesmo dado** — altura da barra, rótulo do valor, máximo
  para a escala, título. Mudei a fonte de dados da ALTURA da barra mas deixei o RÓTULO no dado antigo
  (`prep(s).EBITDAprofajust` na barra, `D.scen[s].EBITDAprof` no label) → barra em 14,7 com rótulo 16,2.
  Ao trocar a fonte de um dado, troque TODAS as referências dele.
- **Use sempre o mesmo caminho de cálculo.** O comparativo lia o dado BRUTO armazenado (`D.scen[s].LL`,
  stale) enquanto a DRE usava `prep()` (recomputado). Resultados divergentes. Tudo que exibe deve
  consumir o `prep()`, não os arrays crus.
- **SVG tem viewBox próprio — confira a altura antes de adicionar elemento.** O `eb-svg` era
  `viewBox="0 0 1920 700"` e o `rc-svg` `...790`; adicionar conteúdo no eb-svg **cortou** o que passava
  de 700. Cheque o viewBox do SVG-alvo antes de inserir.

### A varredura de stale (a armadilha nº1 ao mudar uma métrica de base)
Quando introduz/altera uma métrica central (ex.: criar um "EBITDA ajustado" ao lado do reportado),
**dezenas de pontos** ainda apontam o valor antigo. Eu fui caçando um por um e sempre achava mais:
título do one-pager, card de KPI, base da sensibilidade (tornado), prosa de premissas, rótulo do
mini-gráfico, margem de um card. **Faça uma varredura sistemática:**
1. `grep` pelo valor/string antigos (`8,7M`, `16,2M`, `13,6M`, `normalizado`…) em TODO o arquivo.
2. **Texto E prosa** — não só tabelas; frases descritivas também citam o número.
3. **Render-meça** os pontos suspeitos (não confie no grep sozinho; valores JS não aparecem no grep).
4. Excua o bloco de DADOS (`D.scen`) da varredura — lá o valor reportado VIVE legitimamente; o que
   muda são as EXIBIÇÕES.
5. Itere até `grep` limpo + render dos slides afetados conferido.

---

## 3. Editar HTML — multi-linha (Edit) vs linha-monstro legada (replace)

**Deck gerado pelo `engine/data-deck.md` é multi-linha** (motor + `DATA` legíveis, nenhuma linha-monstro)
→ use a **ferramenta Edit** (diff por linha, mais barato e seguro). Numa sessão real, ~metade das 466
edições foram em título/HTML de linha curta que **não precisavam** de `python3 replace` — sub-uso do Edit.

A regra abaixo (Python string-replace atômico) vale **só para deck legado de linha-monstro** (motor/dados
concatenados numa linha de centenas de KB), onde a ferramenta Edit não casa:

- **`assert h.count(old)==N` antes de cada replace, e `open(...).write` só no FIM do batch.** Assim um
  assert que falha **não salva nada** (atômico). Salvou-me de um batch meio-aplicado.
- **Case na STRING ÚNICA, não no que você ACHA que é a fronteira.** Tentei casar `+"%"` mas o literal
  era `+"%</td></tr>"` → `count==0`, batch abortou. Quando em dúvida, case em identificadores únicos
  (`f(z.EBITDAprof[3])`, `id="..."`) em vez de pedaços de string que podem se estender.
- **Sempre valide `typeof window.deck === "object"` após edição em massa.** Um script que reconstruiu o
  HTML por `''.join(sections)` começando no 1º `<section>` DROPOU o preâmbulo (head/CSS/`deckStage`) →
  `new SlidePresentation()` quebrou em "Cannot read 'style' of null", `window.deck` undefined. Ao fatiar
  o HTML por seções, **preserve `parts=[s[:secs[0]]]`** (tudo antes da 1ª seção).
- **`!important` inline vence sua regra CSS.** Adicionei `.opg td{padding:9px}` e não pegou — havia um
  `<style>.opg td{padding:6px!important}</style>` inline. Procure `!important` antes de adicionar regra.
- **Adicionar um SLIDE desloca os índices** e quebra `deck.show(N)` da agenda e dos dividers
  (mini-agendas "Onde estamos"). Inserir no meio exige renumerar TODA a navegação subsequente. Prefira
  **append** no fim (mexe só na contra-capa) ou atualize cada `deck.show()` com cuidado.
- **Conteúdo ancorado embaixo (`position:absolute;bottom:104px`) encosta no rodapé quando cresce.**
  Adicionar 2 linhas à DRE deixou a tabela a **4px** do rodapé. Depois de adicionar linhas, MEÇA
  `tabela.bottom` vs `.foot.top`; se apertado, reduza o padding (a alavanca `.opg !important`, ~1-2px/linha,
  é imperceptível) — **mantendo a altura das linhas**, não comprimindo o texto.

---

## 4. Integridade analítica — a regra que mais importa

Esta passou do HTML para o número, e é a que custa mais caro.

- **NUNCA "conta de chegada" (plug).** Uma ponte cuja última linha existe só para fechar no alvo acordado é plug, e a pergunta
  "foi bottom-up ou conta de chegada?" sempre chega. **Cada linha
  de uma ponte/cascata tem que ter origem rastreável na fonte.** Se o bottom-up não bate no número alvo,
  **diga isso** (mostre o resíduo nomeado, ou que o alvo é negociado/aproximado) — não esconda num "outros".
- **Atribuição de fonte é fato, não conveniência.** Um deck já atribuiu um número a um laudo que não existia: o documento real era uma
  minuta anterior, e dizia outra coisa. Fact-check multi-fonte
  antes de cravar quem disse o quê. (Regra: não expor o autor com número/atribuição errada.)
- **Mudança de base cascateia — mapeie o cascateamento ANTES.** Trocar a base de um indicador toca DRE,
  one-pager, gráfico, comparativo, sensibilidade, LL, geração de caixa. Avise que cascateia e ofereça a
  decisão, em vez de mexer num slide e deixar o resto inconsistente.
- **Reportado vs ajustado é dualidade legítima — rotule.** Ao exibir um "ajustado", preserve o
  "reportado" onde ele é âncora (ex.: o slide que reconcilia o LL com a contabilidade fica reportado, com
  NOTA explicando as duas visões). Não force tudo a ajustado nem deixe os dois sem rótulo.

---

## 5. rclone / entrega (reforço)
- Subir `.html`/`.xlsx` ao SharePoint: **deletar antes de sobrescrever** + `--ignore-checksum
  --ignore-size` (o wrapper Office muda size/hash; round-trip OK). Validar com `rclone lsl` (delta de
  ~108 bytes no html = metadado Office, esperado). [[reference_sharepoint_html_upload_rclone]]
- Versionar `vN+1`, nunca sobrescrever (igual pptx).

---

## 6. A suíte de testes tem contrato implícito — e falha em VERDE quando o deck não o cumpre

> Origem: <issue>, 01/09/2026. `test-deck.py` passou **0 FAIL · 0 WARN** num deck com o texto
> sobrepondo o rodapé em dois slides. Quem pegou foi olhar o print renderizado. Gate verde não é
> prova de que está certo — é prova de que o teste conseguiu medir.

Três contratos que o deck **precisa** cumprir para a suíte enxergá-lo. Nenhum é validado, todos
degradam em silêncio:

- **O rodapé precisa ter a classe `.foot`, e a paginação `.pager`.** O probe monta
  `CHROME = '.foot,.topnav,.pager,.rulev,.title,.subt,.hd'` e mede `cont.bottom > foot.top`.
  Com qualquer outro nome (`.src`, `.pg`, `.fonte`), `foot` volta `null`, a asserção de
  sobreposição **não roda**, e o rodapé ainda é contado como conteúdo. Resultado: verde com
  sobreposição visível.
- **O controller precisa expor `window.deck.show(idx)`.** O probe começa com
  `if (window.deck && typeof window.deck.show === 'function') window.deck.show(idx)`. Se o método
  se chamar `go()`, ou se a instância não estiver em `window.deck`, o probe **nunca troca de
  slide** e você persegue um FAIL num slide que não é o que está sendo medido.
- **O índice do relatório é 0-based.** `FAIL [#6]` é o **sétimo** `<section class="slide">`.
  Cortar texto do sexto não muda nada, e parece que o teste está errado.

Nota: `CHROME` lista `.rulev`, mas a régua vertical do `design.md` é `.rule-v`. A régua não é
contada porque não tem `textContent`, então na prática não morde — mas não conte com isso ao criar
elemento decorativo com texto.

**Regra que fecha:** depois do gate verde, **capture os slides e olhe** (`--force-color-profile=srgb`,
`window.deck.show(i)` por slide, folha de contato 3×N). Custa ~40s e é o único passo que pega o que
o teste não sabe medir. Quem renomeia classe do tema herda a cegueira junto com o layout.

**Chrome para os scripts:** os scripts acham sozinhos (`$CHROME_BIN`, depois PATH, depois caminhos comuns de Linux e macOS). Para forçar: `--chrome /caminho/do/chrome`.
O `playwright.chromium.launch()` sem `executable_path` falha nesta VPS, o browser do Playwright
não está instalado.

## Falso positivo do `test-deck.py` em deck de posição absoluta (10/09/2026, Proposta C Acme)

O gate de browser acusou "conteúdo sobrepõe rodapé (cont.bottom 1066 > 1001)" e "conteúdo sobe sobre
título (cont.top 0)" em dois slides que, medidos pelo DOM a 1920×1080 com `transform:none`, terminavam
em 928 px. A sonda escolhe a folha mais baixa por `getBoundingClientRect` no viewport do teste, e em
deck com `.slide` absoluto e stage escalado a medida sai deslocada. **Antes de corrigir um FAIL de
sobreposição, meça você mesmo:** liste os filhos do `<section>` com `top`/`bottom` em px de palco e
compare com 271 e 1001. Se bate, registre a divergência e siga; o gate ainda não tem esse caso coberto
por `tests/test_gates.py`.
