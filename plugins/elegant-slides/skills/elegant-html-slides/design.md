# design.md — reThink / reMarkable workbook identity (palco 1920×1080)

> Design system **editorial monocromático**, modelado na identidade do workbook
> **reThink / Annual Review** (reMarkable × Farnam Street). Branco, tinta quase-preta,
> **serifa só nos títulos + sans no corpo**, régua vertical à esquerda como assinatura,
> nav de seções no topo. Calmo, caro, sem cor (cor só em link). Sem marca de empresa.
>
> **Variante alternativa (papel quente "Elegant"):** ver §Variantes no fim — um toggle de
> tokens + fonte de corpo. O default desta skill é a identidade reMarkable branca.

## Princípio
Hierarquia vem de **tipografia (serifa × sans), peso, espaço e fios** — nunca de cor ou sombra.
Muito respiro. A serifa de alto contraste aparece **só nos títulos**; tudo que se lê em quantidade é **sans**.

## Fontes (no `<head>` de todo deck)
```html
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;1,9..144,400&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
```
- **Fraunces** — serifa display de alto contraste (opsz alta). **Só títulos, numerais grandes, citações.** É o "elegante".
- **Inter** — grotesco neutro (escolhido por bater nas métricas/quebras da fonte da reMarkable). **Corpo, subtítulos (bold), nav, labels, rodapé.** É o "papel". (alternativa de tom mais quente: Inter.)
- Fallback: `Georgia, serif` (display) · `system-ui, sans-serif` (corpo).
- **Nunca** serifa no corpo (inverte a identidade); **nunca** Arial/Inter/Roboto (sans genérica/slop).

## Tokens (cole no `:root`)
```css
:root{
  --paper:#FCFCFC;        /* fundo branco (quase puro; pode ser #FFFFFF) */
  --ink:#141414;          /* tinta quase-preta, alto contraste */
  --g1:#4A4A4A;           /* texto secundário, subtítulo de seção */
  --g2:#7C7C7C;           /* nav inativo, rodapé, legenda */
  --hair:#DADAD6;         /* régua fina, divisória, fio de topo */
  --rule:#141414;         /* régua de assinatura (vertical à esquerda + barra do título) */
  --link:#3F46C4;         /* ÚNICA cor do tema — só em link (azul/índigo) */
  --stage-bg:#22232A;     /* moldura fora do slide */
  --slide-bg:var(--paper);
  --serif:'Fraunces',Georgia,serif;
  --sans:'Inter',system-ui,sans-serif;
}
```
**Proibido:** gradiente colorido · `box-shadow` · qualquer hue além do `--link`. Imagem só em **duotone B&W**.
**Exceção sancionada:** as tintas de caneta da camada **Prova revisada** (ver §Prova revisada) e logos/imagens externas em cor.

## Assinatura visual — a régua à esquerda (NÃO opcional)
Toda página de conteúdo tem:
1. **Fio vertical fino** de altura cheia na margem esquerda: `position:absolute;left:104px;top:0;bottom:0;width:1px;background:var(--hair)`.
2. **Barra grossa curta** em `--ink` ao lado do título de seção, na altura do título: `position:absolute;left:103px;width:4px;height:<altura do título>;background:var(--ink)`.
A barra grossa sobrepõe o fio fino na altura do título. É o elemento que diz "reMarkable".

## Nav de seções no topo (running header)
Lista horizontal das seções do deck, item ativo em **bold ink**, demais em `--g2` regular:
```html
<div class="topnav"><span><b>Intro</b></span><span>Annual review</span><span>Mental models</span><span>Clear thinking</span></div>
```
`font-family:var(--sans);font-size:25px;` · gap ~44px · em `top:54px`, alinhado ao início do conteúdo.
**Pager à direita (assinatura reThink):** no canto superior-direito da nav, `‹  04 / 13  ›` (chevrons + posição/total), em `--g2`. É o "Level X of 11" do reThink. Com o pager no topo, o **rodapé fica só com a fonte/seção** (não duplica o número).

## Tipografia no palco (1920×1080)
| Papel | Fonte | Tamanho | Peso | Notas |
|---|---|---|---|---|
| Nav de topo | Inter | 26px | 400 / **700** ativo | `--g2` inativo, `--ink` ativo |
| Título de seção (conteúdo) | Fraunces | 92–104px | 400 | grande, com muito ar; barra grossa à esquerda (seletiva — nem toda página) |
| Título de divisória/capa | Fraunces | 130–160px | 400 | centralizado na capa; à esquerda na divisória |
| Subtítulo de seção | Inter | 32–34px | 400 | `--g1` |
| Lead / abertura | Inter | 33px | **700** | parágrafo de entrada em bold |
| Subhead | Inter | 31px | **700** | mesma escala do corpo, só bold |
| Corpo | Inter | 30px | 400 | line-height 1.5, espaço generoso entre parágrafos |
| Citação | Fraunces | 72–84px | 400 | com a barra grossa à esquerda; atribuição em sans itálico |
| Rodapé / legenda / link | Inter | 22px | 400 | `--g2`; link sublinhado em `--link` |

Alinhamento à **esquerda** (capa/divisória podem centralizar). Medida confortável ~30–34em. Sem ponto final em título/subtítulo; minúscula após dois-pontos. Parágrafos separados por linha em branco (respiro), não por recuo.

## Composição
- **Conteúdo flui do topo** (como o reThink): header (nav + título) no topo; o bloco de conteúdo começa numa linha fixa logo abaixo do título (`.cb{position:absolute;left:150px;right:140px;top:360px}`) e flui para baixo, com respiro entre título e conteúdo. Página curta deixa a base em branco, é o respiro do reThink, não erro. (NÃO ancorar à base nesta identidade.)
- **Subhead bold + parágrafo(s) sans** é o padrão de bloco (como "The tools inside", "Why this works").
- Rodapé: fonte/seção à esquerda (`--g2`); o número fica no **pager** do topo-direito.

## Linhas e listas — o "tabular" do reThink (preferir a cards)
A gramática estruturada do reThink são **linhas separadas por fio horizontal full-width** (atravessam a página inteira), não cards com borda. Três componentes (em `snippets.html`):
- **Label-row (empilhada):** cada item = um fio full-width + **rótulo bold** + *texto-guia itálico* (microcopy `--g1`) + conteúdo. Use para "decisores", "passos do método", "ondas", "Goal/Success metric/Next 30 days". Empilhar 3–4 linhas full-width > cards lado a lado.
- **Lista numerada:** `1. 2. 3.` com fio full-width entre cada (como "top 10 goals"). Para listas/enumerações.
- **Duas colunas com divisor vertical:** só quando são 2 lados em paralelo (ex.: "baixo risco × alto risco"); fio vertical fino no meio + rótulos bold no topo de cada.
- **Microcopy em itálico:** prompts/legendas de campo em *itálico* `--g1` (ex.: "*como você mede o sucesso?*"). É marca registrada do reThink — usar nas linhas estruturadas.

## Imagem (duotone B&W) — opcional, e SEMPRE própria
Imagem é **opcional**. O default da capa/divisória é **tipográfico limpo** (título serifa + subtítulo, fio, rodapé) — quase sempre é o mais forte e o mais seguro. Se usar imagem, **duotone preto-e-branco** de alto contraste, e tem que ser **arte sua** (foto duotone do acervo, textura geométrica gerada). ⚠️ **NÃO copiar a esfera grafo/estipulado do reThink** nem qualquer artwork da reMarkable — isto é benchmark de **estilo**, não plágio de arte. Sem cor, sem bloco chapado.

## Elementos geométricos
Finos, monocromáticos, `stroke:var(--ink);fill:none` (ou preenchimento `--ink` sólido). Ex.: alvo de foco (círculos concêntricos + ponto central preenchido). Nada de ícone colorido.

## Prova revisada — a caneta por cima do digital (camada opt-in)

> Conceito definido com o Flavio em 21/08/2026, iterando protótipos sobre o W1 RIPack
> (slide "Um trabalho completo, do início ao fim"). Frase-conceito dele, literal:
> **"primeira versão feita no digital, mas Flávio pegou a caneta e corrigiu alguns pontos."**

O slide tem DUAS camadas com papéis fixos:

**Camada digital (a base — é a Régua deste arquivo, intocada):** tipografia, layout, fios,
números, kickers, prints de tela, tabelas. Sempre limpa, sempre preta/cinza. Números são
digitais (nunca circulados à mão); kickers sempre em `--ink`.

**Camada de caneta (a revisão — o que "o Flavio rabiscou" por cima):**
- **Ícones desenhados à mão** (rough.js): traço monocromático na **cor da caneta que o
  desenhou** — SEM hachura/preenchimento colorido (testado e rejeitado). Contorno único.
- **Sublinhado de caneta** sob a palavra-chave do título. Em produção entra como **GIF que
  se desenha sozinho** (revela da esquerda pra direita, ~0,8s, loop único — anima nativo no
  modo apresentação).
- **Setas curtas de caneta** entre passos de um fluxo (nunca linha horizontal contínua
  atravessando os ícones — testado e rejeitado).
- **Marginália manuscrita** (fonte **Caveat**, levemente rotacionada, com setinha desenhada):
  o "comentário feito na revisão do documento" — ex.: "começa no e-mail de sempre",
  "é aqui que mora a confiança". É o elemento mais forte da linguagem: usar como
  **tempero, máx. 1 por slide, só em slides-chave** (fluxo, case, síntese) — nunca em
  slides de print/tour.

### As canetas (escolher por contexto; 1 caneta de cor + preto por slide)

| Caneta | Hex | Registro |
|---|---|---|
| preto | `#1a1a1a` | a caneta default — estrutura, maioria dos ícones |
| vermelho/vinho | `#8C3A2B` | correção, destaque, o check de aprovação |
| azul/índigo | `#3F46C4` | anotação de estudo, referência (é o `--link` encorpado) |
| verde | `#0F6E5C` | confirmação, prática, "isso funciona" |
| laranja | `#D97656` | energia, marca Claude (casa com logos Chat/Cowork/Code) |

Dosagem: a cor ocupa **≤ 10–20% do slide**. Base P&B+cinza intacta. Logos e imagens
externas coloridas por cima são bem-vindas (benchmark: slide dos 3 workshops com os
logos Chat/Cowork/Code).

### Técnica

- **rough.js** (`roughness:1.4, bowing:1.6, strokeWidth:2.4`) para ícones/setas/sublinhado;
  marginália em **Caveat** 500–600 (adicionar ao `<head>` quando a camada for usada).
- Em HTML o traço nasce vivo; para **pptx**, pipeline HTML→PNG (Playwright, scale 2) e
  imagem embutida — protótipos de referência em
  `32_MKP/05_Projetos/02_RIPack/02_Workshops/01_W1_ClaudeChat/02_Roteiro/design_prova_revisada/`.
- Rejeitados nos testes (não reabrir sem fato novo): hachura colorida nos ícones · véu
  cinza sobre prints (destaque é contorno grosso) · números circulados à mão · kicker
  colorido · ícones geométricos "de biblioteca" (sem graça — a autoria está no traço).

## Links
Sublinhado, cor `--link`. É a única cor do tema — usar com parcimônia (URL, referência).

## Export reMarkable / e-ink
O tema já é monocromático. Para impressão/reMarkable, setar `--link:var(--ink)` (links viram tinta sublinhada). Régua, nav e pesos seguram a hierarquia sem cor. Validar contraste.

## Escrita
Title de seção = rótulo curto ou conclusão (so-what), serifa · subhead bold sans + corpo sans · pirâmide · 1 ideia/bloco. Voz do autor em `VOICE.md` (travessão zerado, sem hipérbole, número→fonte). Tema sóbrio: texto e espaço falam.

## Variantes (toggle de tokens)
- **reThink / reMarkable (default):** o acima — branco, Fraunces título + Inter corpo, régua à esquerda, nav de topo, mono + link-azul.
- **Elegant (papel quente):** `--paper:#F6F5F1`, corpo em serifa (`Literata`), accent bronze `#8C6D46`, régua dupla sob o título no lugar da barra à esquerda. Use quando o material pede tom mais quente/editorial-impresso em vez do branco clínico do reMarkable.


---

## Régua W2 — identidade vigente (referência: decks W1/W2 RIPack, set/2026)

> Adicionado em 05/09/2026 depois de o Flavio recusar dois decks feitos pelas seções acima: *"esse elegant
> skills estão antigos - veja como fizemos nos casos da ripack workshops. principal falta aqui são as
> imagens em colunas e em fundos, como na capa"*. **A fonte viva é o pptx mais recente do tema**
> (`32_MKP/05_Projetos/02_RIPack/02_Workshops/02_W2_Cowork/20260908_Wks2_RIPack_v04.pptx`): abra e olhe
> 5–6 páginas antes de gerar. O que segue é o que dele se extrai.

**Tokens:** papel `#FCFCFC` · tinta `#141414` · corpo `#4A4A4A` · mudo `#6E6E6E` · fio `#DADAD6` ·
**accent laranja `#D37455`** (numerais, setas, chevrons, pontos) · papel quente `#F5F1EC` para texto sobre foto.
**Fontes:** **Literata Light** no título (33 pt = 66 px no palco, `weight 300`), Literata no rótulo de coluna
e nas frases-chave, Literata itálico nas dicas, **Inter** no corpo, kicker e rodapé. Não é Fraunces.

**Chrome de página de conteúdo (palco 1920×1080):** fio vertical `x=104` de `y=84` a `996` · kicker Inter 20 px
caixa-alta `letter-spacing .14em` em `(130,118)` · barra de 2 px em `x=114, y=153` com a altura do título ·
título em `(130,145)`, largura 1660 · pager `‹ 02 / 07 ›` Inter 21 px em `(1529,40)` alinhado à direita ·
fecho/fonte Inter 23 px em `y=1001`. Foto full-bleed leva overlay `rgba(20,20,20,.55–.62)` e texto em papel quente;
crédito da foto em 14 px no canto inferior direito.

**Arquétipos que o W2 usa (e o que cada um representa):**
- **capa / fecho full-bleed** — foto CC0 que carrega a metáfora do deck (caderno em branco; agulha e fio).
- **colunas com foto** (511×281 em `y=328`, rótulo Literata 24 pt, dica itálica, corpo Inter 16 pt). Largura das
  colunas pode carregar a ideia: proporção "quase 100% × o resto" = coluna larga × coluna estreita.
- **foto-metade** (639×1080 à direita) + lista curta à esquerda.
- **chevrons** (`PENTAGON` + `CHEVRON`, 3 accent + 1 papel) para processo em etapas, sobre foto full-bleed.
- **linha do tempo** (fio + pontos accent + numeral Literata Light) para sequência de N itens com 2 palavras cada.
- **bifurcação** (um sintoma, duas leituras: a errada tracejada e riscada, a certa em accent) para "parece × acontece".
- **troca entre raias** ("o agente" · "eu", setas accent com o rótulo em cima) para protocolo entre dois lados.
- **camada de caneta** (§Prova revisada acima) — opcional; o W2 usa post-it amarelo, ícones a traço e marginália.

**Regra do Flavio (05/09/2026): nunca um slide chato — o design representa a ideia.** Lista numerada só quando a
ordem é o conteúdo (passos, cronologia); "sempre usar lista numerada não é a melhor direção". Slide de conceito puro
vira diagrama, proporção, contraste ou foto que carrega a metáfora — não colunas de texto com número na frente.

**Fotos:** CC0/PD com crédito (`fotos/CREDITOS.md` na pasta do deck). Busca: Openverse API
(`license=cc0,pdm`, `source=wikimedia,flickr` para originais grandes) e Commons API (`extmetadata`). StockSnap e
rawpixel só entregam 960–1300 px (rawpixel com marca d'água acima de 1024): servem para coluna, não para full-bleed.
Nunca repetir a mesma foto em dois slides. Tom comum entre as fotos ajuda o deck a ler como uma peça.

**Para PowerPoint nativo:** `/elegant-html-to-pptx` → método W2 (clonar arquétipos do pptx anterior,
`lib/exemplo_build_regua_w2.py`); `lib/pptx2html.py` gera a versão web do mesmo deck.
